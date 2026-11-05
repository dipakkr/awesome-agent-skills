---
name: report-front-page
description: Create the opening cover graphic for a useful LinkedIn document, guide or carousel using a clear reader promise. Use when a user needs a 4:5 portrait document cover; takes supplied text and optional brand assets at runtime.
---

# Report Front Page

## Runtime input contract
Run this skill directly with a brief; never ask the user to modify skill files. Accept `text`, `brand` (name, palette, typography), `logo`, `image`, `product`, `audience` and `placement` as optional runtime inputs, plus the job-specific facts below. Demo briefs are examples, never defaults. If a logo is absent, omit it cleanly; never render a logo placeholder. Preserve supplied logos and product references with image editing, not invented replacements. Request missing facts only when required to make the output truthful. No forced Claude Directory mark.

## Workflow
1. Identify the document subject, reader, practical promise and actual scope. Never imply the cover includes an authored full document.
2. Use a three-level hierarchy: short category label, primary title and one concise subtitle. Page count or edition numbers are allowed only when supplied.
3. Design a clear opening image with no fake swipe controls. Leave room for real logos only when supplied; omit the logo area cleanly otherwise.
4. Write an editable brief and a full generation prompt. Quote all approved words exactly. Use the built-in image generation tool for a finished raster image; describe composition, spacing, color, exact wording and exclusions. For supplied assets, inspect them first, assign their reference roles and preserve identity through the image-edit reference inputs.
5. Inspect the actual returned image. Check spelling, meaning, margins, geometry and supplied asset fidelity. Measure dimensions and file size. Reject mistakes and regenerate or edit with the image tool; save every attempt without overwriting.
6. Deliver the accepted image, editable brief/prompt and concise usage notes with actual dimensions, limitations and suggested alt text. Do not claim layered PSD/SVG editability, guaranteed performance, or platform upload testing that was not performed.

## Placement guidance
LinkedIn document ads accept PDF, DOC/DOCX and PPT/PPTX, up to 100 MB and 300 pages. The 4:5 example canvas is an editorial choice, not a mandatory LinkedIn pixel dimension. Insert the raster cover into a document with consistent page sizes before posting.

See [research](references/research.md) for authoritative sources, checked 2026-10-28. Recheck the platform specifications before a campaign launch.

## Examples
See [editable briefs](references/example-briefs.json). Call `report-front-page` (or `$report-front-page`) with your text and optional assets. The example brands/events/data are fictional demonstrations.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
