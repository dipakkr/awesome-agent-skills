export const FORMATS={landscape:[1920,1080],portrait:[1080,1920],square:[1080,1080]};
export const TIMELINES={brush:[['uncover',3],['title',3],['postcard',4],['signature',4]],pixel:[['boot',3],['command',4],['build',5],['gallery',4],['ship',4]]};
export const duration=b=>TIMELINES[b.mode].reduce((n,s)=>n+s[1],0);
export function validate(b){
 if(!b||!TIMELINES[b.mode]||!FORMATS[b.format])throw Error('Choose brush/pixel and landscape/portrait/square');
 for(const [k,n] of Object.entries({brand:16,headline:32,ending:34,cta:25,url:32}))if(typeof b[k]!=='string'||!b[k].trim()||b[k].length>n)throw Error(`${k}: 1–${n} characters required`);
 if(!Array.isArray(b.chapters)||b.chapters.length!==3||b.chapters.some(s=>typeof s!=='string'||s.length>30||!s.trim()))throw Error('Three chapters, 1–30 characters each');
 if(!/^#[0-9a-f]{6}$/i.test(b.accent))throw Error('Use a six-digit hex accent');
 if(b.mode==='brush'&&(!/^[a-z0-9][a-z0-9._-]*\.(png|jpg|jpeg|webp)$/i.test(b.image)||!['horizontal','diagonal'].includes(b.stroke)))throw Error('Use a local public image basename and horizontal/diagonal stroke');
 if(b.mode==='pixel'&&(!['site','release'].includes(b.subject)||!Array.isArray(b.files)||b.files.length!==3||b.files.some(s=>!/^[-a-z0-9.]{1,20}$/.test(s))))throw Error('Pixel needs site/release and three simple file names');
 if(b.mode==='pixel'&&!/^[a-z .]+$/i.test(b.brand))throw Error('Bitmap brand supports letters, spaces and periods');
 if(b.concept!==true)throw Error('These examples illustrate fictional concepts, not operational proof');return b;
}
