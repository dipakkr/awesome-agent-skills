#!/usr/bin/env python3
"""Parametric geometry, validated STL/3MF, offline WebGL and exact-mesh renders."""
import argparse
import hashlib
import html
import json
import math
from pathlib import Path
import re
import subprocess
import zipfile

import manifold3d as md
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import trimesh

MODES = ('vessel', 'robot', 'mushroom', 'nameplate', 'organizer')


def number(c, key, default, low, high):
    x = c.get(key, default)
    if type(x) not in (int, float) or not math.isfinite(x) or not low <= x <= high:
        raise ValueError(f'{key} must be a finite number between {low} and {high}')
    return x


def validate(c):
    if not isinstance(c, dict) or c.get('mode') not in MODES:
        raise ValueError('Choose a supported mode')
    if not isinstance(c.get('name'), str) or not 1 <= len(c['name']) <= 70:
        raise ValueError('name must have 1 to 70 characters')
    if not isinstance(c.get('color'), str) or not re.fullmatch('#[0-9a-fA-F]{6}', c['color']):
        raise ValueError('color must be a six-digit hex color')
    allowed = {'mode', 'name', 'color'}
    if c['mode'] == 'vessel':
        allowed |= {'height', 'profile', 'wall', 'base', 'flutes', 'amplitude', 'twist'}
        number(c, 'height', 120, 25, 180); number(c, 'wall', 3, 2.4, 7)
        number(c, 'base', 3, 2.4, 8); number(c, 'amplitude', 2, 0, 5)
        number(c, 'twist', 60, -100, 100)
        flutes = number(c, 'flutes', 16, 4, 24)
        if int(flutes) != flutes: raise ValueError('flutes must be an integer')
        profile = c.get('profile')
        if not isinstance(profile, list) or not 2 <= len(profile) <= 8: raise ValueError('profile needs 2 to 8 [height fraction, radius] pairs')
        for pair in profile:
            if not isinstance(pair, list) or len(pair) != 2: raise ValueError('Invalid profile pair')
            number({'t':pair[0]}, 't', 0, 0, 1); number({'r':pair[1]}, 'r', 30, 12, 75)
        if profile[0][0] != 0 or profile[-1][0] != 1 or any(a[0] >= b[0] for a,b in zip(profile,profile[1:])): raise ValueError('Profile must increase from 0 to 1')
        if min(p[1] for p in profile)-c.get('amplitude',2)-c.get('wall',3) < 5: raise ValueError('Inner radius too small')
    elif c['mode'] in ('robot', 'mushroom'):
        allowed |= {'height', 'head_scale', 'eye_spacing', 'cap_width'}
        number(c,'height',85,65,140); number(c,'head_scale',1,.85,1.2)
        number(c,'eye_spacing',13,10,17); number(c,'cap_width',56,48,68)
        irrelevant = {'robot': {'cap_width'}, 'mushroom': {'head_scale'}}[c['mode']]
        if irrelevant & c.keys(): raise ValueError('Parameter does not apply to selected character')
    elif c['mode'] == 'nameplate':
        allowed |= {'text', 'width', 'depth', 'relief'}
        if not isinstance(c.get('text'),str) or not re.fullmatch('[A-Z0-9 ]{1,9}', c['text']) or not c['text'].strip(): raise ValueError('text supports 1 to 9 uppercase Latin letters, digits or spaces')
        number(c,'width',130,90,180);number(c,'depth',48,35,65);number(c,'relief',2.6,1.5,4)
    else:
        allowed |= {'width', 'depth', 'cup_height'}
        number(c,'width',132,120,170);number(c,'depth',86,80,110);number(c,'cup_height',52,35,70)
    if set(c)-allowed: raise ValueError('Unknown config keys: '+', '.join(sorted(set(c)-allowed)))
    return c


def ball(scale, pos, segments=40):
    return md.Manifold.sphere(1,segments).scale(scale).translate(pos)


