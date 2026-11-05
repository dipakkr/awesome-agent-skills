---
name: storefront-panorama
description: Create a text-free collection banner with a planned focal region and usable space for theme-rendered headings; adapt composition to the actual Shopify section.
metadata:
  author: Claude Directory
  ownership: original-workflow
  version: 1.0.0
---

# Storefront Panorama

Ask for section aspect ratio and heading position. Build a coherent collection scene rather than isolated unrelated products. Reserve real low-detail space for HTML copy, avoid baked-in promotional text, and keep the main group compact enough to survive plausible mobile crops. State that focal point support depends on theme/version and mobile proof needs an actual theme preview.

## Runtime inputs

Invoke this skill directly with a brief; no editing SKILL.md or package files is required. Accept optional logo, product photograph, reference image, brand name, palette and exact text at runtime. Example: `$storefront-panorama create two images for my product; use the attached product photo, optional logo and supplied copy.` Omit absent logos cleanly; never invent a mark or render placeholder text. Supplied logos are preservation inputs for the image edit, never redrawn from a textual guess. Brand names in bundled demonstrations are examples only, never default customer branding. Claude Directory branding does not belong in generated customer imagery.

## Inputs and execution

Use the user's product, brand and composition choices. Collect destination slot, requested dimensions, approved facts, exact label text and any product photographs. Read [platform notes](references/platform-notes.md) for Shopify sizing/crop decisions. [Example briefs](references/example-briefs.json) are editable fictional demonstrations, not facts about a merchant's products.

For a real SKU, inspect its supplied photograph, identify it as the edit target and record invariants before using built-in image generation. Without a photo, label the run conceptual; never claim exact product fidelity. Label any styling reference separately. Do not invent customer proof, certification, technical performance or endorsements.

Use built-in image generation with one independent call per asset. Supply the approved scene, lighting, framing, exact text, requested size and invariants. For revisions change one documented problem at a time, retain every prior attempt and record the input roles and hashes. Stop after two unsuccessful corrections to the same problem and report it rather than claiming completion. Do not silently switch to paid API fallback.

Save outputs as versioned files immediately. Measure actual dimensions, size and format; disclose any requested-size mismatch. Visually inspect silhouette, object count, joins, shadows, cropping and every word. For real products compare the rendered product against the supplied reference; generated fidelity remains a review requirement, not a guarantee. Review desktop/mobile crops in the intended theme before publishing.

Deliver the accepted raster, editable brief and full prompt, facts/feature or inclusion ledger where applicable, alt text and a run record containing tool, inputs, actual size, hashes, acceptance reasons and limits. Raster output is flattened; do not promise layered PSD/SVG. Do not upload, publish, change product listings or use paid services without task authorization.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
