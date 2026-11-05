#!/usr/bin/env python3
"""Claude Directory original deterministic motion engine. No network or external assets."""
import argparse
from functools import lru_cache
import hashlib
import html
import json
import math
from pathlib import Path
import subprocess

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parents[1]
W, H, FPS = 1280, 720, 24
DURATIONS = {'logo': 8, 'bars': 10, 'process': 12, 'timeline': 12, 'lower': 8, 'pattern': 8, 'radial': 10, 'compare': 12}
THEMES = {
    'chalk': ['#f1eee5', '#182f35', '#cf4933', '#ffffff', '#65716d', '#d7ddd5', '#285b63'],
    'ink': ['#111e32', '#f4f0e7', '#b5e789', '#203148', '#b5c2d1', '#354760', '#91b6f8'],
    'rose': ['#f6e8e5', '#3a2945', '#9054af', '#fff9f1', '#786775', '#dfcdd6', '#ca604c'],
    'cobalt': ['#e8edf7', '#152f66', '#2459ce', '#ffffff', '#66758c', '#c7d3e9', '#be492c'],
}


def ease(x):
    x = min(1, max(0, x))
    return x*x*x*(x*(x*6-15)+10)


def progress(t, start, duration=.8): return ease((t-start)/duration)
def mix(a, b, p): return a+(b-a)*p
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def rgb(color): return tuple(bytes.fromhex(color.lstrip('#')))


@lru_cache(maxsize=100)
def font(size, serif=False):
    return ImageFont.truetype(str(HERE/'assets/fonts'/('DM-Serif.ttf' if serif else 'DM-Sans.ttf')), size)


def text_check(value, key, limit):
    if not isinstance(value, str) or not value.strip() or len(value)>limit or any(ord(c)<32 for c in value):
        raise ValueError(f'{key}: use 1..{limit} printable characters')
    # Bundled fonts and text review currently cover Latin-script copy only.
    if any(ord(c)>0x024f and c not in '·%’–→' for c in value):
        raise ValueError(f'{key}: unsupported glyph; supply a suitable font and adapt validation first')
    return value


def validate(b, mode):
    if mode not in DURATIONS: raise ValueError('Unknown motion technique')
    for key, cap in [('brand',24),('title',46),('subtitle',88),('source',85)]: text_check(b.get(key), key, cap)
    if b.get('theme') not in THEMES: raise ValueError('Unknown theme')
    def items(key, count, fields):
        rows=b.get(key)
        if not isinstance(rows,list) or len(rows)!=count: raise ValueError(f'{key}: exactly {count} entries required')
        for row in rows:
            if not isinstance(row,dict):raise ValueError(f'{key}: object entries required')
            for field, cap in fields: text_check(row.get(field),field,cap)
        return rows
    if mode=='logo':
        text_check(b.get('tagline'),'tagline',48)
        if b.get('motif') not in ['orbit','tiles','petals','ribbon']:raise ValueError('Unknown logo motif')
    elif mode=='bars':
        rows=items('items',4,[('label',20)])
        if len({r['label'] for r in rows})!=4:raise ValueError('Labels must be distinct')
        nums=[r.get('value') for r in rows]
        if any(type(n) not in (int,float) or not math.isfinite(n) or not 0<=n<=1000000 for n in nums):raise ValueError('Bars require finite nonnegative values up to 1,000,000')
        if not max(nums):raise ValueError('At least one bar must be positive')
        text_check(b.get('unit'),'unit',18)
        scale=b.get('scale_max')
        if type(scale) not in (int,float) or not math.isfinite(scale) or not max(nums)<=scale<=10000000:raise ValueError('scale_max must be finite and cover all values')
    elif mode=='process':items('steps',4,[('label',18),('detail',52)])
    elif mode=='timeline':items('events',4,[('date',14),('label',24),('detail',52)])
    elif mode=='lower':
        text_check(b.get('speaker'),'speaker',35);text_check(b.get('role'),'role',45)
    elif mode=='pattern':
        if b.get('motif') not in ['orbit','tiles','petals','ribbon']:raise ValueError('Unknown pattern motif')
        text_check(b.get('caption'),'caption',40)
    elif mode=='radial':
        rows=items('items',3,[('label',20)])
        nums=[r.get('value') for r in rows]
        if any(type(n) not in (int,float) or not math.isfinite(n) or n<=0 for n in nums):raise ValueError('Segments must be finite positive numbers')
        if not math.isclose(sum(nums),100,abs_tol=1e-8):raise ValueError('Radial shares must total exactly 100 percent')
        text_check(b.get('center'),'center',15)
    elif mode=='compare':
        items('options',2,[('name',23),('summary',42)])
        items('criteria',3,[('label',18),('left',28),('right',28)])
    return b


