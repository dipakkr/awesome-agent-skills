---
name: liftoff-sequence
description: Build anticipation through technical drawings, rocket assembly, countdown, ignition and payload deployment. Use for product-release teasers, countdown films and space-themed launch announcements. Render complete films with distinct sound and editable scenes.
---

# Liftoff Sequence

Create a finished MP4 from an approved brief, with editable source, input snapshot and review frames. Blueprint, exploded assembly, countdown, launch-pad ignition, tracking flight, capsule or satellite deployment, and brand sign-off. 25 seconds.

## Give the story its own identity

Read `references/direction.md` before adapting. Change the subject and actions to fit the story, not only the text and accent. This package has its own material and motion system. Do not replace it with the generic rings, dashboard cards and headline template used in other motion skills. Keep the user's requested visual direction when it differs from the examples.

The examples are fictional concepts. They do not prove product functionality, environmental outcomes or flight performance. Use approved wording, supplied assets and supported claims. Longer stories, new characters, real screens and voiceover require source work beyond the JSON fields.

## Render and review

1. Copy a relevant `examples/*.json` into a new brief; read `references/input.md`. Adapt source when the subject needs different props, scenes or pacing. Keep existing accepted renders intact.
2. Requires Node 22+, FFmpeg/FFprobe and Remotion 4.0.539. In `renderer`, run `npm ci`. Review Remotion's separate license for the user's organization. No paid generation API is required.
3. Run `node render.mjs /absolute/brief.json /absolute/new-run --stills`. Inspect every composition at full size and card size. Check text fit, object clearances and a coherent narrative.
4. Run the same command without `--stills`. It renders H.264/AAC, composes original synthesized sound, decodes the film and records exact sources and artifact hashes. Never fix only the exported MP4; fix reusable source and render a new version.
5. Review the encoded film, scene samples and audio. Inspect transitions as well as held frames. Do not equate successful encoding with visual acceptance. Retain honest author-review notes.
6. Set `format` to landscape, portrait or square for separate layout-aware exports. Validate each requested shape. Deliver film, editable brief/source, soundtrack, poster and receipts.

## Provenance and scope

Original React/SVG artwork, animation and synthesized audio. Bundled DM Sans and DM Serif are OFL licensed. Public Skillry previews informed the gap review but their code, artwork and media are not included. Remotion has a separate license. No narration or live footage is bundled. The paper effect is vector illustration with procedural paper texture; the rocket is shaded vector animation, not a physical 3D simulation.
