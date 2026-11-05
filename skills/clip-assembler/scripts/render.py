#!/usr/bin/env python3
"""Assemble approved local ad artwork/clips into a review MP4 and optional GIF.
Python 3.10+, ffmpeg and ffprobe. No network calls or generation dependencies.
"""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


def run(args):
    result = subprocess.run(args, capture_output=True, text=True, check=False)
    if result.returncode:
        raise ValueError(f'{Path(args[0]).name} failed: {result.stderr[-1600:]}')
    return result.stdout


def probe(path):
    return json.loads(run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def number(value, label, low, high):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f'{label} must be a finite number between {low} and {high}')
    return value


def local_file(base, value, suffixes):
    if not isinstance(value, str) or not value or '://' in value:
        raise ValueError('Input must be a local file path')
    path = (base / value).resolve()
    if not path.is_file() or path.suffix.lower() not in suffixes:
        raise ValueError(f'Unsupported or missing input: {value}')
    return path


def render(manifest, out, gif=False):
    for tool in ('ffmpeg', 'ffprobe'):
        if not shutil.which(tool):
            raise ValueError(f'{tool} is required on PATH')
    data = json.loads(manifest.read_text())
    width = number(data.get('width', 1080), 'width', 320, 2160)
    height = number(data.get('height', 1920), 'height', 320, 3840)
    if any(not isinstance(v, int) or v % 2 for v in (width, height)):
        raise ValueError('Dimensions must be even integers')
    background = data.get('background', '#101010')
    if not isinstance(background, str) or not re.fullmatch(r'#[0-9a-fA-F]{6}', background):
        raise ValueError('background must be a six-digit hex colour')
    shots = data.get('shots')
    if not isinstance(shots, list) or not 1 <= len(shots) <= 12:
        raise ValueError('Provide 1 to 12 shots')
    prepared = []
    for shot in shots:
        if not isinstance(shot, dict):
            raise ValueError('Each shot must be an object')
        duration = number(shot.get('duration'), 'shot duration', 1, 30)
        path = local_file(manifest.parent, shot.get('file'), {'.png', '.jpg', '.jpeg', '.webp', '.mp4', '.mov'})
        still = path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp'}
        info = probe(path)
        stream = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
        if stream is None:
            raise ValueError(f'No decodable visual stream in {path.name}')
        start = number(shot.get('start', 0), 'shot start', 0, 86400)
        if still and start:
            raise ValueError('Image shots cannot specify a nonzero start')
        if not still and start + duration > float(info['format'].get('duration', 0)) + .04:
            raise ValueError(f'Shot exceeds available footage: {path.name}')
        prepared.append(dict(path=path, duration=duration, still=still, start=start, sha256=digest(path)))
    total = sum(s['duration'] for s in prepared)
    if total > 120:
        raise ValueError('This short-ad exporter supports at most 120 seconds')
    audio = None
    if data.get('audio'):
        audio = local_file(manifest.parent, data['audio'], {'.wav', '.mp3', '.m4a', '.aac', '.flac'})
        audio_info = probe(audio)
        if not any(s['codec_type'] == 'audio' for s in audio_info['streams']):
            raise ValueError('Soundtrack has no audio stream')
        if float(audio_info['format'].get('duration', 0)) + .04 < total:
            raise ValueError('Soundtrack must cover the full ad; provide an intentional edit rather than an automatic loop')
    if out.exists():
        raise ValueError('Output directory exists; choose a new version to preserve previous outputs')
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.ad-render-', dir=out.parent) as temp:
        work = Path(temp)
        clips = []
        for i, shot in enumerate(prepared):
            clip = work / f'shot-{i:02}.mp4'
            args = ['ffmpeg', '-v', 'error', '-y']
            args += ['-loop', '1', '-framerate', '30'] if shot['still'] else ['-ss', str(shot['start'])]
            args += ['-i', str(shot['path']), '-t', str(shot['duration'])]
            vf = (f'scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2,'
                  f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x{background[1:]},setsar=1,fps=30,'
                  f'fade=t=in:st=0:d=0.2,fade=t=out:st={shot["duration"]-.2}:d=0.2,format=yuv420p')
            args += ['-vf', vf, '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '18', '-threads', '2', str(clip)]
            run(args)
            clips.append(clip)
        concat = work / 'clips.txt'
        concat.write_text(''.join(f"file '{p.name}'\n" for p in clips))
        assembled = work / 'assembled.mp4'
        run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '1', '-i', str(concat), '-c', 'copy', str(assembled)])
        deliver = work / 'deliver'
        deliver.mkdir()
        target = deliver / 'ad.mp4'
        args = ['ffmpeg', '-v', 'error', '-y', '-i', str(assembled)]
        if audio:
            args += ['-i', str(audio), '-map', '0:v:0', '-map', '1:a:0', '-c:a', 'aac', '-b:a', '192k', '-t', str(total)]
        else:
            args += ['-an']
        run(args + ['-c:v', 'copy', '-movflags', '+faststart', str(target)])
        if gif:
            run(['ffmpeg', '-v', 'error', '-y', '-i', str(target), '-filter_complex',
                 '[0:v]fps=12,scale=480:-2:flags=lanczos,split[a][b];[a]palettegen[p];[b][p]paletteuse',
                 '-loop', '0', str(deliver / 'preview.gif')])
        measured = probe(target)
        stream = next(s for s in measured['streams'] if s['codec_type'] == 'video')
        if (stream['width'], stream['height']) != (width, height) or abs(float(measured['format']['duration']) - total) > .15:
            raise ValueError('Export dimensions or duration failed verification')
        # Decode every output, not only the container headers.
        for path in deliver.iterdir():
            run(['ffmpeg', '-v', 'error', '-i', str(path), '-f', 'null', '-'])
        report = dict(kind='image-based animatic' if all(s['still'] for s in prepared) else 'assembled footage review master',
                      platform_approval='not evaluated', destination_review='pending', width=width, height=height,
                      duration=float(measured['format']['duration']), fps=stream['avg_frame_rate'], codec=stream['codec_name'],
                      audio=bool(audio), source_clip_audio='discarded; only an explicit soundtrack is included',
                      inputs=[dict(file=str(s['path']), sha256=s['sha256'], duration=s['duration'], start=s['start']) for s in prepared],
                      soundtrack=dict(file=str(audio), sha256=digest(audio)) if audio else None,
                      files={p.name:dict(bytes=p.stat().st_size,sha256=digest(p)) for p in deliver.iterdir()})
        (deliver / 'render-report.json').write_text(json.dumps(report, indent=2)+'\n')
        shutil.copyfile(manifest, deliver / 'render-input.json')
        deliver.rename(out)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--gif', action='store_true')
    args = parser.parse_args()
    try:
        report = render(args.manifest.resolve(), args.out.resolve(), args.gif)
        print(json.dumps(dict(output=str(args.out.resolve()), kind=report['kind'], duration=report['duration'], audio=report['audio'])))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(1, f'Cannot render: {exc}\n')
