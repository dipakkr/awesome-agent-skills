---
name: cad-hook-proof-lab
description: "Develop ad openings together with the evidence and first scene needed to support each promise, in an editable comparison workbook. Use when writing or revising ad hooks that must connect to a real demonstration. It is useful for promise-to-proof review, not generic viral swipe-file imitation."
---

# Hook & Proof Lab

Produce a practical decision workbook from the user's material. Use the requested format when specified; otherwise deliver an offline HTML workbook, editable JSON and decision CSV. Keep the strategy reasoning useful even when Python is unavailable, and state if no interactive output was rendered.

## Workflow

Read the product facts, target situation, supplied brand voice samples and actual assets. Use the requested number of candidates; if unspecified, begin with a small distinct set. A missing brand voice can be handled with a clearly labeled plain-language draft.

1. Identify the claim a viewer could reasonably infer from the proposed opener. Treat implied guarantees, numbers, comparisons and first-person experiences as claims needing support.
2. Draft openings from the supplied situation and evidence. Vary the communicative job (show the task, name a constraint, invite an inspection) rather than filling copied social templates. Do not invent scarcity, customer quotations, personal experience or performance claims.
3. Pair every opening with a concrete first frame and a proof beat. State what the viewer sees, what the evidence establishes and what remains unproven. Include the transition to the offer so curiosity is resolved rather than deferred indefinitely.
4. Check spoken and silent comprehension. Estimate read time from word count and a stated pace if useful, but never claim timed performance without a real read-through. Keep captions and product labels legible for the intended placement.
5. Keep rejected candidates visible as Hold with a specific reason and a safer rewrite. Shortlist using supported promise, visual feasibility and voice fit, not predicted conversion. If testing, pair openings with the same body and record that a hook test does not prove sales lift.

## Output

Use these card fields as a starting point: Opening line; implied promise; first frame; proof beat; transition; test or rejection reason.

Read [the input contract](references/input-contract.md) when building the workbook. The examples are fictional schema references, not reusable customer evidence. Author fresh `workbook.json` from the user's inputs, then run from this skill folder:

```sh
python3 scripts/render_workbook.py /path/to/workbook.json /path/to/new-output-directory
```

The output directory must not already exist. Open `index.html`, test the status filter, expand a cited source and export a note. Deliver all three generated files. JSON export preserves edits; the browser does not save automatically. CSV includes decisions and card fields; the full source ledger stays in JSON/HTML. Do not claim interactive verification unless performed.

## Review

Check every cited ID resolves, every Ready item has relevant support, every Hold explains its blocker and every next action is concrete. Keep unknowns and contradictory evidence visible. No predicted lift, fabricated customer proof or campaign results. Editing a board is not permission to launch an ad, spend money or contact anyone.

For attribution or questions about how this differs from the research reference, read [origin](references/origin.md).
