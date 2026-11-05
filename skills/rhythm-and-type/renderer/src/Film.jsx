import React,{useState,useEffect} from 'react';
import {AbsoluteFill,Img,useCurrentFrame,useVideoConfig,staticFile,delayRender,continueRender,cancelRender} from 'remotion';
import {sceneAt,duration} from './model.mjs';

// Original frame-driven art direction. No CSS animation, remote assets or borrowed engine.
const clamp=(x)=>Math.max(0,Math.min(1,x));
const ease=(x)=>1-Math.pow(1-clamp(x),4);
const inout=x=>{x=clamp(x);return x*x*(3-2*x);};
const enter=(t,delay=0,speed=.8)=>ease((t-delay)/speed);
const abs={position:'absolute'};
const center={display:'flex',alignItems:'center',justifyContent:'center'};
const mono={fontFamily:'monospace',fontSize:16,letterSpacing:2};

function Type({text,size=116,color,style={},t=2,delay=0,align='center'}){
 const lines=text.split('\n');
 return <div style={{fontWeight:700,fontSize:size,lineHeight:.98,letterSpacing:-size*.055,textAlign:align,color,...style}}>{lines.map((s,i)=><div key={i} style={{overflow:'hidden',paddingBottom:size*.1,marginBottom:-size*.04}}><div style={{transform:`translateY(${(1-enter(t,delay+i*.12))*115}%)`}}>{s}</div></div>)}</div>;
}
function Mark({size=54,color}){return <svg width={size} height={size} viewBox="0 0 100 100"><path d="M12 76 41 12h20L88 76H64L51 42 37 76Z" fill={color}/><circle cx="51" cy="79" r="9" fill={color}/></svg>;}

function Art({motif='rings',accent,t=0,variant=0,ink='#fff'}){
 const phase=t*.3+variant*.7;
 return <svg viewBox="0 0 800 800" width="100%" height="100%" style={{overflow:'visible'}}>
 <defs><linearGradient id={`chrome-${variant}`} x1="0" y1="0" x2="1" y2="1"><stop stopColor={ink}/><stop offset=".22" stopColor="#777"/><stop offset=".45" stopColor={ink}/><stop offset=".52" stopColor="#222"/><stop offset=".75" stopColor={accent}/><stop offset="1" stopColor={ink}/></linearGradient></defs>
 {motif==='rings'&&<g transform={`translate(400 400) rotate(${t*12})`}>{Array.from({length:7},(_,i)=><ellipse key={i} rx={300-i*22} ry={105+i*14} fill="none" stroke={`url(#chrome-${variant})`} strokeWidth={18-i*.8} transform={`rotate(${i*25+Math.sin(phase)*16})`}/>)}<circle r="30" fill={accent}/></g>}
 {motif==='ribbons'&&<g transform={`translate(400 400) rotate(${-25+Math.sin(phase)*12})`}>{Array.from({length:11},(_,i)=><rect key={i} x={-280+i*40} y={-280+Math.sin(i*.55+phase)*120} width="34" height="480" rx="17" fill={i%3===0?accent:`url(#chrome-${variant})`}/> )}</g>}
 {motif==='grid'&&<g transform={`translate(400 400) rotate(${-14+Math.sin(phase)*8})`}>{Array.from({length:25},(_,i)=>{let x=(i%5-2)*114,y=(Math.floor(i/5)-2)*114,s=.55+.35*(1+Math.sin(i*.9+phase))/2;return <g key={i} transform={`translate(${x} ${y}) scale(${s}) rotate(${t*15+i*7})`}><rect x="-58" y="-58" width="116" height="116" rx={i%2?58:20} fill={i%4===0?accent:`url(#chrome-${variant})`}/></g>;})}</g>}
 </svg>;
}