def box(size,pos,r=0):
    if r:
        s=md.Manifold.cube([v-2*r for v in size],True).minkowski_sum(md.Manifold.sphere(r,16))
    else:s=md.Manifold.cube(size,True)
    return s.translate(pos)


def cylinder(radius,height,pos=(0,0,0)):
    return md.Manifold.cylinder(height,radius,radius,64).translate(pos)


def combine(parts):
    return md.Manifold.batch_boolean(parts,md.OpType.Add)


def vessel(c):
    n,steps=192,96;v=[];faces=[];h=c.get('height',120)
    profile=np.array(c['profile']);wall=c.get('wall',3);base=c.get('base',3)
    def ring(z,inner=False):
        t=z/h;radius=np.interp(t,profile[:,0],profile[:,1]);a=np.arange(n)*2*np.pi/n
        r=radius+c.get('amplitude',2)*np.cos(c.get('flutes',16)*(a-np.deg2rad(c.get('twist',60))*t))-wall*inner
        ids=np.arange(len(v),len(v)+n);v.extend(np.column_stack((r*np.cos(a),r*np.sin(a),np.full(n,z))))
        return ids
    def join(a,b,reverse=False):
        for i in range(n):
            j=(i+1)%n
            for f in ((a[i],a[j],b[j]),(a[i],b[j],b[i])):faces.append(f[::-1] if reverse else f)
    outer=[ring(h*j/steps) for j in range(steps+1)]
    inner=[ring(base+(h-base)*j/steps,True) for j in range(steps+1)]
    for j in range(steps):join(outer[j],outer[j+1]);join(inner[j],inner[j+1],True)
    join(outer[-1],inner[-1]);a=len(v);v.extend([(0,0,0),(0,0,base)])
    for i in range(n):
        j=(i+1)%n;faces.extend([(a,outer[0][j],outer[0][i]),(a+1,inner[0][i],inner[0][j])])
    return md.Manifold(md.Mesh(np.array(v,dtype=np.float32),np.array(faces,dtype=np.uint32)))


FONT = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',[
'01110/10001/10001/11111/10001/10001/10001','11110/10001/10001/11110/10001/10001/11110','01111/10000/10000/10000/10000/10000/01111','11110/10001/10001/10001/10001/10001/11110','11111/10000/10000/11110/10000/10000/11111','11111/10000/10000/11110/10000/10000/10000','01111/10000/10000/10111/10001/10001/01111','10001/10001/10001/11111/10001/10001/10001','11111/00100/00100/00100/00100/00100/11111','00111/00010/00010/00010/10010/10010/01100','10001/10010/10100/11000/10100/10010/10001','10000/10000/10000/10000/10000/10000/11111','10001/11011/10101/10101/10001/10001/10001','10001/11001/10101/10011/10001/10001/10001','01110/10001/10001/10001/10001/10001/01110','11110/10001/10001/11110/10000/10000/10000','01110/10001/10001/10001/10101/10010/01101','11110/10001/10001/11110/10100/10010/10001','01111/10000/10000/01110/00001/00001/11110','11111/00100/00100/00100/00100/00100/00100','10001/10001/10001/10001/10001/10001/01110','10001/10001/10001/10001/10001/01010/00100','10001/10001/10001/10101/10101/11011/10001','10001/10001/01010/00100/01010/10001/10001','10001/10001/01010/00100/00100/00100/00100','11111/00001/00010/00100/01000/10000/11111','01110/10001/10011/10101/11001/10001/01110','00100/01100/00100/00100/00100/00100/01110','01110/10001/00001/00010/00100/01000/11111','11110/00001/00001/01110/00001/00001/11110','00010/00110/01010/10010/11111/00010/00010','11111/10000/10000/11110/00001/00001/11110','01110/10000/10000/11110/10001/10001/01110','11111/00001/00010/00100/01000/01000/01000','01110/10001/10001/01110/10001/10001/01110','01110/10001/10001/01111/00001/00001/01110']))


