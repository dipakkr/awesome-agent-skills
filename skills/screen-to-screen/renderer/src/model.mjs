export const FORMATS={landscape:[1920,1080],portrait:[1080,1920],square:[1080,1080]};
export const TIMELINES={handoff:[['capture',4],['transfer',4],['develop',4],['present',4],['connected',4],['signature',4]],collage:[['cover',4],['specimen',4],['contact-sheet',4],['cut-and-paste',4],['signature',4]]};
export const duration=b=>TIMELINES[b.mode].reduce((n,s)=>n+s[1],0);
export function validate(b){
 if(!b||!TIMELINES[b.mode]||!FORMATS[b.format])throw Error('Choose handoff/collage and landscape/portrait/square');
 for(const [k,n] of Object.entries({brand:16,headline:34,ending:34,cta:25,url:32,item:22}))if(typeof b[k]!=='string'||!b[k].trim()||b[k].length>n)throw Error(`${k}: 1-${n} characters required`);
 if(!Array.isArray(b.chapters)||b.chapters.length!==3||b.chapters.some(s=>typeof s!=='string'||s.length>26||!s.trim()))throw Error('Three chapters, 1-26 characters');
 if(b.theme!==undefined&&!['light','dark'].includes(b.theme))throw Error('Theme must be light or dark');
 if(!/^#[0-9a-f]{6}$/i.test(b.accent))throw Error('Six-digit accent required');
 if(!['notes','design','audio','sport'].includes(b.subject))throw Error('Unsupported subject');
 if(b.mode==='collage'&&!/^[a-z0-9][a-z0-9._-]*\.(png|webp|jpg|jpeg)$/i.test(b.image))throw Error('Local public image basename required');
 if(b.screens&&(!Array.isArray(b.screens)||b.screens.length!==3||b.screens.some(s=>!/^[a-z0-9][a-z0-9._-]*\.(png|webp|jpg|jpeg)$/i.test(s))))throw Error('Three local screen images required');
 if(typeof b.concept!=='boolean')throw Error('Declare whether this is a fictional concept');
 if(!b.concept&&!b.screens&&b.mode==='handoff')throw Error('Real product demonstrations need supplied captures');
 return b;
}
