import React from 'react';
import {Composition,registerRoot} from 'remotion';
import Film from './Film';
import {FORMATS,validate,duration} from './model.mjs';
registerRoot(()=> <Composition id="Film" component={Film} width={1920} height={1080} fps={30} durationInFrames={540} calculateMetadata={({props})=>{const b=validate(props),[width,height]=FORMATS[b.format];return {width,height,durationInFrames:duration(b)*30};}}/>);
