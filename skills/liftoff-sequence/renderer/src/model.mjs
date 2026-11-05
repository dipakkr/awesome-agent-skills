export const FORMATS={landscape:[1920,1080],portrait:[1080,1920],square:[1080,1080]};
export const TIMELINES={paper:[['spark',4],['journey',5],['weather',4],['arrival',4],['change',5],['close',4]],rocket:[['blueprint',4],['assembly',4],['countdown',3],['ignition',3],['flight',4],['orbit',4],['close',3]]};
export const duration=b=>TIMELINES[b.mode].reduce((n,s)=>n+s[1],0);
export function validate(b){
 if(!b||!TIMELINES[b.mode]||!FORMATS[b.format])throw Error('Choose paper/rocket and landscape/portrait/square');
 for(const [k,n] of Object.entries({brand:20,headline:42,ending:45,cta:30,url:32}))if(typeof b[k]!=='string'||!b[k].trim()||b[k].length>n)throw Error(`${k}: 1–${n} characters required`);
 if(!Array.isArray(b.chapters)||b.chapters.length!==4||b.chapters.some(s=>typeof s!=='string'||s.length>38||!s.trim()))throw Error('Four chapters, 1–38 characters each');
 if(!/^#[0-9a-f]{6}$/i.test(b.accent))throw Error('Use a six-digit hex accent');
 if(b.mode==='paper'&&!['seed','letter'].includes(b.subject))throw Error('Paper subject: seed or letter');
 if(b.mode==='rocket'&&!['capsule','satellite'].includes(b.subject))throw Error('Rocket payload: capsule or satellite');
 if(b.concept!==true)throw Error('Bundled animated examples are fictional concepts, not operational product proof');
 return b;
}
