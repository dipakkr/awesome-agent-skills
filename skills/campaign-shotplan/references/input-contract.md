# Workbook input contract

Use `examples/foldwell.json` as a structural example, never as evidence about the user's product. Read the other example for a different business context.

Top-level text: `title`, `brand`, `purpose`, `disclosure`. State whether the inputs are real, supplied, inferred or synthetic in disclosure. `accent` is lime, blue, coral or lavender.

`sources`: objects containing unique `id`, `label`, `text`, `locator`. Record exact quotes only when actually quoted; otherwise label paraphrases. Locators identify the supplied file/row or public URL and retrieval date. Do not embed personal information unnecessarily.

`cards`: objects with unique alphanumeric/hyphen `id`, `title`, `status` (Ready, Explore, Hold), `decision`, `fields` (named text values), `next`, `evidence` (source ID array), and optional `note`. Ready requires evidence. A source reference is not automatic proof: the author must review relevance and limits. Unsupported hypotheses use Explore; contradictory or unsubstantiated promises use Hold. Ready is scoped to the next action, not campaign approval or predicted success.

Use the field set in SKILL.md. Add user-specific fields where useful. Keep paragraphs brief enough to scan, with full detail in the evidence ledger. Exported notes can be re-rendered using the same script. The renderer has no network requests, account integration or persistent storage; JSON export is required to keep edits.
