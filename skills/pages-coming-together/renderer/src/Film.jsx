import React from 'react';
import {staticFile} from 'remotion';
import Scene from './Documents';
export default function Film(b){return <><style>{`@font-face{font-family:DM;src:url('${staticFile('DM-Sans.ttf')}')}@font-face{font-family:Serif;src:url('${staticFile('DM-Serif.ttf')}')}*{box-sizing:border-box}`}</style><Scene {...b}/></>}
