#!/usr/bin/env python3
"""Render an original objection/reversal film from local copy and fixture data."""
import argparse
from functools import lru_cache
import hashlib
import html
import json
import math
from pathlib import Path
import subprocess
from PIL import Image,ImageDraw,ImageFont

ROOT=Path(__file__).resolve().parents[1]
W,H,FPS,DURATION=1920,1080,30,32
THEMES={
 'blueprint':('#0d1427','#78baf4','#1c2b47'),
 'aubergine':('#211322','#eea6cd','#3b253d'),
 'copper':('#1c1714','#f0b080','#382a22'),
 'tidal':('#0b2428','#8ed6cc','#1a3d43'),
}
SCALES=[1.32,1.62,1.95,2.35,2.8,3.25,3.7,4.05,4.4]
CUTS=[0,.8,1.3,1.7,2,2.2,2.4,2.6,2.8]

def ease(v):
 v=max(0,min(1,v));return 1-(1-v)**3
def lerp(a,b,v):return a+(b-a)*v
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
@lru_cache(maxsize=160)
def font(size,mono=False):
 f=ImageFont.truetype(str(ROOT/'assets/fonts'/('Mono.ttf' if mono else 'DM-Sans.ttf')),max(10,int(size)))
 if not mono:
  try:f.set_variation_by_axes([14,650])
  except (OSError,ValueError):pass
 return f

def validate(b,data):
 for key,limit in {'brand':22,'claim':62,'hinge':26,'turn':20,'invocation':14,'prompt':85,'closer':65,'thesis':64,'cta':30,'source_label':26}.items():
  if not isinstance(b.get(key),str) or not b[key].strip() or len(b[key])>limit or any(ord(c)<32 for c in b[key]):raise ValueError(f'{key}: nonempty single-line string, max{limit}')
 if len(b['turn'].split())!=2:raise ValueError('turn must contain two words')
 if b.get('theme') not in THEMES:raise ValueError('Unknown theme')
 if not isinstance(b.get('posts'),list) or len(b['posts'])!=3 or any(not isinstance(p,str) or not p.strip() or len(p)>135 or b['hinge'] not in p or any(ord(c)<32 for c in p) for p in b['posts']):raise ValueError('Three posts, max135characters each, all including the exact hinge')
 if not isinstance(data,dict) or not isinstance(data.get('records'),list) or len(data['records'])!=4:raise ValueError('Fixture needs exactly four records')
 for r in data['records']:
  for key,limit in [('title',30),('detail',72),('status',20)]:
   if not isinstance(r.get(key),str) or not r[key].strip() or len(r[key])>limit or any(ord(c)<32 for c in r[key]):raise ValueError('Invalid fixture '+key)
 return b,data

