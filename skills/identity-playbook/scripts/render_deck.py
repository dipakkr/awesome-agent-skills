#!/usr/bin/env python3
"""Original portable slide renderer. Standard library for HTML; python-pptx for PPTX."""
import argparse, base64, copy, hashlib, json, math, re
from pathlib import Path

COL = re.compile(r'^#[0-9a-fA-F]{6}$')
def validate(d):
    if not isinstance(d.get('title'),str) or not d['title'].strip(): raise ValueError('A title is required')
    if not 1 <= len(d.get('slides',[])) <= 80: raise ValueError('Expected 1–80 slides')
    for s in d['slides']:
        if not COL.fullmatch(s['background']): raise ValueError('Invalid background')
        if not s.get('notes'): raise ValueError('Every slide needs speaker notes')
        for o in s['objects']:
            if o['kind'] not in ['text','rect','ellipse','image']: raise ValueError('Unsupported object')
            for k in ['x','y','w','h']:
                if not isinstance(o[k],(int,float)) or not math.isfinite(o[k]): raise ValueError('Invalid geometry')
            if o['x']<0 or o['y']<0 or o['w']<=0 or o['h']<=0 or o['x']+o['w']>1280.1 or o['y']+o['h']>720.1: raise ValueError('Object outside slide')
            for k in ['color','fill','stroke']:
                if k in o and not COL.fullmatch(o[k]): raise ValueError('Invalid color')
            if o['kind']=='text' and (not isinstance(o['text'],str) or not 12<=o.get('size',24)<=160): raise ValueError('Invalid text')
    return d

def embed(d,root):
    d=copy.deepcopy(d)
    for s in d['slides']:
        for o in s['objects']:
            if o['kind']!='image':continue
            src=o['src']
            if src.startswith('data:image/'):
                if not re.match(r'^data:image/(png|jpeg|webp);base64,[A-Za-z0-9+/=]+$',src):raise ValueError('Invalid embedded image')
                continue
            p=(root/src).resolve()
            if not p.is_relative_to(root.resolve()) or p.suffix.lower() not in ['.png','.jpg','.jpeg','.webp']:raise ValueError('Image must be local and inside the deck folder')
            raw=p.read_bytes()
            if len(raw)>20_000_000:raise ValueError('Image too large')
            mime={'.png':'png','.jpg':'jpeg','.jpeg':'jpeg','.webp':'webp'}[p.suffix.lower()]
            o['src']='data:image/'+mime+';base64,'+base64.b64encode(raw).decode()
    return d

def html(d):
    template=Path(__file__).with_name('viewer.html').read_text()
    return template.replace('__DECK_DATA__',json.dumps(d,ensure_ascii=False).replace('<','\\u003c'))

def pptx(d,out):
    import io
    from pptx import Presentation
    from pptx.util import Inches,Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import PP_ALIGN,MSO_ANCHOR
    p=Presentation();p.slide_width=Inches(13.333333);p.slide_height=Inches(7.5)
    unit=lambda n:Inches(n/96)
    rgb=lambda c:RGBColor.from_string(c.lstrip('#'))
    for s in d['slides']:
        slide=p.slides.add_slide(p.slide_layouts[6]);slide.background.fill.solid();slide.background.fill.fore_color.rgb=rgb(s['background'])
        slide.notes_slide.notes_text_frame.text=s['notes']
        for o in s['objects']:
            x,y,w,h=[unit(o[k]) for k in ['x','y','w','h']]
            if o['kind']=='image':
                b=base64.b64decode(o['src'].split(',',1)[1]);pic=slide.shapes.add_picture(io.BytesIO(b),x,y)
                ratio=pic.width/pic.height;box=w/h
                if ratio>box:
                    pic.width=w;pic.height=h;crop=(1-box/ratio)/2;pic.crop_left=crop;pic.crop_right=crop
                else:
                    pic.width=w;pic.height=h;crop=(1-ratio/box)/2;pic.crop_top=crop;pic.crop_bottom=crop
                pic.name=o.get('alt','Illustration');continue
            if o['kind']=='text':
                sh=slide.shapes.add_textbox(x,y,w,h);tf=sh.text_frame;tf.clear();tf.word_wrap=True
                tf.margin_left=tf.margin_right=tf.margin_top=tf.margin_bottom=0;tf.vertical_anchor=MSO_ANCHOR.TOP
                for i,line in enumerate(o['text'].split('\n')):
                    para=tf.paragraphs[0] if i==0 else tf.add_paragraph();para.text=line
                    para.font.name=o.get('font',d.get('font','Arial'));para.font.italic=o.get('italic',False);para.font.size=Pt(o.get('size',24)*.75);para.font.bold=o.get('bold',False)
                    para.font.color.rgb=rgb(o.get('color','#111111'));para.line_spacing=1.08;para.space_after=Pt(0)
                    para.alignment={'left':PP_ALIGN.LEFT,'center':PP_ALIGN.CENTER,'right':PP_ALIGN.RIGHT}[o.get('align','left')]
            else:
                sh=slide.shapes.add_shape(MSO_SHAPE.OVAL if o['kind']=='ellipse' else MSO_SHAPE.ROUNDED_RECTANGLE if o.get('radius') else MSO_SHAPE.RECTANGLE,x,y,w,h)
                sh.fill.solid();sh.fill.fore_color.rgb=rgb(o.get('fill','#111111'))
                if o.get('radius') and o['kind']=='rect':sh.adjustments[0]=min(.5,o['radius']/min(o['w'],o['h']))
                if o.get('stroke'):sh.line.color.rgb=rgb(o['stroke']);sh.line.width=Pt(o.get('strokeWidth',2)*.75)
                else:sh.line.fill.background()
    p.core_properties.title=d['title'];p.core_properties.author='Claude Directory';p.core_properties.subject=d.get('disclosure','')
    # python-pptx 1.0.2 omits this presentation-level reference when adding
    # notes. Keynote requires it (upstream issue #1051 / PR #1128).
    from pptx.oxml.xmlchemy import OxmlElement
    from pptx.oxml.ns import qn
    from pptx.opc.constants import RELATIONSHIP_TYPE as RT
    if p._element.find(qn('p:notesMasterIdLst')) is None:
        rel=next((r for r in p.part.rels.values() if r.reltype==RT.NOTES_MASTER),None)
        if rel:
            listing=OxmlElement('p:notesMasterIdLst');item=OxmlElement('p:notesMasterId')
            item.set(qn('r:id'),rel.rId);listing.append(item)
            master=p._element.find(qn('p:sldMasterIdLst'))
            p._element.insert(p._element.index(master)+1 if master is not None else 0,listing)
    p.save(out)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('input',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--pptx',action='store_true');ap.add_argument('--force',action='store_true');a=ap.parse_args()
    d=embed(validate(json.loads(a.input.read_text())),a.input.parent)
    targets=[a.out.with_suffix('.html'),a.out.with_suffix('.receipt.json')]+([a.out.with_suffix('.pptx')] if a.pptx else [])
    if not a.force and any(p.exists() for p in targets):raise SystemExit('Output exists. Use a new name or --force.')
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.with_suffix('.html').write_text(html(d))
    if a.pptx:pptx(d,a.out.with_suffix('.pptx'))
    receipt={'title':d['title'],'slideCount':len(d['slides']),'dimensions':[1280,720],'sourceSha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),'outputs':[]}
    for p in targets:
        if p.suffix=='.json':continue
        receipt['outputs'].append({'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
    a.out.with_suffix('.receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'title':d['title'],'slides':len(d['slides']),'html':str(a.out.with_suffix('.html')),'pptx':a.pptx}))
if __name__=='__main__':main()
