# Contributing skills

Use a separate branch and pull request for each skill. Start from the current
main branch and include the complete reusable package under `skills/<name>/`.
Keep `SKILL.md`, supporting scripts, templates, assets and licence notices together.
Use original or explicitly redistributable materials; retain third-party notices.
Do not include credentials, runtime caches or generated preview exports.

Maintainers importing from the site use `scripts/sync.py --workspace <workspace>
--skill <name>` to update the source, catalogue, hashes and website link together.

Before merging:

- Run `python3 scripts/validate.py` and `git diff --check`.
- Check the diff contains only the intended skill and its catalogue changes.
- Verify the workflow's local references and runtime requirements.
- Describe the output, website preview link and actual checks in the PR.
- Distinguish structural validation from a new runtime/visual test.

Merge the PR before starting the next addition. Avoid unrelated website or
commerce changes in this repository.
