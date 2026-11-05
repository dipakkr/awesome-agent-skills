---
name: share-of-circle
description: Animate a three-part percentage breakdown as a segmented ring with an explicit total, legend and source. Use for shares of one whole, not unrelated metrics.
---

# Share Of Circle

Create a fresh motion piece from the user's content. The examples demonstrate the technique; they are not titles, brands or claims to repeat in a new job. Keep exact names, numbers and approved wording. Ask only for missing facts that affect the result. A requested demo can use clearly labelled fictional material.

## Edition 2 quality standard

Compose the final frame before animating. Use a clear focal point, generous type scale and enough space around secondary copy. Sequence one idea at a time with eased motion; avoid abrupt card appearance. Keep at least a two-second readable end hold, except continuous loops. Render typography directly at Full HD, not by enlarging a low-resolution video.

## Design the motion

Draw each share around one circular ring, with an adjacent legend and exact final percentage. Keep stable segment colors and an explicit 100 percent total. Use this only when the categories partition one whole; do not convert unrelated values into a misleading pie.

Use the included visual system as a starting point, then adapt composition and pacing to the brief when needed. Change the actual story, labels, data and call to action together; swapping colors alone does not make a new example. Do not promise unsupported formats or capabilities.

## Prepare and render

Read [input fields and boundaries](references/inputs.md). Review [the four recorded examples](references/examples.md) for concrete input patterns. Write a fresh JSON brief. The bundled renderer is self-contained and uses local files only.

Requirements: Python 3.10+, Pillow, FFmpeg and FFprobe with libx264. Licensed fonts are bundled. No API key or paid generation service is needed. Use the user's existing environment; install missing dependencies through their normal package workflow. For Pillow, `python3 -m pip install Pillow` is sufficient in a suitable Python environment.

```sh
python3 <installed-skill>/scripts/render.py brief.json --out output/review-01 --stills-only
python3 <installed-skill>/scripts/render.py brief.json --out output/final-01
```

Use a new output directory for each run. The script rejects overwrite, invalid data and text that does not fit. It measures every timeline frame before encoding. It renders 1920×1080, 30fps, 10 seconds, silent. The four provided palettes are chalk, ink, rose and cobalt. Custom colors, other aspect ratios, durations, soundtrack and extra content require deliberate source changes and a fresh validation pass.

## Inspect the actual result

Inspect all five review frames and the final playback in `preview.html`. Check the full entrance and exit, reading holds, text fit, source notes, the user's exact content and any supplied logo. For data, compare final numbers against the input. For lower thirds, inspect the transparent WebM on both bright and dark footage. For seamless patterns, review the wrap from the final frame into the first. Decode and geometry checks do not establish visual quality.

Deliver the MP4, poster, editable brief, preview page, review frames and `render-report.json`, plus the skill source. Describe the actual format, silence, any fictional material and any adaptation made. A generated example is not a customer result, endorsement or live integration.

[Provenance](references/provenance.md) records the high-level reference and font licenses. No upstream source implementation or branding is bundled.
