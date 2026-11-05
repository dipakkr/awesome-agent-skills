---
name: numbers-to-narrative
description: Turn a small supplied dataset into an accurate, clearly labelled feed graphic with units, source and an honest takeaway. Use when a user needs a 1:1 square data graphic; takes supplied text and optional brand assets at runtime.
---

# Numbers To Narrative

## Runtime input contract
Run this skill directly with a brief; never ask the user to modify skill files. Accept `text`, `brand` (name, palette, typography), `logo`, `image`, `product`, `audience` and `placement` as optional runtime inputs, plus the job-specific facts below. Demo briefs are examples, never defaults. If a logo is absent, omit it cleanly; never render a logo placeholder. Preserve supplied logos and product references with image editing, not invented replacements. Request missing facts only when required to make the output truthful. No forced Claude Directory mark.

## Workflow
1. Require source data, units, date/period and whether the data is real or illustrative. Stop for missing source context. Never invent customer traction or use a demo result as evidence.
2. Calculate totals, differences and proportions before generation. Choose a simple horizontal bar chart with zero baseline or two-value comparison; provide exact label/value mapping in the prompt.
3. After generation compare every number and label to the source. Check relative bar lengths, baseline and legends; reject misleading geometry, omissions or accidental causal claims. Put Demo data visibly on synthetic examples.
4. Write an editable brief and a full generation prompt. Quote all approved words exactly. Use the built-in image generation tool for a finished raster image; describe composition, spacing, color, exact wording and exclusions. For supplied assets, inspect them first, assign their reference roles and preserve identity through the image-edit reference inputs.
5. Inspect the actual returned image. Check spelling, meaning, margins, geometry and supplied asset fidelity. Measure dimensions and file size. Reject mistakes and regenerate or edit with the image tool; save every attempt without overwriting.
6. Deliver the accepted image, editable brief/prompt and concise usage notes with actual dimensions, limitations and suggested alt text. Do not claim layered PSD/SVG editability, guaranteed performance, or platform upload testing that was not performed.

## Placement guidance
The square feed canvas follows LinkedIn single-image ad aspect guidance; organic post upload and distribution are separate. Numerical accuracy, baseline and source labels matter more than stylistic embellishment.

See [research](references/research.md) for authoritative sources, checked 2026-10-28. Recheck the platform specifications before a campaign launch.

## Examples
See [editable briefs](references/example-briefs.json). Call `numbers-to-narrative` (or `$numbers-to-narrative`) with your text and optional assets. The example brands/events/data are fictional demonstrations.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
