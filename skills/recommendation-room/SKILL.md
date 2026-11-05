---
name: recommendation-room
description: Build a recommendation-first decision deck with a clear issue, supported analysis, tradeoffs and an owned next step. Use for consulting decision deck requests; accept the user's topic, audience, evidence, brand and optional assets at runtime.
---

# Recommendation Room

Create a complete presentation for the user's situation. The examples demonstrate possibilities, not content to copy. Do not require editing this skill or hardcode a demo brand into a new output.

## Inputs and judgment

Take the brief, audience, desired decision, duration or slide count, language, supplied facts, optional brand assets and preferred format. Use reasonable defaults for missing design preferences. Ask only when a missing source or requirement materially changes the work. Defaults: 16:9, 1280 × 720, editable HTML plus JSON; create PowerPoint when dependencies are available. Let users override the visual treatment. A logo is optional; omit it when absent.

## Content method

Recommendation → evidence and assumptions → options and tradeoffs → implementation decision.

Separate observed data, assumptions and recommendations. Use units, periods and zero baselines. Do not fabricate client data or causal certainty.

Write one claim or story beat per slide before drawing anything. Map each factual claim to a supplied source; label uncertainty. Put detailed context in speaker notes. Adapt length to the task: the compact examples are not a maximum or a mandatory outline.

## Art direction

Select an audience-appropriate visual direction before layout. The examples demonstrate Queue Atlas, Activation Lab, Stockroom Ledger. Read references/design.md for the typography, image treatment and composition of each. Adapt a visual grammar or create a new coherent direction; do not limit reuse to an example brand or palette.

Read `references/design.md` for the three demonstrated visual directions, audience fit, typography, imagery and composition choices. Choose an art direction before layout; a copy or accent-color change alone does not create a new design. Inspect cover and interior examples together. Choose new compositions, palette and content from the brief. Avoid making every slide the same arrangement. Use at least three distinct arrangements in a deck of four or more slides. Preserve a legible hierarchy: titles usually 48–88 px, body 26–36 px, source notes 14–20 px. Keep a 48–64 px safe margin. Shorten crowded text before shrinking it.

If the deck needs illustration or photography, use an available image-generation tool or cleared user assets. Generate individual scenes and inspect each asset. Keep all headings and body copy as native editable text, not baked into art. Maintain character or product fidelity using reference images. Do not silently replace required art with placeholders; disclose an unavailable tool and deliver a clearly marked draft if blocked. Generated art must not imply a real product, event or person when it is conceptual.

## Build and export

1. Read `references/schema.md`. Author a fresh `deck.json` with positioned editable text, shapes, image references and speaker notes. The renderer is freeform: the agent chooses the layout, it is not a fixed slide template.
2. Keep local artwork inside the deck's folder. Review any reuse across slides; default to distinct scenes except a deliberate recurring symbol.
3. Render an offline HTML deck with `python3 scripts/render_deck.py /path/to/deck.json --out /path/to/output/deck`. All images embed into the HTML. No API key or network access is needed to view it.
4. For PowerPoint, install `scripts/requirements.txt` into a local virtual environment and run that environment's Python with the same command plus `--pptx`. Text and simple shapes remain native editable objects; generated artwork remains raster. Notes are exported. The optional package install requires network access; generating HTML itself does not.
5. Use a browser to review every slide at full size. Check clipping, text overflow, image cropping, contrast, source labels, sequence and notes. Verify first/last navigation, Edit text, Undo, Save HTML and reopening the saved copy. Check the exported PPTX separately when PowerPoint/LibreOffice is available; otherwise report structural validation only, not native-app visual parity.
6. Deliver HTML, editable JSON, assets and optional PPTX with an honest review note. Do not claim a PDF export exists merely because the browser provides Print / PDF. Do not publish or send to clients without authorization.

## Reuse and limits

The HTML has text editing, slide navigation, speaker notes, HTML save, JSON save and print styles. Text edits do not automatically rewrite the original JSON or previously exported PPTX: save JSON and rerun the renderer to refresh PowerPoint. For layout, order, image or theme changes, edit the JSON and rebuild. No slide reordering UI, native chart workbook, video export or cloud editor integration is claimed.

Three independently authored example decks are in `examples/`. Their content is fictional or explicitly labeled demonstration material. Use them to understand composition and output behavior, then generate a new deck from the user's brief.

## Worked examples

Read [the worked-example guide](references/usage-examples.md) for copyable requests, supplied briefs, actual output previews, source references and review limits. Change inputs in your request; do not edit this skill to change topics.
