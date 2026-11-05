#!/usr/bin/env python3
"""Validate a dialogue brief, synthesize each turn, and derive its actual timeline.
No secrets are written to outputs. TTS failures never silently change providers.
"""
import argparse, array, hashlib, json, math, os, re, shutil, subprocess, sys, urllib.request, urllib.error, urllib.parse, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def run(args):
    return subprocess.run(args, check=True, capture_output=True).stdout
def validate(b):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', b.get('id', '')): raise ValueError('id must be a lowercase slug')
    for key, limit in [('title', 34), ('subtitle', 48), ('takeaway', 76)]:
        if not isinstance(b.get(key), str) or not 1 <= len(b[key]) <= limit: raise ValueError(f'{key}: 1–{limit} characters')
    if b.get('theme') not in ['mint', 'peach', 'violet', 'night']: raise ValueError('Unknown theme')
    if not 8 <= len(b.get('turns', [])) <= 20: raise ValueError('Use 8–20 dialogue turns')
    if not 1 <= len(b.get('boards', [])) <= 8: raise ValueError('Use 1–8 board states')
    for board in b['boards']:
        if len(board.get('heading', '')) > 30 or not board.get('heading'): raise ValueError('Board heading: 1–30 characters')
        if len(board.get('note', '')) > 56: raise ValueError('Board note: max 56 characters')
        if not 1 <= len(board.get('nodes', [])) <= 3: raise ValueError('Board needs 1–3 nodes')
        for n in board['nodes']:
            if not n.get('label') or len(n['label']) > 16: raise ValueError('Node label: 1–16 characters')
            if n.get('icon') not in ['book','shelf','bell','shop','phone','gate','ticket','worker','tray','clock','database','lightning']: raise ValueError('Unknown diagram icon')
        if board.get('kind', 'flow') not in ['flow','cycle','queue']: raise ValueError('Unknown diagram kind')
    for t in b['turns']:
        if t.get('speaker') not in ['student', 'tutor']: raise ValueError('Unknown speaker')
        if not isinstance(t.get('text'), str) or not 1 <= len(t['text']) <= 108: raise ValueError('Each turn must contain 1–108 characters; split long turns')
        if not isinstance(t.get('board'), int) or not 0 <= t['board'] < len(b['boards']): raise ValueError('Invalid board state')
        if t.get('shot') not in ['wide', 'student', 'tutor', 'board']: raise ValueError('Unknown shot')
    if sum(len(t['text'].split()) for t in b['turns']) > 180: raise ValueError('Keep the lesson under 180 words')
    return b

def load_env(path):
    # Values are used only in memory, never printed or copied into the package.
    if path:
        for line in Path(path).read_text().splitlines():
            m = re.match(r'^\s*(?:export\s+)?([A-Z][A-Z0-9_]*)\s*=\s*(.*?)\s*$', line)
            if m:
                value=m[2]
                if value[:1] in ['"', "'"] and value[-1:] == value[:1]: value=value[1:-1]
                os.environ.setdefault(m[1], value)

