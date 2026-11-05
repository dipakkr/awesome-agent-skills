---
name: cad-ad-motion-export
description: Assemble supplied ad images and local video clips into a short MP4 review master and optional GIF, with explicit soundtrack, preserved aspect ratios and measured export validation. Use for ad cutdowns and image-based animatics, not new live-action generation.
---

# Ad Motion Export

Turn the user's approved artwork and clips into a timed ad assembly. Accept natural-language instructions and create the render manifest yourself; no manual editing of this skill is required. This is a standalone local renderer with no API key or mandatory companion skill.

## Choose what the output can truthfully be

For image-only inputs, deliver an image-based animatic with fades. This script does not synthesize camera movement, product action, lip sync or live-action footage. For a finished demonstration ad, obtain the required footage or use the user's available video-generation tool before assembly. A fade between stills is not evidence of product performance and may be unsuitable for some video-ad placements.

Decide duration and beats from the brief. A useful starting point is a product/hook, one supported feature or demonstration, and an offer/CTA, but don't force every ad into three equal shots. Keep longer readable text on screen long enough to read. Vary sequencing and timing for different products instead of copying a demo.

Ask for local assets, desired ratio and soundtrack only when they are missing and necessary. Default to a 1080 x 1920 vertical review master. Verify the current ad destination rules before describing any file as ready to upload. Read [export notes](references/export.md) for input format and destination limitations.

## Preserve assets and scope

Inspect supplied media. Keep SKU design, label, logo, garment and claims unchanged. The renderer fits and pads each asset without cropping; choose a background from the user's brand. For a fully filled frame, first create a correctly composed source with the available image/video editing tool. Do not stretch the asset. Add exact text upstream using a tool that preserves typography; this exporter does not draw text or invent branding.

Use licensed or original audio the user is entitled to use. Clip audio is discarded; only the explicit soundtrack is included. If narration from a clip matters, extract and intentionally mix it first, then supply that audio. If audio is absent, identify the export as silent. A silent master is not automatically valid for every ad placement. GIF has no audio and is primarily a preview.

## Render

Requirements: Python 3.10+, FFmpeg and FFprobe on PATH, with the libx264 encoder. Do not install dependencies, change ad accounts or incur provider charges merely by loading this skill.

Create a JSON manifest based on the actual inputs, using [the schema and example](references/export.md), then execute the bundled script from this skill directory:

```sh
python3 scripts/render.py campaign.json --out output/version-01 --gif
```

Resolve the script path from the installed skill location. Asset paths resolve relative to the manifest. Use a fresh output directory for each version. The script accepts PNG/JPEG/WebP and MP4/MOV inputs, 1-12 shots, 1-30 seconds per shot, and up to 120 seconds total. These are renderer limits, not platform rules. It rejects missing assets, out-of-range footage and a short soundtrack rather than silently repeating or dropping content.

## Review and deliver

Open the result, review the full timeline, and inspect first, middle and final beats. Check text at phone scale, product visibility, consistent colour, pacing, padding and audio. Automated decode and dimension checks do not establish visual or ad-policy quality.

Deliver ad.mp4, optional preview.gif, the editable manifest and render-report.json. The report includes measured duration/dimensions, source hashes and the actual render type. Keep source assets available to the buyer so the manifest can be reused; package only assets they can redistribute. For a different brand or product, start with their new assets and brief, not a mandatory example skin. Preserve the user's optional branding; never add a platform watermark.

This creates files. It does not publish, buy media, predict ROAS or promise ad approval.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