class Scene:
    def __init__(self,b,mode,base):
        self.b,self.mode=b,mode
        self.bg,self.ink,self.accent,self.paper,self.muted,self.line,self.secondary=THEMES[b['theme']]
        self.logo=None;self.inputs={}
        if mode=='logo' and b.get('logo'):
            p=(base/b['logo']).resolve()
            if not p.is_file() or p.suffix.lower() not in ('.png','.webp') or p.stat().st_size>20000000:raise ValueError('logo must be a local PNG/WebP below 20 MB')
            with Image.open(p) as im:
                if im.width*im.height>16000000:raise ValueError('Logo too large')
                self.logo=ImageOps.contain(im.convert('RGBA'),(210,210))
            self.inputs['logo']=sha(p)
        self.text_boxes=[]

    def text(self,x,y,s,size=26,color=None,maxw=None,serif=False,anchor='lt'):
        f=font(size,serif)
        bounds=self.d.textbbox((x,y),s,font=f,anchor=anchor)
        if maxw and self.d.textlength(s,font=f)>maxw:raise ValueError(f'Text does not fit: {s}')
        if bounds[0]<32 or bounds[1]<24 or bounds[2]>W-32 or bounds[3]>H-20:raise ValueError(f'Text outside safe area: {s}')
        self.d.text((x,y),s,font=f,fill=color or self.ink,anchor=anchor)
        self.text_boxes.append(bounds)

    def wrap(self,x,y,s,maxw,size=24,color=None,maxlines=2):
        lines=[];line=''
        for word in s.split():
            trial=(line+' '+word).strip()
            if self.d.textlength(trial,font=font(size))>maxw:
                if not line:raise ValueError('Word too wide: '+word)
                lines.append(line);line=word
            else:line=trial
        lines.append(line)
        if len(lines)>maxlines:raise ValueError('Copy too long: '+s)
        for i,line in enumerate(lines):self.text(x,y+i*size*1.35,line,size,color,maxw)

    def rr(self,box,fill=None,r=20,outline=None,width=1):
        self.d.rounded_rectangle(tuple(round(v) for v in box),radius=r,fill=fill,outline=outline,width=width)

    def mark(self,cx,cy,r,kind,p=1):
        if kind=='orbit':
            for i in range(3):
                a=math.tau*i/3-.7+(1-p)*1.1
                x=cx+math.cos(a)*r*.45;y=cy+math.sin(a)*r*.45
                self.d.ellipse((x-r*.55,y-r*.55,x+r*.55,y+r*.55),outline=self.accent,width=max(2,int(r*.16)))
        elif kind=='tiles':
            for i in range(4):
                x=cx+(-1 if i%2==0 else 1)*r*.48;y=cy+(-1 if i<2 else 1)*r*.48
                self.rr((x-r*.38,y-r*.38,x+r*.38,y+r*.38),self.accent if i!=3 else self.secondary,r=int(r*.15))
        elif kind=='petals':
            for i in range(6):
                a=i*math.tau/6+(1-p)*.5;x=cx+math.cos(a)*r*.52;y=cy+math.sin(a)*r*.52
                self.d.ellipse((x-r*.36,y-r*.36,x+r*.36,y+r*.36),fill=self.accent if i%2 else self.secondary)
            self.d.ellipse((cx-r*.22,cy-r*.22,cx+r*.22,cy+r*.22),fill=self.bg)
        else:
            for i in range(3):
                x=cx-r+i*r*.65
                self.d.polygon([(x,cy+r*.7),(x+r*.5,cy-r*.7),(x+r,cy-r*.7),(x+r*.5,cy+r*.7)],fill=self.accent if i%2==0 else self.secondary)

