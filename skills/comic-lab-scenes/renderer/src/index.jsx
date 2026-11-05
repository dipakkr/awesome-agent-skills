import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Film} from './Film';
const Root=()=> <Composition id="Lesson" component={Film} width={720} height={1280} fps={30} durationInFrames={1800} defaultProps={{turns:[],boards:[],duration:60,theme:'citrus',title:'Your lesson',subtitle:'ONE IDEA. A BETTER EXPLANATION.'}} calculateMetadata={({props})=>({durationInFrames:Math.ceil(props.duration*30)})}/>;
registerRoot(Root);