function Interface({b,t=0,stage=0,w=1120,h=560,dark=false}){
 const bg=dark?'#111':'#fff',fg=dark?'#fff':'#101010',muted=dark?'#a7a7a7':'#666',line=dark?'#303030':'#e7e7e7';
 const select=enter(t,.9,1),done=enter(t,2.5,.7);
 return <div style={{width:w,height:h,background:bg,color:fg,borderRadius:24,border:`1px solid ${line}`,boxShadow:'0 35px 90px #0003',overflow:'hidden',position:'relative',textAlign:'left'}}>
 <div style={{height:62,borderBottom:`1px solid ${line}`,display:'flex',alignItems:'center',padding:'0 26px',gap:9}}>{['#ff7767','#ffc94b','#c7ff6b'].map(c=><span key={c} style={{background:c,width:9,height:9,borderRadius:10}}/>)}<span style={{fontSize:18,fontWeight:700,marginLeft:22}}>{b.brand}</span><span style={{marginLeft:'auto',fontSize:14,color:muted}}>{b.concept?'CONCEPT WORKSPACE':'WORKSPACE'}</span></div>
 <div style={{padding:32,display:'flex',gap:28,height:h-62,boxSizing:'border-box'}}>
 {w>850&&<div style={{width:145,flexShrink:0,borderRight:`1px solid ${line}`,paddingRight:24}}>{['Workspace','Overview','Projects','Activity'].map((s,i)=><div key={s} style={{padding:'15px 12px',marginBottom:7,borderRadius:8,fontSize:17,background:i===1?b.accent:'transparent',color:i===1?'#111':muted}}>{s}</div>)}</div>}
 <div style={{flex:1,minWidth:0}}><div style={{...mono,fontSize:12,color:muted}}>YOUR NEXT BIG THING</div><div style={{fontSize:32,fontWeight:650,margin:'12px 0 24px'}}>{stage===0?'Start with an idea.':stage===1?'Everything, connected.':'Ready when you are.'}</div>
 {stage===0?<><div style={{border:`2px solid ${line}`,padding:22,borderRadius:15,height:72,fontSize:22,display:'flex',alignItems:'center'}}>{b.task.slice(0,Math.floor(clamp((t-.3)/1.5)*b.task.length))}<span style={{color:fg,opacity:Math.floor(t*3)%2?0:1}}>|</span></div><div style={{marginTop:24,display:'flex',gap:12}}>{b.words.map((s,i)=><div key={s} style={{padding:'12px 16px',border:`1px solid ${line}`,borderRadius:30,opacity:enter(t,.4+i*.15),fontSize:16}}>{s}</div>)}</div><div style={{marginTop:25,background:b.accent,color:'#111',borderRadius:10,padding:16,width:190,textAlign:'center',fontWeight:700,fontSize:18,transform:`scale(${1-.05*Math.sin(select*Math.PI)})`}}>Create workspace ↗</div></>:<><div style={{display:'flex',gap:14}}>{b.steps.map((s,i)=><div key={i} style={{flex:1,border:`1px solid ${line}`,borderRadius:14,padding:18,minHeight:180,opacity:enter(t,i*.18),transform:`translateY(${(1-enter(t,i*.18))*45}px)`}}><span style={{...mono,fontSize:14,color:muted}}>0{i+1}</span><div style={{width:35,height:35,background:i===stage-1?b.accent:line,borderRadius:9,margin:'15px 0',color:'#111',...center,fontSize:22}}>↗</div><div style={{fontWeight:650,fontSize:19,lineHeight:1.2}}>{s}</div><div style={{height:5,marginTop:24,background:line,borderRadius:9}}><div style={{height:5,width:`${(stage===2?100:55+i*16)*enter(t,.6+i*.2)}%`,background:b.accent,borderRadius:9}}/></div></div>)}</div><div style={{marginTop:22,fontSize:17,color:muted,opacity:done}}>{stage===2?'✓  Your workspace is ready.':'✓  Ideas organized. Next step, yours.'}</div></>}
 </div></div>
 {stage===0&&<svg width="34" height="44" viewBox="0 0 34 44" style={{position:'absolute',left:(w>850?300:80)+select*40,top:h-120-select*10,opacity:enter(t,.5)}}><path d="M3 2 29 27 17 28 12 40Z" fill={fg} stroke={bg} strokeWidth="2"/></svg>}
 </div>;
}