def build(c):
    mode=c['mode']
    if mode=='vessel':solid=vessel(c)
    elif mode=='robot':
        head=c.get('head_scale',1);eyes=c.get('eye_spacing',13)
        parts=[cylinder(26,4),box((28,22,29),(0,0,28),5),cylinder(7,10,(0,0,41)),box((39*head,29*head,28*head),(0,0,62),6)]
        for x in (-9,9):parts.extend([box((13,20,9),(x,3,8),3),cylinder(4.5,11,(x,0,11))])
        for sign in (-1,1):parts.append(ball((6,7,15),(sign*17,0,28),32))
        parts.extend([cylinder(2.3,8,(0,0,74)),ball((4.5,4.5,4.5),(0,0,83),32)])
        solid=combine(parts)
        cuts=[ball((3.3,4,3.3),(x,14.5*head,64),32) for x in (-eyes/2,eyes/2)]
        cuts.append(box((12,4,2),(0,14.5*head,56),.6))
        cuts.extend([ball((2.8,3,2.8),(x,11,29),24) for x in (-5,5)])
        solid=solid-combine(cuts)
    elif mode=='mushroom':
        cap=c.get('cap_width',56)/2;eyes=c.get('eye_spacing',13)
        solid=combine([cylinder(25,4),ball((15,13,26),(0,0,25)),ball((cap,cap,17),(0,0,54))]).trim_by_plane((0,0,1),0)
        cuts=[ball((2.5,3.5,3),(x,12.5,27),32) for x in (-eyes/2,eyes/2)]
        cuts.append(ball((3,2,1.3),(0,13,20),24))
        for x,y in [(-10,5),(8,10),(0,-10),(17,-4),(-17,-7)]:
            z=54+17*math.sqrt(max(0,1-(x*x+y*y)/(cap*cap)))
            cuts.append(ball((4,4,2.7),(x,y,z),32))
        solid=solid-combine(cuts)
    elif mode=='nameplate':
        w,d=c.get('width',130),c.get('depth',48);relief=c.get('relief',2.6)
        parts=[box((w,d,7),(0,0,3.5),3)]
        text=c['text'];pixel=min((w-24)/(len(text)*6-1),(d-16)/7)
        for index,char in enumerate(text):
            if char==' ':continue
            for y,row in enumerate(FONT[char].split('/')):
                for x,value in enumerate(row):
                    if value=='1':parts.append(box((pixel*1.015,pixel*1.015,relief+1),((index*6+x-(len(text)*6-2)/2)*pixel,(y-3)*pixel,7+(relief-1)/2)))
        solid=combine(parts)
    else:
        w,d=c.get('width',132),c.get('depth',86);height=c.get('cup_height',52)
        parts=[box((w,d,7),(0,0,3.5),3)]
        # Rear wells and a shallow front tray all share the same base.
        for x,h in [(-w*.27,height),(w*.25,height*.72)]:
            outer=cylinder(20,h,(x,-d*.22,5))
            inner=cylinder(16.5,h+2,(x,-d*.22,9))
            parts.append(outer-inner)
        tray=box((w-14,d*.42,15),(0,d*.24,10),4)-box((w-21,d*.42-7,19),(0,d*.24,15),3)
        parts.append(tray);solid=combine(parts)
    if str(solid.status())!='Error.NoError' or solid.is_empty():raise ValueError('Geometry kernel rejected model')
    raw=solid.to_mesh64() if mode=='organizer' else solid.to_mesh();mesh=trimesh.Trimesh(raw.vert_properties[:,:3],raw.tri_verts,process=True)
    if mesh.area_faces.min()<1e-12:
        repaired=md.Manifold(md.Mesh64(np.array(mesh.vertices),np.array(mesh.faces,dtype=np.uint64))).simplify(1e-6).to_mesh64()
        mesh=trimesh.Trimesh(repaired.vert_properties[:,:3],repaired.tri_verts,process=True)
    if mode in ('robot','mushroom'):mesh.apply_scale(c.get('height',85)/mesh.extents[2])
    mesh.apply_translation([-mesh.bounds[:,0].mean(),-mesh.bounds[:,1].mean(),-mesh.bounds[0,2]])
    return mesh


