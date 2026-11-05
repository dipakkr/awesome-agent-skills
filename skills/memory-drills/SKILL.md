---
name: memory-drills
description: Turn supplied learning material into handwritten active-recall worksheet images with answer space and a separate, clearly aligned answer key.
metadata:
  author: Claude Directory
  edition: 1.0.0
---

# Memory Drills

Turn supplied learning material into handwritten active-recall worksheet images with answer space and a separate, clearly aligned answer key. Create original notebook artwork. Use the source to decide the structure; the examples are adaptable recipes, not fixed templates.

## Start from the request

Accept the source or topic, learner level, language, page count, paper texture (graph, ruled, dotted or plain), palette, and output aspect ratio in the conversation. Default to one portrait study sheet, a subtle paper texture and no branding. For A4 printing, request a near-A4 ratio and report actual pixels; do not call a small raster image print-ready or editable text.

Read supplied PDFs/photos with available document or vision tools. Record page references and unclear passages in an editable brief. Do not guess illegible equations, dates, technical labels or missing pages. With a topic alone, write an original explanation and verify unfamiliar or current claims; do not imply a textbook was supplied. Separate source facts from added teaching examples in the brief and, when useful, with a small visible legend.

## Plan the learning page

Design questions that can be answered from the supplied material. Mix retrieval, explanation and a short application where appropriate. Create the answer key first and check that each question has a matching answer or, for open writing tasks, an explicit evaluation criterion. Leave genuinely blank space to write. Keep answers in a clearly separated lower panel marked “Cover before answering”, or on a separate page when requested. Do not accidentally reveal answers in nearby diagram labels. A fold line must not cross question text. Avoid upside-down generated text; a separate answer page is more reliable.

Use fine dark ink, readable handwriting, pale paper lines, restrained translucent highlighter and small purposeful sketches. Vary composition, paper and visual devices across a collection; do not merely recolour the same template. Keep generous outer margins and strong contrast. Decorative tape or binding should not consume the writing area. Do not copy a reference site's wording, branding or illustrations.

## Generate and check

Use the available image-generation tool for the finished raster artwork. Pass the exact approved visible copy, diagram relationships, page layout, palette and blank-space requirements. Keep equations short and explicit. A tool without image generation can prepare the brief and prompt but must say it has not produced the image; it should not silently substitute a screenshot or SVG.

Inspect the generated image at full size and at reading size. Check every word, fraction, answer number, arrow direction and diagram count against the brief. Reject plausible-looking but incorrect educational diagrams. Correct errors with image editing or simplify and regenerate, retaining versioned originals. Record actual tool, prompt, source links, dimensions and review findings. Do not claim every future topic or model was validated from the bundled examples.

Deliver the PNG or WebP, editable copy/brief, full prompt and a short review note. Raster handwriting is not editable text. A PDF or additional format is optional and requires a real export and inspection, not a renamed file.

## First use

After extracting this folder into your agent's skill directory, open the agent and invoke this skill with your material. In Claude Code a project installation can use `.claude/skills/`; in Codex use `.agents/skills/` or `~/.codex/skills/`. If your host does not discover skills, attach SKILL.md and ask it to follow the instructions. Image generation must be available separately; installing this file does not provide a model or API credits.

Read [usage examples](references/usage.md) for a copyable request. The `examples/` folder contains the exact briefs, full prompts and original generated examples for four topics. Change your request to change the subject; do not edit SKILL.md for each new topic.
