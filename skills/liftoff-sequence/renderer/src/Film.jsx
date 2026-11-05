import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig,staticFile} from 'remotion';
import {Paper} from './Paper.jsx';
import {Rocket} from './Rocket.jsx';
export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export const ease=v=>{v=clamp(v);return v*v*(3-2*v)};
export const out=v=>1-(1-clamp(v))**3;
export const mix=(a,b,v)=>a+(b-a)*v;
export function Film(b){const f=useCurrentFrame(),{width,height,fps}=useVideoConfig();return <AbsoluteFill style={{background:b.mode==='paper'?'#faf9f5':'#05080c'}}><style>{`@font-face{font-family:Story;src:url('${staticFile('DM-Serif.ttf')}')}@font-face{font-family:Sans;src:url('${staticFile('DM-Sans.ttf')}')}*{box-sizing:border-box}`}</style>{b.mode==='paper'?<Paper b={b} t={f/fps} w={width} h={height}/>:<Rocket b={b} t={f/fps} w={width} h={height}/>}</AbsoluteFill>}
