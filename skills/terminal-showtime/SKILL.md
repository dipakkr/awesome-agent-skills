---
name: terminal-showtime
description: Turn a short product idea into a pixel terminal promo with typed input, file assembly and a visual result. Use for developer tool promos and stylized terminal launch films. Includes editable source and landscape, portrait and square layouts.
---

# Terminal Showtime

Boot a bitmap identity, type an input, assemble three files, preview the result and finish with a pixel character. 20 seconds.

Read `references/direction.md` for the material and choreography. Read `references/input.md` before editing an example. Keep the user's requested direction. Change the actual imagery, task and scene actions when adapting to a new brief, not just the brand name. The bundled examples are fictional concepts, not recordings of working software or real places.

## Produce a complete film

1. Copy an example into a new brief. Use approved claims and authorized imagery. Match the command, file names and result to the actual task. The supplied site and release branches are illustrative starting scenes; other products need source changes.
2. Requires Node22+, FFmpeg/FFprobe and Remotion4.0.539. Run `npm ci` in renderer. Remotion has separate license terms. No paid generation API is needed to reproduce the included examples.
3. Run `node render.mjs /absolute/brief.json /absolute/new-run --stills`. Inspect all scenes at full and thumbnail sizes. Correct source if text, crop or motion conflicts.
4. Render without `--stills`. The renderer writes a full H.264/AAC film, original synthesized soundtrack, input snapshot, encoded review frames and hash receipt. Never overwrite accepted films; use a new run directory.
5. Inspect the encoded transitions, ending, legibility and sound. Repeat for each requested format. Deliver MP4 plus editable source and brief. Encoding success alone is not visual acceptance.

Read `references/audio.md` when adapting the soundtrack or scene timing.

## Scope and provenance

Original React/SVG animation, bitmap glyph artwork and synthesized sound. Fonts are bundled under OFL. The two photographic stills were originally generated for our own Waypoint concept; they depict fictional scenes and are reused here independently of that project's preview-only engine. No Skillry code, third-party reference footage or copied rendering engine is included. Camera motion on still imagery is not live-action video. No voiceover is included. Longer timelines, different products, new media types and languages require source adaptation and review.
