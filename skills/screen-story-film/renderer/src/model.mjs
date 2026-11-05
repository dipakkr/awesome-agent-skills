export const FORMATS={landscape:[1920,1080],portrait:[1080,1920],square:[1080,1080]};
export const TIMELINES={
 cinematic:[['signal',4],['hook',3],['reveal',4],['interface',5],['orbit',4],['flow',5],['resolve',3],['end',4]],
 demo:[['demoHook',3],['input',5],['organize',5],['focus',5],['ready',4],['end',4]],
 promo:[['punch',3],['relay',3],['ribbons',4],['tiles',4],['manifesto',3],['end',3]],
 portfolio:[['folioOpen',3],['projectA',5],['projectB',5],['projectC',5],['wall',4],['folioIndex',3],['end',3]],
};
export const duration=b=>TIMELINES[b.mode].reduce((a,s)=>a+s[1],0);
export function validate(b){
 if(!Object.hasOwn(TIMELINES,b.mode)||!Object.hasOwn(FORMATS,b.format))throw Error('Unknown mode or aspect ratio');
 for(const [key,max] of Object.entries({brand:16,category:30,hook:42,promise:42,cta:28,url:32,task:60}))if(typeof b[key]!=='string'||!b[key].trim()||b[key].length>max)throw Error(`${key}: require 1..${max} characters`);
 if(!/^#[0-9a-f]{6}$/i.test(b.accent)||!['black','white'].includes(b.theme))throw Error('Use a black/white stage and a six-digit accent');
 const rgb=[1,3,5].map(i=>parseInt(b.accent.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);const luminance=rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;
 if((luminance+.05)/.05<4.5)throw Error('Accent must support readable black text (contrast >=4.5)');
 for(const key of ['words','steps','projects'])if(!Array.isArray(b[key])||b[key].length!==3||b[key].some(x=>typeof x!=='string'||!x.trim()||x.length>20))throw Error(`${key}: exactly three labels, max 20 characters`);
 if(!['rings','ribbons','grid'].includes(b.motif))throw Error('Unknown graphic motif');
 if(!Number.isInteger(b.seed)||b.seed<0)throw Error('seed must be a nonnegative integer');
 if(typeof b.concept!=='boolean')throw Error('Declare whether the brief is fictional');
 if(b.images&&(!Array.isArray(b.images)||b.images.length!==3||b.images.some(s=>!s||s.startsWith('/')||s.includes('..')||s.includes('://'))))throw Error('images must be three relative public asset paths');
 return b;
}
export function sceneAt(b,time){let start=0;for(const [name,seconds] of TIMELINES[b.mode]){if(time<start+seconds)return {name,seconds,time:time-start,start};start+=seconds;}return {name:'end',seconds:4,time:4,start:start-4};}