# Original edition 2 art direction. Logical coordinates stay at 1280x720;
# all primitives and font outlines are rasterized directly at 1920x1080.
SCALE=1.5
OUT_W,OUT_H=1920,1080
FPS=30

class RetinaDraw:
    def __init__(self, im): self.raw=ImageDraw.Draw(im)
    def xy(self, pts):
        if isinstance(pts[0],(tuple,list)):return [tuple(v*SCALE for v in p) for p in pts]
        return tuple(v*SCALE for v in pts)
    def shape(self,name,xy,**kw):
        if 'width' in kw:kw['width']=max(1,round(kw['width']*SCALE))
        if 'radius' in kw:kw['radius']=round(kw['radius']*SCALE)
        return getattr(self.raw,name)(self.xy(xy),**kw)
    def line(self,xy,**kw):return self.shape('line',xy,**kw)
    def ellipse(self,xy,**kw):return self.shape('ellipse',xy,**kw)
    def rectangle(self,xy,**kw):return self.shape('rectangle',xy,**kw)
    def polygon(self,xy,**kw):return self.shape('polygon',xy,**kw)
    def rounded_rectangle(self,xy,**kw):return self.shape('rounded_rectangle',xy,**kw)
    def arc(self,xy,start,end,**kw):return self.raw.arc(self.xy(xy),start,end,**{k:round(v*SCALE) if k=='width' else v for k,v in kw.items()})
    def textlength(self,s,font):return self.raw.textlength(s,font=retina_font(font.size, font.getname()[0].startswith('DM Serif')))/SCALE
    def textbbox(self,xy,s,font,anchor):return tuple(v/SCALE for v in self.raw.textbbox(self.xy(xy),s,font=retina_font(font.size,font.getname()[0].startswith('DM Serif')),anchor=anchor))
    def text(self,xy,s,font,fill,anchor):return self.raw.text(self.xy(xy),s,font=retina_font(font.size,font.getname()[0].startswith('DM Serif')),fill=fill,anchor=anchor)

@lru_cache(maxsize=120)
def retina_font(size,serif=False):return font(round(size*SCALE),serif)
def tint(a,b,p):return tuple(round(mix(x,y,p)) for x,y in zip(rgb(a) if isinstance(a,str) else a,rgb(b) if isinstance(b,str) else b))
def out(t,start,duration=.8):
    p=min(1,max(0,(t-start)/duration));return 1-(1-p)**4

