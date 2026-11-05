import React from 'react';
import {clamp,ease,out,mix} from './Film.jsx';
const mono='ui-monospace, monospace';
function Vehicle({x,y,s=1,angle=0,explode=0,accent,flame=0,t=0,outline=false}){return <g transform={`translate(${x} ${y}) rotate(${angle}) scale(${s})`}>
 {flame>0&&<g><path d={`M-34 165Q-65 ${250+flame*80} 0 ${320+flame*230+Math.sin(t*43)*22}Q65 ${250+flame*80} 34 165Z`} fill="url(#exhaust)" filter="url(#glow)"/><path d={`M-21 165Q-35 260 0 ${290+flame*100+Math.sin(t*36)*18}Q35 260 21 165Z`} fill="#ecf9ff"/></g>}
 <g transform={`translate(0 ${-explode*160})`}><path d="M-53 -135Q-50 -240 0 -310Q50 -240 53 -135Z" fill={outline?'none':'url(#metal)'} stroke={outline?accent:'#a9bac2'} strokeWidth="2"/><path d="M0 -309Q24 -220 20 -135" fill="none" stroke={outline?accent:'#fff'} strokeWidth="2" opacity=".5"/><path d="M-43 -185H43" stroke={accent} strokeWidth="8"/><circle cy="-213" r="14" fill={outline?'none':'#11242e'} stroke={accent} strokeWidth="4"/></g>
 <g><path d="M-53 -130H53L48 112H-48Z" fill={outline?'none':'url(#metal)'} stroke={outline?accent:'#94a2a9'} strokeWidth="2"/><path d="M-52 -95H52M-49 75H49" stroke={outline?accent:'#69757c'} strokeWidth="4"/>{Array.from({length:14},(_,i)=><path key={i} d={`M${-40+i*6} -80V55`} stroke={outline?accent:'#aebfc7'} strokeWidth=".7" opacity=".3"/>)}<rect x="-14" y="-50" width="28" height="72" rx="4" fill={accent}/><path d="M-5 -36L5 -27L-5 -18L5 -9" fill="none" stroke="#102028" strokeWidth="3"/></g>
 {[-1,1].map(dir=><g key={dir} transform={`translate(${dir*explode*95} ${explode*30}) scale(${dir} 1)`}><path d="M48 35L100 120L101 174L48 125Z" fill={outline?'none':'url(#fin)'} stroke={outline?accent:'#8a9ca6'} strokeWidth="2"/><path d="M52 70L84 125L84 150L52 124Z" fill={outline?'none':accent} opacity=".8"/></g>)}
 <g transform={`translate(0 ${explode*110})`}><path d="M-48 116H48L32 147H-32Z" fill={outline?'none':'#3c505c'} stroke={outline?accent:'#9baab2'} strokeWidth="2"/><path d="M-28 147H28L40 183H-40Z" fill={outline?'none':'url(#metal)'} stroke={outline?accent:'#80929b'} strokeWidth="2"/>{[-24,-12,0,12,24].map(x=><path key={x} d={`M${x} 151L${x*1.3} 178`} stroke={outline?accent:'#4a616d'} strokeWidth="2"/>)}</g>
 </g>}
