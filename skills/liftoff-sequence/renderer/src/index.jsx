import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film.jsx';
import {FORMATS,duration,validate} from './model.mjs';
const defaults={mode:'paper',format:'landscape',brand:'TENDER',headline:'Big things start small.',ending:'Make room for something good.',cta:'Plant your first idea',url:'tender.example',chapters:['Take the first step.','Keep going, gently.','Find your place.','Watch what happens.'],accent:'#f05b32',subject:'seed',concept:true};
registerRoot(()=> <Composition id="Film" component={Film} defaultProps={defaults} width={1920} height={1080} fps={30} durationInFrames={780} calculateMetadata={({props})=>{validate(props);const [width,height]=FORMATS[props.format];return{width,height,durationInFrames:duration(props)*30};}}/>);
