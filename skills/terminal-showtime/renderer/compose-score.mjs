import fs from 'node:fs';
import path from 'node:path';
import {execFileSync,spawnSync} from 'node:child_process';
const [output,mode,seconds,variant='']=process.argv.slice(2),duration=Number(seconds);
if(!output||!['brush','pixel'].includes(mode)||!Number.isFinite(duration)||duration<4||duration>120)throw Error('Usage: node compose-score.mjs output.wav brush|pixel seconds [brand]');
if(fs.existsSync(output))throw Error('Score exists. Use a new output path.');
const sr=48000,N=Math.round(duration*sr),music=[new Float64Array(N),new Float64Array(N)],fx=[new Float64Array(N),new Float64Array(N)],send=[new Float64Array(N),new Float64Array(N)];
let seed=271828;for(const c of variant)seed=(seed*31+c.charCodeAt(0))>>>0;
const random=()=>{seed=(1664525*seed+1013904223)>>>0;return seed/4294967296;};
const hz=m=>440*2**((m-69)/12),clip=(x,a=0,b=1)=>Math.max(a,Math.min(b,x));
const events=[];
function note(at,len,midi,amp,kind='keys',pan=0,wet=.2){
 const f=hz(midi),start=Math.round(at*sr),left=Math.sqrt((1-pan)/2),right=Math.sqrt((1+pan)/2),phase=random()*6.28;
 for(let j=0;j<len*sr&&start+j<N;j++){
  const t=j/sr,k=start+j;if(k<0)continue;const q=t/len,attack=kind==='pad'?.35:.008,release=kind==='pad'?.6:.13;
  let env=Math.min(1,t/attack)*Math.min(1,(len-t)/release),v=0;
  if(kind==='pad'){env*=.75+.25*Math.sin(Math.PI*q);v=(Math.sin(2*Math.PI*f*t)+.32*Math.sin(2*Math.PI*f*1.002*t+phase)+.17*Math.sin(2*Math.PI*2*f*t))*.6;}
  else if(kind==='bass'){env*=Math.exp(-t*2/len);v=Math.sin(2*Math.PI*f*t)+.25*Math.sin(2*Math.PI*2*f*t)+.08*Math.sin(2*Math.PI*3*f*t);}
  else if(kind==='keys'){env*=Math.exp(-t*3.8/len);v=Math.sin(2*Math.PI*f*t+.9*Math.exp(-t*6)*Math.sin(2*Math.PI*f*t))+.2*Math.sin(2*Math.PI*2*f*t)*Math.exp(-t*5);}
  else {env*=Math.exp(-t*2.5/len);for(let h=1;h<=7;h+=2)v+=Math.sin(2*Math.PI*f*h*t)*((h%4===1?1:-1)/(h*h));}
  v*=env*amp;music[0][k]+=v*left;music[1][k]+=v*right;send[0][k]+=v*left*wet;send[1][k]+=v*right*wet;
 }
}
function noise(at,len,amp,kind='swish',pan=0){const start=Math.round(at*sr);let low=0,last=0;for(let j=0;j<len*sr&&start+j<N;j++){const k=start+j;if(k<0)continue;const t=j/sr,q=t/len,r=random()*2-1;low=.92*low+.08*r;const high=r-low;let v,env;if(kind==='swish'){env=Math.sin(Math.PI*q)**2;v=low*.9+high*.07;}else if(kind==='hat'){env=Math.exp(-t*65);v=high*.25;}else if(kind==='snare'){env=Math.exp(-t*22);v=high*.3+Math.sin(t*2*Math.PI*185)*.13;}else{env=Math.exp(-t*180);v=(r-last)*.2;}last=r;v*=env*amp;fx[0][k]+=v*Math.sqrt((1-pan)/2);fx[1][k]+=v*Math.sqrt((1+pan)/2);}}
function kick(at,amp=.25){const start=Math.round(at*sr);let phase=0;for(let j=0;j<sr*.4&&start+j<N;j++){const t=j/sr,k=start+j;phase+=2*Math.PI*(48+95*Math.exp(-t*42))/sr;const v=Math.sin(phase)*Math.exp(-t*13)*Math.min(1,t/.003)*amp;music[0][k]+=v*.707;music[1][k]+=v*.707;}}
function chord(at,len,notes,amp=.075){notes.forEach((m,i)=>note(at+i*.012,len,m,amp,'pad',(i/(notes.length-1)-.5)*1.2,.38));}
function cue(at,label){events.push({time:at,label});}
if(mode==='brush'){
 const shift=variant==='COMMON'?3:0,roots=[38,35,31,33,38];
 const chords=[[62,66,69,73,76],[59,62,66,69],[55,59,62,66,69],[57,61,64,71],[62,66,69,73,76]],starts=[0,3,6,9,10.5];
 starts.forEach((at,i)=>{let len=i===4?duration-at:Math.min(3.5,duration-at);chord(at,len,chords[i].map(x=>x+shift),i===4?.07:.055);note(at,Math.min(2.5,len),roots[i]+shift,.16,'bass',0,.04);});
 const melody=[[.35,74,1.1],[1.15,73,.8],[2,69,1],[3.2,66,1],[4.15,69,1.2],[5.25,73,.8],[6.25,71,1.2],[7.2,69,1],[8.25,66,.9],[9.35,64,.7],[10.55,66,.7],[11.2,69,.7],[11.95,74,1.65]];
 melody.forEach(([at,m,len],i)=>note(at,len,m+shift,.12,'keys',Math.sin(i)*.32,.4));
 for(let at=3;at<9;at+=.75){noise(at,.12,.12,'hat',.35);if(Math.round(at/.75)%2===0)kick(at,.13);if(Math.round(at/.75)%4===2)noise(at,.18,.1,'snare',-.2);}
 for(const at of [.15,5.3,9.3,10.05]){noise(at,.65,.55,'swish',at<6?-.25:.25);cue(at,'soft bristle sweep');}
 noise(6,.08,.23,'tap',-.3);cue(6,'postcard landing');cue(10.5,'resolved brand chord');
}else{
 const shift=variant==='PATCH'?3:0,seq=[[52,55,59,62],[48,52,55,59],[55,59,62,66],[50,54,57,64]];
 for(let bar=0;bar<8;bar++){const at=bar*2,notes=seq[bar%4].map(x=>x+shift);chord(at,2.45,notes.map(x=>x+12),.045);for(let beat=0;beat<4;beat++){const t=at+beat*.5;if(t<3||t>=7){kick(t,beat%2===0?.22:.1);if(beat%2)noise(t,.19,.36,'snare',-.12);}note(t,.38,notes[0]-12,.17,'bass',0,.02);if(t>=3)noise(t+.25,.07,.12,'hat',beat%2?.45:-.45);}
  const offsets=bar%2?[0,.75,1.25]:[.25,1,1.5];offsets.forEach((o,i)=>note(at+o,.42,notes[(i+bar)%4]+24,.09,'chip',i%2?.22:-.22,.25));
 }
 // The final four seconds become a short sonic signature, leaving room for the CTA.
 chord(16,3.8,[52,55,59,62,66].map(x=>x+12+shift),.055);note(16,2.8,40+shift,.15,'bass');
 [[16,76],[16.3,79],[16.65,83],[17.2,86]].forEach(([at,m])=>note(at,1.4,m+shift,.09,'keys',.15,.45));
 for(let at=3.2;at<4.5;at+=.09)noise(at,.035,.16,'tap',(random()-.5)*.4);
 for(const at of [7,7.65,8.3]){note(at,.24,76+shift,.08,'keys',-.1,.12);note(at+.09,.3,83+shift,.06,'keys',.1,.12);cue(at,'file assembly tick');}
 for(const at of [2.75,6.75,11.7,15.7]){noise(at,.45,.35,'swish');cue(at,'scene handoff');}
 cue(3.2,'typing begins');cue(16,'four-note completion signature');
}
// Short stereo reflections plus a diffuse tail; effects stay centered and dry.
const delays=[.043,.079,.113,.173,.257,.359,.467];
for(let c=0;c<2;c++)for(let d=0;d<delays.length;d++){const samples=Math.round((delays[d]+c*.009)*sr),gain=.28*Math.exp(-d*.34);let lp=0;for(let k=samples;k<N;k++){lp=.64*lp+.36*send[(c+d)%2][k-samples];music[c][k]+=lp*gain;}}
const mixed=[new Float64Array(N),new Float64Array(N)];let peak=0;
for(let i=0;i<N;i++){const t=i/sr,fade=Math.min(1,t/.025,Math.max(0,(duration-t)/.85));for(let c=0;c<2;c++){const v=(music[c][i]+fx[c][i])*fade;mixed[c][i]=v;peak=Math.max(peak,Math.abs(v));}}
const gain=.82/Math.max(.82,peak),pcm=Buffer.alloc(N*4);for(let i=0;i<N;i++)for(let c=0;c<2;c++)pcm.writeInt16LE(Math.round(clip(mixed[c][i]*gain,-1,1)*32767),i*4+c*2);
const h=Buffer.alloc(44);h.write('RIFF');h.writeUInt32LE(36+pcm.length,4);h.write('WAVEfmt ',8);h.writeUInt32LE(16,16);h.writeUInt16LE(1,20);h.writeUInt16LE(2,22);h.writeUInt32LE(sr,24);h.writeUInt32LE(sr*4,28);h.writeUInt16LE(4,32);h.writeUInt16LE(16,34);h.write('data',36);h.writeUInt32LE(pcm.length,40);
fs.mkdirSync(path.dirname(path.resolve(output)),{recursive:true});const raw=output+'.mix.wav';fs.writeFileSync(raw,Buffer.concat([h,pcm]));
const base='highpass=f=35,lowpass=f=14500',target='loudnorm=I=-16:TP=-1.5:LRA=8';
const measure=spawnSync('ffmpeg',['-hide_banner','-i',raw,'-af',base+','+target+':print_format=json','-f','null','-'],{encoding:'utf8'});if(measure.status!==0)throw Error(measure.stderr);
const stats=JSON.parse(measure.stderr.slice(measure.stderr.lastIndexOf('{'),measure.stderr.lastIndexOf('}')+1));
const filter=base+','+target+`:measured_I=${stats.input_i}:measured_TP=${stats.input_tp}:measured_LRA=${stats.input_lra}:measured_thresh=${stats.input_thresh}:offset=${stats.target_offset}:linear=true`;
execFileSync('ffmpeg',['-v','error','-i',raw,'-af',filter,'-ar',String(sr),'-c:a','pcm_s16le',output]);fs.unlinkSync(raw);
fs.writeFileSync(output+'.json',JSON.stringify({version:2,mode,variant,duration,sampleRate:sr,original:true,externalSamples:false,targetLUFS:-16,truePeakCeilingDBTP:-1.5,preMaster:stats,events,character:mode==='brush'?'Warm electric keys, extended chords, restrained percussion, stereo ambience and paint-synchronized swishes':'Warm electronic groove, soft chip melody, rounded bass, restrained drums, task effects and a four-note ending'},null,2)+'\n');
console.log(`Composed ${mode}/${variant}: ${duration}s with ${events.length} timed cues`);