function Satellite({x,y,t,accent,s=1}){let e=out(t/1.3);return <g transform={`translate(${x} ${y}) rotate(${-15+t*4}) scale(${s})`}><rect x="-45" y="-55" width="90" height="110" rx="5" fill="url(#gold)" stroke="#fff"/><rect x="-25" y="-35" width="50" height="50" fill="#102b3e" stroke="#fff"/>{[-1,1].map(d=><g key={d} transform={`scale(${d} 1)`}><path d="M45 0H100" stroke="#b8c8d3" strokeWidth="9"/><g transform={`translate(100 0) scale(${e} 1)`}><rect y="-85" width="165" height="170" fill="#17344c" stroke={accent} strokeWidth="3"/>{[0,1,2,3].map(i=><path key={i} d={`M${i*41} -85V85M0 ${-85+i*43}H165`} stroke={accent} opacity=".55"/>)}</g></g>)}<path d="M0 -55V-110M-45 -110Q0 -60 45 -110" stroke="#e1edf2" strokeWidth="5" fill="none"/><circle cy="-111" r="5" fill={accent}/></g>}
function Label({x,y,children,accent='#93a9b8',size=19,anchor='start'}){return <text x={x} y={y} fill={accent} fontFamily={mono} fontSize={size} textAnchor={anchor} letterSpacing="2">{children}</text>}
export function Rocket({b,t,w,h}){const tall=h>w,W=h>=w?1080:1600,H=W*h/w,cx=w>h&&t<22?W*.67:W/2,cy=tall?H*.55:H*.58,a=b.accent;const scene=t<4?0:t<8?1:t<11?2:t<14?3:t<18?4:t<22?5:6,starts=[0,4,8,11,14,18,22],q=t-starts[scene],light=scene===0;const fg=light?'#10212a':'#f1f7fa';
 const title=[b.headline,b.chapters[0],b.chapters[1],b.chapters[2],b.chapters[3],b.ending,b.brand][scene];
 const headerY=tall?280:175;const lines=[''];for(const word of title.split(' ')){const last=lines.length-1;if((lines[last]+' '+word).trim().length>(w>h?24:29)&&lines[last])lines.push(word);else lines[last]=(lines[last]+' '+word).trim();}
 return <svg width={w} height={h} viewBox={`0 0 ${W} ${H}`}><defs><clipPath id="launchClearance"><rect x="0" y={w<=h?headerY+(lines.length-1)*76+55:0} width={W} height={H}/></clipPath>
 <linearGradient id="metal"><stop stopColor="#3a505e"/><stop offset=".17" stopColor="#a9b8c0"/><stop offset=".38" stopColor="#fff"/><stop offset=".51" stopColor="#e3edf1"/><stop offset=".69" stopColor="#8399a6"/><stop offset=".85" stopColor="#263e4b"/><stop offset="1" stopColor="#617d8c"/></linearGradient>
 <linearGradient id="fin"><stop stopColor="#839ba8"/><stop offset=".5" stopColor="#e3edf2"/><stop offset="1" stopColor="#283c48"/></linearGradient>
 <linearGradient id="gold"><stop stopColor="#7d5121"/><stop offset=".4" stopColor="#ffe2a3"/><stop offset=".7" stopColor="#c5943d"/><stop offset="1" stopColor="#f6d07f"/></linearGradient>
 <linearGradient id="exhaust" x1="0" y1="0" x2="0" y2="1"><stop stopColor="#fff"/><stop offset=".15" stopColor={a}/><stop offset=".6" stopColor="#ff6a2b"/><stop offset="1" stopColor="#ff4e22" stopOpacity="0"/></linearGradient>
 <radialGradient id="space"><stop stopColor="#142733"/><stop offset="1" stopColor="#030609"/></radialGradient><radialGradient id="earth"><stop stopColor="#0b1820"/><stop offset=".85" stopColor="#122b3e"/><stop offset=".97" stopColor="#3c88a4"/><stop offset="1" stopColor="#b9ecff"/></radialGradient>
 <filter id="glow" x="-150%" y="-100%" width="400%" height="400%"><feGaussianBlur stdDeviation="9"/></filter><pattern id="technical" width="64" height="64" patternUnits="userSpaceOnUse"><path d="M64 0H0V64" fill="none" stroke={light?'#a8b9bf':'#243540'} strokeWidth="1" opacity=".35"/></pattern>
 </defs><rect width={W} height={H} fill={light?'#f4f6f5':'url(#space)'}/>{scene<3&&<rect width={W} height={H} fill="url(#technical)"/>}
 {!light&&Array.from({length:85},(_,i)=>{let x=(i*317+81)%W,y=(i*191+40)%H;return <circle key={i} cx={x} cy={(y+(scene===4?q*180:0))%H} r={i%7===0?1.7:.8} fill="#d5e8f3" opacity={.15+(i%5)*.1}/>})}
 <Label x={70} y={65} accent={fg}>{b.brand} / FLIGHT SYSTEMS</Label><Label x={W-70} y={65} anchor="end" accent={fg}>SEQ 0{scene+1}</Label>
 {scene!==6&&<><text x={70} y={headerY} fill={fg} fontFamily="Sans" fontWeight="600" fontSize={w>h?62:Math.min(65,(W-140)/(Math.max(...lines.map(l=>l.length))*.55))} letterSpacing="-2" opacity={out(q/.55)}>{lines.map((line,i)=><tspan key={i} x={70} dy={i?76:0}>{line}</tspan>)}</text><path d={`M70 ${headerY+28+(lines.length-1)*76}H${70+140*out(q/.7)}`} stroke={a} strokeWidth="5"/></>}
 {scene===0?<>
  <g opacity={.2}><path d={`M${cx-290} ${cy-280}V${cy+250}M${cx+290} ${cy-280}V${cy+250}M${cx-310} ${cy-280}H${cx+310}M${cx-310} ${cy+250}H${cx+310}`} fill="none" stroke="#36566a" strokeDasharray="5 7"/></g>
  <Vehicle x={cx} y={cy+45} s={tall?1.5:1.12} t={t} accent="#376071" outline/>
  <g opacity={out(q-1)}><path d={`M${cx+50} ${cy-185}H${cx+210}l40 -40`} fill="none" stroke="#36566a"/><Label x={cx+150} y={cy-240} size={17} accent="#36566a">01 / PAYLOAD</Label><path d={`M${cx-50} ${cy+155}H${cx-260}`} stroke="#36566a"/><Label x={cx-280} y={cy+195} size={17} accent="#36566a">02 / PROPULSION</Label></g>
  <Label x={70} y={H-110} accent="#36566a">DESIGNED TO MOVE AN IDEA FORWARD.</Label>
 </>:scene===1?<>
  <Vehicle x={cx} y={cy+45} s={tall?1.25:.8} explode={1-ease((q-.5)/2.5)} accent={a} t={t}/>
  {['PAYLOAD','AIRFRAME','GUIDANCE','THRUST'].map((txt,i)=><g key={txt} opacity={out((q-i*.45)/.5)}><Label x={70} y={H-195+i*31} size={16} accent={q>i*.45+1?a:'#758995'}>{`${q>i*.45+1?'[+]':'[ ]'} ${txt}`}</Label></g>)}
  <path d={`M${cx+180} ${cy-260}V${cy+220}`} stroke={a} strokeWidth="1" strokeDasharray="4 12" opacity=".4"/>
 </>:scene===2?<>
  <text x={cx} y={cy+240} textAnchor="middle" fontFamily="Sans" fontWeight="700" fontSize={tall?600:570} fill="none" stroke={a} strokeWidth="2" opacity=".55">{Math.max(1,3-Math.floor(q))}</text>
  <Vehicle x={cx} y={cy+55} s={tall?1.25:.9} accent={a} t={t}/>
  <Label x={cx} y={H-115} anchor="middle" accent={a} size="24">T − 00:0{Math.max(1,3-Math.floor(q))}</Label>
 </>:scene===3?<>
  <g clipPath="url(#launchClearance)"><g transform={`translate(0 ${q>1.25?-((q-1.25)**2)*140:0})`}><Vehicle x={cx+Math.sin(q*80)*q*.7} y={cy+20} s={tall?1.4:1.04} flame={out(q/1.3)} accent={a} t={t}/></g></g>
  <path d={`M${cx-180} ${cy+245}H${cx+180}L${cx+230} ${cy+280}H${cx-230}Z`} fill="#243844"/><path d={`M${cx-110} ${cy+280}V${H}M${cx+110} ${cy+280}V${H}`} stroke="#435767" strokeWidth="20"/>
  {Array.from({length:25},(_,i)=>{let p=clamp((q-.5)/2),xx=cx+(i%2?1:-1)*(25+i*18)*p, yy=cy+270+(i%4)*28;return <ellipse key={i} cx={xx} cy={yy} rx={(35+i%5*15)*p} ry={(28+i%4*13)*p} fill={i%3?'#becbd1':'#fff'} opacity={.2*p}/>})}
 </>:scene===4?<>
  <g transform={`translate(${cx} ${cy}) rotate(26)`}><path d="M0 -700V1000" stroke={a} strokeWidth="2" opacity=".15"/>{Array.from({length:34},(_,i)=><path key={i} d={`M${-500+(i*117)%1000} ${-700+((i*83+q*600)%1700)}v${70+i%5*15}`} stroke="#c6e9ff" strokeWidth="1" opacity=".22"/>)}<Vehicle x={0} y={-10+Math.sin(q)*18} s={tall?1.4:1.05} flame={1} accent={a} t={t}/></g>
  <Label x={70} y={H-115} size={20} accent={a}>FLIGHT / BEYOND THE EVERYDAY</Label>
 </>:scene===5?<>
  <ellipse cx={cx} cy={H+420} rx={W*1.1} ry={700} fill="url(#earth)"/>
  {b.subject==='satellite'?<Satellite x={cx} y={cy-35} s={tall?1.5:1.15} t={q} accent={a}/>:<g transform={`translate(${cx} ${cy-5}) rotate(${-22+q*5})`}><path d="M-110 45Q-90 -140 0 -210Q90 -140 110 45Z" fill="url(#metal)"/><ellipse cy="47" rx="110" ry="25" fill="#405864"/><circle cy="-90" r="34" fill="#092331" stroke={a} strokeWidth="9"/><path d="M-75 -20H75" stroke={a} strokeWidth="13"/>{[-1,1].map(d=><path key={d} d={`M${d*80} 15l${d*80} 50l${-d*42} -90Z`} fill="#7c99a8"/>)}</g>}
  <path d={`M${cx-380} ${cy+75}Q${cx} ${cy+250} ${cx+380} ${cy-110}`} fill="none" stroke={a} strokeWidth="2" strokeDasharray="6 14" strokeDashoffset={-q*45} opacity=".5"/>
  <Label x={cx} y={H-105} anchor="middle" accent={a}>PAYLOAD DEPLOYED / CONCEPT SEQUENCE</Label>
 </>:<>
  <ellipse cx={cx} cy={H+500} rx={W*1.2} ry={750} fill="url(#earth)"/>
  <path d={`M${cx-60} ${cy-175}L${cx} ${cy-245}L${cx+60} ${cy-175}L${cx} ${cy-203}Z`} fill={a}/>
  <text x={cx} y={cy-30} textAnchor="middle" fill="#fff" fontFamily="Sans" fontWeight="600" fontSize={Math.min(150,1100/b.brand.length)} letterSpacing="12">{b.brand}</text>
  <text x={cx} y={cy+45} textAnchor="middle" fill="#b6c9d3" fontFamily="Sans" fontSize="32">{b.cta}</text>
  <rect x={cx-205} y={cy+105} width="410" height="64" rx="32" fill={a}/><text x={cx} y={cy+146} textAnchor="middle" fontFamily={mono} fontSize="22" fill="#07121b">{b.url}</text>
 </>}
 <path d={`M70 ${H-63}H${W-70}`} stroke={light?'#c6d0d3':'#30444e'} strokeWidth="1"/><rect x="70" y={H-65} width={(W-140)*clamp(t/25)} height="4" fill={a}/><Label x="70" y={H-27} size="13" accent={light?'#526d79':'#7994a2'}>ORIGINAL CONCEPT / FLIGHT STUDY</Label>
 </svg>
}
