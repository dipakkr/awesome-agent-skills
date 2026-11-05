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
for(const f of ['src/Film.jsx','src/Brush.jsx','src/Pixel.jsx','public/DM-Serif.ttf','src/model.mjs','src/index.jsx','render.mjs','compose-score.mjs','public/DM-Sans.ttf','package.json','package-lock.json',...(b.mode==='brush'?['public/'+b.image]:[])])sources[f]=hash(await fs.readFile(path.join(root,f)));
await fs.writeFile(path.join(out,'brief.json'),JSON.stringify(b,null,2)+'\n');
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.jsx'),publicDir:path.join(root,'public')});
const composition=await selectComposition({serveUrl,id:'Film',inputProps:b});
const samples=[];let at=0;const posterIndex=b.mode==='brush'?1:2;
for(const [scene,seconds] of TIMELINES[b.mode]){samples.push({scene,time:at+Math.min(1.8,seconds*.6)});at+=seconds;}
await fs.mkdir(path.join(out,'review'),{recursive:true});
for(let i=0;i<samples.length;i++)await renderStill({serveUrl,composition,inputProps:b,frame:Math.round(samples[i].time*30),output:path.join(out,'review',`${String(i).padStart(2,'0')}-${samples[i].scene}.png`)});
await fs.copyFile(path.join(out,'review',`${String(posterIndex).padStart(2,'0')}-${samples[posterIndex].scene}.png`),path.join(out,'poster.png'));
await fs.writeFile(path.join(out,'storyboard.json'),JSON.stringify(samples,null,2)+'\n');
if(stills){console.log('Stills ready: '+out);process.exit(0);}
let last=-1;
await renderMedia({serveUrl,composition,inputProps:b,codec:'h264',outputLocation:path.join(out,'picture.mp4'),crf:18,concurrency:4,onProgress:({progress})=>{const n=Math.floor(progress*4);if(n!==last){console.log(`${b.mode}/${b.brand}/${b.format} ${n*25}%`);last=n;}}});
const wav=path.join(out,'score.wav');
try{await fs.access(wav);}catch{execFileSync(process.execPath,[path.join(root,'compose-score.mjs'),wav,b.mode,String(at),b.brand]);}
const film=path.join(out,'film.mp4');
execFileSync('ffmpeg',['-v','error','-y','-i',path.join(out,'picture.mp4'),'-i',wav,'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','192k','-t',String(at),'-movflags','+faststart',film]);
execFileSync('ffmpeg',['-v','error','-i',film,'-f','null','-']);
const probe=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',film],{encoding:'utf8'}));
const v=probe.streams.find(s=>s.codec_type==='video'),a=probe.streams.find(s=>s.codec_type==='audio');
if(v.width!==composition.width||v.height!==composition.height||Number(v.nb_frames)!==composition.durationInFrames||!a||Math.abs(Number(probe.format.duration)-at)>.1)throw Error('Encoded geometry, duration, frames or soundtrack mismatch');
// Review samples are extracted from the actual encoded delivery, not source-only stills.
for(let i=0;i<samples.length;i++)execFileSync('ffmpeg',['-v','error','-y','-ss',String(samples[i].time),'-i',film,'-frames:v','1',path.join(out,'review',`${String(i).padStart(2,'0')}-${samples[i].scene}.png`)]);
await fs.copyFile(path.join(out,'review',`${String(posterIndex).padStart(2,'0')}-${samples[posterIndex].scene}.png`),path.join(out,'poster.png'));
const files={};for(const f of ['film.mp4','poster.png','brief.json','storyboard.json','score.wav','score.wav.json']){const bytes=await fs.readFile(path.join(out,f));files[f]={sha256:hash(bytes),bytes:bytes.length};}
await fs.writeFile(path.join(out,'render-report.json'),JSON.stringify({version:1,decode:'pass',format:b.format,width:v.width,height:v.height,frames:Number(v.nb_frames),fps:v.r_frame_rate,duration:Number(probe.format.duration),audio:a.codec_name,sources,files,review:'Encoded scene samples prepared; visual acceptance recorded separately.',concept:b.concept},null,2)+'\n');
await fs.writeFile(path.join(out,'preview.html'),`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>${b.mode} film</title><style>body{background:#080808;color:white;font:16px system-ui;margin:24px}video{display:block;max-height:86vh;max-width:100%;margin:auto}p{text-align:center}</style><video controls playsinline src="film.mp4" poster="poster.png"></video><p>Original concept film · synthesized instrumental · editable source included</p>`);
await fs.unlink(path.join(out,'picture.mp4'));console.log('Complete: '+out);
