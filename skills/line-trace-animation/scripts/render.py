#!/usr/bin/env python3
"""Original frame-driven countdown, path, conversation and particle compositions."""
import argparse,html,json,math
from pathlib import Path
from PIL import Image
import engine as e
HERE=Path(__file__).resolve().parents[1]

def validate(b,mode):
 for k,n in [('brand',24),('title',46),('subtitle',88),('source',85)]:e.text_check(b.get(k),k,n)
 if b.get('theme') not in e.THEMES:raise ValueError('Unknown theme')
 if mode=='countdown':
  if type(b.get('seconds')) is not int or not 3<=b['seconds']<=60:raise ValueError('seconds: integer from 3 to 60')
  e.text_check(b.get('ending'),'ending',22)
 elif mode=='vector':
  segments=b.get('segments')
  if not isinstance(segments,list) or not 1<=len(segments)<=4:raise ValueError('Use 1..4 cubic segments')
  for seg in segments:
   if not isinstance(seg,list) or len(seg)!=4:raise ValueError('Each cubic needs four control points')
   for point in seg:
    if not isinstance(point,list) or len(point)!=2 or any(type(v) not in (float,int) or not math.isfinite(v) or not 0<=v<=1 for v in point):raise ValueError('Control points must be finite normalized x,y pairs')
  if any(a[-1]!=b[0] for a,b in zip(segments,segments[1:])):raise ValueError('Adjacent path endpoints must join')
  e.text_check(b.get('caption'),'caption',30)
 elif mode=='chat':
  if not isinstance(b.get('people'),list) or len(b['people'])!=2:raise ValueError('Two participant labels required')
  for name in b['people']:e.text_check(name,'person',16)
  if not isinstance(b.get('messages'),list) or len(b['messages'])!=4:raise ValueError('Exactly four messages required')
  for m in b['messages']:
   if type(m.get('from')) is not int or m['from'] not in (0,1):raise ValueError('Message sender must be 0 or 1')
   e.text_check(m.get('text'),'message',60)
  e.text_check(b.get('closing'),'closing',35)
 elif mode=='particles':
  if b.get('shape') not in ['sphere','torus','helix','wave']:raise ValueError('Unknown particle shape')
  if type(b.get('density')) is not int or not 180<=b['density']<=700:raise ValueError('density: integer 180..700')
  e.text_check(b.get('caption'),'caption',35)
 else:raise ValueError('Unknown technique')
 return b

def duration(b,mode):return b['seconds']+2 if mode=='countdown' else {'vector':10,'chat':16,'particles':8}[mode]
def remaining(b,t):return max(0,math.ceil(b['seconds']-max(0,t)))
def message_start(i):return 1+i*3.2

def curve_points(segments):
 points=[]
 for seg in segments:
  for i in range(121):
   if points and i==0:continue
   t=i/120;weights=[(1-t)**3,3*(1-t)**2*t,3*(1-t)*t*t,t**3]
   points.append(tuple(sum(w*p[k] for w,p in zip(weights,seg)) for k in (0,1)))
 return points

