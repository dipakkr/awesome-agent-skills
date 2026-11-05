import React,{useMemo,useLayoutEffect} from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig} from 'remotion';
import {ThreeCanvas} from '@remotion/three';
import {useThree} from '@react-three/fiber';
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

const palettes={mint:{wall:'#9bb9ae',trim:'#426b60',accent:'#e99f55',hoodie:'#317f82',paper:'#fff9ed'},peach:{wall:'#c7a08e',trim:'#744c43',accent:'#8ab8a4',hoodie:'#675b9b',paper:'#fff8ea'},violet:{wall:'#a5a4c3',trim:'#5f5d83',accent:'#e5aa63',hoodie:'#b25e5b',paper:'#fbf7ef'},night:{wall:'#344e61',trim:'#152f40',accent:'#e5b95e',hoodie:'#5b9589',paper:'#fff8e8'}};
const clamp=(n,a=0,b=1)=>Math.min(b,Math.max(a,n));
const ease=n=>1-Math.pow(1-clamp(n),3);
function Box({size=[1,1,1],color='#fff',radius=.06,...props}){
  const geometry=useMemo(()=>new RoundedBoxGeometry(...size,2,Math.min(radius,...size.map(v=>v*.2))),[...size,radius]);
  return <mesh geometry={geometry} castShadow receiveShadow {...props}><meshStandardMaterial color={color} roughness={.75}/></mesh>;
}
function Ball({size=[1,1,1],color='#fff',...props}){return <mesh scale={size} castShadow receiveShadow {...props}><sphereGeometry args={[1,24,16]}/><meshStandardMaterial color={color} roughness={.78}/></mesh>;}
function Rod({from,to,radius=.035,color='#fff'}){
  const a=new THREE.Vector3(...from),b=new THREE.Vector3(...to),delta=b.clone().sub(a),q=new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(0,1,0),delta.clone().normalize());
  return <mesh position={a.add(b).multiplyScalar(.5)} quaternion={q} castShadow><cylinderGeometry args={[radius,radius,delta.length(),12]}/><meshStandardMaterial color={color} roughness={.7}/></mesh>;
}
function Eye({x,y,z,blink=1,looking=0}){return <group position={[x,y,z]}><Ball size={[.118,.14*blink,.08]} color="#fff7e8"/><Ball position={[looking,.005,.073]} size={[.052,.071*blink,.025]} color="#243337"/><Ball position={[looking+.017,.031,.093]} size={[.016,.019*blink,.012]} color="#ffffff"/></group>;}
function Student({t,talking,p,energy,shot}){
  const blink=Math.sin(t*2.3)>.985?.16:1;
  const nod=talking?Math.sin(t*4.5)*.035:Math.sin(t*1.5)*.016;
  const hand=talking?.07+Math.sin(t*5)*.08:0;
  return <group position={[1.03,1.12,.35]} rotation={[0,-.16,0]}>
    <Box position={[0,.32,-.1]} size={[.84,.86,.67]} color={p.hoodie} radius={.2}/>
    <Ball position={[0,.74,.02]} size={[.43,.22,.38]} color={p.hoodie}/>
    <Rod from={[-.2,.65,.3]} to={[-.18,.2,.33]} radius={.018} color="#e9e0d1"/><Rod from={[.2,.65,.3]} to={[.18,.2,.33]} radius={.018} color="#e9e0d1"/>
    <group position={[0,1.09,.02]} rotation={[nod,Math.sin(t*.9)*.035,Math.sin(t*1.4)*.018]}>
      <Ball position={[0,.12,0]} size={[.48,.55,.43]} color="#c78a63"/>
      <Ball position={[-.46,.1,0]} size={[.10,.16,.12]} color="#bd7b55"/><Ball position={[.46,.1,0]} size={[.1,.16,.12]} color="#bd7b55"/>
      <Ball position={[0,.36,-.16]} size={[.5,.4,.4]} color="#3e2d27"/>
      {[-.34,-.14,.08,.3].map((x,i)=><Ball key={i} position={[x,.56+Math.sin(i)*.04,.15]} size={[.19,.2,.2]} color={i%2?'#493128':'#382921'}/>)}
      <Eye x={-.18} y={.16} z={.37} blink={blink} looking={-.015}/><Eye x={.18} y={.16} z={.37} blink={blink} looking={-.015}/>
      {[-.18,.18].map(x=><mesh key={x} position={[x,.16,.456]}><torusGeometry args={[.16,.018,8,32]}/><meshStandardMaterial color="#383d38"/></mesh>)}
      <Rod from={[-.025,.18,.456]} to={[.025,.18,.456]} radius={.014} color="#383d38"/>
      <Ball position={[0,.01,.445]} size={[.075,.09,.08]} color="#d2946e"/>
      <Ball position={[0,-.16,.395]} size={[.09,talking?.014+energy*.08:.019,.018]} color="#4a2928"/>
      <Rod from={[-.29,.36,.38]} to={[-.09,.37+nod,.43]} radius={.023} color="#493128"/>
      <Rod from={[.09,.37,.43]} to={[.29,.36+nod,.38]} radius={.023} color="#493128"/>
    </group>
    <Rod from={[-.38,.54,0]} to={[-.57,.11,.27]} radius={.15} color={p.hoodie}/><Rod from={[-.57,.11,.27]} to={[-.37,.04,.74]} radius={.13} color={p.hoodie}/>
    <Ball position={[-.33,.06,.79]} size={[.15,.08,.17]} color="#c78a63"/>
    <Rod from={[.39,.55,.03]} to={[.57,.18+hand,.3]} radius={.15} color={p.hoodie}/><Rod from={[.57,.18+hand,.3]} to={[.42,.07+hand*2,.74]} radius={.12} color={p.hoodie}/>
    <Ball position={[.4,.09+hand*2,.78]} size={[.14,.09,.16]} color="#c78a63"/>
  </group>;
}
function Tutor({t,talking,p,energy}){
  const wave=talking?Math.sin(t*3.3)*.12:Math.sin(t*1.1)*.035;
  const blink=Math.sin(t*1.8+.4)>.99?.15:1;
  return <group position={[-1.13,1.56,.4]} rotation={[0,.12,Math.sin(t*2)*.018]}>
    <Box size={[.78,.69,.57]} position={[0,.5,0]} color={p.accent} radius={.18}/>
    <Box size={[.61,.4,.1]} position={[0,.52,.29]} color="#28474a" radius={.1}/>
    <Ball position={[-.14,.57,.36]} size={[.065,.085*blink,.018]} color="#f7efd8"/><Ball position={[.14,.57,.36]} size={[.065,.085*blink,.018]} color="#f7efd8"/>
    <Ball position={[0,.4,.361]} size={[.08,talking?.015+energy*.065:.018,.014]} color="#f7efd8"/>
    <Rod from={[0,.84,0]} to={[.04,1.02,0]} radius={.025} color="#476566"/><Ball position={[.04,1.04,0]} size={[.065,.065,.065]} color={p.accent}/>
    <Box size={[.55,.33,.4]} position={[0,.02,0]} color={p.accent} radius={.1}/>
    <Box size={[.23,.13,.29]} position={[-.2,-.18,.07]} color="#38585a"/><Box size={[.23,.13,.29]} position={[.2,-.18,.07]} color="#38585a"/>
    <Rod from={[-.28,.12,0]} to={[-.5,.05+wave,.1]} radius={.07} color={p.accent}/><Ball position={[-.5,.05+wave,.1]} size={[.09,.09,.09]} color="#38585a"/>
    <Rod from={[.29,.13,0]} to={[.56,.32+wave,0]} radius={.07} color={p.accent}/><Ball position={[.56,.32+wave,0]} size={[.09,.09,.09]} color="#38585a"/>
    <Rod from={[.57,.35+wave,0]} to={[.95,1.1+wave,-.4]} radius={.018} color="#425b5a"/>
  </group>;
}

