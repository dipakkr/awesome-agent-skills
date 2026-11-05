---
name: particle-rings
description: Create a seamless projected particle loop with a sphere, torus, helix or wave and a stable editorial headline. Use for abstract brand films, interludes and event backdrops.
---

# Particle Rings

Turn the user's brief into a new motion piece. Retain approved facts and exact wording. The provided examples are fictional subjects, not names or claims to repeat in client work.

## Composition and timing

Generate a deterministic point field, project depth into position and size, and rotate it over an exact eight-second period. Sort back to front and keep the point cloud away from the headline. The analytical phase loops exactly without an entrance or exit fade.

Lock the readable final composition before refining motion. Prioritize a strong focal point, generous type and safe margins. Inspect transitions as well as posters; a technically valid encode is not proof of a good visual result.

## Render a fresh brief

Read [inputs and limits](references/inputs.md) and [recorded examples](references/examples.md). Write a fresh JSON brief. The self-contained renderer uses Python 3.10+, Pillow, FFmpeg and FFprobe with libx264. Fonts and their licenses are included. No API key or paid generator is needed.

```sh
python3 <skill-folder>/scripts/render.py brief.json --out output/review --stills-only
python3 <skill-folder>/scripts/render.py brief.json --out output/final
```

Use new output directories. The renderer refuses overwrite and checks text fit across every frame. Output is silent 1920×1080 at 30fps. It uses frame time and deterministic geometry, so replay is reproducible. Custom sizes, music and different content structures require deliberate source adaptation and fresh review.

## Review and deliver

Inspect the five review images, full MP4 playback and exact text against the input. Confirm readable holds and safe edges. For countdowns check the final nonzero frame and the zero hold; for particle loops check the wrap. For curves inspect joins and the exported SVG. For conversations verify speaker alignment and that each new reply has enough reading time.

Deliver film.mp4, poster.png, brief.json, preview.html, review frames, render-report.json and the editable skill source. Include path.svg for Vector Draw-On. Disclose fictional examples and the silent output format. [Provenance](references/provenance.md) records the high-level reference; our implementation and artwork are independently authored.
