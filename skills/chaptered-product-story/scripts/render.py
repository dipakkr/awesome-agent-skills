#!/usr/bin/env python3
"""Original Product Chapters film renderer. No network or generation API."""
import argparse
from array import array
from functools import lru_cache
import hashlib
import html
import json
import math
from pathlib import Path
import shutil
import subprocess
import wave
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
W,H,FPS,DURATION=1920,1080,30,40
THEMES={
 'ink':('#142a30','#f8f2df','#eec879','#243e45','#a9bebc'),
 'paper':('#f1eee5','#23312d','#57743c','#fffdf6','#63766b'),
 'plum':('#292235','#f5efff','#d6b6ff','#3b304c','#baaaca'),
 'forest':('#20382e','#f4f0de','#c8db8b','#304b3f','#b0c4b4'),
}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def clamp(x):return max(0,min(1,x))
def ease(x):x=clamp(x);return 1-(1-x)**3
def mix(a,b,p):return a+(b-a)*p
@lru_cache(maxsize=80)
def font(size):return ImageFont.truetype(str(ROOT/'assets/fonts/DM-Sans.ttf'),round(size))
def run(args):return subprocess.run(args,check=True,capture_output=True,text=True).stdout

def text_value(value,key,limit):
 if not isinstance(value,str) or not value.strip() or len(value)>limit or any(ord(c)<32 for c in value):raise ValueError(f'{key}: nonempty single line, max {limit} characters')

def validate(b,base):
 for key,limit in [('brand',24),('title',50),('promise',65),('cta',42),('domain',50),('disclosure',95)]:text_value(b.get(key),key,limit)
 if b.get('theme') not in THEMES:raise ValueError('Unknown theme')
 if b.get('audio') not in ('silent','original-pulse'):raise ValueError('audio must be silent or original-pulse')
 if b.get('kind') not in ('concept','product'):raise ValueError('kind must be concept or product')
 if b['kind']=='concept' and 'concept' not in b['disclosure'].lower():raise ValueError('Concept interfaces must be disclosed')
 if not isinstance(b.get('chapters'),list) or len(b['chapters'])!=3:raise ValueError('Exactly three chapters required')
 for c in b['chapters']:
  for key,limit in [('label',18),('headline',42),('detail',95),('proof',55),('source',180),('screen',200)]:text_value(c.get(key),key,limit)
  focus=c.get('focus')
  if not isinstance(focus,list) or len(focus)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1 for v in focus):raise ValueError('focus: two finite fractions in 0..1')
  p=(base/c['screen']).resolve()
  if not p.is_file() or p.suffix.lower() not in ('.png','.jpg','.jpeg','.webp') or p.stat().st_size>30_000_000:raise ValueError('Supply local screenshot under 30 MB')
  with Image.open(p) as im:
   if im.width<1280 or im.height<720 or im.width*im.height>25_000_000:raise ValueError('Screenshot must be at least 1280x720 and below 25 megapixels')
 return b