def verify(mesh):
    if not np.isfinite(mesh.vertices).all() or not mesh.is_watertight or not mesh.is_winding_consistent or mesh.volume<=0:raise ValueError('Mesh validation failed')
    adjacency=[set() for _ in mesh.vertices]
    for a,b in mesh.edges:
        adjacency[a].add(int(b));adjacency[b].add(int(a))
    seen=set();pending=[0]
    while pending:
        i=pending.pop()
        if i not in seen:seen.add(i);pending.extend(adjacency[i]-seen)
    if len(seen)!=len(mesh.vertices):raise ValueError('Expected one connected body')
    if mesh.area_faces.min()<1e-12:raise ValueError('Degenerate face')
    return {'status':'Mesh checked','units':'millimeter','vertices':len(mesh.vertices),'triangles':len(mesh.faces),'watertight':True,'consistent_winding':True,'connected_bodies':1,'size_mm':mesh.extents.round(3).tolist(),'volume_mm3':round(float(mesh.volume),3),'slicer_tested':False,'physically_printed':False,'limits':['No minimum wall-thickness or overhang certification','No printer profile or G-code','Preview color is illustrative; exports are single-material geometry']}


def write_3mf(mesh,path):
    verts=''.join(f'<vertex x="{x:.9f}" y="{y:.9f}" z="{z:.9f}"/>' for x,y,z in mesh.vertices)
    faces=''.join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a,b,c in mesh.faces)
    model=f'<?xml version="1.0" encoding="UTF-8"?><model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02"><resources><object id="1" type="model"><mesh><vertices>{verts}</vertices><triangles>{faces}</triangles></mesh></object></resources><build><item objectid="1"/></build></model>'
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" Target="/3D/3dmodel.model"/></Relationships>')
        z.writestr('3D/3dmodel.model',model)


def frame(mesh,c,angle=.45,size=960):
    """Exact triangle rasterization with a z buffer and smooth vertex lighting."""
    tilt=.58 if c['mode'] not in ('nameplate','organizer') else .94
    rotation=np.array([[math.cos(angle),-math.sin(angle),0],[math.sin(angle)*math.sin(tilt),math.cos(angle)*math.sin(tilt),-math.cos(tilt)],[math.sin(angle)*math.cos(tilt),math.cos(angle)*math.cos(tilt),math.sin(tilt)]])
    v=mesh.vertices-mesh.bounds.mean(axis=0);p=v@rotation.T
    # Fit every turn of the complete object consistently.
    span=max(float(np.linalg.norm(mesh.extents[:2])),float(mesh.extents[2]))
    scale=size*.69/span
    p[:,:2]=p[:,:2]*scale+np.array([size*.5,size*.47])
    normals=mesh.vertex_normals@rotation.T
    base=np.array([int(c['color'][i:i+2],16) for i in (1,3,5)])
    light=np.array([-.35,-.5,.79]);light/=np.linalg.norm(light)
    bright=.42+.58*np.maximum(0,normals@light)
    spec=np.maximum(0,normals@np.array([-.2,-.3,.9327]))**30*.17
    colors=np.clip(base[None,:]*bright[:,None]+255*spec[:,None],0,255)
    image=Image.new('RGB',(size,size),'#e8e9e3')
    shadow=Image.new('RGBA',(size,size));draw=ImageDraw.Draw(shadow)
    # A floor shadow is an illustration; it is not extra exported geometry.
    floor=p[mesh.vertices[:,2]<.001,1];y=max(floor) if len(floor) else size*.8
    draw.ellipse((size*.25,y-size*.025,size*.75,y+size*.045),fill=(47,59,49,55));shadow=shadow.filter(ImageFilter.GaussianBlur(size*.018));image.paste(shadow,(0,0),shadow)
    pixels=np.array(image);depth=np.full((size,size),-np.inf,dtype=np.float32)
    for face in mesh.faces:
        t=p[face];x0=max(0,int(np.floor(t[:,0].min())));x1=min(size-1,int(np.ceil(t[:,0].max())));y0=max(0,int(np.floor(t[:,1].min())));y1=min(size-1,int(np.ceil(t[:,1].max())))
        if x1<x0 or y1<y0:continue
        den=(t[1,1]-t[2,1])*(t[0,0]-t[2,0])+(t[2,0]-t[1,0])*(t[0,1]-t[2,1])
        if abs(den)<1e-10:continue
        yy,xx=np.mgrid[y0:y1+1,x0:x1+1];xx=xx+.5;yy=yy+.5
        a=((t[1,1]-t[2,1])*(xx-t[2,0])+(t[2,0]-t[1,0])*(yy-t[2,1]))/den
        b=((t[2,1]-t[0,1])*(xx-t[2,0])+(t[0,0]-t[2,0])*(yy-t[2,1]))/den;d=1-a-b
        zz=a*t[0,2]+b*t[1,2]+d*t[2,2];buffer=depth[y0:y1+1,x0:x1+1]
        mask=(a>=-1e-7)&(b>=-1e-7)&(d>=-1e-7)&(zz>buffer)
        if not mask.any():continue
        shade=a[:,:,None]*colors[face[0]]+b[:,:,None]*colors[face[1]]+d[:,:,None]*colors[face[2]]
        pixels[y0:y1+1,x0:x1+1][mask]=np.clip(shade[mask],0,255).astype(np.uint8);buffer[mask]=zz[mask]
    return Image.fromarray(pixels)


