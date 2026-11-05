---
name: cad-handwritten-notes-document
description: Turn supplied material into readable handwritten notes with real generated doodle artwork, then export a single page, continuous long document or paginated PDF. Accept format, paper size, source facts and optional branding at runtime.
metadata:
  author: Claude Directory
  edition: 1.0.0
---

# Handwritten Notes Document

Create illustration-led handwritten notes from the user's source, retaining an editable brief and source text alongside real raster artwork and a PDF. This is a separate document workflow; do not modify other visual-notes skills.

## Runtime choices

Accept `format: page | long | pdf`, `paper: A4 | Letter`, the source material, intended reader, optional exact wording, palette and authorised logo directly in the request. No SKILL.md editing is needed. Default to `pdf` and `A4`; use the source language unless specified otherwise.

- `page`: one generated image on one standard paper page; the exporter requires exactly one image.
- `long`: multiple ordered image sections on one continuous PDF page. Paper selects the width; height follows the sections. This is a scrolling document, not standard printer pagination.
- `pdf`: one image per standard paper page, in the supplied order, with no cropping.

All three exporter modes produce **PDFs**. Keep and deliver the original page/section PNGs separately when a native image is wanted. A raster-backed PDF is not editable handwriting or searchable body text; the editable source brief and copy are separate files.

## Source and visual plan

Read the supplied source and extract its actual facts, numbers, names, relationships and qualifications into `brief.json` or Markdown. Keep citations or source references in the editable brief. Do not invent quotations, statistics, findings or missing steps. Mark unknowns in the brief, not as placeholder text in final artwork. If the user supplies only a topic, distinguish an original general explanation from a summary of a source.

Use a short title, short phrases and illustration-led relationships. Prefer 3–6 clearly separated ideas per standard page; split dense material into more pages instead of shrinking handwriting. Keep exact technical notation and numbers legible. Use restrained marker colour, thin pen drawings, clear arrows and a visible reading order. Follow requested design rather than a fixed brand template.

For a long document, plan a sequence of portrait sections with a shared width, palette, handwriting treatment and modest internal margins. Avoid repeating the main title on every section. The exporter stacks complete images with a small gap; it does not remove backgrounds or make joins visually seamless. For standard paper, request portrait artwork near the chosen paper ratio; measured output may differ and is fitted without cropping.

Use an authorised logo only when provided and requested. Otherwise omit it cleanly. Never print a logo placeholder, replacement instruction or Claude Directory branding on customer artwork.

## Generate and review artwork

Use the available built-in image generation tool to create each page/section separately. Include the exact short copy, drawing plan, reading direction and style in the prompt. Do not use HTML/SVG stand-ins for the requested generated artwork. Inspect supplied reference images first and assign product, logo and style references distinct roles.

Save every attempt with versioned filenames. Record full prompts, source/reference hashes, actual tool and actual output dimensions. Inspect every page at full size and reading size: copy character by character, numerical values, arrow direction, visual meaning, legibility and clipping. Correct mistakes with the image tool or reduce the copy and regenerate. Retain rejected attempts and reasons. Never treat generated handwriting as automatically accurate.

After artwork review, export with the bundled local script. It only places unchanged source images in a PDF; it does not rewrite, retouch or resample source files. Transparent areas appear against the PDF's white page. Supply images in their intended pixel orientation; EXIF rotation is not applied.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/export_notes.py page-01.png page-02.png --format pdf --paper A4 --output notes.pdf
python3 scripts/export_notes.py section-01.png section-02.png --format long --paper Letter --output long-notes.pdf
python3 scripts/export_notes.py page-01.png --format page --paper A4 --output single-page.pdf
```

Run these commands from this skill folder, or use absolute paths to the script and inputs. Existing PDF **or receipt** paths are refused; choose a new output filename. The receipt is `<output-stem>.receipt.json` and records ordered source hashes, original pixels, placed rectangles, page dimensions and output hash. Long documents above 14,400 points (200 inches) are refused; switch to `pdf` or divide into multiple long documents. No paid PDF renderer or logo is required.

Inspect the exported PDF in a viewer or render its pages with an available local PDF viewer. Confirm page order, expected page count, text readability, no cropping and appropriate scale. Do not claim printing, accessibility or searchable-text support from an export-only check. Deliver the PDF, original PNGs, export receipt, editable brief/copy and prompt recipe.

## Example requests

- “Turn these meeting notes into one handwritten summary page. Format page, paper A4, no logo. Keep the owners and deadlines exactly as supplied.”
- “Make a long doodle document explaining this onboarding process. Format long, paper Letter; one illustrated section per stage, preserving the order.”
- “Create a four-page handwritten study guide from this chapter. Format pdf, paper A4; use my supplied palette and leave out branding.”

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
