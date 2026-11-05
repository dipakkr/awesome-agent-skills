#!/usr/bin/env python3
"""Original local motion renderer. Pillow + FFmpeg; no network or browser."""
import argparse
from functools import lru_cache
import hashlib
import html
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parents[1]
PALETTES = {
    'paper': ('#f5f1e9', '#202a2d', '#b94d32', '#ffffff', '#6c7777', '#dedbd2'),
    'night': ('#101923', '#f5f4ed', '#a8e681', '#1d2a37', '#b0bdc8', '#344351'),
    'lavender': ('#f1edfa', '#302840', '#7550c4', '#ffffff', '#736980', '#dcd4eb'),
    'ocean': ('#eaf4f5', '#12383e', '#167a87', '#ffffff', '#638086', '#c9dee1'),
}
DURATIONS = {'kinetic': 12, 'chat': 6.4, 'chart': 6.4, 'morph': 20, 'wall': 12, 'crew': 24}


def clamp(v): return max(0, min(1, v))
def ease(v):
    v = clamp(v)
    return v*v*(3-2*v)
def mix(a, b, p): return a+(b-a)*p
def phase(t, start, duration): return ease((t-start)/duration)


@lru_cache(maxsize=100)
def font(size, serif=False):
    return ImageFont.truetype(str(HERE/'assets/fonts'/('DM-Serif.ttf' if serif else 'DM-Sans.ttf')), max(8, int(size)))


def validate(b, mode):
    limits = {'brand':24, 'title':38, 'subtitle':90, 'cta':28, 'disclosure':72}
    for key, limit in limits.items():
        value = b.get(key)
        if not isinstance(value, str) or not value.strip() or len(value)>limit or any(ord(c)<32 for c in value):
            raise ValueError(f'{key}: nonempty single line, maximum {limit} characters')
    if b.get('theme') not in PALETTES: raise ValueError('Unknown theme')
    def lines(key, count, limit):
        value=b.get(key)
        if not isinstance(value,list) or len(value)!=count or any(not isinstance(s,str) or not s.strip() or len(s)>limit or any(ord(c)<32 for c in s) for s in value):
            raise ValueError(f'{key}: {count} nonempty strings of at most {limit} characters')
    if mode=='kinetic': lines('beats',3,32)
    if mode=='chat':
        lines('context',3,54)
        lines('conversation',2,110)
    if mode=='chart':
        lines('labels',5,10); lines('series_names',2,18)
        series=b.get('series')
        if not isinstance(series,list) or len(series)!=2 or any(not isinstance(a,list) or len(a)!=5 or any(type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=100 for v in a) for a in series):
            raise ValueError('series: two arrays of five finite values in 0..100')
        if not isinstance(b.get('unit'),str) or not b['unit'] or len(b['unit'])>20: raise ValueError('unit required, max20')
    if mode=='morph': lines('steps',4,42); lines('sessions',6,20)
    if mode=='wall': lines('filters',3,18)
    if mode=='crew': lines('roles',3,18); lines('tasks',3,50)
    return b


