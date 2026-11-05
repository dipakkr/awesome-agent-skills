---
name: benefit-panels
description: Turn verified product attributes into a readable secondary listing graphic with concise callouts. Use for Amazon feature infographic requests; accept optional runtime product photos, brand assets, copy and placement without editing this skill.
metadata:
  author: Claude Directory
  edition: 1.0.0
---

# Benefit Panels

Turn verified product attributes into a readable secondary listing graphic with concise callouts.

## Runtime inputs

Use the current request as the brief. Optional inputs are product photos, authorised logo, brand colours, exact copy, supplied facts, marketplace/category and target module dimensions. Never require edits to SKILL.md. If no logo is supplied, omit it cleanly; never print placeholder or replacement instructions on the image. Do not insert Claude Directory branding into customer artwork. Follow explicit user colours and products rather than demonstration defaults. If no product is specified, start with a clearly disclosed concept still life and offer a refinement; ask only for facts needed to make product claims.

Inspect supplied photos before generation. Assign product, logo and style references distinct roles; preserve product geometry, colour, count, labels and packaging when supplied. If none exists, say outside the artwork that the subject is a fictional concept and fidelity to a real item is untested.

## Placement workflow

Use secondary listing or a selected A+ image placement, never MAIN. Extract up to three supplied factual attributes and repeat exact units. Do not invent measured benefits, certifications, medical claims, waterproof ratings or customer proof. Use one clear product view with short readable callouts and restrained leader lines. When only a concept brief exists, label the concept outside the image and state its specs are fictional. Review every letter, unit, callout anchor and visible geometry at full size and thumbnail size. Deliver native-copy text separately for accessibility; verify the selected placement dimensions before upload.

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