function Project({b,index,t,ink,w,h,full=false}){
 const accent=b.accent,dark=index!==1,fg=dark?'#fff':'#101010';
 return <div style={{position:'relative',width:w,height:h,background:dark?'#0b0b0b':'#f7f7f2',color:fg,overflow:'hidden',borderRadius:full?0:18,border:'1px solid #7774'}}>
 {b.images?<Img src={staticFile(b.images[index])} style={{width:'100%',height:'100%',objectFit:'cover',transform:`scale(${1+t*.012})`}}/>:<><div style={{position:'absolute',width:h*1.05,height:h*1.05,right:-h*.03,top:-h*.03,transform:`scale(${.8+enter(t)*.2})`}}><Art motif={['rings','ribbons','grid'][index]} accent={accent} t={t+index*2} variant={index} ink={fg}/></div><div style={{...abs,left:w*.07,top:h*.12,fontSize:Math.min(w*.2,h*.22),fontWeight:750,letterSpacing:-7,lineHeight:.9,mixBlendMode:'difference',color:'#fff'}}>{b.projects[index].split(' ').map((s,i)=><div key={i}>{s}</div>)}</div></>}
 <div style={{...abs,left:w*.07,right:w*.07,bottom:h*.08,display:'flex',justifyContent:'space-between',fontSize:Math.min(w*.034,21),fontWeight:600,color:b.images?'#fff':fg,textShadow:b.images?'0 1px 5px #000':undefined}}><span>{b.brand} / 0{index+1}</span><span>↗</span></div>
 </div>;
}

