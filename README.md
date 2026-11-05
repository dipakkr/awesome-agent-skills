# Awesome Agent Skills

Reusable agent skills for design, video, presentations, ecommerce and more.

**[Explore visual previews and downloads at Claude Directory →](https://claudeai.directory/skills)**

This repository contains real skill instructions, scripts, templates and supporting
files. Find a skill in the [source index](CATALOG.md), or visit the website to see
what it creates, download a packaged skill and read its usage examples.

## Use a skill

1. Choose a skill from [CATALOG.md](CATALOG.md).
2. Keep its entire folder from `skills/`, including scripts, references and assets.
3. Read its `SKILL.md` for the required tools, inputs and installation guidance.
4. Install it using your agent's supported skill workflow, then provide your brief.

Agent features and external services vary by skill. Provider usage may carry
separate costs. Source is available here under the applicable licences; website
purchase/access conditions are separate. No hosted execution is provided here.

Visual previews live on the website. Rendered demo exports are omitted from this
repository; reusable example inputs remain. If a reference mentions a local
recorded example, use the corresponding website page to view its output.

## Contribute

Add one skill per branch and pull request. Include its complete reusable source,
licence, catalogue record and website link. Validate and review it, then merge
before starting the next addition. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Maintain the site export

The website workspace's `.agents/skills/` folders remain the authoring source.
This repository imports original packages from its catalogue and profile downloads.
For maintainers with that workspace:

```sh
python3 scripts/sync.py --workspace /path/to/claudeai.directory --skill cad-ecommerce-store-brief
python3 scripts/validate.py
python3 scripts/sync.py --workspace /path/to/claudeai.directory --check
```

`--skill` adds one eligible package. Without it, sync updates only packages already
in this repository. It refuses locally modified exports, unexpected private files
and unreviewed source removals. It never imports adapted third-party packages.
`catalog.json` records file hashes and omitted demo exports.

Standalone check, without the website workspace:

```sh
python3 scripts/validate.py
```

These checks verify source integrity and structure. They do not claim every skill
has been executed in every agent environment.

## Licence

Original instructions and code use [MIT](LICENSE). Embedded fonts and other
third-party materials retain their own notices. See [LICENSING.md](LICENSING.md).
Skills with unresolved source redistribution rights are excluded from this public
repository.
