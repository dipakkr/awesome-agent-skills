---
name: tall-product-story
description: Create a vertical shopping Pin with a useful visual hook, a clear product and legible text.
---


# Tall Product Story


One 2:3 vertical image that makes a product idea useful to save, with hierarchy that works in a mobile feed.


## Run without editing this skill


Accept a natural-language brief plus optional product photos, logo file, exact copy, brand colours, placement and aspect ratio. Use supplied inputs directly; do not ask the user to edit SKILL.md or replace template tokens. Example brands in references are demonstration inputs, never defaults.

If no logo is supplied, omit it and rebalance the composition. Never draw a placeholder, "your logo", Claude Directory mark, invented brand mark or compulsory attribution in the user output. If a logo is supplied, treat it as an exact asset, not inspiration; inspect it and use an image-edit/compositing workflow that preserves its shape and wording. Check it against the source. If accurate placement fails, deliver a clean logo-free image and explain the limitation instead of fabricating a replacement.

If no product image is supplied, generate a clearly described concept and label it as conceptual in the delivery note. For a real product listing, request the actual product photo and approved facts; never infer construction, ingredient, performance or certification claims from a name.


## Composition decisions


1. Choose a specific use or shopping intent rather than a generic inspiration collage. Keep one product or a coherent supplied set as the focus.

2. Use a 2:3 canvas, normally 1000x1500 or larger at the same ratio. Measure the actual result; do not claim exact pixel compliance from prompt alone.

3. Reserve breathing room for a concise headline and optionally a brand supplied by the user. Put destinations in the Pin link field, not a fake UI button.

4. Deliver a suggested Pin title and descriptive alt text outside the image. Make different compositions for variants, not illegible dense multipanels.


## Generate, review, deliver


Use the available image-generation tool for new raster artwork, and its image-edit path for supplied assets. No particular paid provider is required, but image generation depends on the user’s available tool/account. If unavailable, return the finished generation brief and clearly state that no image was generated; never substitute a text mockup and claim completion.

Generate one independent file per variant. Save every attempt with a unique filename, the input brief and exact prompt; record input/output hashes, actual dimensions, tool, review result and any correction. Inspect product structure, readable exact text, aspect ratio, safe margins and the distinctive composition decisions above. Correct a specific issue with an image edit or regenerate, keeping prior attempts. Do not claim exact pixels until measured.

Deliver accepted raster files, an editable brief and exact prompt, alt text, and a short placement/use note. These are editable generation inputs, not layered image files. Provide source/layer files only if actually created. Do not promise sales lift, virality, platform approval or product-photo accuracy from a concept image.


## Usage


Upload the image as a Pin, add a truthful product or collection destination and descriptive alt text. Preview the crop in Pinterest before publishing.


## References


Read [example briefs](references/examples.json) for two different compositions, replacing their runtime inputs with the user’s brief. Read [format and research notes](references/research.md) for source context; recheck current placement rules before publishing.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
