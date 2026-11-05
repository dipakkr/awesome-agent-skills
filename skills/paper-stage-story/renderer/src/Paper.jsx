import React from 'react';
import {clamp,ease,out,mix} from './Film.jsx';
const ink='#172e2b',teal='#196b59',paper='#faf9f5';
function Leaf({x=0,y=0,r=0,s=1,fill=teal}){return <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`}><path d="M0 0 Q-64 -80 0 -136 Q64 -80 0 0Z" fill={fill}/><path d="M0 -8L0 -119" stroke="#fff" opacity=".3" strokeWidth="2"/></g>}
function Envelope({x=0,y=0,s=1,accent}){return <g transform={`translate(${x} ${y}) scale(${s})`} filter="url(#paperShadow)"><path d="M-90 -57L92 -60L90 61L-92 58Z" fill="#fff"/><path d="M-90 -57L0 13L92 -60M-92 58L-22 -1M90 61L22 -1" fill="none" stroke="#d2cec2" strokeWidth="3"/><rect x="45" y="-40" width="25" height="30" fill={accent}/><path d="M-63 25h43M-63 36h30" stroke={ink} strokeWidth="3"/></g>}
function Seed({x=0,y=0,s=1,r=0,accent}){return <g transform={`translate(${x} ${y}) rotate(${r}) scale(${s})`} filter="url(#paperShadow)"><path d="M0 30C-65 10 -55 -57 0 -86C55 -57 65 10 0 30Z" fill={accent}/><path d="M0 18Q-14 -25 0 -65" fill="none" stroke="#fff" strokeWidth="4" opacity=".5"/></g>}
function Bird({x,y,s=1,t=0,accent,carrying=false,letter=false,look=0}){const step=Math.sin(t*8),flap=Math.sin(t*5)*8;return <g transform={`translate(${x} ${y-5*Math.abs(step)}) scale(${s})`}>
 <ellipse cx="0" cy="145" rx="85" ry="10" fill={ink} opacity=".08"/>
 <g stroke={ink} strokeWidth="7" strokeLinecap="round" fill="none"><path d={`M-25 65L${-30+step*14} 118L${-10+step*14} 122`}/><path d={`M28 65L${29-step*14} 117L${49-step*14} 121`}/></g>
 <g filter="url(#paperShadow)"><path d="M-65 -5L-120 -52L-101 23L-70 42Z" fill={teal}/><path d="M-72 -16Q-74 85 23 87Q94 62 85 -23L41 -77L-8 -63Z" fill={accent}/><path d="M-65 -10Q-7 -37 42 16Q17 83 -65 34Z" fill="#ffd7b9" transform={`rotate(${flap} -35 5)`}/><path d="M41 -77L78 -103L109 -63L85 -23Z" fill="#fff"/><path d="M100 -62L138 -42L100 -30Z" fill={ink}/><circle cx={79+look} cy="-57" r="6" fill={ink}/><circle cx={81+look} cy="-59" r="1.8" fill="white"/></g>
 {carrying&&(letter?<Envelope x={150} y={-3} s={.44} accent={accent}/>:<Seed x={137} y={-17} s={.34} r={15} accent={accent}/>)}
 </g>}
function Tree({growth=1,accent,letter=false,t=0}){const g=out(growth);return <g transform={`translate(0 40) scale(${g||.001})`} filter="url(#paperShadow)"><path d="M-19 0L-9 -285L12 -289L25 0Z" fill={ink}/>{[-1,1].map((dir,i)=><g key={dir} transform={`scale(${dir} 1)`}><path d={`M0 -${100+i*40}Q90 -190 124 -310`} stroke={ink} strokeWidth="13" fill="none"/>{[0,1,2].map(j=><Leaf key={j} x={50+j*37} y={-150-j*63-i*28} s={.65+j*.12} r={30+j*13+Math.sin(t+j)*2} fill={j===1?'#99bca0':teal}/>)}</g>)}<Leaf y={-270} s={1.1} r={-10}/>{[[-106,-264],[130,-230],[-46,-360]].map(([x,y],i)=>letter?<Envelope key={i} x={x} y={y} s={.33} accent={accent}/>:<circle key={i} cx={x} cy={y} r={24} fill={accent}/> )}</g>}
function Grass({x,y,s=1}){return <g transform={`translate(${x} ${y}) scale(${s})`} fill={teal}><path d="M0 0Q-52 -19 -43 -72Q-4 -59 0 0M0 0Q3 -99 35 -108Q51 -38 0 0M0 0Q37 -45 68 -26Q40 7 0 0"/></g>}
function Caption({title,sub,w,y,center=false,accent,show=1}){return <g opacity={out(show)} transform={`translate(0 ${24*(1-out(show))})`}><text x={center?w/2:90} y={y} textAnchor={center?'middle':'start'} fill={ink} fontFamily="Story" fontSize={Math.min(title.length>32?65:78,(w-180)/(title.length*.49))} letterSpacing="-2">{title}</text><text x={center?w/2:94} y={y+48} textAnchor={center?'middle':'start'} fill={ink} opacity=".66" fontFamily="Sans" fontSize="22" letterSpacing="1">{sub}</text></g>}
export function Paper({b,t,w,h}){
 const tall=h>=w, W=tall?1080:1600,H=tall?1920:900,ratio=w/h,viewH=W/ratio; const y=tall?viewH*(h>w?.55:.64):viewH*.71,scene=t<4?0:t<9?1:t<13?2:t<17?3:t<22?4:5,starts=[0,4,9,13,17,22],q=t-starts[scene],a=b.accent,letter=b.subject==='letter',cx=W/2;
 const cut=scene>0?1-ease(q/.42):0;
 const title=[b.headline,b.chapters[0],b.chapters[1],b.chapters[2],b.chapters[3],b.ending][scene];
 return <svg width={w} height={h} viewBox={`0 0 ${W} ${viewH}`} style={{position:'absolute',inset:0}}>
 <defs><filter id="paperShadow" x="-50%" y="-50%" width="200%" height="220%"><feDropShadow dx="3" dy="10" stdDeviation="6" floodColor="#1c2824" floodOpacity=".15"/></filter><filter id="paperGrain"><feTurbulence type="fractalNoise" baseFrequency=".65" numOctaves="3" seed="8"/><feColorMatrix type="saturate" values="0"/></filter><pattern id="tinyGrid" width="38" height="38" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r=".9" fill={ink} opacity=".13"/></pattern></defs>
 <rect width={W} height={viewH} fill={paper}/><rect width={W} height={viewH} fill="url(#tinyGrid)"/>
 <path d={`M0 ${viewH*.81}Q${W*.3} ${viewH*.77} ${W*.55} ${viewH*.84}T${W} ${viewH*.8}V${viewH}H0Z`} fill="#eeeee5"/>
 <text x="90" y="66" fontFamily="Sans" fontSize="18" letterSpacing="4" fill={ink}>{b.brand} / LITTLE STORIES</text><text x={W-90} y="66" textAnchor="end" fontFamily="Sans" fontSize="18" fill={ink}>0{scene+1} / 06</text>
 {scene===0?<>
  <Caption title={title} sub={letter?'A note. A journey. A connection.':'A seed. A journey. A beginning.'} w={W} y={tall?260:205} accent={a} show={q/.7}/>
  <g transform={`translate(${cx} ${y-35}) rotate(${-5+Math.sin(t)*1.5})`}><path d="M-255 -230L255 -220L268 192L-260 207Z" fill="#fff" filter="url(#paperShadow)"/><rect x="-230" y="-200" width="460" height="370" fill="none" stroke={ink} strokeWidth="2" strokeDasharray="4 12"/>
  {letter?<Envelope y={-23} s={1.6} accent={a}/>:<><Seed y={-12+Math.sin(t*2)*7} s={1.65} r={-15} accent={a}/><Leaf x={30} y={-107} r={55} s={.6}/></>}
  <text y="138" textAnchor="middle" fontFamily="Sans" letterSpacing="5" fontSize="19" fill={ink}>{letter?'HANDLE WITH HEART':'FULL OF POSSIBILITY'}</text></g>
  <Bird x={cx+(tall?270:410)} y={y+65} s={.75} t={t} accent={a}/><path d={`M${cx-340} ${y-90}q-55 -60 -85 -30M${cx-360} ${y+30}l-74 20`} fill="none" stroke={a} strokeWidth="6"/>
 </>:scene===1?<>
  <Caption title={title} sub="A little courage goes a long way." w={W} y={tall?250:190} show={q/.5}/>
  <g transform={`translate(${-q*24} 0)`}>{[0,1,2,3,4].map(i=><g key={i} transform={`translate(${80+i*390} ${y-110-i%2*45})`} filter="url(#paperShadow)"><path d="M-65 130L-65 -20L0 -82L65 -20L65 130Z" fill={i%2?'#e0e8dc':'#e8e3d7'}/><path d="M-83 -14L0 -97L82 -14" stroke={i%2?teal:a} strokeWidth="17" fill="none"/><rect x="-17" y="65" width="35" height="65" fill="#faf9f5"/><rect x="-25" y="-8" width="50" height="40" fill="#faf9f5"/></g>)}</g>
  <path d={`M-50 ${y+180}Q${cx} ${y-20} ${W+50} ${y+180}`} fill="none" stroke="#fff" strokeWidth="95" filter="url(#paperShadow)"/><path d={`M-50 ${y+180}Q${cx} ${y-20} ${W+50} ${y+180}`} fill="none" stroke={a} strokeWidth="3" strokeDasharray="8 14" strokeDashoffset={-q*45}/>
  <Bird x={mix(cx-170,cx+100,ease(q/4.5))} y={y-20} s={1.3} t={t} accent={a} carrying letter={letter}/><Grass x={120} y={y+260}/><Grass x={W-140} y={y+200} s={1.3}/>
 </>:scene===2?<>
  <Caption title={title} sub="Even when the weather turns." w={W} y={tall?250:190} show={q/.5}/>
  {[0,1,2].map(i=><g key={i} transform={`translate(${cx-270+i*270+Math.sin(q+i)*20} ${y-290}) scale(.7)`} filter="url(#paperShadow)"><path d="M-110 35Q-150 -10 -95 -33Q-82 -104 -16 -65Q35 -100 61 -42Q121 -45 117 20L97 42Z" fill={i%2?'#d3ded8':'#e1e6de'}/></g>)}
  {Array.from({length:28},(_,i)=>{const xx=cx-430+(i*137)%860, yy=y-350+((q*260+i*89)%600);return <path key={i} d={`M${xx} ${yy}l-12 32`} stroke="#72a49c" strokeWidth="4" opacity=".6"/>})}
  <Bird x={cx} y={y+30} s={1.35} t={t*.35} accent={a} carrying letter={letter}/>
  <g transform={`translate(${cx+40} ${y-190}) rotate(${Math.sin(q*3)*3})`} filter="url(#paperShadow)"><path d="M-220 0Q0 -260 220 0Q160 -30 110 0Q55 -28 0 0Q-55 -28 -110 0Q-165 -28 -220 0Z" fill={a}/><path d="M0 -173V157Q0 200 45 173" fill="none" stroke={ink} strokeWidth="10"/><path d="M0 -173Q-90 -100 -110 0M0 -173Q90 -100 110 0" stroke="#fff" opacity=".35" fill="none" strokeWidth="3"/></g>
  <ellipse cx={cx} cy={y+218} rx="260" ry="22" fill="#cddbd7" opacity=".6"/>
 </>:scene===3?<>
  <Caption title={title} sub={letter?'The right words find their way.':'Good roots need a little care.'} w={W} y={tall?250:190} show={q/.5}/>
  <Bird x={cx-180} y={y-15} s={1.45} t={t*.25} accent={a}/>
  {letter?<g transform={`translate(${cx+190} ${y-40})`} filter="url(#paperShadow)"><path d="M-75 120V-155Q-75 -245 20 -245Q100 -245 100 -155V120Z" fill={teal}/><path d="M-45 -156H66" stroke={ink} strokeWidth="19"/><path d="M13 120V245" stroke={ink} strokeWidth="20"/><Envelope x={0} y={mix(-280,-170,out(q/2))} s={.7*(1-ease((q-2)/.8))} accent={a}/><path d="M95 -110h80v-90h-65" fill={a}/></g>:<><ellipse cx={cx+180} cy={y+105} rx="140" ry="28" fill="#c8bdac"/><Seed x={cx+180} y={mix(y-180,y+93,out(q/2))} s={.8*(1-ease((q-2)/.6))} r={q*30} accent={a}/><g transform={`translate(${cx+180} ${y+110}) scale(${out((q-2)/1.4)})`}><path d="M0 0V-95" stroke={teal} strokeWidth="9"/><Leaf x={0} y={-45} r={-60} s={.5}/><Leaf y={-65} r={55} s={.45}/></g></>}
  <Grass x={cx-400} y={y+130} s={1.1}/><Grass x={cx+420} y={y+130} s={.7}/>
 </>:scene===4?<>
  <Caption title={title} sub={letter?'One small hello can bring us together.':'What you nurture grows.'} w={W} y={tall?250:190} show={q/.5}/>
  <g transform={`translate(${cx+55} ${y+65}) scale(${h>w?1.35:h===w?.95:1.2})`}><Tree growth={q/2.8} accent={a} letter={letter} t={t}/></g>
  <Bird x={cx-265} y={y+35} s={1.1} t={t*.45} accent={a}/><g transform={`translate(${cx+330} ${y+45}) scale(-.85 .85)`}><Bird x={0} y={0} t={t*.5} accent="#edb440"/></g><Grass x={cx-60} y={y+140}/><Grass x={cx+420} y={y+160}/>
  {[0,1,2,3,4].map(i=><g key={i} transform={`translate(${cx-400+i*190} ${y-260-Math.sin(q*2+i)*30-i%2*90}) rotate(${q*20+i*36})`} opacity={out(q-1)}><path d="M-8 0H8M0 -8V8" stroke={a} strokeWidth="3"/></g>)}
 </>:<>
  <g transform={`translate(${cx} ${viewH*.49}) scale(${tall?1.05:.8})`}><Bird x={-230} y={10} s={1} t={t*.3} accent={a}/>{letter?<Envelope x={135} y={-10} s={1.2} accent={a}/>:<Tree growth={1} accent={a} t={t}/>}</g>
  <Caption title={title} sub={b.cta} w={W} y={viewH-190} center show={q/.65}/><text x={cx} y={viewH-70} fill={ink} textAnchor="middle" fontFamily="Sans" fontWeight="700" fontSize="25">{b.url}</text>
 </>}
 <rect width={W} height={viewH} filter="url(#paperGrain)" opacity=".035" style={{mixBlendMode:'multiply'}} pointerEvents="none"/>
 <path d={`M${-W+cut*W} 0L${-W+cut*W+60} 130L${-W+cut*W-10} 270L${-W+cut*W+35} 470L${-W+cut*W-20} ${viewH}H-1800V0Z`} fill={paper}/>
 <text x="90" y={viewH-42} fontFamily="Sans" fontSize="15" letterSpacing="2" fill={ink} opacity=".45">AN ORIGINAL CONCEPT STORY</text>
 </svg>
}
