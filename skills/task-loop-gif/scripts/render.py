#!/usr/bin/env python3
"""Render original, input-driven workflow GIFs. No network calls."""
import argparse
from functools import lru_cache
import hashlib
import html
import json
import math
from pathlib import Path
import shutil
import subprocess
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parents[1]
THEMES = {
    'midnight': ['#111218', '#1b1d26', '#292c39', '#f7f5f0', '#a6a9b6', '#ff795c', '#13151b'],
    'paper': ['#f4f0e8', '#fffdf9', '#ded9cf', '#252c39', '#68707d', '#b8442f', '#ffffff'],
    'forest': ['#102b29', '#193b37', '#31534b', '#f4f3df', '#afc4b6', '#dbef8c', '#18302c'],
    'plum': ['#261b36', '#352747', '#544064', '#fff5f0', '#c0accb', '#f7b0c5', '#2a1e38'],
}


@lru_cache(maxsize=40)
def font(size, serif=False):
    return ImageFont.truetype(str(HERE / 'assets/fonts' / ('DM-Serif.ttf' if serif else 'DM-Sans.ttf')), size)


def validate(b):
    for key, limit in [('brand', 28), ('eyebrow', 32), ('subtitle', 100), ('panel_title', 36), ('cta', 36), ('alt', 220), ('disclosure', 70)]:
        if not isinstance(b.get(key), str) or not b[key].strip() or len(b[key]) > limit or any(ord(c) < 32 for c in b[key]):
            raise ValueError(f'{key}: needs nonempty single-line text, at most {limit} characters')
    if not isinstance(b.get('headline'), list) or len(b['headline']) != 2:
        raise ValueError('headline needs exactly two lines')
    for line in b['headline']:
        if not isinstance(line, str) or not 1 <= len(line) <= 28 or any(ord(c) < 32 for c in line):
            raise ValueError('Each headline line needs 1–28 printable characters')
    if not isinstance(b.get('beats'), list) or not 3 <= len(b['beats']) <= 5:
        raise ValueError('Use 3–5 workflow beats')
    for beat in b['beats']:
        for key in ['request', 'result']:
            value = beat.get(key) if isinstance(beat, dict) else None
            if not isinstance(value, str) or not 1 <= len(value) <= 78 or any(ord(c) < 32 for c in value):
                raise ValueError(f'Beat {key} needs 1–78 printable characters')
    if not isinstance(b.get('chips'), list) or not 2 <= len(b['chips']) <= 4 or any(not isinstance(c, str) or not 1 <= len(c) <= 24 or any(ord(x) < 32 for x in c) for c in b['chips']):
        raise ValueError('Use 2–4 short capability chips')
    b = dict(b)
    for key, default in [('theme', 'midnight'), ('duration', 12), ('width', 720), ('fps', 24), ('cta_url', '')]:
        b.setdefault(key, default)
    if b['theme'] not in THEMES:
        raise ValueError('Unknown theme')
    if type(b['width']) is not int or not 640 <= b['width'] <= 1080 or b['width'] % 2:
        raise ValueError('Width must be an even integer from 640 to 1080')
    if type(b['duration']) not in [int, float] or not math.isfinite(b['duration']) or not 8 <= b['duration'] <= 24:
        raise ValueError('Duration must be 8–24 seconds')
    if type(b['fps']) is not int or not 10 <= b['fps'] <= 30:
        raise ValueError('fps must be an integer from 10 to 30')
    u = urlparse(b['cta_url'])
    if b['cta_url'] and (u.scheme != 'https' or not u.netloc or u.username or u.password):
        raise ValueError('cta_url must be an HTTPS URL without credentials')
    return b


def wrap(text, size, width, max_lines=1, serif=False):
    f = font(size, serif)
    lines = ['']
    for word in text.split():
        candidate = (lines[-1] + ' ' + word).strip()
        if f.getlength(candidate) <= width:
            lines[-1] = candidate
        elif lines[-1]:
            lines.append(word)
        else:
            raise ValueError(f'Text does not fit: {text}')
    if len(lines) > max_lines or any(f.getlength(line) > width for line in lines):
        raise ValueError(f'Text does not fit {width}px/{max_lines} lines: {text}')
    return lines


def label(draw, text, x, y, size, color, width, max_lines=1, serif=False, line_height=None):
    lines = wrap(text, size, width, max_lines, serif)
    for i, line in enumerate(lines):
        draw.text((x, y + i * (line_height or size * 1.22)), line, font=font(size, serif), fill=color, anchor='lt')
    return len(lines)


