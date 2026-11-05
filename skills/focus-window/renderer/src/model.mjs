export const FORMATS={landscape:[1920,1080],square:[1080,1080]};
export const MODES=['spotlight'];
export const TIMELINES=Object.fromEntries(MODES.map(m=>[m,[['opening',4.5],['action',4.5],['resolution',4.5],['signature',4.5]]]));
export const duration=()=>18;
export function validate(b){
 if(!b||!MODES.includes(b.mode)||!FORMATS[b.format])throw Error('Supported mode and landscape/square format required');
 for(const [k,n] of Object.entries({brand:18,headline:42,ending:42,cta:24,item:26,source:65}))if(typeof b[k]!=='string'||!b[k].trim()||b[k].length>n)throw Error(`${k}: 1-${n} characters required`);
 for(const k of ['labels','details'])if(!Array.isArray(b[k])||b[k].length!==3||b[k].some(x=>typeof x!=='string'||!x.trim()||x.length>(k==='labels'?20:38)))throw Error(`${k}: three short strings required`);
 if(!/^#[0-9a-f]{6}$/i.test(b.accent)||!/^#[0-9a-f]{6}$/i.test(b.ink))throw Error('Six-digit accent and ink required');
 if(typeof b.concept!=='boolean'||!['fictional','real'].includes(b.brandKind))throw Error('Declare concept and brandKind');
 if(b.brandKind==='real'){
  if(!b.brandAudit||!/^https:\/\//.test(b.brandAudit.sourceUrl||'')||!Array.isArray(b.brandAudit.colors)||![b.accent,b.ink].every(c=>b.brandAudit.colors.map(x=>x.toLowerCase()).includes(c.toLowerCase())))throw Error('Real product requires website palette evidence');
 }
 if(b.concept!==true)throw Error('Built-in scenes are illustrative. Use concept:true or adapt source to verified captures.');
 if(![0,1].includes(b.variant))throw Error('variant 0 or 1 required');
 if(b.mode==='results'&&(!Number.isFinite(b.before)||!Number.isFinite(b.after)||b.before<=0||b.after<0||b.after>=b.before||b.before>1000))throw Error('Results requires 0 <= after < before <= 1000');
 if(b.logo!==undefined&&!/^[a-z0-9][a-z0-9._-]*\.(svg|png|webp)$/i.test(b.logo))throw Error('logo must be a local public image basename');
 return b;
}
