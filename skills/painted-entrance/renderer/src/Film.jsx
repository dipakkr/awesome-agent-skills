import React from 'react';
import {AbsoluteFill,useCurrentFrame,useVideoConfig,staticFile} from 'remotion';
import {Brush} from './Brush.jsx';import {Pixel} from './Pixel.jsx';
export const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
export const ease=v=>{v=clamp(v);return v*v*(3-2*v)};
export const out=v=>1-(1-clamp(v))**3;
export const mix=(a,b,v)=>a+(b-a)*v;
export function Film(b){const f=useCurrentFrame(),{width,height,fps}=useVideoConfig();return <AbsoluteFill style={{background:b.mode==='brush'?'#fcfbf7':'#080a09'}}><style>{`@font-face{font-family:Serif;src:url('${staticFile('DM-Serif.ttf')}')}@font-face{font-family:Sans;src:url('${staticFile('DM-Sans.ttf')}')}*{box-sizing:border-box}`}</style>{b.mode==='brush'?<Brush b={b} t={f/fps} w={width} h={height}/>:<Pixel b={b} t={f/fps} w={width} h={height}/>}</AbsoluteFill>}