class Film(e.ArtScene):
 def __init__(self,b,mode,base):
  super().__init__(b,mode,base);self.duration=duration(b,mode);e.DURATIONS[mode]=self.duration
  if mode=='vector':
   self.points=[(650+510*x,160+430*y) for x,y in curve_points(b['segments'])]
   self.dist=[0]
   for a,c in zip(self.points,self.points[1:]):self.dist.append(self.dist[-1]+math.dist(a,c))
   if self.dist[-1]<20:raise ValueError('The path is too short to animate')
 def layout(self,label):
  self.start();self.kicker(label);self.headline(56,136,self.b['title'],480,55,maxlines=3)
  self.wrap(58,394,self.b['subtitle'],440,22,self.muted,3);self.footer()
 def countdown(self,t):
  self.layout('An opening worth waiting for');cx,cy,r=928,352,220
  for i in range(60):
   a=i*math.tau/60-math.pi/2;rr=r-9 if i%5 else r-18
   self.d.line([(cx+math.cos(a)*rr,cy+math.sin(a)*rr),(cx+math.cos(a)*r,cy+math.sin(a)*r)],fill=self.line,width=2)
  self.d.ellipse((cx-r-17,cy-r-17,cx+r+17,cy+r+17),outline=self.line,width=1)
  p=min(1,max(0,t/self.b['seconds']))
  if p<1:self.d.arc((cx-r+30,cy-r+30,cx+r-30,cy+r-30),-90+360*p,270,fill=self.accent,width=5)
  value=remaining(self.b,t)
  self.text(cx,286,f'{value//60:02}:{value%60:02}',89,maxw=360,serif=True,anchor='mt')
  self.text(cx,410,'STARTING SOON' if value else self.b['ending'].upper(),17,self.muted,370,anchor='mt')
  self.text(58,573,'A MOMENT TO GET READY',13,self.muted,460)
  self.d.line((58,613,530,613),fill=self.line,width=2)
  self.d.line((58,613,58+472*p,613),fill=self.accent,width=2)
  return self.im
 def vector(self,t):
  self.layout('One continuous gesture');self.text(58,566,self.b['caption'],27,self.accent,470,serif=True)
  for r in [120,190,248]:self.d.ellipse((915-r,368-r*.85,915+r,368+r*.85),outline=self.line,width=1)
  # Progress follows sampled arc length, not control-point index.
  target=self.dist[-1]*e.progress(t,.4,3.6);shown=[self.points[0]]
  for i in range(1,len(self.points)):
   if self.dist[i]<=target:shown.append(self.points[i]);continue
   if self.dist[i]>self.dist[i-1]:
    p=(target-self.dist[i-1])/(self.dist[i]-self.dist[i-1]);shown.append(tuple(e.mix(a,b,p) for a,b in zip(self.points[i-1],self.points[i])))
   break
  if len(shown)>1:
   self.d.line(shown,fill=self.accent,width=13,joint="curve")
   for x,y in shown:self.d.ellipse((x-6.5,y-6.5,x+6.5,y+6.5),fill=self.accent)
  for idx in [0,len(self.points)//2,len(self.points)-1]:
   x,y=self.points[idx];self.d.ellipse((x-9,y-9,x+9,y+9),fill=self.bg,outline=self.line,width=2)
  if t>.4:
   x,y=shown[-1];self.d.ellipse((x-8,y-8,x+8,y+8),fill=self.ink)
  return self.im
 def chat(self,t):
  self.layout('A story, one reply at a time')
  self.panel((599,94,1224,642),self.paper,28)
  self.text(632,120,' / '.join(self.b['people']),21,maxw=555)
  self.text(632,155,'AN ILLUSTRATIVE CONVERSATION',11,self.muted,555)
  self.d.line((630,185,1193,185),fill=self.line,width=1)
  for i,m in enumerate(self.b['messages']):
   start=message_start(i);y=207+i*103;x=631 if m['from']==0 else 686
   if start-.6<t<start:
    self.rr((x,y,x+86,y+39),self.line,18)
    for j in range(3):
     radius=3+math.sin((t-start)*8+j)*1.2;xx=x+25+j*17
     self.d.ellipse((xx-radius,y+19-radius,xx+radius,y+19+radius),fill=self.muted)
   p=e.out(t,start,.55)
   def bubble():
    yy=y+12*(1-p);fill=self.bg if m['from']==0 else self.ink;ink=self.ink if m['from']==0 else self.bg
    self.rr((x,yy,x+505,yy+88),fill,15)
    self.wrap(x+21,yy+18,m['text'],462,22,ink,2)
   self.blend_group(p,bubble)
  p=e.out(t,11.6,.8)
  self.blend_group(p,lambda:self.wrap(58,548,self.b['closing'],460,31,self.accent,2))
  return self.im
 def particles(self,t):
  self.layout('A field of possibilities');phase=math.tau*(t%8)/8
  self.text(58,571,self.b['caption'],28,self.accent,470,serif=True)
  pts=[];n=self.b['density'];shape=self.b['shape']
  for i in range(n):
   u=i/n;angle=i*2.399963229728653
   if shape=='sphere':
    y=1-2*u;r=math.sqrt(max(0,1-y*y));x=r*math.cos(angle);z=r*math.sin(angle)
   elif shape=='torus':
    a=u*math.tau*17;b=u*math.tau;r=.72+.24*math.cos(a);x=r*math.cos(b);z=r*math.sin(b);y=.24*math.sin(a)
   elif shape=='helix':
    a=u*math.tau*4;r=.64+.12*math.sin(i*1.7);x=r*math.cos(a);z=r*math.sin(a);y=1.8*u-.9
   else:
    side=math.ceil(math.sqrt(n));x=(i%side)/(side-1)*1.9-.95;z=(i//side)/(side-1)*1.9-.95;y=math.sin(x*3+z*2+phase)*.28
   xx=x*math.cos(phase)+z*math.sin(phase);zz=-x*math.sin(phase)+z*math.cos(phase)
   yy=y*.85-zz*.38;depth=y*.38+zz*.85;scale=2.6/(2.6-depth*.55)
   px=917+xx*208*scale;py=355+yy*208*scale
   pts.append((depth,px,py,i))
  for depth,x,y,i in sorted(pts):
   q=(depth+1.4)/2.8;r=1.8+2.8*q;col=e.tint(self.bg,self.accent,.28+.7*q)
   self.d.ellipse((x-r,y-r,x+r,y+r),fill=col)
   if i%31==0:
    self.d.line((x-6,y,x+6,y),fill=col,width=1);self.d.line((x,y-6,x,y+6),fill=col,width=1)
  return self.im
 def frame(self,t,transparent=False):return getattr(self,self.mode)(t)

def svg(b):
 commands=[]
 for i,seg in enumerate(b['segments']):
  points=[(round(x*1020,3),round(y*860,3)) for x,y in seg]
  if i==0:commands.append('M '+' '.join(map(str,points[0])))
  commands.append('C '+' '.join(str(v) for p in points[1:] for v in p))
 return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-20 -20 1060 900" role="img"><title>'+html.escape(b['caption'])+'</title><path d="'+' '.join(commands)+'" fill="none" stroke="'+e.THEMES[b['theme']][2]+'" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def main():
 p=argparse.ArgumentParser();p.add_argument('brief',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--stills-only',action='store_true');a=p.parse_args()
 if a.out.exists():raise ValueError('Use a new output directory')
 mode=json.loads((HERE/'config.json').read_text())['mode'];b=validate(json.loads(a.brief.read_text()),mode)
 hashes={'sourceSha256':e.sha(a.brief),'rendererSha256':e.sha(__file__),'engineSha256':e.sha(HERE/'scripts/engine.py'),'configSha256':e.sha(HERE/'config.json')}
 scene=Film(b,mode,a.brief.parent);d=scene.duration
 for i in range(d*e.FPS):scene.frame(i/e.FPS)
 a.out.mkdir(parents=True);(a.out/'brief.json').write_text(json.dumps(b,indent=2)+'\n')
 times=[0,.8,2.8,d*.65,d-1/e.FPS]
 for i,t in enumerate(times):scene.frame(t).save(a.out/f'review-{i+1:02}.png')
 poster=2 if mode=='countdown' else 13 if mode=='chat' else 5
 scene.frame(poster).save(a.out/'poster.png')
 if mode=='vector':(a.out/'path.svg').write_text(svg(b))
 report={'mode':mode,**hashes,'reviewTimes':times,'posterTime':poster,'silence':True,'authoredExample':True,'decode':'not-rendered','files':{}}
 if mode=='particles':
  report['loopSeamExact']=scene.frame(0).tobytes()==scene.frame(d).tobytes()
  assert report['loopSeamExact']
 if mode=='countdown':report['countdownBoundary']={'beforeZero':remaining(b,b['seconds']-1/e.FPS),'atZero':remaining(b,b['seconds']),'last':remaining(b,d-1/e.FPS),'zeroHoldSeconds':2}
 if not a.stills_only:report['video']=e.encode(scene,a.out);report['decode']='pass'
 (a.out/'preview.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+html.escape(b['title'])+'</title><style>body{max-width:1200px;margin:40px auto;padding:20px;background:#161c23;color:#eee;font:18px system-ui}video{width:100%;border-radius:20px}a{color:#b5e789}</style><h1>'+html.escape(b['title'])+'</h1><video controls muted playsinline poster="poster.png" src="film.mp4"></video><p>'+html.escape(b['source'])+'</p><p>Silent Full HD motion. <a href="brief.json">Editable brief</a></p>'+('<a href="path.svg">Editable vector path</a>' if mode=='vector' else '')+'</html>')
 for f in sorted(a.out.iterdir()):report['files'][f.name]={'sha256':e.sha(f),'bytes':f.stat().st_size}
 (a.out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'mode':mode,'decode':report['decode'],'output':str(a.out)}))
if __name__=='__main__':main()
