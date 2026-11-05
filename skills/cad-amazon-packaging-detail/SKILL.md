---
name: cad-amazon-packaging-detail
description: Show the exact package contents in a clear secondary listing image, with quantities and packaging grounded in supplied facts. Accept optional runtime product photos, branding and copy without editing this skill.
metadata:
  author: Claude Directory
  edition: 1.0.0
---

# Amazon Packaging Detail

Show the exact package contents in a clear secondary listing image, with quantities and packaging grounded in supplied facts.

## Runtime inputs

Use the current request as the brief. Optional inputs are product photos, authorised logo, brand colours, exact copy, supplied facts, marketplace/category and target module dimensions. Never require edits to SKILL.md. If no logo is supplied, omit it cleanly; never print placeholder or replacement instructions on the image. Do not insert Claude Directory branding into customer artwork. Follow explicit user colours and products rather than demonstration defaults. If no product is specified, start with a clearly disclosed concept still life and offer a refinement; ask only for facts needed to make product claims.

Inspect supplied photos before generation. Assign product, logo and style references distinct roles; preserve product geometry, colour, count, labels and packaging when supplied. If none exists, say outside the artwork that the subject is a fictional concept and fidelity to a real item is untested.

## Placement workflow

Choose a secondary listing image, never MAIN. Obtain the included-item inventory and distinguish shipping packaging from included accessories. Show each supplied item exactly once in the stated quantity, with plausible relative scale. Do not add decorative props that look included. Use a quiet coloured or neutral background and short optional exact-copy labels. Preserve actual product and packaging photos when supplied; without them disclose a fictional demonstration outside the artwork. Review counts, packaging geometry, any visible labels and all copy. Check current category rules and actual file dimensions before upload; no Amazon acceptance or real-product-fidelity guarantee.

## Generate and review

1. Read references/placement.md and identify placement plus supplied versus assumed facts. Draft a concise brief with composition, lighting, palette, exact copy and invariants.
2. Use the available built-in image generation tool. Generate each requested asset separately. For edits, inspect the source and pass its actual local path as a reference; explain what must remain fixed. Never substitute an HTML mockup for an image.
3. Save every attempt with a versioned filename and retain the full prompt, reference roles and SHA256 hashes. Keep rejects and state the reason.
4. Inspect the actual raster. Check copy character by character, geometry, clutter, artefacts, margins and intended crop. Measure actual pixel dimensions and file size, not just requested values. Correct via the image tool when needed.
5. Deliver accepted raster files plus editable brief, exact copy and prompt recipe. Raster is not a layered design file. Give factual alt text and placement limitations. Do not claim Amazon approval, universal compliance, conversion improvement or real-product fidelity without verification.

## Examples

The two briefs in examples/briefs.json are explicit fictional demonstrations, not defaults. A normal invocation can be: “Use this skill for my supplied product and brand assets; prepare two distinct compositions for the stated placement.”

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
