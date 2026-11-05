---
name: cad-linkedin-insight-card
description: Turn one defensible professional insight into a concise feed graphic with a memorable visual metaphor. Use when a user needs a 1:1 square feed graphic; takes supplied text and optional brand assets at runtime.
---

# LinkedIn Insight Card

## Runtime input contract
Run this skill directly with a brief; never ask the user to modify skill files. Accept `text`, `brand` (name, palette, typography), `logo`, `image`, `product`, `audience` and `placement` as optional runtime inputs, plus the job-specific facts below. Demo briefs are examples, never defaults. If a logo is absent, omit it cleanly; never render a logo placeholder. Preserve supplied logos and product references with image editing, not invented replacements. Request missing facts only when required to make the output truthful. No forced Claude Directory mark.

## Workflow
1. Reduce the supplied idea to one statement and at most one short supporting sentence. Preserve meaning; do not attribute quotations to someone who did not say them.
2. Choose one concrete metaphor that explains the statement. Choose either an editorial split layout or a poster composition; avoid generic business clip art.
3. Keep text in the central readable field with a quiet margin. Check the statement remains understandable without the accompanying post.
4. Write an editable brief and a full generation prompt. Quote all approved words exactly. Use the built-in image generation tool for a finished raster image; describe composition, spacing, color, exact wording and exclusions. For supplied assets, inspect them first, assign their reference roles and preserve identity through the image-edit reference inputs.
5. Inspect the actual returned image. Check spelling, meaning, margins, geometry and supplied asset fidelity. Measure dimensions and file size. Reject mistakes and regenerate or edit with the image tool; save every attempt without overwriting.
6. Deliver the accepted image, editable brief/prompt and concise usage notes with actual dimensions, limitations and suggested alt text. Do not claim layered PSD/SVG editability, guaranteed performance, or platform upload testing that was not performed.

## Placement guidance
Square 1:1 is a LinkedIn single-image ad format, with 1200×1200 recommended. It is a useful feed composition choice, not a claim that organic reach is guaranteed.

See [research](references/research.md) for authoritative sources, checked 2026-10-28. Recheck the platform specifications before a campaign launch.

## Examples
See [editable briefs](references/example-briefs.json). Call `cad-linkedin-insight-card` (or `$cad-linkedin-insight-card`) with your text and optional assets. The example brands/events/data are fictional demonstrations.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
