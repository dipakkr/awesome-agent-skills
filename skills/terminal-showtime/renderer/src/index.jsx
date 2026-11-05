import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film.jsx';
import {FORMATS,duration,validate} from './model.mjs';
const defaults={mode:'pixel',format:'landscape',brand:'BYTE',headline:'Make something small.',ending:'Your next project starts here.',cta:'Start making',url:'byte.example',chapters:['Start with an idea.','Give it a structure.','See it come together.'],accent:'#ffd37a',subject:'site',files:['index.html','style.css','app.js'],concept:true};
registerRoot(()=> <Composition id="Film" component={Film} defaultProps={defaults} width={1920} height={1080} fps={30} durationInFrames={600} calculateMetadata={({props})=>{validate(props);const [width,height]=FORMATS[props.format];return{width,height,durationInFrames:duration(props)*30};}}/>);