class Scene:
    def __init__(self,b,mode,media):
        self.b,self.mode,self.media=b,mode,media
        self.w,self.h=(1080,1080) if mode=='morph' else (1280,720)
        self.bg,self.ink,self.accent,self.card,self.muted,self.line=PALETTES[b['theme']]
        self.fit_checks=set()
        self.wall_image=None
        self.morph_tile=None
        if mode=='wall':
            wall=Image.new('RGB',(1800,1100),self.bg)
            for n in range(24):
                tile=ImageOps.fit(media[n%len(media)],(280,240))
                wall.paste(tile,((n%6)*300,(n//6)*260))
            self.wall_image=wall.rotate(13,resample=Image.Resampling.BICUBIC,expand=True,fillcolor=self.bg)

    def text(self,xy,s,size=28,color=None,serif=False,maxw=None,anchor=None):
        f=font(size,serif)
        width=self.d.textlength(s,font=f)
        if maxw and width>maxw: raise ValueError(f'Text does not fit ({width:.0f}>{maxw}): {s}')
        self.fit_checks.add(s)
        self.d.text(xy,s,font=f,fill=color or self.ink,anchor=anchor)

    def paragraph(self,xy,s,width,size=27,color=None,maxlines=3):
        words=s.split(); rows=[]; row=''
        for word in words:
            test=(row+' '+word).strip()
            if self.d.textlength(test,font=font(size))>width:
                if not row: raise ValueError('Word does not fit: '+word)
                rows.append(row);row=word
            else: row=test
        if row: rows.append(row)
        if len(rows)>maxlines: raise ValueError('Too many text lines: '+s)
        for i,row in enumerate(rows): self.text((xy[0],xy[1]+i*size*1.35),row,size,color,maxw=width)
        return len(rows)*size*1.35

    def rect(self,box,fill=None,radius=18,outline=None,width=1):
        self.d.rounded_rectangle(tuple(round(v) for v in box),radius=radius,fill=fill or self.card,outline=outline,width=width)

    def pill(self,x,y,s,active=False):
        width=self.d.textlength(s,font=font(19))+34
        self.rect((x,y,x+width,y+39),self.accent if active else self.card,19)
        self.text((x+17,y+7),s,19,self.bg if active else self.ink)
        return width

    def cursor(self,x,y,press=0):
        self.d.polygon([(x,y),(x+9,y+33),(x+15,y+23),(x+28,y+22)],fill=self.ink,outline=self.bg,width=2)
        if press: self.d.ellipse((x-18*press,y-18*press,x+18*press,y+18*press),outline=self.accent,width=3)

    def heading(self,kicker=None):
        self.text((56,35),self.b['brand'],24,maxw=340)
        self.text((self.w-56,40),kicker or 'MOTION STUDY',14,self.muted,anchor='ra')

    def footer(self,t):
        self.d.rectangle((0,self.h-58,self.w,self.h),fill=self.bg)
        self.d.line((56,self.h-56,self.w-56,self.h-56),fill=self.line,width=1)
        self.text((56,self.h-39),self.b['disclosure'],14,self.muted,maxw=self.w-210)
        self.text((self.w-56,self.h-39),f'{t:04.1f} / {DURATIONS[self.mode]:04.1f}',14,self.muted,anchor='ra')

    def presenter(self,frame,box,circle=False):
        x,y,w,h=map(round,box)
        fitted=ImageOps.fit(frame,(w,h),centering=(.34,.38))
        mask=Image.new('L',(w,h),0);md=ImageDraw.Draw(mask)
        if circle: md.ellipse((0,0,w-1,h-1),fill=255)
        else: md.rounded_rectangle((0,0,w-1,h-1),radius=20,fill=255)
        self.im.paste(fitted,(x,y),mask)
        self.d=ImageDraw.Draw(self.im)
        self.text((x+18,y+h-29),'STOCK FOOTAGE',12,'#ffffff')

    def frame(self,t,presenter=None):
        self.im=Image.new('RGB',(self.w,self.h),self.bg);self.d=ImageDraw.Draw(self.im)
        getattr(self,self.mode)(t,presenter)
        self.footer(t)
        return self.im

    def kinetic(self,t,_):
        self.heading('KINETIC NOTES')
        # Three deliberately different typographic motions, then a quiet CTA.
        beat=min(3,int(t/3)); q=t%3
        if beat==3:
            self.text((640,223),self.b['title'],64,serif=True,anchor='ma',maxw=1100)
            self.paragraph((290,335),self.b['subtitle'],700,28,maxlines=2)
            self.pill(490,461,self.b['cta'],True)
            return
        self.text((56,125),f'0{beat+1} / FIELD NOTES',17,self.muted)
        s=self.b['beats'][beat]
        if beat==0:
            words=s.split(); x=110
            for i,word in enumerate(words):
                p=phase(q,i*.12,.7)
                y=310+(1-p)*190
                self.text((x,y),word,66,self.accent if i==len(words)-1 else self.ink,serif=True)
                x+=self.d.textlength(word+' ',font=font(66,True))
            if x>1200: raise ValueError('Kinetic headline too long')
        elif beat==1:
            p=phase(q,0,1)
            self.rect((80,230,80+1120*p,440),self.accent,4)
            self.text((115,278),s,62,self.bg,serif=True,maxw=1050)
            self.text((115,465),self.b['subtitle'],25,self.muted,maxw=1050)
        else:
            p=phase(q,0,.9)
            self.d.ellipse((930-160*p,175,1190,435+100*p),outline=self.accent,width=6)
            self.text((100,260+(1-p)*110),s,66,serif=True,maxw=1080)
            self.d.line((105,370,105+850*phase(q,.6,.8),370),fill=self.accent,width=6)

    def chat(self,t,p):
        self.heading('ASK / REVIEW / APPLY')
        self.text((65,105),self.b['title'],49,serif=True,maxw=1130)
        self.rect((64,191,824,630),outline=self.line)
        self.text((94,219),'WORKSPACE / NOTES',15,self.muted)
        for i,line in enumerate(self.b['context']):
            self.d.ellipse((95,279+i*47,103,287+i*47),fill=self.accent)
            self.text((117,270+i*47),line,22,maxw=650)
        question,reply=self.b['conversation']
        q=phase(t,.3,.6)
        if q>0:
            y=429+(1-q)*28
            self.rect((92,y,791,y+75),self.bg,12)
            self.paragraph((113,y+13),question,650,22,maxlines=2)
        if .95<t<2.05:
            for i in range(3):
                r=4+2*math.sin(t*8-i)
                self.d.ellipse((120+i*22-r,539-r,120+i*22+r,539+r),fill=self.accent)
        if t>=2.05:
            v=phase(t,2.05,.8)
            self.rect((92,518,791,518+90*v),self.accent,12)
            if v>.85:self.paragraph((113,532),reply,650,22,self.bg,maxlines=2)
        self.presenter(p,(890,215,300,300),True)
        self.text((1040,548),'A useful answer.',29,serif=True,anchor='ma')
        self.text((1040,588),'Your context stays visible.',18,self.muted,anchor='ma')

    def chart(self,t,p):
        self.heading('A COMPARISON IN MOTION')
        self.text((64,100),self.b['title'],49,serif=True,maxw=1140)
        swap=phase(t,1.8,.65)-phase(t,4,.65)
        chartx=mix(64,414,swap); px=934+350*swap
        self.rect((chartx,190,chartx+804,630),outline=self.line)
        self.text((chartx+30,213),self.b['unit'],18,self.muted)
        left,top,cw,ch=chartx+72,276,680,256
        for val in [0,25,50,75,100]:
            y=top+ch*(1-val/100)
            self.d.line((left,y,left+cw,y),fill=self.line)
            self.text((left-15,y-10),str(val),14,self.muted,anchor='ra')
        for i,label in enumerate(self.b['labels']):self.text((left+i*cw/4,547),label,16,self.muted,anchor='ma')
        for n,values in enumerate(self.b['series']):
            progress=phase(t,.15 if n==0 else 2.5,1.35)
            color=self.accent if n==0 else self.muted
            coords=[(left+i*cw/4,top+ch*(1-v/100)) for i,v in enumerate(values)]
            length=4*progress
            for i in range(4):
                if length<=i: break
                f=clamp(length-i); a,z=coords[i],coords[i+1]
                self.d.line((a[0],a[1],mix(a[0],z[0],f),mix(a[1],z[1],f)),fill=color,width=5)
                self.d.ellipse((a[0]-5,a[1]-5,a[0]+5,a[1]+5),fill=color)
            if progress==1:
                x,y=coords[-1];self.d.ellipse((x-5,y-5,x+5,y+5),fill=color)
            self.d.line((chartx+34+n*370,594,chartx+56+n*370,594),fill=color,width=4)
            self.text((chartx+65+n*370,580),self.b['series_names'][n],19,maxw=290)
        self.presenter(p,(px,190,282,440))
        if swap>0:self.presenter(p,(px-1220,190,282,440))

    def morph(self,t,_):
        self.heading('ONE GESTURE / FOUR STATES')
        self.text((540,138),self.b['title'],57,serif=True,anchor='ma',maxw=950)
        self.paragraph((140,223),self.b['subtitle'],800,27,maxlines=2)
        # One geometric panel persists through button, prompt, options, result.
        if t<11:
            grow=phase(t,1.4,1.2); options=phase(t,4.9,1); result=phase(t,8,1)
            w=mix(280,850,grow);h=mix(94,235,grow)+options*125-result*65
            x=(1080-w)/2;y=420-(h-94)/3
            self.rect((x+7,y+12,x+w+7,y+h+12),self.line,22)
            self.rect((x,y,x+w,y+h),self.accent if grow<.4 else self.card,22)
            if grow<.2:self.text((540,y+25),self.b['steps'][0],29,self.bg,anchor='ma',maxw=250)
            elif grow>.9:
                self.text((x+35,y+30),'PROMPT / '+self.b['brand'].upper(),17,self.muted)
                typed=self.b['steps'][1][:int(len(self.b['steps'][1])*clamp((t-2.6)/1.4))]
                self.paragraph((x+35,y+84),typed,w-70,33,maxlines=2)
                if options>.9 and result<.6:
                    self.pill(x+35,y+210,self.b['steps'][2],True)
                    self.cursor(x+w-100,y+240,math.sin(clamp(t-6.5)*math.pi))
                if result>.9:
                    self.rect((x+24,y+184,x+w-24,y+258),self.accent,12)
                    self.text((x+45,y+198),self.b['steps'][3],27,self.bg,maxw=w-90)
            if t<1.5:self.cursor(mix(800,620,phase(t,0,.8)),mix(650,465,phase(t,0,.8)))
            if 4<t<10:
                for i in range(3):self.d.ellipse((95+i*390,790+math.sin(t+i)*15,121+i*390,816+math.sin(t+i)*15),fill=self.accent)
        elif t<16:
            p=phase(t,11,1.2); zoom=phase(t,14,1.5)
            if self.morph_tile is None:
                saved=self.im.copy()
                self.morph(10.95,None)
                self.morph_tile=self.im.crop((115,353,965,648))
                self.im=saved;self.d=ImageDraw.Draw(self.im)
            for i in [1,2,3,4,5,0]:
                s=self.b['sessions'][i]
                if i and p<.2:continue
                x=95+(i%2)*465;y=350+(i//2)*180
                scale=mix(1.8,1,p)
                x=540+(x-540)*scale;y=550+(y-550)*scale
                if i==3:
                    x=mix(x,95,zoom);y=mix(y,350,zoom)
                    w=mix(425,890,zoom);h=mix(145,450,zoom)
                else:w=425;h=145
                if i==0:
                    x=mix(115,95,p);y=mix(353,350,p);w=mix(850,425,p);h=mix(295,145,p)
                if zoom>.25 and i!=3:continue
                if i==0:
                    tile=self.morph_tile.resize((round(w),round(h)),Image.Resampling.LANCZOS)
                    self.im.paste(tile,(round(x),round(y)));self.d=ImageDraw.Draw(self.im)
                    continue
                self.rect((x,y,x+w,y+h),outline=self.accent if i==3 else self.line,width=2)
                self.text((x+25,y+25),s,23,maxw=w-50)
                self.d.line((x+25,y+82,x+w-25,y+82),fill=self.line,width=3)
                if i==3 and zoom>.85:self.paragraph((x+30,y+150),self.b['steps'][3],w-60,42,maxlines=2)
        else:
            self.text((540,440),self.b['steps'][3],49,serif=True,anchor='ma',maxw=960)
            self.text((540,560),self.b['cta'],29,self.accent,anchor='ma',maxw=900)

    def wall(self,t,_):
        p=phase(t,0,2.2)
        x=-300;y=int(mix(280,-330,p))
        self.im.paste(self.wall_image,(x,y));self.d=ImageDraw.Draw(self.im)
        # Readable library surface over a tilted wall of supplied artwork.
        self.rect((48,28,1232,100),self.bg,16);self.heading('COLLECT / SELECT / OPEN')
        z=phase(t,6.7,1.6)
        if z<.98:
            self.rect((310,177,970,605),self.card,22,outline=self.line)
            self.text((345,210),self.b['title'],42,serif=True,maxw=590)
            xx=345
            for i,s in enumerate(self.b['filters']):xx+=self.pill(xx,280,s,t>2.7 and i==1)+12
            for i in range(3):
                thumb=ImageOps.fit(self.media[i%len(self.media)],(180,174))
                self.im.paste(thumb,(345+i*194,345))
                if t>3 and i==1:self.d.rectangle((538,343,721,520),outline=self.accent,width=4)
            self.text((345,546),self.b['cta'],24,self.accent,maxw=550)
            self.cursor(mix(1060,635,phase(t,1.5,1)),mix(580,303,phase(t,1.5,1)))
        if z>0:
            w=int(mix(180,610,z));h=int(mix(174,470,z));x=int(mix(539,64,z));y=int(mix(345,153,z))
            hero=ImageOps.fit(self.media[1%len(self.media)],(w,h));self.im.paste(hero,(x,y));self.d=ImageDraw.Draw(self.im)
            if z>.98:
                self.rect((710,153,1216,623),self.card,20)
                self.text((746,193),'SELECTED / 02',17,self.muted)
                self.paragraph((746,252),self.b['title'],430,47,maxlines=2)
                self.paragraph((746,399),self.b['subtitle'],424,24,maxlines=3)
                self.pill(746,536,'Ready to review' if t>10 else self.b['cta'],t>10)

    def character(self,x,y,kind,scale=1,t=0):
        # Original geometric crew, not reference characters or third-party mascots.
        y+=math.sin(t*2+kind)*6;w=110*scale;h=(105+kind*18)*scale
        colors=[self.accent,'#e8b45c','#71a7a1']
        if kind==1:self.d.ellipse((x-w/2,y-h/2,x+w/2,y+h/2),fill=colors[kind])
        elif kind==2:self.d.polygon([(x,y-h*.65),(x-w*.62,y+h*.45),(x+w*.62,y+h*.45)],fill=colors[kind])
        else:self.rect((x-w/2,y-h/2,x+w/2,y+h/2),colors[kind],int(25*scale))
        for xx in [x-17*scale,x+17*scale]:self.d.ellipse((xx-4*scale,y-5*scale,xx+4*scale,y+5*scale),fill='#17272c')
        self.d.arc((x-12*scale,y+7*scale,x+12*scale,y+22*scale),0,180,fill='#17272c',width=max(1,int(3*scale)))

    def crew(self,t,_):
        for x in range(30,1280,30):
            for y in range(25,650,30):self.d.ellipse((x,y,x+1,y+1),fill=self.line)
        self.heading('MEET YOUR WORKFLOW CREW')
        if t<5:
            self.text((640,142),self.b['title'],61,serif=True,anchor='ma',maxw=1130)
            for i,role in enumerate(self.b['roles']):
                x=320+i*320;p=phase(t,i*.3,.9)
                self.character(x,400+(1-p)*300,i,1.45,t)
                if p>.95:self.text((x,540),role,26,anchor='ma',maxw=290)
        elif t<17:
            i=min(2,int((t-5)/4));q=(t-5)%4
            self.text((80,157),self.b['roles'][i],55,serif=True,maxw=530)
            self.character(260,430 if i==2 else 390,i,2,t)
            self.rect((570,151,1190,601),self.card,22,self.line)
            self.text((604,182),'WORKSPACE / DRAFT',17,self.muted)
            self.d.line((603,226,1157,226),fill=self.line)
            self.paragraph((605,269),self.b['tasks'][i],520,37,maxlines=3)
            if q>.8:
                progress=phase(q,.8,1.2)
                self.rect((605,442,605+520*progress,451),self.accent,4)
            if q>2.1:self.pill(605,496,'Ready for your review',True)
        elif t<20:
            self.text((640,176),'One shared workspace.',59,serif=True,anchor='ma')
            for i in range(3):
                x=mix(250+i*390,480+i*160,phase(t,17,1.5))
                self.character(x,410,i,1,t)
            self.text((640,550),'You make the final call.',27,self.muted,anchor='ma')
        else:
            self.text((640,195),self.b['brand'],75,serif=True,anchor='ma',maxw=1120)
            self.paragraph((310,322),self.b['subtitle'],660,30,maxlines=2)
            self.pill(510,480,self.b['cta'],True)


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('brief',type=Path);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--presenter',type=Path);ap.add_argument('--preview-at',type=float)
    args=ap.parse_args()
    config=json.loads((HERE/'config.json').read_text());mode=config['mode']
    b=validate(json.loads(args.brief.read_text()),mode)
    for binary in ['ffmpeg','ffprobe']:
        if not shutil.which(binary):raise ValueError(f'{binary} is required on PATH')
    duration=DURATIONS[mode];fps=24
    if args.out.exists():raise ValueError('Use a new output directory; refusing overwrite')
    media=[];asset_hashes={}
    if mode=='wall':
        paths=b.get('media',[])
        if not isinstance(paths,list) or not 3<=len(paths)<=12:raise ValueError('wall needs 3–12 local media paths')
        for path in paths:
            p=(args.brief.parent/path).resolve()
            with Image.open(p) as src:media.append(ImageOps.exif_transpose(src).convert('RGB').copy())
            asset_hashes[p.name]=digest(p)
    if mode in ['chat','chart']:
        if not args.presenter or not args.presenter.is_file():raise ValueError('Supply --presenter with a continuous local clip')
        info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(args.presenter)]))
        if float(info['format']['duration'])<duration:raise ValueError('Presenter clip is shorter than 6.4s; it will not be looped')
        asset_hashes[args.presenter.name]=digest(args.presenter)
    scene=Scene(b,mode,media)
    # Full dry run of the timeline at 4fps catches text overflow before writing.
    blank=Image.new('RGB',(640,360),'#777777')
    for n in range(math.ceil(duration*4)):scene.frame(n/4,blank)
    args.out.mkdir(parents=True)
    (args.out/'brief.json').write_text(json.dumps(b,indent=2)+'\n')
    if args.preview_at is not None:
        scene.frame(args.preview_at,blank).save(args.out/'preview.png');return
    with tempfile.TemporaryDirectory(prefix='cad-motion-') as tmp:
        frames=Path(tmp)
        if args.presenter:
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(args.presenter),'-t',str(duration),'-vf',f'fps={fps},scale=960:-2','-q:v','3',str(frames/'%05d.jpg')],check=True)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{scene.w}x{scene.h}','-r',str(fps),'-i','-','-an','-c:v','libx264','-preset','fast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(args.out/'film.mp4')]
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
        sample_frames=[int(fps*s) for s in [.5,duration*.28,duration*.53,duration*.8,duration-.3]]
        try:
            for n in range(round(duration*fps)):
                presenter=None
                if args.presenter:
                    with Image.open(frames/f'{n+1:05d}.jpg') as src:presenter=src.convert('RGB')
                im=scene.frame(n/fps,presenter)
                proc.stdin.write(im.tobytes())
                if n in sample_frames:im.save(args.out/f'review-{sample_frames.index(n)+1}.jpg',quality=90)
                if n==int(duration*.53*fps):im.save(args.out/'poster.png')
        finally:proc.stdin.close()
        if proc.wait():raise RuntimeError('FFmpeg failed')
    subprocess.run(['ffmpeg','-v','error','-i',str(args.out/'film.mp4'),'-f','null','-'],check=True)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(args.out/'film.mp4')]))
    report={'mode':mode,'width':scene.w,'height':scene.h,'fps':fps,'duration':float(info['format']['duration']),'audio':False,'decode':'pass','briefSha256':digest(args.brief),'rendererSha256':digest(Path(__file__)),'inputAssets':asset_hashes,'textFitChecks':len(scene.fit_checks),'files':{p.name:{'sha256':digest(p),'bytes':p.stat().st_size} for p in args.out.iterdir() if p.is_file()}}
    (args.out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
    title=html.escape(b['title'])
    (args.out/'preview.html').write_text(f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>{title}</title><style>body{{background:#121820;color:white;font:18px system-ui;max-width:1000px;margin:40px auto;padding:20px}}video{{width:100%;max-height:80vh}}a{{color:#a8e681}}</style><h1>{title}</h1><video controls playsinline poster="poster.png" src="film.mp4"></video><p>{html.escape(b["disclosure"])}</p><a href="film.mp4" download>Download film</a> · <a href="brief.json" download>Editable inputs</a></html>')
    print(json.dumps({'out':str(args.out),'mode':mode,'seconds':report['duration'],'bytes':(args.out/'film.mp4').stat().st_size}))


if __name__=='__main__':main()