function Scene({b,s,W,H,P,Q,fg,bg}){
 const t=s.time,e=enter(t),accent=b.accent,mid=H/2,pad=P?60:90;
 const stack=P||Q;
 const title=(text,size=120,extra={})=><Type text={text} size={P?size*.78:Q?size*.87:size} color={fg} t={t} style={extra}/>;
 const centered=(child,style={})=><div style={{...abs,inset:0,...center,flexDirection:'column',padding:pad,...style}}>{child}</div>;
 switch(s.name){
 case 'signal': return <>
  <div style={{...abs,width:P?W*1.3:Q?W*.74:H*1.05,height:P?W*1.3:Q?W*.74:H*1.05,left:P?-W*.15:Q?W*.28:W*.43,top:P?H*.27:Q?H*.36:-H*.02,transform:`scale(${.8+.2*e})`}}><Art motif={b.motif} accent={accent} t={t} ink={fg}/></div>
  <div style={{...abs,left:pad,top:P?H*.16:Q?H*.16:H*.29,width:stack?W-pad*2:W*.57}}><div style={{...mono,color:fg,marginBottom:32}}>MEET {b.brand.toUpperCase()}</div><Type text={b.hook} size={P?96:Q?85:116} color={fg} align="left" t={t+.25}/><div style={{width:100*e,height:8,background:accent,marginTop:34}}/></div>
 </>;
 case 'hook':return centered(<><div style={{...abs,width:W*1.2,height:4,background:accent,transform:`rotate(-23deg) scaleX(${e})`}}/>{title(b.words[0]+'.',P?145:200)}<div style={{...mono,marginTop:36,opacity:enter(t,.5)}}>{b.category}</div></>);
 case 'reveal':return centered(<><div style={{width:P?W:700,height:P?W:700,...abs,opacity:.55,transform:`scale(${1.4-.4*e})`}}><Art motif={b.motif} accent={accent} t={t} ink={fg}/></div><div style={{zIndex:1,background:bg,padding:'32px 45px',borderRadius:100,display:'flex',alignItems:'center',gap:25,transform:`scale(${.7+.3*e})`}}><Mark size={P?65:86} color={accent}/><div style={{fontSize:P?100:148,fontWeight:700,letterSpacing:-8}}>{b.brand}</div></div><div style={{...mono,position:'absolute',bottom:H*.16}}>{b.category}</div></>);
 case 'interface':return centered(<><div style={{...abs,top:H*.14,left:pad,right:pad}}>{title(b.words[1]+'.',90)}</div><div style={{transform:`perspective(1600px) rotateX(${10*(1-e)}deg) rotateY(${-8*(1-e)}deg) translateY(${45*(1-e)}px) scale(${.91+.09*e})`,marginTop:P?80:100}}><Interface b={b} t={t} stage={1} w={P?W-70:Q?W-100:W-220} h={P?650:Q?550:510}/></div></>);
 case 'orbit':return centered(<><div style={{width:P?W:750,height:P?W:750,...abs,transform:`rotate(${t*14}deg)`}}><Art motif="rings" accent={accent} t={t} ink={fg}/></div><div style={{zIndex:1,background:bg,padding:'22px 38px'}}>{title(b.words[2]+'.',140)}</div></>);
 case 'flow':return centered(<><div style={{marginBottom:stack?65:60}}>{title(b.promise,stack?100:110)}</div><div style={{display:'flex',flexDirection:P?'column':'row',gap:22,width:'100%',maxWidth:1300}}>{b.steps.map((s,i)=><div key={s} style={{flex:1,border:`1px solid ${fg}35`,background:i===1?accent:bg,color:i===1?'#111':fg,borderRadius:24,padding:stack?30:40,transform:`translateY(${(1-enter(t,.35+i*.18))*80}px)`,opacity:enter(t,.35+i*.18)}}><div style={{...mono,marginBottom:25}}>0{i+1} /</div><div style={{fontSize:stack?36:38,fontWeight:650}}>{s}</div><div style={{fontSize:40,marginTop:25}}>↗</div></div>)}</div></>);
 case 'resolve':return centered(<><div style={{width:W,height:4,...abs,top:H*.3,background:accent,transform:`scaleX(${e})`}}/>{title(b.promise,130)}</>);
 case 'demoHook':return centered(<><div style={{border:`1px solid ${fg}30`,borderRadius:40,padding:'12px 25px',...mono,marginBottom:40}}>IDEA → ACTION</div>{title(b.hook,125)}<div style={{fontSize:26,marginTop:35,color:fg,opacity:enter(t,.3)}}>{b.category}</div></>);
 case 'input':case 'organize':case 'ready':{
  const stage={input:0,organize:1,ready:2}[s.name];return centered(<><div style={{...abs,top:H*.15,left:pad,right:pad,display:'flex',alignItems:'center',gap:25}}><div style={{borderRadius:100,width:60,height:60,background:accent,color:'#111',...center,fontSize:22}}>0{stage+1}</div><Type text={b.steps[stage]} size={P?55:70} color={fg} align="left" t={t}/></div><div style={{marginTop:P?40:140,transform:`translateY(${40*(1-e)}px) scale(${.95+.05*e})`}}><Interface b={b} t={t} stage={stage} w={P?W-60:Q?W-80:W-220} h={P?670:Q?560:510}/></div>{P&&<div style={{fontSize:28,marginTop:50,opacity:enter(t,.4)}}>{b.words[stage]}.</div>}</>);}
 case 'focus':return centered(<><div style={{...abs,top:stack?H*.15:H*.13}}>{title(b.promise,105)}</div><div style={{background:accent,color:'#111',borderRadius:30,padding:stack?45:50,width:stack?W*.7:W*.63,marginTop:stack?170:170,transform:`rotate(${-3+3*e}deg) scale(${.8+.2*e})`}}><div style={{...mono}}>ONE CLEAR NEXT STEP</div><div style={{fontSize:stack?58:76,fontWeight:700,letterSpacing:-3,marginTop:25}}>{b.steps[2]}</div><div style={{marginTop:35,display:'flex',gap:12}}>{b.steps.map((_,i)=><div key={i} style={{height:10,flex:1,background:'#1112',borderRadius:20}}><div style={{height:'100%',width:`${enter(t,.3+i*.25,1)*100}%`,background:'#111',borderRadius:20}}/></div>)}</div><div style={{fontSize:55,textAlign:'right',marginTop:15}}>✓</div></div></>);
 case 'punch':return centered(<><div style={{...abs,top:mid-(P?W:W*.55)/2,width:P?W:W*.55,height:P?W:W*.55,borderRadius:'50%',border:`${P?45:60}px solid ${accent}`,boxSizing:'border-box',transform:`scale(${.55+.45*e})`}}/><Type text={b.hook} size={P?110:Q?125:158} color={fg} t={t+.25} style={{zIndex:1}}/></>);
 case 'relay':return centered(<>{b.words.map((s,i)=><div key={s} style={{fontSize:P?120:Q?140:160,lineHeight:1.02,fontWeight:750,letterSpacing:-7,color:i===1?'#111':fg,background:i===1?accent:'transparent',padding:'0 30px',transform:`translateX(${(1-enter(t,i*.25))*(i%2?-W:W)}px) rotate(${i===1?-4:0}deg)`}}>{s.toUpperCase()}</div>)}</>);
 case 'ribbons':return <><div style={{...abs,inset:0,...center}}><div style={{width:P?W*1.2:W*.7,height:P?W*1.2:W*.7}}><Art motif="ribbons" accent={accent} t={t} ink={fg}/></div></div>{[0,1,2].map(i=><div key={i} style={{...abs,top:H*(.3+i*.16),left:-W*.12,width:W*1.3,background:i===1?accent:bg,color:i===1?'#111':fg,border:`1px solid ${fg}30`,fontSize:P?58:90,fontWeight:700,letterSpacing:-3,padding:'12px 0',textAlign:'center',transform:`rotate(${i%2?-9:9}deg) translateX(${(i%2?1:-1)*(1-enter(t,i*.15))*W}px)`}}>{b.words[i]} / {b.words[(i+1)%3]}</div>)}</>;
 case 'tiles':return centered(<div style={{display:'grid',gridTemplateColumns:P?'1fr':'1fr 1fr 1fr',gap:18,width:'100%'}}>{b.words.map((s,i)=><div key={s} style={{height:P?H*.23:Q?500:470,borderRadius:24,border:`1px solid ${fg}40`,position:'relative',overflow:'hidden',transform:`translateY(${(1-enter(t,i*.16))*100}px)`}}><div style={{height:'85%',transform:`scale(${P?.8:1.1})`}}><Art motif={['rings','grid','ribbons'][i]} accent={accent} t={t+i} ink={fg} variant={i}/></div><div style={{...abs,bottom:25,left:25,right:25,fontSize:P?38:36,fontWeight:650,display:'flex',justifyContent:'space-between'}}>{s}<span>↗</span></div></div>)}</div>);
 case 'manifesto':return centered(title(b.promise,P?140:155));
 case 'folioOpen':return <><div style={{...abs,top:H*.16,left:pad,right:pad}}><div style={{...mono,marginBottom:30}}>SELECTED WORK / VOL. 01</div><Type text={b.hook} size={P?98:125} color={fg} align="left" t={t+.2}/></div><div style={{...abs,top:P?H*.52:Q?H*.56:H*.58,left:pad,right:pad,display:'flex',gap:20,transform:`translateX(${(1-e)*W*.3}px)`}}>{b.projects.map((_,i)=><div key={i} style={{transform:`rotate(${[-7,3,9][i]}deg) translateY(${i===1?-20:25}px)`}}><Project b={b} index={i} t={t} w={P?W*.42:W*.28} h={P?H*.28:Q?H*.30:H*.31} ink={fg}/></div>)}</div></>;
 case 'projectA':case 'projectB':case 'projectC':{
 const i={projectA:0,projectB:1,projectC:2}[s.name];return <><div style={{...abs,inset:P?'190px 40px 220px':'100px 70px 100px',transform:`perspective(1700px) rotateY(${(1-e)*(i%2?-14:14)}deg) scale(${.8+.2*e})`}}><Project b={b} index={i} t={t} w={P?W-80:W-140} h={P?H-410:H-200} ink={fg}/></div><div style={{...abs,bottom:P?140:45,left:pad,right:pad,...mono,display:'flex',justifyContent:'space-between'}}><span>0{i+1} / {b.projects[i].toUpperCase()}</span><span>{b.brand}</span></div></>;}
 case 'wall':return <div style={{...abs,left:-W*.2,top:-H*.3,transform:`rotate(-13deg) translateY(${-t*38}px)`}}>{Array.from({length:4},(_,r)=><div key={r} style={{display:'flex',gap:22,marginBottom:22,transform:`translateX(${(r%2?-1:1)*t*42}px)`}}>{Array.from({length:5},(_,c)=><Project key={c} b={b} index={(r+c)%3} t={t} w={P?400:480} h={P?360:330} ink={fg}/>)}</div>)}</div>;
 case 'folioIndex':return centered(<><Type text={b.promise} size={P?94:110} color={fg} t={t} style={{marginBottom:60}}/>{b.projects.map((s,i)=><div key={s} style={{width:'100%',borderTop:`1px solid ${fg}45`,padding:'22px 0',display:'flex',alignItems:'center',gap:30,transform:`translateX(${(1-enter(t,i*.15))*80}px)`,opacity:enter(t,i*.15)}}><span style={{...mono}}>0{i+1}</span><span style={{fontSize:P?50:58,fontWeight:600}}>{s}</span><span style={{marginLeft:'auto',fontSize:55,color:fg}}>↗</span></div>)}</>);
 case 'end':return centered(<><div style={{width:P?W*1.1:H,height:P?W*1.1:H,...abs,opacity:.18,transform:`scale(${1+.03*t})`}}><Art motif={b.motif} accent={accent} t={t} ink={fg}/></div><div style={{display:'flex',alignItems:'center',gap:20,zIndex:1}}><Mark size={P?70:90} color={fg}/><Type text={b.brand} size={Math.min(P?110:155,(W-2*pad-110)/(b.brand.length*.55))} color={fg} t={t}/></div><div style={{fontSize:P?40:46,marginTop:30,fontWeight:500,opacity:enter(t,.3),textAlign:'center',zIndex:1}}>{b.cta}</div><div style={{background:accent,color:'#111',padding:'20px 34px',borderRadius:100,fontSize:25,fontWeight:650,marginTop:40,opacity:enter(t,.5),transform:`translateY(${20*(1-enter(t,.5))}px)`,zIndex:1}}>{b.url} ↗</div></>);
 default:return null;
 }
}

