---
name: gathering-announcement
description: Build a clear LinkedIn Event cover around the supplied topic, schedule and host without inventing speaker credentials. Use when a user needs a 16:9 LinkedIn Event cover; takes supplied text and optional brand assets at runtime.
---

# Gathering Announcement

## Runtime input contract
Run this skill directly with a brief; never ask the user to modify skill files. Accept `text`, `brand` (name, palette, typography), `logo`, `image`, `product`, `audience` and `placement` as optional runtime inputs, plus the job-specific facts below. Demo briefs are examples, never defaults. If a logo is absent, omit it cleanly; never render a logo placeholder. Preserve supplied logos and product references with image editing, not invented replacements. Request missing facts only when required to make the output truthful. No forced Claude Directory mark.

## Workflow
1. Require an event title, date, time with timezone and host identity. If absent, ask for missing schedule details; never infer a timezone.
2. Keep the event title dominant; group date, time and host into one readable schedule block. If no speaker photo is supplied, choose abstract topical art, not a fictional speaker portrait.
3. Use only a supplied event registration destination in accompanying copy. Do not draw a fake clickable button into an Event cover.
4. Write an editable brief and a full generation prompt. Quote all approved words exactly. Use the built-in image generation tool for a finished raster image; describe composition, spacing, color, exact wording and exclusions. For supplied assets, inspect them first, assign their reference roles and preserve identity through the image-edit reference inputs.
5. Inspect the actual returned image. Check spelling, meaning, margins, geometry and supplied asset fidelity. Measure dimensions and file size. Reject mistakes and regenerate or edit with the image tool; save every attempt without overwriting.
6. Deliver the accepted image, editable brief/prompt and concise usage notes with actual dimensions, limitations and suggested alt text. Do not claim layered PSD/SVG editability, guaranteed performance, or platform upload testing that was not performed.

## Placement guidance
LinkedIn Event creation guidance specifies a 16:9 cover and at least 480 pixels width. Event cover and Event Ad specifications are different; these examples target the Event cover.

See [research](references/research.md) for authoritative sources, checked 2026-10-28. Recheck the platform specifications before a campaign launch.

## Examples
See [editable briefs](references/example-briefs.json). Call `gathering-announcement` (or `$gathering-announcement`) with your text and optional assets. The example brands/events/data are fictional demonstrations.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
