#!/usr/bin/env node
// Original deterministic instrumental arrangement for local concept films.
// Optional, not a substitute for a user-supplied/licensed soundtrack.
// node compose-score.mjs output.wav --seconds 84 --bpm 120 --dip 56 --seed 17
import fs from 'node:fs';
import path from 'node:path';
const [out,...args]=process.argv.slice(2);
const option=(key,fallback)=>{const i=args.indexOf('--'+key);return i<0?fallback:Number(args[i+1]);};
const duration=option('seconds',84),bpm=option('bpm',120),dip=option('dip',56);
if(!out||duration<5||duration>600||bpm<60||bpm>180) throw Error('Supply output.wav, --seconds 5..600 and --bpm 60..180');
if(fs.existsSync(out)) throw Error('Use a new soundtrack path');
const sr=44100,count=Math.round(duration*sr),left=new Float32Array(count),right=new Float32Array(count),beat=60/bpm;
let rng=option('seed',17)>>>0;const noise=()=>{rng=(1664525*rng+1013904223)>>>0;return rng/2147483648-1;};
const freq=n=>440*2**((n-69)/12),tau=Math.PI*2;
function put(at,length,fn,pan=0){
 const start=Math.round(at*sr),n=Math.min(Math.round(length*sr),count-start);
 const lp=Math.sqrt((1-pan)/2),rp=Math.sqrt((1+pan)/2);
 for(let j=0;j<n;j++){const v=fn(j/sr,j);left[start+j]+=v*lp;right[start+j]+=v*rp;}
}
const chords=[[50,57,61,66],[47,54,59,62],[43,50,57,59],[45,52,59,61]];
const gainAt=t=>t>=dip&&t<dip+4?.14:t<4?.35:t>duration-6?.55:1;
for(let bar=0;bar*beat*4<duration;bar++){
 const at=bar*beat*4,chord=chords[Math.floor(bar/2)%4],g=gainAt(at);
 // Soft stereo pad, gently detuned with slow attack and release.
 for(let j=0;j<chord.length;j++){
  const f=freq(chord[j]+12),len=beat*5;
  put(at,len,t=>.028*(1-Math.exp(-t*3))*Math.exp(-t*.7)*(Math.sin(tau*f*t)+.35*Math.sin(tau*f*1.003*t)),(j-1.5)*.28);
 }
 for(let b=0;b<4;b++){
  const when=at+b*beat;if(when>=duration)continue;
  if(when>=4&&g>.2){
   put(when,.35,t=>g*.35*Math.exp(-t*17)*Math.sin(tau*(49*t+7*(1-Math.exp(-t*30))/30)),0);
   if(b%2)put(when,.18,t=>g*.085*noise()*(Math.exp(-t*38)+.3*Math.exp(-(((t-.025)/.008)**2))),.08);
  }
  const f=freq(chord[0]-12);
  if(when>=8)put(when,beat*.9,t=>g*.11*Math.min(1,t*150)*Math.exp(-t*5)*(Math.sin(tau*f*t)+.18*Math.sin(tau*f*2*t)),0);
 }
 for(let j=0;j<8;j++){
  const when=at+j*beat/2;if(when>=duration)continue;
  if(when>=12&&g>.2)put(when,.09,t=>g*.018*noise()*Math.exp(-t*55),j%2?.55:-.4);
  const note=chord[[0,2,1,3,2,1,3,2][j]]+24,f=freq(note),amplitude=.065*g;
  put(when,1.4,t=>amplitude*(1-Math.exp(-t*180))*Math.exp(-t*6)*(Math.sin(tau*f*t)+.3*Math.sin(tau*f*2*t)+.12*Math.sin(tau*f*3*t)),j%2?.32:-.32);
 }
}
// A simple original piano-like motif, voiced over the established pulse.
const melody=[74,73,69,66,69,71,73,69,74,78,76,73,71,69,66,69];
for(let m=0;8+m*beat*2<duration-4;m++){
 const at=8+m*beat*2,f=freq(melody[m%melody.length]),g=gainAt(at);
 put(at,2,t=>g*.08*Math.min(1,t*160)*Math.exp(-t*2.9)*(Math.sin(tau*f*t)+.25*Math.sin(tau*f*2.001*t)+.08*Math.sin(tau*f*3*t)),.12);
}
// Stereo quarter-note echoes; no external samples or borrowed melody.
const delay=Math.round(beat*.75*sr);
for(let i=delay;i<count;i++){left[i]+=right[i-delay]*.16;right[i]+=left[i-delay]*.14;}
let peak=0;for(let i=0;i<count;i++)peak=Math.max(peak,Math.abs(left[i]),Math.abs(right[i]));
const pcm=Buffer.alloc(count*4),scale=.78/Math.max(peak,.01);
for(let i=0;i<count;i++){const t=i/sr,fade=Math.min(1,t/1.2,(duration-t)/3);pcm.writeInt16LE(Math.round(Math.tanh(left[i]*scale)*fade*32767),i*4);pcm.writeInt16LE(Math.round(Math.tanh(right[i]*scale)*fade*32767),i*4+2);}
const h=Buffer.alloc(44);h.write('RIFF');h.writeUInt32LE(36+pcm.length,4);h.write('WAVEfmt ',8);h.writeUInt32LE(16,16);h.writeUInt16LE(1,20);h.writeUInt16LE(2,22);h.writeUInt32LE(sr,24);h.writeUInt32LE(sr*4,28);h.writeUInt16LE(4,32);h.writeUInt16LE(16,34);h.write('data',36);h.writeUInt32LE(pcm.length,40);
fs.mkdirSync(path.dirname(path.resolve(out)),{recursive:true});fs.writeFileSync(out,Buffer.concat([h,pcm]));
fs.writeFileSync(out+'.json',JSON.stringify({type:'original synthesized instrumental',duration,bpm,dip,seed:option('seed',17),sampleRate:sr,channels:2,borrowedSamples:false,description:'Layered soft keys, chord pads, arpeggio, bass, percussion and a quieter reveal section.'},null,2)+'\n');
console.log(out);
