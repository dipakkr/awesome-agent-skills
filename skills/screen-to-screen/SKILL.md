---
name: screen-to-screen
description: Carry one idea between phone, laptop and tablet through connected screen transitions and camera movement. Use for multi-device launch films and connected product journeys. Includes editable source and three aspect ratios.
---

# Screen To Screen

Capture on a phone, carry a shared card into a laptop, develop the idea, present on a tablet and assemble a connected device family. 24 seconds.

Set `theme` to `light` for a white stage or `dark` for a black stage (default). The theme also adjusts heading contrast, shadows and floor guides.

For a new video after installation, start with `references/quickstart.md`. It contains a fill-in prompt and explains supported options. Read `references/input.md` before adapting a brief. Change the narrative, assets and scene actions for the user's product. The examples are fictional concepts, not real software recordings or physical product demonstrations.

## Produce the film

- Requires Node22+, FFmpeg/FFprobe and Remotion4.0.539. Run `npm ci` in renderer. Remotion has separate license terms.
- Copy an example JSON into a new brief. For a real product, supply three authorized captures in renderer/public and set screens to their basenames, in phone/laptop/tablet order. The renderer preserves their aspect ratio. Built-in notes/design interfaces are illustrative and require concept:true. Capture real state changes when proving product behavior.
- Run `node render.mjs /absolute/brief.json /absolute/new-run --stills`. Inspect all scenes and layout in every requested format. Adapt source for long text, different media or new scene actions.
- Render without `--stills`. Supply a cleared music file with `--music /absolute/music.mp3 --credit /absolute/credit.txt --music-start 16`. Read `references/music.md`. Without a music file the film is intentionally silent.
- Review full encoding, scene and transition samples, ending, legibility and sound. Deliver MP4, source, brief and publishing credit. Use a fresh output directory for every accepted revision.

## Scope

Original React/CSS/SVG motion and generated product cutouts; DM fonts bundled under OFL. No reference footage or third-party rendering source is included. These are authored scene structures, not a general video generation model. Realistic live footage, other narratives and narration require additional assets or source adaptation. The recorded examples use credited Scott Buckley music; raw music files are not bundled.
