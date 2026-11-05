import fs from 'node:fs';
const [output,mode,seconds]=process.argv.slice(2),duration=Number(seconds),sr=44100,n=Math.ceil(duration*sr),channels=[new Float32Array(n),new Float32Array(n)];
const tone=(at,len,freq,vol,pan=0,type='bell')=>{for(let j=0;j<len*sr&&Math.floor(at*sr)+j<n;j++){let t=j/sr,k=Math.floor(at*sr)+j,env=Math.min(1,t/.012)*Math.exp(-t*(type==='bell'?5:2)/len)*Math.min(1,(len-t)/.03),v=type==='bell'?Math.sin(t*freq*2*Math.PI)+.26*Math.sin(t*freq*4*Math.PI)*Math.exp(-t*7):Math.sin(t*freq*2*Math.PI);channels[0][k]+=v*env*vol*(1-pan*.4);channels[1][k]+=v*env*vol*(1+pan*.4);}};
let seed=42;const rand=()=>{seed=(seed*1664525+1013904223)>>>0;return seed/4294967296*2-1;};
const noise=(at,len,vol,rising=false)=>{let smooth=0;for(let j=0;j<len*sr&&Math.floor(at*sr)+j<n;j++){const t=j/sr,k=Math.floor(at*sr)+j,p=t/len;smooth=.91*smooth+.09*rand();const v=smooth*vol*Math.sin(Math.PI*p)*(rising?.2+p:1);channels[0][k]+=v;channels[1][k]+=v*.94;}};
if(mode==='paper'){
 const notes=[261.63,329.63,392,523.25,440,392,329.63,293.66];
 for(let beat=0;beat<duration/.375;beat++){let at=beat*.375; if(beat%3!==2)tone(at,.55,notes[(beat+Math.floor(beat/12))%notes.length],.105,Math.sin(beat)*.6);if(beat%6===0)tone(at,1.4,[130.81,146.83,174.61,130.81][Math.floor(beat/12)%4],.11,0,'round');if(beat%3===0)noise(at,.05,.12);}
 for(const at of [4,9,13,17,22])noise(at-.15,.45,.2);
 noise(9,3.5,.08);tone(17,.9,523.25,.15,-.4);tone(17.2,1.2,659.25,.12,.4);tone(22,1.8,783.99,.1);
}else{
 for(let k=0;k<duration*sr;k++){const t=k/sr,fade=Math.min(1,t/2,(duration-t)/1.2),pulse=t<11?.6+.4*Math.sin(t*Math.PI*4):1; const v=(Math.sin(t*55*2*Math.PI)*.08+Math.sin(t*82.4*2*Math.PI)*.045)*fade*pulse;channels[0][k]+=v;channels[1][k]+=v;}
 for(let t=0;t<22;t+=.5){tone(t,.16,110,.06,0,'round');if(t%2===0)tone(t,.7,220+(t%4)*55,.045,.4);}
 for(let t of [8,9,10])tone(t,.24,880,.1);noise(10.4,3.8,.9,true);noise(13,5,.45);for(let t of [4,18,22]){tone(t,1.6,55,.2,0,'round');noise(t,.7,.35);}
 for(let i=0;i<5;i++)tone(18+i*.3,2,[261.63,329.63,392,523.25,659.25][i],.07,(i-2)/3);
}
let peak=0;for(let c of channels)for(let x of c)peak=Math.max(peak,Math.abs(x));const gain=.78/Math.max(.78,peak),pcm=Buffer.alloc(n*4);
for(let i=0;i<n;i++){const fade=Math.min(1,(duration-i/sr)/.5);for(let c=0;c<2;c++)pcm.writeInt16LE(Math.round(Math.max(-1,Math.min(1,channels[c][i]*gain*fade))*32767),i*4+c*2);}
const header=Buffer.alloc(44);header.write('RIFF');header.writeUInt32LE(36+pcm.length,4);header.write('WAVEfmt ',8);header.writeUInt32LE(16,16);header.writeUInt16LE(1,20);header.writeUInt16LE(2,22);header.writeUInt32LE(sr,24);header.writeUInt32LE(sr*4,28);header.writeUInt16LE(4,32);header.writeUInt16LE(16,34);header.write('data',36);header.writeUInt32LE(pcm.length,40);fs.writeFileSync(output,Buffer.concat([header,pcm]));fs.writeFileSync(output+'.json',JSON.stringify({mode,duration,original:true,externalSamples:false,peak:peak*gain,character:mode==='paper'?'Plucked storybook melody, wood ticks, page swishes and gentle rain':'Low pulsing drone, countdown tones, synthesized ignition and deployment chord'},null,2));