def preview(mesh,c,report):
    template=(Path(__file__).parent.parent/'assets/preview.html').read_text()
    data=json.dumps({'config':c,'report':report,'vertices':mesh.vertices.round(6).tolist(),'faces':mesh.faces.tolist(),'normals':mesh.vertex_normals.round(6).tolist()},separators=(',',':')).replace('<','\\u003c')
    return template.replace('__TITLE__',html.escape(c['name'])).replace('__DATA__',data)


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--config',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);parser.add_argument('--video',action='store_true')
    args=parser.parse_args()
    try:
        c=validate(json.loads(args.config.read_text()))
        allowed_path=Path(__file__).with_name('allowed-modes.json')
        if allowed_path.exists() and c['mode'] not in json.loads(allowed_path.read_text()):raise ValueError('Mode is not supported by this skill package')
        if args.out.exists():raise ValueError('Output exists; choose a new directory')
        mesh=build(c);report=verify(mesh)
        visual=trimesh.graph.smooth_shade(mesh,angle=np.radians(25),facet_minarea=40)
        page=preview(visual,c,report)
        args.out.mkdir(parents=True)
        mesh.export(args.out/'model.stl');write_3mf(mesh,args.out/'model.3mf')
        (args.out/'parameters.json').write_text(json.dumps(c,indent=2)+'\n');(args.out/'checks.json').write_text(json.dumps(report,indent=2)+'\n');(args.out/'preview.html').write_text(page)
        frame(visual,c).save(args.out/'poster.png')
        if args.video:
            command=['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size','720x720','-framerate','12','-i','-','-an','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-movflags','+faststart',str(args.out/'turntable.mp4')]
            process=subprocess.Popen(command,stdin=subprocess.PIPE)
            try:
                for i in range(72):
                    process.stdin.write(frame(visual,c,angle=.45+2*math.pi*i/72,size=720).tobytes())
                    if i%12==0:print(f'{c["name"]}: turntable frame {i}/72',flush=True)
            finally:process.stdin.close()
            if process.wait()!=0:raise ValueError('Video encoding failed')
        report['files']={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in args.out.iterdir() if p.is_file()}
        (args.out/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
    except (ValueError,OSError) as error:parser.error(str(error))


if __name__=='__main__':main()