class Film:
 def __init__(self,b,base):
  self.b=b;self.bg,self.ink,self.accent,self.panel,self.muted=THEMES[b['theme']]
  self.screens=[Image.open((base/c['screen']).resolve()).convert('RGB') for c in b['chapters']]
  self.boxes=[]
 def text(self,x,y,s,size=40,color=None,width=None):
  f=font(size);box=self.d.textbbox((x,y),s,font=f)
  if width and self.d.textlength(s,font=f)>width:raise ValueError('Copy too wide: '+s)
  if box[0]<48 or box[1]<32 or box[2]>W-48 or box[3]>H-40:raise ValueError('Text outside safe frame: '+s)
  self.d.text((x,y),s,font=f,fill=color or self.ink);self.boxes.append(box)
 def wrap(self,x,y,s,size,width,lines=3,color=None):
  rows=[];line=''
  for word in s.split():
   test=(line+' '+word).strip()
   if self.d.textlength(test,font=font(size))>width:
    if not line:raise ValueError('Word too wide')
    rows.append(line);line=word
   else:line=test
  rows.append(line)
  if len(rows)>lines:raise ValueError('Too many lines: '+s)
  for i,row in enumerate(rows):self.text(x,y+i*size*1.15,row,size,color,width)
  return len(rows)*size*1.15
 def mark(self,x,y,size,t):
  # Three offset rounded tabs align into an original chapter mark.
  for i in range(3):
   offset=(1-ease(t-i*.1))*30
   self.d.rounded_rectangle((x+i*size*.22,y+offset+i*size*.1,x+i*size*.22+size*.34,y+offset+size*.78+i*size*.1),radius=size*.1,fill=self.accent)
 def chrome(self,t):
  self.text(88,47,self.b['brand'],29,width=600)
  self.text(1435,53,'PRODUCT CHAPTERS',20,self.muted,width=395)
  self.d.line((88,100,1832,100),fill=self.muted,width=1)
  self.text(88,1004,self.b['disclosure'],21,self.muted,width=1600)
  for i,(start,end) in enumerate([(0,8),(8,16),(16,24),(24,32),(32,40)]):
   x=88+i*352;self.d.rounded_rectangle((x,970,x+330,976),radius=3,fill=self.panel)
   progress=clamp((t-start)/(end-start))
   if progress:self.d.rounded_rectangle((x,970,x+max(3,330*progress),976),radius=3,fill=self.accent)
 def screen(self,index,box,zoom,focus):
  im=self.screens[index];width,height=box[2]-box[0],box[3]-box[1]
  # Fit the whole screenshot, then crop into its specified focus without distortion.
  canvas=Image.new('RGB',(width,height),self.panel)
  fitted=ImageOps.contain(im,(width,height),Image.Resampling.LANCZOS)
  canvas.paste(fitted,((width-fitted.width)//2,(height-fitted.height)//2))
  cw,ch=width/zoom,height/zoom
  left=max(0,min(width-cw,focus[0]*width-cw/2));top=max(0,min(height-ch,focus[1]*height-ch/2))
  crop=canvas.crop((round(left),round(top),round(left+cw),round(top+ch))).resize((width,height),Image.Resampling.BICUBIC)
  mask=Image.new('L',(width,height));ImageDraw.Draw(mask).rounded_rectangle((0,0,width,height),radius=22,fill=255)
  self.im.paste(crop,(box[0],box[1]),mask)
  self.d.rounded_rectangle(box,radius=22,outline=self.muted,width=2)
 def frame(self,t):
  self.im=Image.new('RGB',(W,H),self.bg);self.d=ImageDraw.Draw(self.im);self.boxes=[]
  self.chrome(t)
  if t<4:
   self.mark(92,210,115,t)
   self.text(92,395,'A clearer way to',52,self.muted,width=1550)
   self.wrap(86,475,self.b['title'],115,1610,2)
   self.text(94,815,'THREE CHAPTERS. ONE CONNECTED STORY.',25,self.accent,width=1600)
   # Expanding chapter brackets give the opening a visible continuous movement.
   p=ease(t/2);self.d.line((92,760,92+round(1620*p),760),fill=self.accent,width=5)
  elif t<8:
   u=t-4;self.text(92,220,'THE IDEA',27,self.accent,width=500)
   words=self.b['promise'].split();visible=max(1,min(len(words),int(u*5)+1))
   self.wrap(86,330,' '.join(words[:visible]),101,1560,3)
   for i,c in enumerate(self.b['chapters']):
    x=92+i*570;y=780+round(25*(1-ease((u-i*.15)/.7)))
    self.d.rounded_rectangle((x,y,x+530,y+98),radius=16,fill=self.panel)
    self.text(x+24,y+24,f'{i+1:02}  '+c['label'],30,self.accent,width=490)
  elif t<32:
   n=min(2,int((t-8)//8));u=(t-8)%8;c=self.b['chapters'][n]
   self.text(88,159,f'{n+1:02}',125,self.accent,width=400)
   self.text(96,321,c['label'].upper(),25,self.muted,width=540)
   self.wrap(88,380,c['headline'],68,540,3)
   self.wrap(94,660,c['detail'],28,520,4,self.muted)
   # Three different scene compositions: workspace, layered canvas, detail takeover.
   if n==0:
    y=205+round(60*(1-ease(u/.8)))
    zoom=1+.27*ease((u-2.3)/1.4)-.12*ease((u-6)/1.2)
    self.screen(n,(690,y,1810,y+620),zoom,c['focus'])
    self.text(712,160,'CONCEPT INTERFACE' if self.b['kind']=='concept' else 'PRODUCT CAPTURE',22,self.muted,width=1060)
   elif n==1:
    # Diagonal paper layers provide depth; the screen glides over them.
    for j in range(3):
     dx=round(35*j*ease(u));dy=round(25*j*ease(u))
     self.d.rounded_rectangle((720+dx,182+dy,1740+dx,774+dy),radius=25,outline=self.muted,width=2)
    x=690+round(70*(1-ease(u/1.1)));y=238-round(25*ease((u-1)/3))
    self.screen(n,(x,y,x+1090,y+610),1+.15*ease((u-1.8)/2),c['focus'])
   else:
    # Replace the split composition with a large screen and a restrained caption band.
    self.im=Image.new('RGB',(W,H),self.bg);self.d=ImageDraw.Draw(self.im);self.chrome(t)
    y=145+round(35*(1-ease(u/.8)))
    self.screen(n,(130,y,1790,y+720),1+.3*ease((u-1.6)/2.2),c['focus'])
    self.d.rounded_rectangle((170,745,1750,925),radius=24,fill=self.panel)
    self.text(205,769,'03 / '+c['label'].upper(),24,self.accent,width=1400)
    self.text(205,819,c['headline'],53,self.ink,width=1480)
   if u>=4.3 and n<2:
    p=ease((u-4.3)/.7);x=690+round(50*(1-p))
    self.d.rounded_rectangle((x,850,1810,928),radius=14,fill=self.accent)
    self.text(x+24,870,c['proof'],29,self.bg,width=1030)
   if n<2:self.d.line((690,837,690+round(1120*clamp(u/8)),837),fill=self.accent,width=4)
  else:
   u=t-32;self.mark(92,185,100,u)
   self.wrap(88,355,self.b['cta'],112,1590,2)
   self.text(95,666,self.b['domain'],38,self.muted,width=1500)
   for i,c in enumerate(self.b['chapters']):
    x=95+i*570;self.d.line((x,790,x+500,790),fill=self.accent,width=2)
    self.text(x,815,f'{i+1:02}  '+c['label'],30,self.accent,width=510)
  # A short solid page-turn crosses scene boundaries; no borrowed slot-machine motif.
  for cut in (4,8,16,24,32):
   delta=t-cut
   if 0<=delta<.3:
    x=round(W*ease(delta/.3));self.d.rectangle((x,105,W,955),fill=self.panel)
  return self.im


def soundtrack(path,duration,theme):
 rate=44100;notes={'ink':[146.83,174.61,220,261.63],'paper':[130.81,164.81,196,246.94],'plum':[138.59,164.81,207.65,246.94],'forest':[130.81,155.56,196,233.08]}[theme]
 samples=array('h')
 for i in range(round(rate*duration)):
  t=i/rate;beat=t%.5;n=notes[int(t/2)%4]
  pad=.055*math.sin(2*math.pi*n*t)+.025*math.sin(2*math.pi*n*1.5*t)
  tick=.06*math.exp(-beat*35)*math.sin(2*math.pi*880*beat)
  low=.08*math.exp(-beat*15)*math.sin(2*math.pi*(65*beat-12*beat*beat))
  fade=min(1,t/1.5,(duration-t)/2)
  samples.append(round((pad+tick+low)*fade*32767))
 import sys
 if sys.byteorder!='little':samples.byteswap()
 with wave.open(str(path),'wb') as out:out.setnchannels(1);out.setsampwidth(2);out.setframerate(rate);out.writeframes(samples.tobytes())


def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('brief',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--start',type=float,default=0);p.add_argument('--end',type=float,default=DURATION);p.add_argument('--review-only',action='store_true')
 a=p.parse_args()
 if not 0<=a.start<a.end<=DURATION or not all(math.isfinite(v) for v in (a.start,a.end)):raise ValueError('Invalid render range')
 renderer_hash=sha(__file__);input_hash=sha(a.brief)
 b=validate(json.loads(a.brief.read_text()),a.brief.resolve().parent)
 if a.out.exists():raise ValueError('Use a new output directory')
 film=Film(b,a.brief.resolve().parent)
 # Preflight critical arrivals, settled copy and transition frames before writing output.
 times=sorted(set([.5,2.5,5.7,7.8,8.05,9,12.8,15.7,16.05,17,20.8,23.7,24.05,25,28.8,31.7,32.05,34,38.5]))
 for t in times:film.frame(t)
 a.out.mkdir(parents=True)
 for i,t in enumerate(times):film.frame(t).resize((960,540)).save(a.out/f'review-{i:02}.jpg',quality=90)
 film.frame(12.8).save(a.out/'poster.png')
 portable=json.loads(json.dumps(b));(a.out/'screens').mkdir()
 for index,c in enumerate(b['chapters'],1):
  source=(a.brief.resolve().parent/c['screen']).resolve();relative='screens/'+str(index)+source.suffix.lower()
  shutil.copyfile(source,a.out/relative);portable['chapters'][index-1]['screen']=relative
 (a.out/'brief.json').write_text(json.dumps(portable,indent=2)+'\n')
 if a.review_only:
  print('Preflight passed; review frames only.');return
 duration=(round(a.end*FPS)-round(a.start*FPS))/FPS
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-']
 if b['audio']=='original-pulse':
  soundtrack(a.out/'soundtrack.wav',DURATION,b['theme'])
  cmd+=['-ss',str(a.start),'-i',str(a.out/'soundtrack.wav'),'-map','0:v:0','-map','1:a:0','-c:a','aac','-b:a','160k']
 cmd+=['-t',str(duration),'-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(a.out/'film.mp4')]
 with (a.out/'encode.log').open('w') as log:
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
  try:
   for frame in range(round(a.start*FPS),round(a.end*FPS)):proc.stdin.write(film.frame(frame/FPS).tobytes())
   proc.stdin.close()
   if proc.wait()!=0:raise RuntimeError('Encoding failed; inspect encode.log')
  except BaseException:
   proc.kill();proc.wait();raise
 probe=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(a.out/'film.mp4')]))
 run(['ffmpeg','-v','error','-i',str(a.out/'film.mp4'),'-f','null','-'])
 video=next(s for s in probe['streams'] if s['codec_type']=='video')
 assert video['width']==W and video['height']==H and video['r_frame_rate']=='30/1'
 assert abs(float(probe['format']['duration'])-duration)<.1
 assert any(s['codec_type']=='audio' for s in probe['streams'])==(b['audio']=='original-pulse')
 (a.out/'preview.html').write_text('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+html.escape(b['brand'])+' film</title><body style="margin:0;background:#142a30;color:white;font:18px system-ui;padding:24px"><h1>'+html.escape(b['brand'])+'</h1><video style="width:100%;max-width:1280px" controls src="film.mp4" poster="poster.png"></video><p>'+html.escape(b['disclosure'])+'</p><p>Audio: '+html.escape(b['audio'])+'. Editable inputs: brief.json. Source capture provenance is recorded per chapter.</p></body>')
 files={f.name:dict(bytes=f.stat().st_size,sha256=sha(f)) for f in a.out.iterdir() if f.is_file()}
 report=dict(width=W,height=H,fps=FPS,duration=duration,range=[a.start,a.end],audio=b['audio'],decode='pass',rendererSha256=renderer_hash,inputSha256=input_hash,sources=[dict(path=c['screen'],source=c['source'],sha256=sha(a.brief.resolve().parent/c['screen'])) for c in b['chapters']],files=files,reviewTimes=times)
 (a.out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'output':str(a.out),'duration':duration,'audio':b['audio'],'decode':'pass'}))

if __name__=='__main__':main()
