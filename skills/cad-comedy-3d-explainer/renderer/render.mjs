import {bundle} from '@remotion/bundler';
import {renderMedia,renderStill,selectComposition} from '@remotion/renderer';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {execFileSync} from 'node:child_process';

const root=path.dirname(fileURLToPath(import.meta.url));
const out=path.resolve(process.argv[2]||'');
if(!process.argv[2])throw new Error('Usage: node render.mjs /path/to/prepared-output [--stills]');
const stills=process.argv.includes('--stills');
const props=JSON.parse(await fs.readFile(path.join(out,'timeline.json'),'utf8'));
const film=path.join(out,'film.mp4');
if(!stills){try{await fs.access(film);throw new Error('film.mp4 exists. Use a new output directory.');}catch(e){if(e.code!=='ENOENT')throw e;}}
const serveUrl=await bundle({entryPoint:path.join(root,'src/index.jsx'),publicDir:path.join(root,'public')});
const chromiumOptions={gl:'angle',enableMultiProcessOnLinux:true};
const composition=await selectComposition({serveUrl,id:'Lesson',inputProps:props,chromiumOptions});
const frames=[0.7,...props.turns.map(t=>t.start+Math.min(t.duration*.5,1.5)),props.duration-1];
await fs.mkdir(path.join(out,'review'),{recursive:true});
for(let i=0;i<frames.length;i++){
  await renderStill({serveUrl,composition,inputProps:props,output:path.join(out,'review',`${String(i).padStart(2,'0')}.png`),frame:Math.floor(frames[i]*30),chromiumOptions});
}
const posterIndex=1;
await fs.copyFile(path.join(out,'review',`${String(posterIndex).padStart(2,'0')}.png`),path.join(out,'poster.png'));
if(stills){console.log('Review stills ready');process.exit(0);}
let last=-1;
const silent=path.join(out,'picture.mp4');
await renderMedia({serveUrl,composition,inputProps:props,codec:'h264',outputLocation:silent,concurrency:3,crf:19,chromiumOptions,onProgress:({progress})=>{const p=Math.floor(progress*10);if(p!==last){console.log(`${props.id}: picture ${p*10}%`);last=p;}}});
execFileSync('ffmpeg',['-v','error','-y','-i',silent,'-i',path.join(out,'voice.wav'),'-c:v','copy','-c:a','aac','-b:a','160k','-movflags','+faststart','-shortest',film]);
execFileSync('ffmpeg',['-v','error','-i',film,'-f','null','-']);
const hash=b=>createHash('sha256').update(b).digest('hex');
const files={};
for(const name of ['film.mp4','poster.png','brief.json','timeline.json','voice.wav','captions.srt','captions.json']){const bytes=await fs.readFile(path.join(out,name));files[name]={sha256:hash(bytes),bytes:bytes.length};}
const meta=JSON.parse(execFileSync('ffprobe',['-v','error','-show_streams','-show_format','-of','json',film],{encoding:'utf8'}));
await fs.writeFile(path.join(out,'render-report.json'),JSON.stringify({skill:'cad-comedy-3d-explainer',id:props.id,decode:'pass',duration:Number(meta.format.duration),width:composition.width,height:composition.height,fps:30,frames:composition.durationInFrames,sourceSha256:hash(await fs.readFile(path.join(root,'src/Film.jsx'))),files,audio:meta.streams.find(s=>s.codec_type==='audio')?.codec_name,voiceProviders:props.providers,verification:'Author-executed local render; not independent customer validation'},null,2)+'\n');
await fs.writeFile(path.join(out,'preview.html'),`<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Comedy 3D Explainer</title><style>body{background:#172425;color:#fff;font:16px system-ui;margin:30px}video{display:block;max-height:86vh;max-width:100%;margin:auto}p{text-align:center}</style><video controls playsinline src="film.mp4" poster="poster.png"></video><p>Original characters. AI-generated voices. <a href="captions.srt">Captions</a></p>`);
await fs.unlink(silent);console.log(`Complete: ${film}`);
