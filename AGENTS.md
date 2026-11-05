# Repository instructions

- Use Deepak Kumar <raj.deeepak@gmail.com> as both commit author and committer.
- Do not add Codex, OpenAI, AI co-author trailers or generated-by attribution.
- Keep skill source here and link to website pages for previews and downloads.
- Preserve third-party notices and the publication status recorded in catalog.json.
- Read LICENSING.md before preparing a public release of this full collection.
- While this is an imported collection, update the authoring sources in the
  parent workspace and run scripts/sync.py; do not overwrite local edits.
- Run scripts/validate.py after updates and scripts/sync.py --check when the
  website workspace is available. Do not claim structural checks prove runtime
  behavior across all skills and agent environments.

## Adding skills

- Start each addition on a dedicated branch and include one skill per pull request.
- Include its source files, catalogue record, hashes and website link together.
- Run standalone validation before committing; review the diff before merging.
- Merge the pull request before starting the next skill addition.
- Keep every commit authored and committed by Deepak; omit AI attribution.
