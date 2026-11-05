# Claude Directory Skills

Reusable agent skills from [Claude Directory](https://claudeai.directory/skills).

**Browse the [website](https://claudeai.directory/skills) to see visual previews,
download a skill and follow its usage instructions.** This repository contains
the instructions, scripts, templates and supporting source files. It does not
provide a visual preview gallery or a hosted skill runner.

See the [complete skill index](CATALOG.md) for source folders and website links.
The prepared local collection covers all 125 catalogue skills and both ecommerce
profile skills. Skills are added to the main branch individually through pull requests;
the source index lists the packages included at each commit. Site purchase/access conditions and each skill's runtime
requirements still apply to the website experience. A public source repository
also lets people obtain and run its available source directly.

## Use a skill

Choose a folder under `skills/` and read its `SKILL.md`. Keep the whole folder
together: scripts, reference files and assets may be required. Install that
folder using your agent's supported skill-installation workflow, then give the
agent your brief and inputs. Dependencies and tool/provider usage vary by skill;
read its instructions before running bundled commands.

Rendered demo exports are hosted separately through the website. Reusable
example briefs and input assets remain here where supplied. References to
omitted local example renders should be viewed through the website instead.
There is no requirement to install all skills together.

## Collection structure

```text
skills/<skill-name>/SKILL.md   Skill entrypoint and supporting source files
CATALOG.md                   Source index and website links
catalog.json                 Site mapping, file hashes and omitted demo outputs
LICENSE                      MIT for repository tooling and original packages
LICENSING.md                 Scope and third-party release limitations
scripts/sync.py              Import updates from the website workspace
scripts/validate.py          Check the standalone source collection
```

## Maintain the collection

This is a separate local Git repository. The existing `.agents/skills/`
authoring folders and website catalogue remain authoritative during this
initial setup. Existing site packaging and download delivery have not changed.

From this repository, after authoring or adding a skill to the website:

```sh
python3 scripts/sync.py
python3 scripts/validate.py
python3 scripts/sync.py --check
```

For another workspace location, pass `--workspace /path/to/claudeai.directory`
to `sync.py`. The sync reads the catalogue and profile download manifests,
imports all listed packages, refreshes the index, and detects source drift.
It refuses to overwrite locally modified imported files or silently delete
removed sources. Reconcile those changes with the authoring folders first.

Run `python3 scripts/validate.py` in a standalone checkout to verify the imported
files without needing the website workspace. This validates package structure,
source hashes and coverage; it does not claim every skill has been executed in
every agent environment.

## Publication status

This collection is prepared locally. No GitHub remote or public release has
been created. Original packages in this collection use MIT, with embedded
third-party notices preserved. Twenty-one adapted packages are included for
complete local coverage but still require third-party redistribution review.
See [LICENSING.md](LICENSING.md) before publishing this entire repository.