function drawIcon(ctx,icon,x,y,color){
  ctx.save();ctx.translate(x,y);ctx.strokeStyle=color;ctx.fillStyle=color;ctx.lineWidth=9;ctx.lineJoin='round';ctx.lineCap='round';
  const rect=(x,y,w,h)=>{ctx.beginPath();ctx.roundRect(x,y,w,h,7);ctx.stroke();};
  const line=(...a)=>{ctx.beginPath();ctx.moveTo(a[0],a[1]);for(let i=2;i<a.length;i+=2)ctx.lineTo(a[i],a[i+1]);ctx.stroke();};
  if(icon==='book'){rect(-47,-40,94,80);line(0,-37,0,40);line(-30,-20,-14,-20);line(13,-20,30,-20);}
  if(icon==='shelf'){line(-55,-45,-55,45,55,45,55,-45);line(-55,7,55,7);[-35,-10,15,38].forEach((v,i)=>rect(v,-35,13,40-i*3));}
  if(icon==='bell'){ctx.beginPath();ctx.moveTo(-40,26);ctx.quadraticCurveTo(-27,15,-28,-10);ctx.bezierCurveTo(-28,-50,28,-50,28,-10);ctx.quadraticCurveTo(27,15,40,26);ctx.closePath();ctx.stroke();line(-14,40,14,40);}
  if(icon==='shop'){rect(-46,-18,92,66);line(-55,-20,-35,-48,35,-48,55,-20,-55,-20);rect(-9,10,24,37);}
  if(icon==='phone'){rect(-29,-48,58,96);line(-11,30,11,30);}
  if(icon==='gate'){line(-50,48,-50,-45,50,-45,50,48);[-25,0,25].forEach(x=>line(x,-40,x,48));line(-50,-4,50,-4);}
  if(icon==='ticket'){rect(-55,-28,110,56);line(27,-22,27,22);line(-35,-5,8,-5);line(-35,10,-3,10);}
  if(icon==='worker'){ctx.beginPath();ctx.arc(0,-26,20,0,Math.PI*2);ctx.stroke();ctx.beginPath();ctx.arc(0,43,39,Math.PI,Math.PI*2);ctx.stroke();line(-19,12,0,35,20,12);}
  if(icon==='tray'){line(-54,-7,-39,37,39,37,54,-7,-54,-7);line(-24,-42,0,-19,24,-42);line(0,-49,0,-19);}
  if(icon==='clock'){ctx.beginPath();ctx.arc(0,0,44,0,Math.PI*2);ctx.stroke();line(0,-28,0,0,23,14);}
  if(icon==='database'){ctx.beginPath();ctx.ellipse(0,-30,47,16,0,0,Math.PI*2);ctx.stroke();line(-47,-30,-47,31);line(47,-30,47,31);[0,30].forEach(y=>{ctx.beginPath();ctx.ellipse(0,y,47,16,0,0,Math.PI);ctx.stroke();});}
  if(icon==='lightning'){ctx.beginPath();ctx.moveTo(10,-50);ctx.lineTo(-35,7);ctx.lineTo(-3,7);ctx.lineTo(-14,50);ctx.lineTo(36,-12);ctx.lineTo(6,-12);ctx.closePath();ctx.fill();}
  ctx.restore();
}
function Board({board,p,progress,t}){
  const texture=useMemo(()=>{
    const canvas=document.createElement('canvas');canvas.width=1500;canvas.height=900;const ctx=canvas.getContext('2d');
    ctx.fillStyle=p.paper;ctx.fillRect(0,0,1500,900);
    ctx.fillStyle='#385952';ctx.font='bold 68px Arial';ctx.textAlign='center';ctx.fillText(board.heading,750,135);
    ctx.strokeStyle='#d4dacb';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(100,181);ctx.lineTo(1400,181);ctx.stroke();
    const n=board.nodes.length;const step=1220/n;const first=750-step*(n-1)/2;
    board.nodes.forEach((node,i)=>{
      const reveal=ease((progress-i*.15)/.4);ctx.globalAlpha=reveal;
      const x=first+i*step,y=475+(1-reveal)*32;
      ctx.fillStyle=i===1?'#e8eadb':'#f1eadd';ctx.beginPath();ctx.roundRect(x-150,y-135,300,287,30);ctx.fill();
      drawIcon(ctx,node.icon,x,y-26,i===1?'#3b827d':'#bc774a');
      ctx.fillStyle='#354a46';ctx.font='bold 38px Arial';ctx.fillText(node.label,x,y+104);
      if(i<n-1){ctx.strokeStyle='#75a09a';ctx.lineWidth=8;ctx.beginPath();ctx.moveTo(x+167,y-15);ctx.lineTo(x+step-175,y-15);ctx.lineTo(x+step-195,y-35);ctx.moveTo(x+step-175,y-15);ctx.lineTo(x+step-195,y+5);ctx.stroke();}
    });
    ctx.globalAlpha=1;
    if(board.kind==='cycle'){
      ctx.strokeStyle='#75a09a';ctx.lineWidth=6;ctx.beginPath();ctx.moveTo(1175,590);ctx.bezierCurveTo(1175,665,325,665,325,590);ctx.stroke();ctx.beginPath();ctx.moveTo(308,611);ctx.lineTo(325,590);ctx.lineTo(343,611);ctx.stroke();
    }
    if(board.kind==='queue'){
      for(let i=0;i<5;i++){const x=570+i*80;ctx.fillStyle=i<Math.floor(t%5)?'#86aba0':'#d6a879';ctx.beginPath();ctx.roundRect(x,619,56,20,6);ctx.fill();}
    }
    ctx.fillStyle='#5c6960';ctx.font='34px Arial';ctx.fillText(board.note,750,254);
    ctx.fillStyle='#d08e5f';ctx.beginPath();ctx.roundRect(655,810,190,9,5);ctx.fill();
    const tex=new THREE.CanvasTexture(canvas);tex.colorSpace=THREE.SRGBColorSpace;return tex;
  },[board,p,Math.round(progress*20),Math.floor(t)]);
  useLayoutEffect(()=>()=>texture.dispose(),[texture]);
  return <group position={[0,3.55,-1.55]}>
    <Box size={[4.18,2.59,.16]} color="#e4d3b4"/>
    <mesh position={[0,0,.091]}><planeGeometry args={[3.99,2.394]}/><meshBasicMaterial map={texture} toneMapped={false}/></mesh>
    <Box position={[0,-1.3,.1]} size={[3.92,.1,.24]} color="#c6b293"/>
    <Rod from={[-.8,-1.23,.21]} to={[-.35,-1.23,.21]} radius={.035} color="#cf8b61"/>
    <Rod from={[-.24,-1.23,.21]} to={[.2,-1.23,.21]} radius={.035} color="#548c83"/>
  </group>;
}
function Plant({position,scale=1}){return <group position={position} scale={scale}>
  <mesh position={[0,.13,0]} castShadow><cylinderGeometry args={[.2,.14,.3,18]}/><meshStandardMaterial color="#c48463"/></mesh>
  {[0,1,2,3,4].map((v)=><group key={v} rotation={[0,v*1.4,0]}><Rod from={[0,.2,0]} to={[.14,.5+v*.05,0]} radius={.012} color="#416f59"/><Ball position={[.16,.47+v*.05,0]} rotation={[0,0,-.5]} size={[.09,.22,.035]} color={v%2?'#709776':'#426e54'}/></group>)}
</group>;}
function Room({p,t,turn,energy,board,progress}){return <>
  <color attach="background" args={[p.wall]}/><ambientLight intensity={1.4}/><hemisphereLight color="#fff9e5" groundColor="#596565" intensity={1.5}/>
  <directionalLight position={[-3,7,6]} intensity={3} color="#fff0d6" castShadow shadow-mapSize={[1024,1024]} shadow-camera-left={-5} shadow-camera-right={5} shadow-camera-top={6} shadow-camera-bottom={-2} shadow-bias={-.001}/>
  <directionalLight position={[4,4,3]} intensity={1} color="#b9e0ec"/>
  <Box position={[0,3,-2]} size={[9,7,.15]} radius={.01} color={p.wall}/>
  <Box position={[0,-.18,0]} size={[10,.25,10]} radius={.01} color="#c6baa3"/>
  <Box position={[-3.05,3,-1.86]} size={[1.4,3.7,.1]} color={p.trim}/>
  <Box position={[-3.05,3,-1.79]} size={[1.17,3.46,.04]} color="#d2e2ce"/>
  <Box position={[-3.05,3,-1.74]} size={[.06,3.45,.06]} color={p.trim}/><Box position={[-3.05,2.9,-1.74]} size={[1.2,.06,.06]} color={p.trim}/>
  <Box position={[2.91,2.8,-1.4]} size={[1.02,.10,.75]} color="#92785e"/><Plant position={[2.8,2.85,-1.4]} scale={.9}/>
  <Box position={[2.91,1.75,-1.4]} size={[1.02,.10,.75]} color="#92785e"/>
  {[0,1,2,3].map(i=><Box key={i} position={[2.55+i*.2,2,-1.44]} size={[.15,.42+(i%2)*.12,.3]} color={['#d9b480','#7d9b94','#c27f68','#d4cba6'][i]}/>)}
  <Board board={board} p={p} progress={progress} t={t}/>
  <Box position={[.05,.98,.8]} size={[5.8,.21,2.1]} color="#bc9168" radius={.08}/>
  <Box position={[-2,.4,.7]} size={[.16,1.05,1.6]} color="#715641"/><Box position={[2,.4,.7]} size={[.16,1.05,1.6]} color="#715641"/>
  {[0,1,2].map(i=><group key={i} position={[-1.18,1.14+i*.13,.4]} rotation={[0,(i-1)*.12,0]}><Box size={[1.02,.11,.75]} color={['#597f70','#d7b978','#a4849c'][i]}/><Box size={[.92,.067,.68]} position={[0,0,.032]} color="#e4dac3"/></group>)}
  <Student t={t} talking={turn.speaker==='student'} energy={energy} p={p}/><Tutor t={t} talking={turn.speaker==='tutor'} energy={energy} p={p}/>
  <Box size={[.75,.025,.61]} position={[.78,1.11,1.25]} rotation={[0,-.15,0]} color="#f8ebd3"/>
  <Rod from={[.4,1.145,1.43]} to={[.92,1.145,1.18]} radius={.018} color="#426d6b"/>
  <mesh position={[1.85,1.28,1.1]} castShadow><cylinderGeometry args={[.15,.13,.33,24]}/><meshStandardMaterial color="#edcd8d"/></mesh>
  <mesh position={[2.02,1.3,1.1]} rotation={[0,Math.PI/2,0]}><torusGeometry args={[.1,.035,12,24]}/><meshStandardMaterial color="#edcd8d"/></mesh>
  <Plant position={[-2.1,1.08,.8]} scale={.7}/>
</>;}