class ArtScene(Scene):
    def __init__(self,b,mode,base):
        super().__init__(b,mode,base)
        from PIL import ImageFilter
        # Quiet directional light, made locally. No downloaded textures or artwork.
        grad=Image.linear_gradient('L').resize((OUT_W,OUT_H))
        self.background=ImageOps.colorize(grad,tint(self.bg,self.paper,.4),rgb(self.bg))
        glow=Image.new('L',(320,180),0);g=ImageDraw.Draw(glow)
        g.ellipse((140,-140,410,130),fill=90);glow=glow.filter(ImageFilter.GaussianBlur(40)).resize((OUT_W,OUT_H))
        self.background=Image.composite(Image.new('RGB',(OUT_W,OUT_H),self.secondary),self.background,glow.point(lambda v:int(v*.18)))
        self.hold=None
    def start(self):
        self.im=self.background.copy();self.d=RetinaDraw(self.im);self.text_boxes=[]
    def footer(self):
        self.text(56,680,self.b['source'],14,self.muted,1168)
    def kicker(self,label):
        self.d.ellipse((56,44,64,52),fill=self.accent)
        self.text(76,40,self.b['brand'].upper(),16,self.ink,550)
        self.text(1224,40,label.upper(),13,self.muted,500,anchor='rt')
    def blend_group(self,p,fn):
        if p<=0:return
        if p>=1:fn();return
        bg=self.im;self.im=Image.new('RGBA',(OUT_W,OUT_H));self.d=RetinaDraw(self.im)
        fn();layer=self.im;layer.putalpha(layer.getchannel('A').point(lambda a:round(a*p)))
        bg.paste(layer,(0,0),layer);self.im=bg;self.d=RetinaDraw(bg)
    def panel(self,box,fill=None,r=22):
        x,y,x2,y2=box
        self.rr((x,y+9,x2,y2+9),tint(self.bg,self.ink,.075),r)
        self.rr(box,fill or self.paper,r,outline=tint(fill or self.paper,self.ink,.1))
    def headline(self,x,y,copy,width,size=56,color=None,maxlines=3):
        self.wrap(x,y,copy,width,size,color,maxlines)
    def ornament(self,cx,cy,r,t,color=None):
        color=color or self.line
        for i in range(4):
            rx=r-i*21;ry=rx*.52
            self.d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),outline=color,width=1)
        a=-1.1+t*.25;x=cx+math.cos(a)*r;y=cy+math.sin(a)*r*.52
        self.d.ellipse((x-6,y-6,x+6,y+6),fill=self.accent)
    def logo_frame(self,t):
        self.start();self.kicker('Identity in motion')
        cx,cy=640,286;p=out(t,.15,1.65)
        # Construction rings resolve into a quiet frame around the final identity.
        for i in range(4):
            r=116+i*34+70*(1-p)
            self.d.ellipse((cx-r,cy-r*.65,cx+r,cy+r*.65),outline=tint(self.bg,self.ink,.06+i*.02),width=1)
        for i in range(12):
            a=i*math.tau/12+.6*(1-p)
            x=cx+math.cos(a)*(248+80*(1-p));y=cy+math.sin(a)*166
            self.d.ellipse((x-2,y-2,x+2,y+2),fill=self.line)
        if self.logo:
            mark=self.logo.resize((max(1,round(self.logo.width*SCALE*(.8+.2*p))),max(1,round(self.logo.height*SCALE*(.8+.2*p)))),Image.Resampling.LANCZOS)
            mark.putalpha(mark.getchannel('A').point(lambda a:round(a*p)))
            self.im.paste(mark,(round(cx*SCALE-mark.width/2),round(cy*SCALE-mark.height/2)),mark)
        else:
            # Four distinct assembly grammars, one per geometric concept mark.
            kind=self.b['motif']
            if kind=='tiles':
                for i in range(4):
                    q=out(t,.12+i*.13,1.1);x=cx+(-1 if i%2==0 else 1)*(45+100*(1-q));y=cy+(-1 if i<2 else 1)*(45+80*(1-q))
                    self.blend_group(q,lambda x=x,y=y,i=i:self.rr((x-35,y-35,x+35,y+35),self.accent if i<3 else self.secondary,14))
            elif kind=='petals':
                for i in range(6):
                    q=out(t,.15+i*.09,1);a=i*math.tau/6+(1-q)*.5;r=55+90*(1-q);x=cx+math.cos(a)*r;y=cy+math.sin(a)*r
                    self.blend_group(q,lambda x=x,y=y,i=i:self.d.ellipse((x-37,y-37,x+37,y+37),fill=self.accent if i%2 else self.secondary))
            elif kind=='ribbon':
                for i in range(3):
                    q=out(t,.2+i*.15,1.1);x=cx-110+i*70;y=cy+90*(1-q)
                    self.blend_group(q,lambda x=x,y=y,i=i:self.d.polygon([(x,y+70),(x+55,y-70),(x+105,y-70),(x+50,y+70)],fill=self.accent if i%2==0 else self.secondary))
            else:
                for i in range(3):
                    q=out(t,.12+i*.13,1.2);a=i*math.tau/3-.7+(1-q);x=cx+math.cos(a)*(45+100*(1-q));y=cy+math.sin(a)*(45+65*(1-q))
                    self.blend_group(q,lambda x=x,y=y:self.d.ellipse((x-54,y-54,x+54,y+54),outline=self.accent,width=15))
        q=out(t,1.15,.85)
        self.blend_group(q,lambda:self.text(640,450+24*(1-q),self.b['brand'],80,maxw=1120,serif=True,anchor='mt'))
        q=out(t,1.8,.8)
        self.blend_group(q,lambda:self.text(640,558+12*(1-q),self.b['tagline'],24,self.muted,1100,anchor='mt'))
        self.footer();return self.im
    def bars_frame(self,t):
        self.start();self.kicker('The numbers / one fixed scale')
        self.headline(56,115,self.b['title'],410,52,maxlines=3)
        self.wrap(58,352,self.b['subtitle'],396,22,self.muted,3)
        highest=max(self.b['items'],key=lambda r:r['value']);p=progress(t,3.8,.8)
        def insight():
            self.text(58,475,'HIGHEST VALUE',13,self.muted)
            self.text(56,505,f"{highest['value']:g}",82,self.accent,360,serif=True)
            self.text(58,605,highest['label']+' · '+self.b['unit'],19,self.muted,410)
        self.blend_group(p,insight)
        panelbg=self.paper if self.b['theme']=='ink' else self.ink
        panelink=self.ink if self.b['theme']=='ink' else self.bg
        self.panel((504,98,1224,638),panelbg,28)
        panelline=tint(panelbg,panelink,.14);muted=tint(panelbg,panelink,.65)
        x0,x1=542,1184;maximum=self.b['scale_max']
        for k in range(5):
            x=mix(x0,x1,k/4);self.d.line((x,164,x,563),fill=panelline,width=1)
            self.text(x,590,f'{maximum*k/4:g}',15,muted,145,anchor='mt')
        self.text(544,124,self.b['unit'].upper(),14,muted,580)
        for i,item in enumerate(self.b['items']):
            y=180+i*99;p=out(t,1+i*.65,1.5);length=(x1-x0)*item['value']/maximum*p
            self.text(x0,y,item['label'],23,panelink,430)
            self.text(x1,y,f"{item['value']*p:,.1f}".removesuffix('.0'),24,panelink,160,anchor='rt')
            self.rr((x0,y+36,x1,y+66),panelline,4)
            col=self.accent if self.b['theme']=='ink' else self.bg
            if length>1:self.rr((x0,y+36,x0+length,y+66),col if item==highest else tint(panelbg,panelink,.58),min(4,int(length/2)))
        self.footer();return self.im
    def process_frame(self,t):
        self.start();self.kicker('From first step to finish')
        self.text(56,106,self.b['title'],52,maxw=1168,serif=True)
        self.text(58,178,self.b['subtitle'],21,self.muted,1160)
        self.d.line((185,281,1097,281),fill=self.line,width=2)
        route=progress(t,1,5.1);self.d.line((185,281,mix(185,1097,route),281),fill=self.accent,width=2)
        for i,step in enumerate(self.b['steps']):
            x=56+i*300;q=out(t,.4+i*1.55,.9);y=323+26*(1-q)
            def card():
                self.panel((x,y,x+268,y+292),self.paper,20)
                self.text(x+24,y+22,f'0{i+1}',64,self.accent,220,serif=True)
                # Each step has a small, separately constructed diagram token.
                self.mark(x+220,y+58,22,['orbit','tiles','ribbon','petals'][i])
                self.text(x+24,y+116,step['label'],27,maxw=220)
                self.wrap(x+24,y+165,step['detail'],218,21,self.muted,3)
                self.d.line((x+24,y+263,x+244,y+263),fill=self.line,width=1)
                self.d.line((x+24,y+263,x+24+220*progress(t,.8+i*1.55,1),y+263),fill=self.accent,width=2)
            self.blend_group(q,card)
            if q>0:
                cx=x+134
                self.d.ellipse((cx-15,266,cx+15,296),fill=self.accent)
                self.d.ellipse((cx-5,276,cx+5,286),fill=self.paper)
                self.d.line((cx,299,cx,312),fill=self.line,width=1)
        self.footer();return self.im
    def timeline_frame(self,t):
        self.start();self.kicker('A story in four moments')
        self.text(56,108,self.b['title'],52,maxw=1168,serif=True)
        self.text(58,180,self.b['subtitle'],21,self.muted,1160)
        self.d.line((78,338,1200,338),fill=self.line,width=2)
        self.d.line((78,338,mix(78,1200,progress(t,.6,5.2)),338),fill=self.accent,width=3)
        for i,event in enumerate(self.b['events']):
            x=56+i*300;p=out(t,.4+i*1.5,.8)
            def milestone():
                self.text(x+4,260+14*(1-p),event['date'],38,self.accent,268,serif=True)
                self.d.ellipse((x+14,330,x+30,346),fill=self.accent)
                self.d.line((x+22,357,x+22,380),fill=self.line,width=1)
                y=393+18*(1-p)
                self.panel((x,y,x+268,y+228),self.paper,16)
                self.text(x+22,y+21,f'CHAPTER 0{i+1}',12,self.muted,225)
                self.wrap(x+22,y+56,event['label'],223,28,maxlines=2)
                self.wrap(x+22,y+146,event['detail'],223,19,self.muted,3)
            self.blend_group(p,milestone)
        self.footer();return self.im
    def lower_frame(self,t,transparent=False):
        self.im=Image.new('RGBA',(OUT_W,OUT_H));self.d=RetinaDraw(self.im);self.text_boxes=[]
        p=out(t,.35,.85)*(1-progress(t,6.6,.8))
        if p>0:
            # Two staggered plates; names are never distorted or scrolled.
            self.rr((76,500,878,637),self.ink,8)
            self.rr((76,500,86,637),self.accent,4)
            self.text(110,518,self.b['brand'].upper(),12,self.bg,720)
            self.text(108,545,self.b['speaker'],37,self.bg,735)
            self.text(110,600,self.b['role'],21,self.bg,725)
            mask=Image.new('L',(OUT_W,OUT_H),0);md=RetinaDraw(mask)
            md.rectangle((76,500,76+802*p,637),fill=255)
            self.im.putalpha(ImageChops.multiply(self.im.getchannel('A'),mask))
        overlay=self.im
        if transparent:return overlay
        self.start();self.kicker('A clear introduction')
        self.headline(56,139,self.b['title'],540,57,maxlines=3)
        self.wrap(58,373,self.b['subtitle'],460,22,self.muted,3)
        # Original abstract set, quietly moving behind the compositing demonstration.
        cx,cy=982,331
        for i in range(12):
            phase=t*.3+i*.14;r=140+i*4
            x=cx+math.sin(phase)*12;y=cy+i*6-35
            self.d.ellipse((x-r,y-r*.55,x+r,y+r*.55),outline=tint(self.accent,self.bg,i/14),width=9)
        self.im.paste(overlay,(0,0),overlay);self.footer();return self.im
    def pattern_frame(self,t):
        self.start();phase=math.tau*(t%8)/8
        # Oversized cropped geometry creates a designed field, rather than an icon grid.
        for row in range(5):
            for col in range(8):
                cx=-70+col*205+20*math.sin(phase+row*.45);cy=-70+row*210+22*math.cos(phase+col*.4)
                r=76+9*math.sin(phase+(row+col)*.6)
                self.mark(cx,cy,r,self.b['motif'],1)
        self.panel((269,225,1011,495),self.ink,24)
        self.text(640,258,self.b['brand'].upper(),15,self.bg,660,anchor='mt')
        # Center each of up to two carefully measured display lines.
        words=self.b['caption'].split();lines=[];line=''
        for word in words:
            trial=(line+' '+word).strip()
            if self.d.textlength(trial,font=font(54,True))>650:lines.append(line);line=word
            else:line=trial
        lines.append(line)
        if len(lines)>2:raise ValueError('Pattern caption exceeds two lines')
        y=320 if len(lines)==1 else 300
        for i,line in enumerate(lines):self.text(640,y+i*65,line,54,self.bg,650,True,'mt')
        self.text(640,452,'CONTINUOUS BY DESIGN',12,self.bg,600,anchor='mt')
        # Legible disclosure on its own backing, even across the busiest geometry.
        self.rr((42,665,980,707),self.bg,8);self.footer();return self.im
    def radial_frame(self,t):
        self.start();self.kicker('Parts of one whole')
        cx,cy,r=338,363,231;box=(cx-r,cy-r,cx+r,cy+r)
        self.d.ellipse((cx-r-17,cy-r-17,cx+r+17,cy+r+17),outline=self.line,width=1)
        self.d.ellipse((cx-r,cy-r+9,cx+r,cy+r+9),outline=tint(self.bg,self.ink,.12),width=62)
        self.d.ellipse(box,outline=self.line,width=62)
        start=-90;colors=[self.accent,self.secondary,self.muted]
        for i,item in enumerate(self.b['items']):
            sweep=item['value']*3.6;p=progress(t,.5+i*.8,1.25)
            if p>0:
                end=start+(sweep-min(2,sweep*.15))*p
                self.d.arc(box,start,end,fill=colors[i],width=62)
                self.d.arc((cx-r+2,cy-r+2,cx+r-2,cy+r-2),start,end,fill=tint(colors[i],self.paper,.23),width=2)
            start+=sweep
        self.text(cx,311,'100%',76,maxw=290,serif=True,anchor='mt')
        self.text(cx,407,self.b['center'],23,self.muted,260,anchor='mt')
        self.headline(673,112,self.b['title'],550,43,maxlines=2)
        self.wrap(675,246,self.b['subtitle'],520,20,self.muted,2)
        for i,item in enumerate(self.b['items']):
            y=355+i*85;p=progress(t,.5+i*.8,1.25)
            self.d.ellipse((675,y+11,689,y+25),fill=colors[i])
            self.text(708,y+4,item['label'],25,maxw=350)
            value=f"{item['value']:g}%" if p==1 else f"{item['value']*p:.0f}%"
            self.text(1217,y,value,40,maxw=150,anchor='rt')
            self.d.line((675,y+63,1220,y+63),fill=self.line,width=1)
        self.footer();return self.im
    def compare_frame(self,t):
        self.start();self.kicker('Two approaches / clear tradeoffs')
        self.text(56,105,self.b['title'],50,maxw=1168,serif=True)
        self.text(58,174,self.b['subtitle'],21,self.muted,1160)
        for i,opt in enumerate(self.b['options']):
            p=out(t,.4+i*.25,.9);x=56+i*598+(1-p)*(16 if i else -16);y=237
            def option():
                self.panel((x,y,x+570,630),self.paper,22)
                self.rr((x+25,y+25,x+76,y+76),self.accent if i==0 else self.secondary,12)
                self.text(x+50,y+38,'A' if i==0 else 'B',26,self.paper,anchor='mt')
                self.text(x+95,y+25,opt['name'],29,maxw=445)
                self.text(x+95,y+68,opt['summary'],16,self.muted,445)
                self.d.line((x+25,y+108,x+545,y+108),fill=self.line,width=1)
                for j,row in enumerate(self.b['criteria']):
                    q=out(t,1.5+j*1.1,.7);yy=y+130+j*82
                    def detail():
                        self.text(x+27,yy,row['label'].upper(),12,self.muted,515)
                        self.text(x+27,yy+26,row['left' if i==0 else 'right'],24,maxw=515)
                    self.blend_group(q,detail)
            self.blend_group(p,option)
        self.footer();return self.im
    def frame(self,t,transparent=False):
        # Keep a genuine still reading hold; avoid rendering the same frame hundreds of times.
        if self.mode not in ('pattern','lower') and t>=6.5:
            if self.hold is None:self.hold=getattr(self,self.mode+'_frame')(6.5).copy()
            return self.hold.copy()
        if self.mode=='lower':return self.lower_frame(t,transparent)
        return getattr(self,self.mode+'_frame')(t)

