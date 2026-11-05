import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film.jsx';
import {FORMATS,duration,validate} from './model.mjs';
const defaults={mode:'cinematic',format:'landscape',brand:'VECTOR',category:'A new creative workspace',hook:'Less friction.\nMore possibility.',promise:'Make room\nfor the good work.',cta:'Build your next idea',url:'vector.example',task:'Organize the next product launch',words:['Imagine','Connect','Create'],steps:['Collect ideas','Connect the dots','Make it happen'],projects:['Identity','Digital','Motion'],theme:'black',accent:'#d7ff3f',motif:'rings',seed:17,concept:true};
registerRoot(()=> <Composition id="Film" component={Film} defaultProps={defaults} width={1920} height={1080} fps={30} durationInFrames={960} calculateMetadata={({props})=>{validate(props);const [width,height]=FORMATS[props.format];return {width,height,durationInFrames:duration(props)*30};}}/>);