def compose(b, t, complete=False):
    bg, panel, line, ink, muted, accent, button_ink = THEMES[b['theme']]
    im = Image.new('RGB', (720, 900), bg)
    d = ImageDraw.Draw(im)
    # Quiet static framing keeps GIF changes confined to the workflow panel.
    brandw = font(14).getlength(b['brand']) + 46
    d.rounded_rectangle((28, 25, 28 + brandw, 57), 16, fill=panel, outline=line)
    d.ellipse((39, 36, 49, 46), fill=accent)
    label(d, b['brand'], 58, 34, 14, ink, 230)
    label(d, b['eyebrow'].upper(), 414, 36, 11, muted, 278)
    label(d, b['headline'][0], 28, 78, 65, ink, 664, serif=True)
    label(d, b['headline'][1], 28, 144, 65, accent, 664, serif=True)
    label(d, b['subtitle'], 30, 225, 18, muted, 652, 2, line_height=24)
    d.rounded_rectangle((28, 286, 692, 704), 20, fill=panel, outline=line, width=1)
    for k in range(3):
        d.ellipse((47+k*14, 305, 53+k*14, 311), fill=line)
    label(d, b['panel_title'].upper(), 103, 301, 12, muted, 520)
    d.line((29, 330, 691, 330), fill=line)
    n = len(b['beats'])
    beat_duration = (b['duration'] - 2.4) / n
    row_height = 332 / n
    complete_count = 0
    for i, beat in enumerate(b['beats']):
        local = 2 if complete else (t - i*beat_duration) / beat_duration
        if local < 0:
            continue
        y = 348 + i * row_height
        request_lines = wrap(beat['request'], 17, 557, 2)
        h = 15 + len(request_lines)*20
        d.rounded_rectangle((48, y, 670, y+h), 9, fill=bg)
        # A numbered request is readable in the very first frame.
        label(d, f'{i+1:02}', 59, y+11, 11, muted, 25)
        label(d, beat['request'], 94, y+8, 17, ink, 557, 2, line_height=20)
        result_y = y+h+7
        if result_y+17 > y+row_height-2:
            raise ValueError('Beat is too dense. Shorten the request or use fewer beats.')
        wrap(beat['result'], 14, 566)
        if local >= .48:
            complete_count += 1
            d.ellipse((54, result_y+1, 68, result_y+15), fill=accent)
            d.line([(58, result_y+8), (61, result_y+11), (65, result_y+5)], fill=button_ink, width=2)
            label(d, beat['result'], 79, result_y, 14, muted, 566)
        else:
            # Progress moves smoothly, but content doesn't flash or scroll away.
            d.rounded_rectangle((79, result_y+5, 220, result_y+9), 2, fill=line)
            d.rounded_rectangle((79, result_y+5, 80+139*max(0, min(1, local/.48)), result_y+9), 2, fill=accent)
    d.line((48, 689, 672, 689), fill=line, width=2)
    if complete_count:
        d.line((48, 689, 48+624*complete_count/n, 689), fill=accent, width=2)
    label(d, 'BUILT AROUND YOUR WORKFLOW', 29, 723, 11, muted, 664)
    x = 28
    for chip in b['chips']:
        w = font(13).getlength(chip) + 28
        if x+w > 692:
            raise ValueError('Capability chips exceed the row. Shorten their copy.')
        d.rounded_rectangle((x, 747, x+w, 782), 17, outline=line, fill=panel)
        label(d, chip, x+14, 757, 13, muted, w-26)
        x += w+8
    d.rounded_rectangle((28, 807, 692, 865), 15, fill=accent)
    wrap(b['cta'], 23, 590)
    text_width = font(23).getlength(b['cta'])
    label(d, b['cta'], (720-text_width)/2-12, 825, 23, button_ink, 590)
    d.line([(652, 829), (659, 836), (652, 843)], fill=button_ink, width=2)
    label(d, b['disclosure'], 29, 880, 10, muted, 664)
    return im


