---
name: focus-window
description: Follow a product control with a moving magnification lens, anchored explanation and visible state change. Use for product launch scenes and short promotional videos. Includes an editable 18-second scene, landscape and square layouts.
---

# Focus Window

Follow a product control with a moving magnification lens, anchored explanation and visible state change.

Read `references/quickstart.md` for a first-use prompt and `references/input.md` for exact supported fields. Read `references/art-direction.md` before changing the scene structure. This is an original scene renderer, not an unrestricted video-generation model.

## Produce and deliver

1. Establish the user's product, message, format and desired action. For a real product, inspect its official website before choosing colors or assets. Record the source URL and palette in `brandAudit`; preserve the supplied logo's proportions. Use only those product colors. Keep the default stage white unless the user explicitly requests a source adaptation.
2. Copy an example JSON and replace its fields. The built-in product interfaces are illustrative and require `concept:true`; do not describe them as captured working software. Fictional demos use declared original brand tokens, not another company's identity.
3. Run `npm ci` inside renderer, then `node render.mjs /absolute/brief.json /absolute/new-output --stills`. Inspect all beats and text in the requested format. Change `src/Spotlight.jsx` when the user's story needs different actions. Do not merely rename a sample whose actions do not fit.
4. Render without `--stills`. Optional licensed music: `--music /absolute/music.mp3 --credit /absolute/credit.txt --music-start 16`. Read `references/music.md`. Without music, the output is silent.
5. Review the encoded MP4, transitions, final hold, brand identity, text fit and audio. Deliver the MP4, exact brief, source and publishing credit. Use a fresh output directory for revisions.

Requirements: Node22+, FFmpeg/FFprobe and pinned Remotion4.0.539. Remotion has separate license terms. No paid generation API is needed for the supplied visuals. Local fonts are included under OFL. Source and examples are original; no Skillry rendering source or media is included.
