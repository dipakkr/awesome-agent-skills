---
name: magazine-in-motion
description: Build a product promo from photographic cutouts, printed frames, expressive typography and layered editorial compositions. Use for photographic product launches and magazine-style promos. Includes editable source and three aspect ratios.
---

# Magazine In Motion

Open with a magazine cover, inspect the product, assemble a contact sheet, slide a typographic collage and close on a product signature. 20 seconds.

Read `references/input.md` before adapting a brief. Change the narrative, assets and scene actions for the user's product. The examples are fictional concepts, not real software recordings or physical product demonstrations.

## Produce the film

- Requires Node22+, FFmpeg/FFprobe and Remotion4.0.539. Run `npm ci` in renderer. Remotion has separate license terms.
- Copy an example JSON into a new brief. Supply a transparent cutout in renderer/public and set image to its basename. Inspect alpha edges, full silhouette and each crop. The included headphones and sneaker are original generated fictional products. Brand text and descriptive claims are editable; do not invent product performance.
- Run `node render.mjs /absolute/brief.json /absolute/new-run --stills`. Inspect all scenes and layout in every requested format. Adapt source for long text, different media or new scene actions.
- Render without `--stills`. Supply a cleared music file with `--music /absolute/music.mp3 --credit /absolute/credit.txt --music-start 16`. Read `references/music.md`. Without a music file the film is intentionally silent.
- Review full encoding, scene and transition samples, ending, legibility and sound. Deliver MP4, source, brief and publishing credit. Use a fresh output directory for every accepted revision.

## Scope

Original React/CSS/SVG motion and generated product cutouts; DM fonts bundled under OFL. No reference footage or third-party rendering source is included. These are authored scene structures, not a general video generation model. Realistic live footage, other narratives and narration require additional assets or source adaptation. The recorded examples use credited Scott Buckley music; raw music files are not bundled.
