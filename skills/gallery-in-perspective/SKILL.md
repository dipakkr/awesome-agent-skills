---
name: gallery-in-perspective
description: Reveal a media library over a tilted moving wall, select a collection and expand one asset into a detail panel. Use for portfolio launches, ecommerce lookbooks and creative libraries.
---

# Gallery In Perspective

Turn the user's brief into a fresh, locally rendered film. Ask only for information that prevents an honest result: the approved claims and any required footage or artwork. Default to a clearly labelled fictional concept when they request an example. Use the user's brand rather than the example brand; never insert another skill marketplace's identity.

## Motion structure

Raise a tilted 24-tile wall made from supplied media. Place a readable library in front, activate its second collection, enlarge its selected image continuously, then show a review-ready state. The wall uses a 2D rotation; this renderer does not implement a perspective 3D camera or embedded video tiles.

## Prepare the inputs

Read [the schema](references/schema.md) and [four worked examples](references/usage-examples.md). Write a new JSON brief from the user's normal-language request. Change the subject, actual content, branding and call to action together. A palette change alone is not a new example. Do not infer verified results, product capabilities or endorsements from the sample films.

## Render locally

Requirements: Python 3.10+, Pillow, FFmpeg and FFprobe with libx264. Licensed fonts are bundled. No paid generation API, model pin, browser renderer or network access is required after installing these dependencies. Install Pillow with your normal Python environment, for example `python3 -m pip install Pillow`.

```sh
python3 <installed-skill>/scripts/render.py brief.json --out output/version-01
```

Use a new directory; overwriting an existing render is refused. The script checks copy fit across the timeline before rendering and rejects overflow. Fix the brief or deliberately change the layout instead of truncating words. Output is 12 seconds, 1280 × 720, 24fps, silent H.264 MP4. The skill's configured layout is fixed; alternate ratios, soundtrack, custom logos and longer films require an explicit renderer adaptation. Text branding is supported directly.

Use authorized local inputs. The bundled examples are illustrative and do not connect to any live product or publish anything.

## Review and hand off

Open `preview.html`, play the whole film, and inspect all five review frames. Check arrival/reading holds, clipping, source accuracy and the final CTA. For the chart, compare every point to the supplied numbers and unit. For the morph, check panel continuity. A successful FFmpeg decode does not prove visual quality.

Deliver `film.mp4`, `poster.png`, `brief.json`, `preview.html`, five review frames and `render-report.json`, plus this editable renderer and its assets. The report records input hashes, renderer hash, dimensions, duration and a full decode. Say explicitly whether the film is silent, illustrative, stock-backed or based on real data. Keep any failed attempts separate. Do not call a demo a live integration or a customer result.