def run(args):
    subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def render(b, out):
    if out.exists():
        raise ValueError('Output directory exists; choose a new version directory')
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        raise ValueError('FFmpeg and FFprobe must be on PATH')
    # Validate the entire final layout before writing any output.
    compose(b, b['duration'], complete=True)
    width = b['width']; height = round(width*1.25/2)*2
    out.mkdir(parents=True)
    (out/'brief.json').write_text(json.dumps(b, indent=2, ensure_ascii=False)+'\n')
    frames = round(b['duration']*b['fps'])
    command = ['ffmpeg','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{width}x{height}','-r',str(b['fps']),'-i','-','-an','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out/'workflow.mp4')]
    with (out/'encoder.log').open('wb') as log:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=log)
        try:
            for frame in range(frames):
                im = compose(b, frame/b['fps'])
                if im.size != (width,height):
                    im = im.resize((width,height), Image.Resampling.LANCZOS)
                process.stdin.write(im.tobytes())
            process.stdin.close()
            if process.wait() != 0:
                raise RuntimeError('Video encoding failed; see encoder.log')
        except BaseException:
            process.kill(); process.wait(); raise
    for name, size in [('workflow.gif',width), ('email.gif',600)]:
        filters=f'fps=10,scale={size}:-2:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle'
        run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(out/'workflow.mp4'),'-filter_complex',filters,'-loop','0',str(out/name)])
    compose(b,0).resize((width,height),Image.Resampling.LANCZOS).save(out/'first-frame.png')
    compose(b,b['duration'],True).resize((width,height),Image.Resampling.LANCZOS).save(out/'poster.png')
    for name, t in [('start',0),('middle',b['duration']/2),('end',b['duration']-.1)]:
        compose(b,t).save(out/f'review-{name}.png')
    esc = lambda value: html.escape(value, quote=True)
    anchor_start = f'<a href="{esc(b["cta_url"])}">' if b['cta_url'] else ''
    anchor_end = '</a>' if b['cta_url'] else ''
    email = f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(b["brand"])} workflow</title><body><table role="presentation" width="100%"><tr><td align="center">{anchor_start}<img src="email.gif" width="600" height="750" alt="{esc(b["alt"])}" style="display:block;width:100%;max-width:600px;height:auto;border:0">{anchor_end}<p style="font:16px/1.5 Arial,sans-serif">{esc(b["subtitle"])}</p><p style="font:16px/1.5 Arial,sans-serif">{anchor_start}{esc(b["cta"])}{anchor_end}</p></td></tr></table></body></html>'
    (out/'email.html').write_text(email)
    preview = f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(b["brand"])} workflow preview</title><style>body{{margin:0;background:#17181d;color:#fff;font:15px system-ui}}main{{max-width:600px;margin:28px auto;padding:0 16px}}video{{display:block;width:100%;border-radius:18px}}nav{{display:flex;gap:18px;padding:18px 0;flex-wrap:wrap}}a{{color:#f2bfac}}</style><main><video controls muted loop playsinline poster="poster.png" aria-label="{esc(b["alt"])}"><source src="workflow.mp4" type="video/mp4"></video><nav><a href="workflow.gif" download>GIF</a><a href="email.gif" download>Email GIF</a><a href="workflow.mp4" download>MP4</a><a href="poster.png" download>Static poster</a></nav><p>{esc(b["disclosure"])}</p></main><script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches)document.querySelector("video").play().catch(()=>{{}})</script></html>'
    (out/'preview.html').write_text(preview)
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out/'workflow.mp4')]))
    run(['ffmpeg','-v','error','-i',str(out/'workflow.mp4'),'-f','null','-'])
    gif_info={}
    for name in ['workflow.gif','email.gif']:
        with Image.open(out/name) as gif:
            duration=0
            for i in range(gif.n_frames):
                gif.seek(i); gif.load(); duration+=gif.info.get('duration',0)
            gif_info[name]={'frames':gif.n_frames,'width':gif.width,'height':gif.height,'durationSeconds':duration/1000,'loop':gif.info.get('loop')}
    files={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in out.iterdir() if p.is_file()}
    report={'renderer':'task-loop-gif 1.0','layoutPassed':True,'width':width,'height':height,'durationSeconds':float(probe['format']['duration']),'fps':b['fps'],'silent':True,'gif':gif_info,'emailTargetBytes':1000000,'emailTargetMet':files['email.gif']['bytes']<=1000000,'files':files}
    (out/'render-report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('brief',type=Path)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    try:
        report=render(validate(json.loads(args.brief.read_text())),args.out)
        print(json.dumps({'output':str(args.out),'emailBytes':report['files']['email.gif']['bytes'],'emailTargetMet':report['emailTargetMet']}))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1,f'{error}\n')
