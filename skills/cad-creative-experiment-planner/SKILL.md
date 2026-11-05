---
name: cad-creative-experiment-planner
description: "Turn a creative question into a controlled test backlog with explicit variables, measurement rules and inconclusive outcomes. Use when a team needs to choose its next ad experiment from existing evidence and production constraints. It plans tests; it does not launch campaigns or predict winners."
---

# Creative Experiment Planner

Produce a practical decision workbook from the user's material. Use the requested format when specified; otherwise deliver an offline HTML workbook, editable JSON and decision CSV. Keep the strategy reasoning useful even when Python is unavailable, and state if no interactive output was rendered.

## Workflow

Read the user's objective, available evidence, current creative, production capacity and measurement setup. If no performance data exists, plan a learning test and label it unrun.

1. Write the unresolved business decision before choosing creative. Connect each test to an observed friction or a clearly labeled hypothesis. Prefer situations and purchase decisions over invented demographic personas.
2. Specify control and treatment. Name the single intended change and list the elements held constant: audience, offer, placement, landing page, timing and budget allocation where relevant. If several elements must change, label the result a concept comparison with limited causal interpretation.
3. Choose a primary metric with numerator, denominator and measurement window. Add a downstream guardrail so attention alone cannot become a business win. Keep unknown baselines and sample requirements explicit. Do not invent universal spend, significance or sample-size thresholds.
4. Define launch prerequisites, the pre-agreed review rule, an inconclusive outcome and a stop condition. A calendar deadline is an operational review point, not proof of sufficient data. Separate operational stops from evidence-based winner selection.
5. Order the backlog by evidence strength, decision value and production effort with a written rationale. Avoid uncalibrated numerical confidence scores. Distinguish Ready to schedule from a measured winning ad. Do not connect accounts, publish or spend as a side effect of planning.

## Output

Use these card fields as a starting point: Question; control; treatment; held constant; primary metric; guardrail; review rule; inconclusive outcome.

Read [the input contract](references/input-contract.md) when building the workbook. The examples are fictional schema references, not reusable customer evidence. Author fresh `workbook.json` from the user's inputs, then run from this skill folder:

```sh
python3 scripts/render_workbook.py /path/to/workbook.json /path/to/new-output-directory
```

The output directory must not already exist. Open `index.html`, test the status filter, expand a cited source and export a note. Deliver all three generated files. JSON export preserves edits; the browser does not save automatically. CSV includes decisions and card fields; the full source ledger stays in JSON/HTML. Do not claim interactive verification unless performed.

## Review

Check every cited ID resolves, every Ready item has relevant support, every Hold explains its blocker and every next action is concrete. Keep unknowns and contradictory evidence visible. No predicted lift, fabricated customer proof or campaign results. Editing a board is not permission to launch an ad, spend money or contact anyone.

For attribution or questions about how this differs from the research reference, read [origin](references/origin.md).