export function Film(b){
 const frame=useCurrentFrame(),{fps,width,height}=useVideoConfig(),time=frame/fps;
 const [handle]=useState(()=>delayRender('Load bundled typeface'));
 useEffect(()=>{const f=new FontFace('MotionSans',`url(${staticFile('DM-Sans.ttf')})`,{weight:'100 1000'});f.load().then(font=>{document.fonts.add(font);continueRender(handle);}).catch(cancelRender);},[handle]);
 const P=height>width,Q=height===width,W=P?900:Q?1000:1600,H=height/(width/W),s=sceneAt(b,time);
 const inverse=['hook','resolve','manifesto','projectB','focus','folioIndex'].includes(s.name);
 const white=(b.theme==='white')!==inverse,bg=white?'#fafaf7':'#080808',fg=white?'#111111':'#f8f8f4';
 const transition=clamp(s.time/.18),wipe=s.start>0&&s.time<.2;
 return <AbsoluteFill style={{background:bg,overflow:'hidden'}}><div style={{position:'absolute',width:W,height:H,transform:`scale(${width/W})`,transformOrigin:'top left',fontFamily:'MotionSans, sans-serif',background:bg,color:fg,overflow:'hidden'}}>
 <Scene b={b} s={s} W={W} H={H} P={P} Q={Q} fg={fg} bg={bg}/>
 <div style={{...abs,top:P?56:40,left:P?55:65,right:P?55:65,display:'flex',justifyContent:'space-between',alignItems:'center',fontSize:18,fontWeight:600,mixBlendMode:s.name==='wall'?'difference':undefined,color:s.name==='wall'?'#fff':fg}}><span style={{display:'flex',alignItems:'center',gap:9}}><Mark size={22} color={s.name==='wall'?'#fff':fg}/>{b.brand}</span><span style={{...mono,fontSize:13}}>{b.mode==='portfolio'?'SELECTED WORK':'IN MOTION'} / {String(Math.floor(time)+1).padStart(2,'0')}</span></div>
 <div style={{...abs,bottom:P?48:32,left:P?55:65,right:P?55:65,display:'flex',justifyContent:'space-between',fontSize:12,letterSpacing:1,color:s.name==='wall'?'#fff':fg,opacity:.7}}><span>{b.concept?'FICTIONAL CONCEPT · ORIGINAL DESIGN':b.category.toUpperCase()}</span><span>{b.mode==='portfolio'?'PORTFOLIO':b.category.toUpperCase()}</span></div>
 <div style={{...abs,bottom:0,left:0,height:4,width:`${time/duration(b)*100}%`,background:fg}}/>
 {wipe&&<div style={{...abs,inset:0,background:fg,transform:`translateX(${inout(transition)*110}%)`}}/>}
 </div></AbsoluteFill>;
}
