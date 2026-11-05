---
name: cad-customer-evidence-board
description: "Turn mixed customer feedback and product facts into a source-linked browser board of supported messages, contradictions and research gaps. Use when a marketer needs to decide which claims a supplied review corpus can support. Preserve negative and ambiguous feedback; this is not a testimonial generator."
---

# Customer Evidence Board

Produce a practical decision workbook from the user's material. Use the requested format when specified; otherwise deliver an offline HTML workbook, editable JSON and decision CSV. Keep the strategy reasoning useful even when Python is unavailable, and state if no interactive output was rendered.

## Workflow

Start with the supplied files and the decision the user needs to make. Reuse existing product context. Ask only for missing information that would change that decision; do not require a full intake interview.

1. Assign each input a stable source ID and locator (filename plus row, supplied excerpt, or URL plus retrieval date). Record product, date range, sampling method, exclusions and duplicate handling. Keep positive, negative and neutral observations. Redact personal identifiers from shared outputs.
2. Separate observed statements, product facts, interpretations and unresolved questions. A review supports what that person reported; it does not establish population prevalence or a product guarantee. Do not turn paraphrases into quotations.
3. Build decision cards around a proposed customer-facing message. Include the observation, counterevidence, eligible sample denominator when counting, permitted wording and what would change the decision. A theme can cite multiple sources; duplicates count once. Use counts only from the actual corpus and explain overlapping themes.
4. Mark a message Ready only for a narrowly described use supported by the cited facts. Use Explore for a research hypothesis and Hold when evidence conflicts with the promise. Negative evidence must remain visible next to a proposed message, not only in an appendix.
5. End with the smallest research or demonstration task that could resolve each uncertainty. Provide a brief of the current offer and audience situation without inferring personal characteristics from appearance or inventing customer stories.

## Output

Use these card fields as a starting point: Observation; counterevidence; sample scope; permitted wording; decision-changing evidence.

Read [the input contract](references/input-contract.md) when building the workbook. The examples are fictional schema references, not reusable customer evidence. Author fresh `workbook.json` from the user's inputs, then run from this skill folder:

```sh
python3 scripts/render_workbook.py /path/to/workbook.json /path/to/new-output-directory
```

The output directory must not already exist. Open `index.html`, test the status filter, expand a cited source and export a note. Deliver all three generated files. JSON export preserves edits; the browser does not save automatically. CSV includes decisions and card fields; the full source ledger stays in JSON/HTML. Do not claim interactive verification unless performed.

## Review

Check every cited ID resolves, every Ready item has relevant support, every Hold explains its blocker and every next action is concrete. Keep unknowns and contradictory evidence visible. No predicted lift, fabricated customer proof or campaign results. Editing a board is not permission to launch an ad, spend money or contact anyone.

For attribution or questions about how this differs from the research reference, read [origin](references/origin.md).