def speech(text, speaker, provider, target):
    instructions = ('Young adult, curious and quick, natural conversational delivery. ' if speaker=='student' else 'Warm friendly tutor, relaxed and playful, concise conversational delivery. ') + 'Clear English. Say only the supplied words. No music or extra sounds.'
    if provider == 'openai':
        key=os.environ.get('OPENAI_API_KEY')
        voice=os.environ.get('OPENAI_'+speaker.upper()+'_VOICE', 'marin' if speaker=='student' else 'cedar')
        model=os.environ.get('OPENAI_TTS_MODEL','gpt-4o-mini-tts')
        url='https://api.openai.com/v1/audio/speech'
        headers={'Authorization':'Bearer '+(key or ''),'Content-Type':'application/json'}
        payload=dict(model=model,voice=voice,input=text,response_format='wav',instructions=instructions,speed=1.04)
    elif provider == 'elevenlabs':
        key=os.environ.get('ELEVENLABS_API_KEY')
        voice=os.environ.get('ELEVENLABS_'+speaker.upper()+'_VOICE_ID')
        if not voice: raise ValueError('Set both ELEVENLABS_STUDENT_VOICE_ID and ELEVENLABS_TUTOR_VOICE_ID')
        url='https://api.elevenlabs.io/v1/text-to-speech/'+urllib.parse.quote(voice,safe='')+'?output_format=mp3_44100_128'
        headers={'xi-api-key':key or '', 'Content-Type':'application/json'}
        model=os.environ.get('ELEVENLABS_MODEL','eleven_multilingual_v2')
        payload=dict(text=text,model_id=model,voice_settings=dict(stability=.45,similarity_boost=.75))
    else:
        key=os.environ.get('FISH_AUDIO_API_KEY')
        voice=os.environ.get('FISH_'+speaker.upper()+'_REFERENCE_ID')
        if not voice: raise ValueError('Set both FISH_STUDENT_REFERENCE_ID and FISH_TUTOR_REFERENCE_ID')
        url='https://api.fish.audio/v1/tts'
        model=os.environ.get('FISH_MODEL','s2.1-pro-free')
        headers={'Authorization':'Bearer '+(key or ''),'Content-Type':'application/json','model':model}
        payload=dict(text=text,reference_id=voice,format='mp3',sample_rate=44100,mp3_bitrate=128)
    if not key: raise ValueError(f'Missing {provider} API key; see references/audio-setup.md')
    req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers=headers,method='POST')
    try:
        with urllib.request.urlopen(req,timeout=180) as response: data=response.read()
    except urllib.error.HTTPError as e:
        # Only safe provider error fields; never expose headers or key-bearing requests.
        raise RuntimeError(f'{provider} returned HTTP {e.code}; check account access, billing and voice/model IDs') from None
    raw=target.with_suffix('.raw')
    raw.write_bytes(data)
    run(['ffmpeg','-v','error','-y','-i',str(raw),'-ar','24000','-ac','1','-af','silenceremove=start_periods=1:start_duration=0.025:start_threshold=-48dB',str(target)])
    raw.unlink()
    return dict(provider=provider,model=model,voice=voice,synthetic=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('brief',type=Path);p.add_argument('--out',required=True,type=Path)
    p.add_argument('--provider',choices=['openai','elevenlabs','fish','recorded'],default='openai')
    p.add_argument('--env-file',type=Path);p.add_argument('--audio-dir',type=Path)
    p.add_argument('--validate-only',action='store_true');p.add_argument('--resume',action='store_true')
    a=p.parse_args();b=validate(json.loads(a.brief.read_text()))
    if a.validate_only: print('Brief valid');return
    load_env(a.env_file)
    out=a.out.resolve()
    if out.exists() and any(out.iterdir()) and not a.resume: raise ValueError('Output exists. Use a fresh directory or --resume for identical inputs.')
    out.mkdir(parents=True,exist_ok=True);(out/'audio').mkdir(exist_ok=True)
    digest=hashlib.sha256(a.brief.read_bytes()).hexdigest()
    state=out/'prepare-state.json'
    if state.exists() and json.loads(state.read_text()) != dict(briefSha256=digest,provider=a.provider): raise ValueError('Resume requires the same brief and provider')
    state.write_text(json.dumps(dict(briefSha256=digest,provider=a.provider)))
    shutil.copy2(a.brief,out/'brief.json')
    cursor=0.35;turns=[];combined=array.array('h',[0]*round(cursor*24000));subtitles=[];providers=[]
    for i,t in enumerate(b['turns']):
        wav=out/'audio'/f'{i:02}.wav';receipt=wav.with_suffix('.json')
        if not wav.exists():
            if a.provider=='recorded':
                if not a.audio_dir: raise ValueError('--audio-dir is required for recorded audio')
                source=a.audio_dir/f'{i:02}.wav'
                run(['ffmpeg','-v','error','-y','-i',str(source),'-ar','24000','-ac','1',str(wav)])
                meta=dict(provider='recorded',synthetic=None,sourceFile=source.name)
            else: meta=speech(t['text'],t['speaker'],a.provider,wav)
            receipt.write_text(json.dumps(meta,indent=2))
        if not receipt.exists(): raise ValueError('Audio receipt missing. Remove incomplete WAV then resume.')
        providers.append(json.loads(receipt.read_text()))
        with wave.open(str(wav)) as w:
            samples=array.array('h',w.readframes(w.getnframes()))
        duration=len(samples)/24000
        if not .2 < duration < 18: raise ValueError(f'Unexpected audio duration at turn {i}; review the source')
        energy=[]
        for k in range(0,len(samples),800):
            chunk=samples[k:k+800];rms=math.sqrt(sum(s*s for s in chunk)/max(1,len(chunk)))/32768
            energy.append(round(min(1,rms*9),3))
        turns.append(dict(**t,start=round(cursor,4),duration=round(duration,4),energy=energy))
        def stamp(n):
            ms=round(n*1000);return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
        subtitles.append(f'{i+1}\n{stamp(cursor)} --> {stamp(cursor+duration)}\n{t["text"]}\n')
        combined.extend(samples);pause=round(.16*24000);combined.extend([0]*pause);cursor+=(len(samples)+pause)/24000
        print(f'{b["id"]}: voice turn {i+1}/{len(b["turns"])} ready ({duration:.1f}s)',flush=True)
    combined.extend([0]*round(2.4*24000))
    with wave.open(str(out/'narration.wav'),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(24000);w.writeframes(combined.tobytes())
    run(['ffmpeg','-v','error','-y','-i',str(out/'narration.wav'),'-af','loudnorm=I=-16:TP=-1.5:LRA=9','-ar','48000',str(out/'voice.wav')])
    disclosure='Original characters · '+('Supplied narration' if a.provider=='recorded' else 'AI-generated voices')
    timeline={**b,**dict(turns=turns,duration=round(len(combined)/24000,4),fps=30,width=720,height=1280,disclosure=disclosure,providers=providers,briefSha256=digest)}
    (out/'timeline.json').write_text(json.dumps(timeline,indent=2)+'\n')
    (out/'captions.srt').write_text('\n'.join(subtitles))
    print(f'Ready: {out} ({timeline["duration"]:.1f}s)')
if __name__=='__main__':
    try: main()
    except (ValueError,RuntimeError) as e: sys.exit(str(e))
