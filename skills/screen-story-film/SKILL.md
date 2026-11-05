---
name: screen-story-film
description: Turn a product workflow into a focused film with a visible input, transformation and result. Use when asked for product demo film videos, original product films or multi-aspect promotional motion. Export complete MP4s with music and editable source.
---

# Screen Story Film

## Deliver the film, not just a script

Create a complete film using the original frame-driven React source in `renderer/`. The examples are fictional concepts. Never represent the animated concept interface as a recording of a real product. For real-product demonstrations, obtain supplied captures and implement the actual states in `src/Film.jsx`; preserve labels and verify every claim. Do not claim unsupported functionality or performance.

## Art direction

Problem, typed input, organized workspace, close-up on the next action, confirmation and CTA. 26 seconds. Use this as a starting grammar, not a requirement to keep every shot. Use a black or white stage, bright accents, generous breathing room and oversized readable type. Keep accent areas intentional. Avoid a repeated headline-and-card slideshow. The opening should work as a poster at small preview size. Hard cuts and short wipes separate compositions; hold the key idea long enough to read. Adapt shots and story to the brief, not only the colors and title.

## Production

1. Read the product brief and inventory approved assets. Identify audience, useful promise, proof, CTA and whether this is a fictional concept. Do not invent numbers, testimonials, UI evidence or discounts.
2. Read `references/input.md`, choose a relevant `examples/*.json`, and write a NEW brief. Set `mode` to `demo`. Use real wording and permitted media; preserve provenance in the handoff. Write the planned scene sequence before rendering. Change composition/timing in source when the story needs it.
3. In `renderer/`, install pinned dependencies with `npm install`. Requires Node 22+, FFmpeg/FFprobe and Remotion's downloaded rendering browser. No paid generation API is required. Review Remotion's licence for the user's organisation.
4. Run `node render.mjs ../examples/01-landscape.json /absolute/path/to/new-run --stills`. Inspect every still at native size AND preview size. Fix clipping, poor contrast, repeated layouts and weak focal points in source. Do not patch exported videos.
5. Run the same command without `--stills`. It writes a complete H.264/AAC MP4, an original synthesized soundtrack, encoded review samples, input snapshot, poster, storyboard and source hashes. Existing films are never overwritten.
6. Review the complete encoded film with sound. Confirm readable holds, intentional transitions, a clear story and audible music without clipping. Compare to the brief and examples, not merely a successful encode. If weak, fix the reusable renderer and rerender to a new versioned directory.
7. For 9:16 or 1:1, change `format` to `portrait` or `square`, render a separate output and inspect it. These have recomposed layouts; do not crop a landscape export. Package approved MP4s with editable brief, source and review notes.

## Assets and sound

Bundled DM Sans is OFL licensed. The abstract artwork and concept interfaces are original source-generated graphics. `compose-score.mjs` creates an original instrumental with no external samples; it is an editable starting score, not a promise of bespoke professional music. Replace with supplied licensed music when appropriate and preserve attribution. Portfolio accepts three relative `images` paths inside `renderer/public`; never imply demo graphics are client projects. Do not redistribute the separate adapted Launch Video engine.

## Validation boundary

The included examples prove local rendering and author review in the documented formats. They do not prove conversion uplift, autonomous success for arbitrary briefs, live product integrations or customer validation. Text limits prevent many layout failures; visual inspection is still required. Node dependencies are not bundled. Review `references/provenance.md` before adding external assets.
