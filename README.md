# Awesome Agent Skills

Reusable workflows for making images, videos, presentations, learning material
and practical business documents with AI agents.

[Browse all skills](CATALOG.md) · [Get started](#get-started) · [Contribute](CONTRIBUTING.md) · [MIT licence](LICENSE)

A skill gives your agent a repeatable way to handle a particular job. Each folder
contains its instructions, supporting references and any scripts, templates or
editable examples needed for that workflow. The full reusable source is public.

## Sponsor

**[ToolJunction](https://tooljunction.io)** supports this collection.
Discover AI tools, startup credits and perks for your next project.

[Explore ToolJunction →](https://tooljunction.io)

## What would you like to make?

| Make something | Start with |
| --- | --- |
| Product and campaign images | [Benefit Panels](skills/benefit-panels/SKILL.md), [Wardrobe Campaigns](skills/wardrobe-campaigns/SKILL.md), [Punchy Photo Cards](skills/punchy-photo-cards/SKILL.md) |
| Videos and motion | [Talking Models](skills/talking-models/SKILL.md), [Words In Motion](skills/words-in-motion/SKILL.md), [Clip Assembler](skills/clip-assembler/SKILL.md) |
| Presentations and proposals | [Funding Story](skills/funding-story/SKILL.md), [Recommendation Room](skills/recommendation-room/SKILL.md), [Client Offer Builder](skills/client-offer-builder/SKILL.md) |
| Learning material | [Memory Drills](skills/memory-drills/SKILL.md), [Visual Learning Pages](skills/visual-learning-pages/SKILL.md), [Drawn Lessons](skills/drawn-lessons/SKILL.md) |
| Business and ecommerce documents | [Merchant Intake](skills/merchant-intake/SKILL.md), [Listing Copywriter](skills/listing-copywriter/SKILL.md), [Voice Of Buyer](skills/voice-of-buyer/SKILL.md) |
| Diagrams and visual explanations | [Team Atlas](skills/team-atlas/SKILL.md), [Concept Layers](skills/concept-layers/SKILL.md), [Workspace Atlas](skills/workspace-atlas/SKILL.md) |

**[See the complete collection →](CATALOG.md)**

## Get started

Clone the repository, or download its ZIP using GitHub's **Code** menu:

```sh
git clone https://github.com/dipakkr/awesome-agent-skills.git
cd awesome-agent-skills
```

Open the folder in your coding agent and point it at a skill:

```text
Read skills/merchant-intake/SKILL.md and follow its workflow.

I am preparing a small homeware store. Help me organize my product facts,
audience and brand voice into a reusable brief. Ask for missing information
when it affects the result, and clearly mark anything we have not confirmed.
```

For another task, choose a different `SKILL.md` from the index and provide your
own brief, files and constraints. For automatic skill discovery, install the
**whole skill folder** using your agent's supported installation workflow.
Keep its scripts, reference files and assets together.

## Give your agent useful inputs

Tell it what you want to make, who it is for, where it will be used, and which
facts or assets must stay unchanged. Include dimensions, duration or format when
relevant. Specify the output folder and any spending or tool restrictions.

Example:

```text
Read skills/punchy-photo-cards/SKILL.md.

Create a social image for my ceramics workshop using the attached photo.
Keep the supplied logo unchanged. Use the headline “Make something by hand”.
Save the image, prompt and editable brief in ./output/workshop.
Use only tools already available in this session.
```

The skill's own instructions describe its required inputs, steps and review
criteria. Check the result against your source material before publishing it.

## Requirements and outputs

- Use an agent that can read workspace files and follow skill instructions.
- Some skills need image generation, document tooling, Python, Node.js, FFmpeg
  or a browser. Read the selected skill before installing dependencies.
- Provider subscriptions and generation usage are separate from this repository.
- Outputs vary: images, videos, decks, briefs, structured files or editable code.
  A skill's presence here does not establish compatibility with every agent.

Reusable example briefs and source assets are included where available. Large
rendered demo exports are omitted. The source index is text-only.
For a visual browsing experience, visit [Claude Directory](https://claudeai.directory).

## Explore a skill folder

```text
skills/<name>/
├── SKILL.md       Instructions and workflow
├── scripts/       Helpers, when the workflow needs them
├── references/    Contracts, guidance and supporting material
├── assets/        Reusable templates or source assets
└── examples/      Editable example inputs
```

Folders vary by skill. `catalog.json` records the source inventory and hashes.
Verify the collection locally with:

```sh
python3 scripts/validate.py
```

Validation checks package structure and file integrity. Individual skills may
provide additional checks for their actual outputs.

## Contribute

Improve a workflow, report a reproducible problem, or propose a new skill.
Keep each skill addition in its own pull request. Include clear instructions,
required source files, licence notices and an honest account of what you tested.
See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow.

## Licence and credits

Original instructions and code use [MIT](LICENSE). Embedded fonts, libraries and
other third-party materials retain their notices and terms. See [LICENSING.md](LICENSING.md).
Maintained by [Deepak](https://github.com/dipakkr).