Scene=ArtScene


def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-4000:])
    return p.stdout


def encode(scene,out,alpha=False):
    mode=scene.mode;duration=DURATIONS[mode];target=out/('overlay.webm' if alpha else 'film.mp4')
    command=['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgba' if alpha else 'rgb24','-s',f'{OUT_W}x{OUT_H}','-r',str(FPS),'-i','pipe:0','-an']
    command+=['-c:v','libvpx-vp9','-pix_fmt','yuva420p','-b:v','0','-crf','24','-auto-alt-ref','0','-threads','2'] if alpha else ['-c:v','libx264','-pix_fmt','yuv420p','-crf','19','-preset','fast','-threads','2','-movflags','+faststart']
    with (out/('alpha-encode.log' if alpha else 'encode.log')).open('wb') as log:
        proc=subprocess.Popen(command+[str(target)],stdin=subprocess.PIPE,stderr=log)
        try:
            for i in range(duration*FPS):proc.stdin.write(scene.frame(i/FPS,alpha).tobytes())
            proc.stdin.close()
            if proc.wait()!=0:raise RuntimeError('Encoder failed; inspect log')
        except BaseException:
            if not proc.stdin.closed:proc.stdin.close()
            if proc.poll() is None:proc.terminate()
            proc.wait();raise
    probe=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(target)]))
    stream=next(s for s in probe['streams'] if s['codec_type']=='video')
    if (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_read_frames']))!=(OUT_W,OUT_H,f'{FPS}/1',duration*FPS):raise ValueError('Encoded geometry/frame count mismatch')
    if abs(float(probe['format']['duration'])-duration)>.05:raise ValueError('Duration mismatch')
    run(['ffmpeg','-v','error','-i',str(target),'-f','null','-'])
    return {'width':OUT_W,'height':OUT_H,'fps':FPS,'frames':duration*FPS,'seconds':duration,'codec':stream['codec_name'],'decode':'pass'}


def alpha_check(path):
    checks={}
    for label,t in [('first',0),('hold',3),('last',8-1/FPS)]:
        p=subprocess.run(['ffmpeg','-v','error','-c:v','libvpx-vp9','-i',str(path),'-ss',str(t),'-frames:v','1','-vf','alphaextract','-f','rawvideo','-pix_fmt','gray','pipe:1'],capture_output=True,check=True)
        if len(p.stdout)!=OUT_W*OUT_H:raise ValueError('Alpha plane missing')
        lo,hi=min(p.stdout),max(p.stdout)
        if (label=='hold' and (lo,hi)!=(0,255)) or (label!='hold' and hi!=0):raise ValueError('Invalid overlay transparency at '+label)
        checks[label]={'min':lo,'max':hi}
    return checks


def main():
    parser=argparse.ArgumentParser();parser.add_argument('brief',type=Path);parser.add_argument('--out',type=Path,required=True);parser.add_argument('--stills-only',action='store_true')
    args=parser.parse_args();mode=json.loads((HERE/'config.json').read_text())['mode'];b=validate(json.loads(args.brief.read_text()),mode)
    if args.out.exists():raise ValueError('Use a new output directory; existing output is never overwritten')
    scene=Scene(b,mode,args.brief.resolve().parent);duration=DURATIONS[mode]
    # Preflight every frame so long copy and changing layouts cannot fail after partial delivery.
    for i in range(duration*FPS):scene.frame(i/FPS)
    args.out.mkdir(parents=True)
    (args.out/'brief.json').write_text(json.dumps(b,indent=2)+'\n')
    times=[0,.75,2.5,duration*.62,duration-1/FPS]
    for i,t in enumerate(times):scene.frame(t).save(args.out/f'review-{i+1:02}.png')
    scene.frame(4 if mode=='lower' else duration*.7).save(args.out/'poster.png')
    report={'edition':2,'mode':mode,'sourceSha256':sha(args.brief),'rendererSha256':sha(__file__),'configSha256':sha(HERE/'config.json'),'inputAssets':scene.inputs,'fonts':{p.name:sha(p) for p in (HERE/'assets/fonts').glob('*.ttf')},'reviewTimes':times,'silence':True,'authoredExample':True,'decode':'not-rendered','files':{}}
    if mode=='pattern':
        report['loopSeamExact']=scene.frame(0).tobytes()==scene.frame(duration).tobytes()
        if not report['loopSeamExact']:raise ValueError('Loop seam mismatch')
    if not args.stills_only:
        report['video']=encode(scene,args.out);report['decode']='pass'
        if mode=='lower':
            report['overlay']=encode(scene,args.out,True);report['alphaCheck']=alpha_check(args.out/'overlay.webm')
    title=html.escape(b['title'])
    (args.out/'preview.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{title}</title><style>body{{margin:40px auto;max-width:1100px;padding:0 20px;background:#111b25;color:#eee;font:16px system-ui}}video,img{{width:100%;border-radius:16px}}a{{color:#b5e789}}</style><h1>{title}</h1><p>{html.escape(b["source"])}</p><video controls preload="metadata" poster="poster.png" src="film.mp4"></video><p>Silent, editable motion example. <a href="brief.json">Input brief</a></p>'+('<p><a href="overlay.webm">Transparent WebM overlay</a>. The MP4 is a demonstration on a solid background.</p>' if mode=='lower' else '')+'</html>')
    for p in sorted(args.out.iterdir()):
        if p.is_file():report['files'][p.name]={'sha256':sha(p),'bytes':p.stat().st_size}
    (args.out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'output':str(args.out),'mode':mode,'decode':report['decode']}))

if __name__=='__main__':main()
