---
name: chaptered-product-story
description: "Reproduce the legacy 40-second chaptered product-film examples when explicitly requested, using supplied facts and screen captures."
---

# Chaptered Product Story

A legacy workflow for reproducing the bundled chaptered-film composition. Use it when this specific format is requested. Its earlier samples were not accepted as a default for new launch films. For a different launch-story format, see [Flagship Introduction](../flagship-introduction/SKILL.md). Keep the two workflows and their results distinct.

Make a finished launch film, not a planning worksheet. Start from the user's actual product, approved facts and available media. When asked for an example without a product, create an explicitly fictional concept. Do not replace a requested real product with one of the sample brands.

## Find the story

Identify one promise and three visible capabilities that support it. Reuse supplied context; ask only for a missing fact or asset that would materially change the film. Read the user's official product material when research is needed, recording the source and retrieval date. A feature claim needs evidence beyond an attractive mockup. Label proposed capabilities and concept interfaces honestly.

Select one legible screen per chapter. Use authorized local PNG/JPEG/WebP captures at least 1280 × 720. Remove private customer data before using a capture. Keep complete source files with the handoff. Never insert reference-site screenshots, another company's logo, or testimonial claims into the user's video.

## Direct the film

The supplied renderer is a 40-second, 1920 × 1080, 30fps starting point:

- 0–4s: an original tab mark resolves, followed by the product's opening line.
- 4–8s: the promise arrives in words and the three chapter labels assemble.
- 8–16s: a framed workspace rises into view, then the camera moves toward the important detail.
- 16–24s: a layered canvas introduces a second capability with different staging.
- 24–32s: the third interface takes over the frame, with a restrained caption band.
- 32–40s: a clear CTA and the three chapter labels form the final lockup. The ending holds long enough to read.

Change the actual story, screens, focus positions and copy together. A palette swap is not a new example. Do not animate a pointer or state change to imply a real action happened unless a supplied recording or actual sequence supports it. Camera movement over a static capture should be described accurately.

For a user-requested duration, alternate ratio or screen recording, adapt the editable renderer and validate the new composition rather than pretending the fixed baseline already supports it. The four bundled themes are starting points, not a substitute for the user's visual identity.

## Build and render

Read [the input schema](references/schema.md). Create a fresh brief JSON from the user's normal-language request. Requirements: Python 3.10+, Pillow, FFmpeg and FFprobe with libx264 and AAC. Licensed fonts are bundled. The renderer makes no network requests and has no model pin or paid-generation dependency.

```sh
python3 <installed-skill>/scripts/render.py brief.json --out output/review-01 --review-only
python3 <installed-skill>/scripts/render.py brief.json --out output/film-01
```

Use new output directories. The renderer refuses overwrite. Review-only creates frames, not a video. Fix copy-fit errors instead of truncating text. Set `audio` to `original-pulse` for the bundled original 120 BPM instrumental or `silent` when requested. A supplied licensed soundtrack needs an explicit renderer adaptation; do not claim it was used when it was not. There is no voiceover.

Use `--start 8 --end 16` for a short motion test. A range render is not the complete film; disclose its duration. For exact examples and reuse, see [worked examples](references/examples.md).

## Quality and delivery

Play the entire encoded MP4. Check motion at scene boundaries, UI sharpness at maximum zoom, readable typography, meaningful focus targets, the last CTA hold and audio level. Review the encoded frames as well as the preflight images. A successful encode is not proof of a convincing film. If the result looks like a static deck, change the staging and motion before listing it.

Deliver `film.mp4`, `preview.html`, `poster.png`, editable renderer, brief and source captures, review frames and `render-report.json`. The report records dimensions, duration, audio, source hashes and a full decode. Check that every claim matches its source and disclose fictional interfaces, original synthetic music or missing footage.

For a directory listing, use the actual rendered video as the preview source and check muted looping autoplay in the grid. A screenshot is only its loading poster. Publish or deploy only within the user's authorized scope.

[Origin and differences](references/origin.md) documents the supplied reference without redistributing its engine or assets.