class Film:
 def __init__(self,b,data):
  self.b,self.data=b,data;self.bg,self.accent,self.line=THEMES[b['theme']];self.ink='#f5f2ee';self.dim='#b6b1bc'
  self.base=Image.new('RGB',(W,H),self.bg);d=ImageDraw.Draw(self.base)
  rgb=tuple(int(self.bg[i:i+2],16) for i in (1,3,5))
  for y in range(H):
   lift=round(8*(1-y/H));d.line((0,y,W,y),fill=tuple(min(255,c+lift) for c in rgb))
  self.checked=set()
  ready=sum(r['status']=='Ready' for r in data['records'])
  self.findings=[f'Loaded {len(data["records"])} records from the local fixture.',f'Source: {b["source_label"]}.',f'{ready} ready; {4-ready} marked for review.','Original details preserved in the output.']

 def text(self,x,y,s,size=36,color=None,mono=False,anchor=None,maxw=None):
  f=font(size,mono);width=self.d.textlength(s,font=f)
  if maxw and width>maxw:raise ValueError(f'Text overflow: {s} ({width:.0f}>{maxw})')
  self.checked.add(s);self.d.text((x,y),s,font=f,fill=color or self.ink,anchor=anchor)

 def wrap(self,s,width,size,mono=False):
  rows=[];line=''
  for word in s.split():
   trial=(line+' '+word).strip()
   if self.d.textlength(trial,font=font(size,mono))>width:
    if not line:raise ValueError('Word overflow: '+word)
    rows.append(line);line=word
   else:line=trial
  if line:rows.append(line)
  return rows

 def para(self,x,y,s,width,size=44,center=False,highlight=False,maxlines=3):
  rows=self.wrap(s,width,size)
  if len(rows)>maxlines:raise ValueError('Too many lines: '+s)
  for i,line in enumerate(rows):
   xx=x-self.d.textlength(line,font=font(size))/2 if center else x
   if highlight:
    for word in line.split():
     self.text(xx,y+i*size*1.3,word,size,self.accent if word.strip('.,!?') in self.b['hinge'].split() else self.ink)
     xx+=self.d.textlength(word+' ',font=font(size))
   else:self.text(xx,y+i*size*1.3,line,size,maxw=width)

 def glass(self,box,r=24):
  x,y,z,q=map(round,box)
  self.d.rounded_rectangle((x+8,y+20,z+8,q+20),radius=r,fill='#090b11')
  layer=Image.new('RGB',(max(1,z-x),max(1,q-y)),self.bg)
  crop=self.im.crop((x,y,z,q));layer=Image.blend(crop,layer,.8)
  mask=Image.new('L',layer.size,0);ImageDraw.Draw(mask).rounded_rectangle((0,0,layer.width-1,layer.height-1),radius=r,fill=255)
  self.im.paste(layer,(x,y),mask);self.d=ImageDraw.Draw(self.im)
  self.d.rounded_rectangle((x,y,z,q),radius=r,outline=self.line,width=2)
  self.d.line((x+r,y+2,z-r,y+2),fill='#52606a',width=1)

 def background(self,t):
  self.im=self.base.copy();self.d=ImageDraw.Draw(self.im);offset=int(t*9)%100
  if self.b['theme']=='blueprint':
   for x in range(-100+offset,W,100):self.d.line((x,0,x,H),fill=self.line)
   for y in range(-100+offset,H,100):self.d.line((0,y,W,y),fill=self.line)
  elif self.b['theme']=='aubergine':
   for x in range(-H-100+offset,W,100):self.d.line((x,0,x+H,H),fill=self.line,width=2)
  elif self.b['theme']=='copper':
   for r in range(120+offset,2200,160):self.d.ellipse((1500-r,150-r,1500+r,150+r),outline=self.line,width=2)
  else:
   for y in range(-100+offset,H,90):
    pts=[(x,y+30*math.sin(x/250+t*.12)) for x in range(0,W+50,50)];self.d.line(pts,fill=self.line,width=2)

 def footer(self,t):
  self.d.rectangle((0,H-76,W,H),fill=self.bg)
  self.text(70,H-51,'CONCEPT FILM / FICTIONAL POSTS / LOCAL FIXTURE DATA',18,self.dim,mono=True)
  self.text(W-70,H-51,self.b['brand'].upper(),18,self.dim,mono=True,anchor='ra')

 def post(self,n,x=0,scale=1):
  # Render a social-style original card; no real handles, avatars or counters.
  self.glass((350+x,250,1570+x,790))
  self.d.ellipse((400+x,294,472+x,366),fill=self.line)
  self.text(436+x,313,['RN','PL','MK'][n],25,anchor='ma')
  self.text(496+x,294,['Research note','Planning note','Maker note'][n],27)
  self.text(496+x,335,'FICTIONAL EXAMPLE',18,self.dim,mono=True)
  self.para(405+x,427,self.b['posts'][n],1090,44,highlight=True,maxlines=4)
  self.text(405+x,729,'A concern this concept explores',21,self.dim)

 def frame(self,t):
  self.background(t)
  if t<2:
   p=ease(t/.6)
   layer=self.im.copy();self.para(960,405,self.b['claim'],1430,91,center=True,maxlines=2)
   if p<1:
    right=int(W*p);self.im.paste(layer.crop((right,0,W,H)),(right,0));self.d=ImageDraw.Draw(self.im)
   if t>1:self.text(960,675,'but...',53,self.dim,anchor='ma')
  elif t<9:
   local=t-2;n=min(2,int(local/(7/3)));q=local-n*7/3
   x=lerp(1900,0,ease(q/.38))
   if q>1.95 and n<2:x=-1900*ease((q-1.95)/.38)
   self.post(n,x)
   if n==2 and q>1.7:
    scale=1+.12*ease((q-1.7)/.63);nw,nh=round(W*scale),round(H*scale);self.im=self.im.resize((nw,nh),Image.Resampling.BICUBIC).crop(((nw-W)//2,(nh-H)//2,(nw+W)//2,(nh+H)//2));self.d=ImageDraw.Draw(self.im)
  elif t<12:
   q=t-9;i=max(j for j,c in enumerate(CUTS) if q>=c);size=round(57*SCALES[i])
   self.text(960,450,self.b['hinge'],size,self.accent,anchor='ma')
   self.text(960,365,'THE SAME OBJECTION.',27,self.dim,mono=True,anchor='ma')
  elif t<14:
   q=t-12;x=960+lerp(1700,0,ease(q/.35))
   if q>1.65:x-=2300*ease((q-1.65)/.35)
   self.text(x,400,self.b['turn'],160,anchor='ma',maxw=1750)
  elif t<24:
   q=t-14
   if q<3:
    p=ease((q-.6)/1.1)
    self.text(960,lerp(430,260,p),'Introducing',lerp(105,48,p),anchor='ma')
    if q>.6:self.text(960,lerp(900,460,p),self.b['invocation'],126,self.accent,mono=True,anchor='ma',maxw=1700)
   else:
    self.glass((240,185,1680,885));self.text(280,216,'LOCAL FIXTURE REPLAY',22,self.dim,mono=True)
    self.text(1640,216,self.b['brand'],22,self.dim,mono=True,anchor='ra')
    progress=ease((q-5)/.7);y=lerp(525,778,progress)
    self.d.rounded_rectangle((280,y-15,1640,y+65),radius=12,fill=self.bg,outline=self.line)
    count=int(min(1,(q-3)/2)*len(self.b['prompt']))
    self.text(305,y,self.b['prompt'][:max(0,count)],27,mono=True,maxw=1260)
    self.d.ellipse((1571,y+6,1617,y+52),fill=self.line)
    self.text(1594,y+8,'>',26,anchor='ma')
    if 4.8<q<5.7:
     px=lerp(1810,1590,ease((q-4.8)/.55));py=lerp(920,y+22,ease((q-4.8)/.55));self.d.polygon([(px,py),(px+12,py+45),(px+22,py+29),(px+40,py+27)],fill=self.ink)
    if 5.7<q<6.3:self.text(290,320,'... reading supplied data',26,self.dim,mono=True)
    for n,line in enumerate(self.findings):
     if q>=6.3+n*.38:self.text(290,325+n*74,'- '+line,31,mono=True,maxw=1320)
    if q>8:self.text(290,670,'Draft output prepared from the fixture.',33)
  elif t<28:
   self.text(960,120,self.b['closer'],62,anchor='ma',maxw=1740)
   p=ease((t-24)/.7)
   for n,r in enumerate(self.data['records']):
    x=170+n%2*810;y=290+n//2*310+(1-p)*130
    self.glass((x,y,x+760,y+260),18)
    self.text(x+32,y+28,r['title'],37,maxw=690)
    self.para(x+32,y+91,r['detail'],690,29,maxlines=2)
    self.text(x+32,y+200,r['status'].upper(),22,self.dim,mono=True,maxw=690)
  else:
   q=t-28;p=ease(q/.6)
   self.para(960,360+(1-p)*140,self.b['thesis'],1520,98,center=True,maxlines=2)
   if q>.55:
    self.glass((720,670,1200,758),44);self.text(960,687,self.b['invocation'],39,self.accent,mono=True,anchor='ma',maxw=440)
   if q>1:self.text(960,820,self.b['brand'].upper(),38,anchor='ma',maxw=1300)
   if q>1.4:self.text(960,893,self.b['cta'],27,self.dim,anchor='ma',maxw=1400)
  self.footer(t);return self.im

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('brief',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--poster-only',action='store_true');args=ap.parse_args()
 if args.out.exists():raise ValueError('Use a fresh output directory')
 b=json.loads(args.brief.read_text());source=(args.brief.parent/b['data']).resolve();data=json.loads(source.read_text());validate(b,data);film=Film(b,data)
 for n in range(DURATION*4):film.frame(n/4)
 args.out.mkdir(parents=True)
 (args.out/'brief.json').write_text(json.dumps({**b,'data':'data.json'},indent=2)+'\n');(args.out/'data.json').write_text(json.dumps(data,indent=2)+'\n')
 film.frame(5).save(args.out/'poster.png')
 if args.poster_only:return
 times=[1,3.2,5.5,7.8,9.8,12.7,16,20,23,26,30]
 captures={round(t*FPS):i for i,t in enumerate(times)}
 proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(args.out/'film.mp4')],stdin=subprocess.PIPE)
 try:
  for n in range(DURATION*FPS):
   im=film.frame(n/FPS);proc.stdin.write(im.tobytes())
   if n in captures:im.save(args.out/f'review-{captures[n]+1:02}.jpg',quality=92)
 finally:proc.stdin.close()
 if proc.wait():raise RuntimeError('Video render failed')
 subprocess.run(['ffmpeg','-v','error','-i',str(args.out/'film.mp4'),'-f','null','-'],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(args.out/'film.mp4')]))
 (args.out/'preview.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+html.escape(b['brand'])+' film</title><style>body{background:#10141d;color:white;font:18px system-ui;margin:3rem}video{width:100%;max-height:85vh}</style><h1>'+html.escape(b['brand'])+'</h1><video controls src="film.mp4" poster="poster.png"></video><p>Illustrative concept; fictional posts; supplied fixture data. Silent.</p></html>')
 (args.out/'proof.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Fixture output</title><h1>'+html.escape(b['source_label'])+'</h1>'+''.join('<article><h2>'+html.escape(r['title'])+'</h2><p>'+html.escape(r['detail'])+'</p><p>'+html.escape(r['status'])+'</p></article>' for r in data['records'])+'</html>')
 report=dict(width=W,height=H,fps=FPS,duration=float(probe['format']['duration']),decode='pass',audio=False,briefSha256=digest(args.brief),dataSha256=digest(source),rendererSha256=digest(Path(__file__)),findings=film.findings,zoomScales=SCALES,textFitChecks=len(film.checked),files={p.name:dict(sha256=digest(p),bytes=p.stat().st_size) for p in args.out.iterdir() if p.is_file()})
 (args.out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(output=str(args.out),duration=DURATION,bytes=(args.out/'film.mp4').stat().st_size)))

if __name__=='__main__':main()