const shots={wide:{pos:[.15,3.25,8.4],target:[0,2.85,0]},student:{pos:[2.5,2.65,5.3],target:[.8,2.12,.2]},tutor:{pos:[-2.25,2.9,5.1],target:[-.82,2.05,.2]},board:{pos:[0,4,7.2],target:[0,3.65,-1.1]}};
function Camera({shot,t,local}){
  const {camera}=useThree();
  useLayoutEffect(()=>{const s=shots[shot]||shots.wide;camera.position.set(s.pos[0]+Math.sin(t*.22)*.035,s.pos[1],s.pos[2]-.08*ease(local/4));camera.lookAt(...s.target);camera.updateProjectionMatrix();},[shot,t,local,camera]);
  return null;
}
export function Film(props){
  const frame=useCurrentFrame(),{fps,width,height}=useVideoConfig(),t=frame/fps,p=palettes[props.theme];
  const index=props.turns.findLastIndex(v=>t>=v.start),turn=props.turns[Math.max(0,index)]||{speaker:'tutor',text:'',board:0,shot:'wide',start:0,duration:1,energy:[]};
  const local=t-turn.start,energy=turn.energy[Math.max(0,Math.floor(local*30))]||0;
  const board=props.boards[turn.board]||{heading:'One idea at a time',nodes:[{label:'Learn',icon:'book'}],note:'Make it simple.'};
  let boardStart=turn.start;for(let i=Math.max(0,index)-1;i>=0&&props.turns[i].board===turn.board;i--)boardStart=props.turns[i].start;
  const end=t>props.duration-2.6;
  const caption=local>=0&&local<turn.duration+.12&&!end;
  return <AbsoluteFill style={{background:p.wall,fontFamily:'Arial, sans-serif'}}>
    <ThreeCanvas width={width} height={height} shadows dpr={1} camera={{fov:47,near:.1,far:50}} gl={{antialias:true,alpha:false}}>
      <Camera shot={end?'wide':turn.shot} t={t} local={local}/>
      <Room p={p} t={t} turn={{...turn,speaker:local<turn.duration?turn.speaker:''}} energy={energy} board={board} progress={clamp((t-boardStart)/.7)} />
    </ThreeCanvas>
    <div style={{position:'absolute',top:0,left:0,right:0,height:195,background:`linear-gradient(${p.wall} 85%, ${p.wall}00)`}}/>
    <div style={{position:'absolute',top:70,left:52,right:80,textAlign:'center',color:props.theme==='night'?'#fff3de':'#263e39'}}>
      <div style={{fontSize:16,fontWeight:700,letterSpacing:3.2,marginBottom:12}}>SMALL QUESTIONS / BIG IDEAS</div>
      <div style={{fontSize:43,fontWeight:800,letterSpacing:-1.6}}>{props.title}</div>
    </div>
    {caption&&<div style={{position:'absolute',bottom:194,left:48,right:76,padding:'20px 24px',borderRadius:20,background:'#1c3031f2',boxShadow:'0 7px 20px #152b3020',transform:`translateY(${(1-ease(local/.17))*12}px)`,opacity:ease(local/.12)}}>
      <div style={{fontSize:14,fontWeight:700,letterSpacing:2,color:turn.speaker==='student'?'#aad7d1':'#f3c58e',marginBottom:7}}>{turn.speaker==='student'?'MILO':'PIP'}</div>
      <div style={{fontSize:31,lineHeight:1.2,color:'#fff9eb',fontWeight:600}}>{turn.text}</div>
    </div>}
    {end&&<div style={{position:'absolute',bottom:200,left:48,right:76,background:'#f9f0dfff',padding:'24px',borderRadius:20,color:'#2c4b46',fontSize:31,lineHeight:1.2,fontWeight:700,boxShadow:'0 8px 25px #18383122'}}>{props.takeaway}</div>}
    <div style={{position:'absolute',bottom:145,left:48,right:76,textAlign:'center',color:props.theme==='night'?'#f3e7ce':'#354940',fontSize:14,fontWeight:600,letterSpacing:.6}}>{props.disclosure||'Original characters · AI-generated voices'}</div>
  </AbsoluteFill>;
}
