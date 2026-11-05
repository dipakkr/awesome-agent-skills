---
name: hesitation-to-yes
description: Create a text-led launch film that turns a repeated objection into a feature reveal, using dark glass cards, accelerating zoom cuts and a terminal-style replay of supplied data. Use for feature announcements and explicitly fictional concept examples.
---

# Hesitation To Yes

Build an original film around one specific concern and a credible response. Use the user's approved product claims, brand and source material. For concept requests, invent the product and concern together and keep the concept disclosure visible. Never imply invented posts are real testimonials or customer complaints. Do not reuse the reference product, copy, handles, branding or footage.

## Shape the film

Follow [the storyboard](references/storyboard.md). A short confident claim gives way to three fictional concern cards. Repeat one exact hinge phrase in all three cards; accelerate through nine growing crops of that phrase. A two-word reversal leads into a command reveal, a terminal-style fixture replay, the resulting records, and a thesis/end card.

This original renderer makes a32-second silent1920×1080film at30fps. Four backgrounds change the actual pattern as well as the color: blue grid, aubergine diagonal lines, copper rings and tidal waves. Fonts, original source and four distinct examples are bundled. The linked reference preview is27.9seconds; this interpretation includes an additional readable fixture-output beat. It does not reproduce the reference footage or claim to be its full HyperFrames project.

## Prepare a fresh brief

Read [the schema](references/schema.md) and [four worked examples](references/usage-examples.md). Convert the user's request into `brief.json` and a four-record `data.json`. Keep the exact hinge in all three posts. Use a short command label, a two-word turn and a thesis that describes the value of the feature. Choose the background to fit the brand.

The terminal findings are derived by the local renderer from the supplied records. The film does not run an agent or connect to a product. For a real product launch, supply actual approved material and replace the concept replay with a verified recording or adapt the renderer; do not simply remove the disclosure and present a mockup as execution evidence. The bundled renderer intentionally labels its fictional posts and fixture data.

## Render

Requires Python3.10+, Pillow, FFmpeg and FFprobe with libx264. Fonts are bundled with their licenses. No API key, image model, video model, browser or paid service is used during rendering.

```sh
python3 <installed-skill>/scripts/render.py brief.json --out output/version-01
```

Use a fresh directory. The renderer refuses overwrites and checks text fit across the timeline before recording. `--poster-only` performs that validation and writes a poster without the full MP4. Resolve overflow by shortening the copy or deliberately adapting the layout. Never silently truncate an input.

## Review and deliver

Review every recorded act and the full playback. Check that all three concern cards differ, the hinge matches, the zoom scale only grows, the reversal reads clearly, the four findings agree with the fixture, and the final thesis has a reading hold. Keep title/role text clear of decorative patterns. Background movement should remain quiet enough for the type to lead.

Deliver `film.mp4`, `poster.png`, `preview.html`, `proof.html`, `brief.json`, `data.json`, eleven review frames and `render-report.json`, with this source package. The receipt records dimensions, duration, decode, data/source hashes and the derived findings. Full recorded examples and exact commands are in the example guide. Render validation does not prove a product capability, audience response or independent agent reuse.

This is a fixed local visual grammar. Music, voiceover, alternate aspect ratios, arbitrary product UI, custom logos and different record counts require explicit adaptations. The example films are silent. Do not publish or deploy unless the user asks.
