---
name: cad-ad-production-blueprint
description: "Translate a supported creative idea and real asset inventory into a production handoff with shot beats, missing assets and acceptance checks. Use when preparing an ad shoot, edit or static creative handoff under practical constraints. The deliverable is a production plan, not generated footage or a finished ad."
---

# Ad Production Blueprint

Produce a practical decision workbook from the user's material. Use the requested format when specified; otherwise deliver an offline HTML workbook, editable JSON and decision CSV. Keep the strategy reasoning useful even when Python is unavailable, and state if no interactive output was rendered.

## Workflow

Start with one selected idea, its evidence, available footage or photography, channel and production constraints. If the user only has an idea, create a provisional plan and label required assets as missing.

1. Write the viewer takeaway and the visible proof needed to justify it. Inventory usable assets, rights status, people, locations, capture time and aspect-ratio requirements. Do not label a planned shot as already captured.
2. Compare only feasible execution routes. Choose the route that makes the proof legible within the user's constraints. Explain the rejected route's cost, missing evidence or feasibility problem without importing a format catalogue.
3. Break the selected route into timed beats for video, or spatial regions for static work. For each, specify on-screen action, copy or voice, asset ID, owner/role and acceptance check. Beat durations must add up to the stated runtime. Use role placeholders honestly when no owner is assigned.
4. Include an alternate execution if a critical asset is unavailable. A still sequence is an animatic; it must not be described as captured or generated live action. Any testimonial or reconstruction must be labeled accurately and supported by authorization.
5. Mark readiness per route or shot, with one next action to unblock it. Check product fidelity, claim scope, captions, sound-off readability and destination requirements when supplied. If current placement rules matter, verify with official platform documentation. Deliver a handoff and list what still needs capture, review or approval. Do not publish or contact creators.

## Output

Use these card fields as a starting point: Viewer takeaway; execution route; beat schedule; asset inventory; owner; acceptance check; fallback.

Read [the input contract](references/input-contract.md) when building the workbook. The examples are fictional schema references, not reusable customer evidence. Author fresh `workbook.json` from the user's inputs, then run from this skill folder:

```sh
python3 scripts/render_workbook.py /path/to/workbook.json /path/to/new-output-directory
```

The output directory must not already exist. Open `index.html`, test the status filter, expand a cited source and export a note. Deliver all three generated files. JSON export preserves edits; the browser does not save automatically. CSV includes decisions and card fields; the full source ledger stays in JSON/HTML. Do not claim interactive verification unless performed.

## Review

Check every cited ID resolves, every Ready item has relevant support, every Hold explains its blocker and every next action is concrete. Keep unknowns and contradictory evidence visible. No predicted lift, fabricated customer proof or campaign results. Editing a board is not permission to launch an ad, spend money or contact anyone.

For attribution or questions about how this differs from the research reference, read [origin](references/origin.md).
