import {bundle} from '@remotion/bundler';
import {selectComposition,renderStill,renderMedia} from '@remotion/renderer';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';
import {validate,TIMELINES} from './src/model.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const [input,output,...options]=process.argv.slice(2);
if(!input||!output)throw Error('node render.mjs brief.json NEW_OUTPUT_DIR [--stills]');
const out=path.resolve(output),b=validate(JSON.parse(await fs.readFile(input))),stills=options.includes('--stills');
await fs.mkdir(out,{recursive:true});
try{await fs.access(path.join(out,'film.mp4'));throw Error('Film exists. Use a new versioned output directory.');}catch(e){if(e.code!=='ENOENT')throw e;}
const hash=bytes=>createHash('sha256').update(bytes).digest('hex'),sources={};
for(const f of ['src/Film.jsx','src/Handoff.jsx','src/Collage.jsx','public/DM-Serif.ttf','src/model.mjs','src/index.jsx','render.mjs','public/DM-Sans.ttf','package.json','package-lock.json',...(b.mode==='collage'?['public/'+b.image]:[]),...(b.screens||[]).map(x=>'public/'+x)])sources[f]=hash(await fs.readFile(path.join(root,f)));
await fs.writeFile(path.join(out,'brief.json'),JSON.stringify(b,null,2)+'\n');
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.jsx'),publicDir:path.join(root,'public')});
const composition=await selectComposition({serveUrl,id:'Film',inputProps:b});
const samples=[];let at=0;const posterIndex=b.mode==='collage'?0:4;
for(const [scene,seconds] of TIMELINES[b.mode]){samples.push({scene,time:at+Math.min(1.8,seconds*.6)});at+=seconds;}
await fs.mkdir(path.join(out,'review'),{recursive:true});
for(let i=0;i<samples.length;i++)await renderStill({serveUrl,composition,inputProps:b,frame:Math.round(samples[i].time*30),output:path.join(out,'review',`${String(i).padStart(2,'0')}-${samples[i].scene}.png`)});
await fs.copyFile(path.join(out,'review',`${String(posterIndex).padStart(2,'0')}-${samples[posterIndex].scene}.png`),path.join(out,'poster.png'));
await fs.writeFile(path.join(out,'storyboard.json'),JSON.stringify(samples,null,2)+'\n');
if(stills){console.log('Stills ready: '+out);process.exit(0);}
let last=-1;
if(!options.includes('--reuse-picture'))await renderMedia({serveUrl,composition,inputProps:b,codec:'h264',outputLocation:path.join(out,'picture.mp4'),crf:18,concurrency:4,onProgress:({progress})=>{const n=Math.floor(progress*4);if(n!==last){console.log(`${b.mode}/${b.brand}/${b.format} ${n*25}%`);last=n;}}});
const opt=k=>options.includes(k)?options[options.indexOf(k)+1]:null;
const music=opt('--music'),creditFile=opt('--credit'),start=Number(opt('--music-start')||0);
const film=path.join(out,'film.mp4');
let musicInfo=null;
if(music){
 if(!creditFile||!Number.isFinite(start)||start<0)throw Error('Music needs --credit and nonnegative --music-start');
 const credit=await fs.readFile(creditFile,'utf8');if(!credit.trim())throw Error('Empty music credit');
 const wav=path.join(out,'working.wav');
 execFileSync('ffmpeg',['-v','error','-y','-ss',String(start),'-i',music,'-t',String(at),'-af',`afade=t=in:d=0.12,afade=t=out:st=${at-1.25}:d=1.25`,'-ar','48000',wav]);
 // FFmpeg writes loudness measurements to stderr.
 const {spawnSync}=await import('node:child_process');
 const probeMix=spawnSync('ffmpeg',['-hide_banner','-i',wav,'-af','loudnorm=I=-16:TP=-1.5:LRA=8:print_format=json','-f','null','-'],{encoding:'utf8'});if(probeMix.status!==0)throw Error(probeMix.stderr);
 const text=probeMix.stderr,m=JSON.parse(text.slice(text.lastIndexOf('{'),text.lastIndexOf('}')+1));
 if(!Number.isFinite(Number(m.input_i)))throw Error('Music excerpt is silent or empty; choose a valid start');
 const filter=`loudnorm=I=-16:TP=-1.5:LRA=8:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}:linear=true`;
 execFileSync('ffmpeg',['-v','error','-i',path.join(out,'picture.mp4'),'-i',wav,'-map','0:v:0','-map','1:a:0','-c:v','copy','-af',filter,'-ar','48000','-c:a','aac','-b:a','256k','-t',String(at),'-metadata','comment='+credit,'-movflags','+faststart',film]);
 musicInfo={sourceSha256:hash(await fs.readFile(music)),start,credit};await fs.writeFile(path.join(out,'MUSIC-CREDITS.txt'),credit);await fs.unlink(wav);
}else await fs.copyFile(path.join(out,'picture.mp4'),film);
execFileSync('ffmpeg',['-v','error','-i',film,'-f','null','-']);
const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',film],{encoding:'utf8'}));
const v=probe.streams.find(s=>s.codec_type==='video'),a=probe.streams.find(s=>s.codec_type==='audio');
if(v.width!==composition.width||v.height!==composition.height||Number(v.nb_frames)!==composition.durationInFrames||(music&&!a)||Math.abs(Number(probe.format.duration)-at)>.1)throw Error('Encoded geometry, duration, frames or soundtrack mismatch');
// Review samples are extracted from the actual encoded delivery, not source-only stills.
for(let i=0;i<samples.length;i++)execFileSync('ffmpeg',['-v','error','-y','-ss',String(samples[i].time),'-i',film,'-frames:v','1',path.join(out,'review',`${String(i).padStart(2,'0')}-${samples[i].scene}.png`)]);
await fs.copyFile(path.join(out,'review',`${String(posterIndex).padStart(2,'0')}-${samples[posterIndex].scene}.png`),path.join(out,'poster.png'));
const files={};for(const f of ['film.mp4','poster.png','brief.json','storyboard.json',...(music?['MUSIC-CREDITS.txt']:[])]){const bytes=await fs.readFile(path.join(out,f));files[f]={sha256:hash(bytes),bytes:bytes.length};}
await fs.writeFile(path.join(out,'render-report.json'),JSON.stringify({version:1,decode:'pass',format:b.format,width:v.width,height:v.height,frames:Number(v.nb_frames),fps:v.r_frame_rate,duration:Number(probe.format.duration),audio:a?.codec_name||null,music:musicInfo,sources,files,review:'Encoded scene samples prepared; visual acceptance recorded separately.',concept:b.concept},null,2)+'\n');
await fs.writeFile(path.join(out,'preview.html'),`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>${b.mode} film</title><style>body{background:#080808;color:white;font:16px system-ui;margin:24px}video{display:block;max-height:86vh;max-width:100%;margin:auto}p{text-align:center}</style><video controls playsinline src="film.mp4" poster="poster.png"></video><p>Original concept film · editable source included · see MUSIC-CREDITS.txt when sound is supplied</p>`);
await fs.unlink(path.join(out,'picture.mp4'));console.log('Complete: '+out);
