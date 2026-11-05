import React from 'react';import {Composition,registerRoot} from 'remotion';
import {Film} from './Film.jsx';import {FORMATS,duration,validate} from './model.mjs';
const defaults={mode:'handoff',format:'landscape',brand:'RELAY',headline:'Keep your idea moving.',ending:'Pick up where you left off.',cta:'Find your flow',url:'relay.example',item:'The next good idea',chapters:['Capture a thought.','Make room for detail.','Bring it to the room.'],accent:'#a3f969',subject:'notes',concept:true};
registerRoot(()=> <Composition id="Film" component={Film} defaultProps={defaults} width={1920} height={1080} fps={30} durationInFrames={720} calculateMetadata={({props})=>{validate(props);const [width,height]=FORMATS[props.format];return{width,height,durationInFrames:duration(props)*30};}}/>);
