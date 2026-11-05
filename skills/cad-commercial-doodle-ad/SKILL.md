---
name: cad-commercial-doodle-ad
description: Turn one product benefit into a commercial illustration with expressive ink doodles, a clear hero and short readable copy. Choose a single image, continuous long PDF or paginated PDF directly in the request.
---


# Commercial Doodle Ad


An illustration-led ad, with one central product and hand-drawn marks that explain its use rather than ornamental clutter.


## Run without editing this skill


Accept a natural-language brief plus optional product photos, logo file, exact copy, brand colours, placement and aspect ratio. Use supplied inputs directly; do not ask the user to edit SKILL.md or replace template tokens. Example brands in references are demonstration inputs, never defaults.

If no logo is supplied, omit it and rebalance the composition. Never draw a placeholder, "your logo", Claude Directory mark, invented brand mark or compulsory attribution in the user output. If a logo is supplied, treat it as an exact asset, not inspiration; inspect it and use an image-edit/compositing workflow that preserves its shape and wording. Check it against the source. If accurate placement fails, deliver a clean logo-free image and explain the limitation instead of fabricating a replacement.

If no product image is supplied, generate a clearly described concept and label it as conceptual in the delivery note. For a real product listing, request the actual product photo and approved facts; never infer construction, ingredient, performance or certification claims from a name.


## Composition decisions


1. Choose one promise from supplied facts; translate it into a literal product plus one visual metaphor.

2. Keep product edges separate from doodles. Use a coherent stroke weight, two accent colours and deliberate negative space.

3. Limit copy to a headline and optional brand/CTA. A doodle must explain an action or benefit, not imply unsupported functionality.

4. For variants change the metaphor or layout, not just colour. Inspect the image at a small feed size.


## Choose the format in your request

Accept `format: image | long | pdf` and `paper: A4 | Letter` as runtime choices; no skill-file edits. Default to `image`, preserving the single-creative workflow. For `long`, plan a sequence of portrait doodle sections with consistent handwriting, palette and width. Use one source-supported idea per section. For `pdf`, plan one idea per paper page. Keep short copy readable; add pages rather than squeeze in paragraphs. Retain the separate original page images in every mode.

After reviewing each generated section, use the included exporter. It places unchanged raster artwork in a real PDF, preserving proportions without cropping. `long` produces one tall scrolling PDF page; `pdf` produces standard paper pages. When exporting an existing set of different campaigns, describe it as a collection, not one continuous story. Image generation uses your available tool/account; PDF export runs locally with Python, Pillow and ReportLab.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/export_notes.py section-01.png section-02.png --format long --paper A4 --output doodle-long.pdf
python3 scripts/export_notes.py section-01.png section-02.png --format pdf --paper Letter --output doodle-pages.pdf
```

Run from this skill directory or use absolute paths. The exporter refuses an existing PDF or receipt; choose a new filename. It writes a `.receipt.json` with ordered source hashes, dimensions and placements. Long pages above 14,400 points are refused; use paginated PDF or split the document. Inspect the exported PDF for order, readability and clipping. PDFs contain raster artwork, not editable or searchable handwriting; deliver the editable brief/copy separately. No logo is required.

Example: “Use this product brief to make a three-section hand-drawn explainer. Format long, paper A4, no logo. Keep only the features stated in my brief.”

## Generate, review, deliver


Use the available image-generation tool for new raster artwork, and its image-edit path for supplied assets. No particular paid provider is required, but image generation depends on the user’s available tool/account. If unavailable, return the finished generation brief and clearly state that no image was generated; never substitute a text mockup and claim completion.

Generate one independent file per variant. Save every attempt with a unique filename, the input brief and exact prompt; record input/output hashes, actual dimensions, tool, review result and any correction. Inspect product structure, readable exact text, aspect ratio, safe margins and the distinctive composition decisions above. Correct a specific issue with an image edit or regenerate, keeping prior attempts. Do not claim exact pixels until measured.

Deliver accepted raster files, an editable brief and exact prompt, alt text, and a short placement/use note. These are editable generation inputs, not layered image files. Provide source/layer files only if actually created. Do not promise sales lift, virality, platform approval or product-photo accuracy from a concept image.


## Usage


Use in an organic social post or display creative where a simple product idea needs a more human, illustrated treatment.


## References


Read [example briefs](references/examples.json) for two different compositions, replacing their runtime inputs with the user’s brief. Read [format and research notes](references/research.md) for source context; recheck current placement rules before publishing.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
