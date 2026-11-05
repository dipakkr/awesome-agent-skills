# Contributing

Use one pull request per new skill. Start from the latest main branch and give
the skill a clear, repository-specific name describing its workflow.

## What to include

- A `SKILL.md` with a matching folder name, description, inputs and usable workflow.
- The scripts, references, templates and assets required to run it.
- Original or redistributable materials with their licence notices intact.
- A catalogue entry and current file hashes.
- A short example request and an accurate description of your validation.

Do not add credentials, runtime caches or large generated demo exports. Keep
repository names independent of external product listings. Do not add per-skill
commercial demo links or source-to-store crosswalks. Preserve attribution and
historical provenance; naming is a presentation choice, not access control.

## Checks before merging

```sh
python3 scripts/validate.py
git diff --check -- README.md CATALOG.md catalog.json
```

Review the complete staged diff and any runtime requirements. Imported source
may retain existing whitespace to preserve source bytes and licence notices.
State which workflow/output checks you actually ran; structural validation is
not a substitute for a runtime or visual test. Merge before the next addition.

## Maintainer imports

Maintainers can import approved original packages from their authoring workspace
using a private naming map. Keep that map outside this repository:

```sh
python3 scripts/sync.py --workspace /path/to/workspace --mapping /path/to/private-names.json --skill merchant-intake
python3 scripts/validate.py
python3 scripts/sync.py --workspace /path/to/workspace --mapping /path/to/private-names.json --check
```

Without `--skill`, sync refreshes only existing packages. It refuses local edits
and unexpected removals. Use `--migrate-names` only for an explicit naming migration.
No source map is required to use or validate a downloaded skill.
