---
name: cad-department-map-infographic
description: Create a LinkedIn department or capability map with six grouped role cards arranged around a central topic symbol and color-coded connectors.
metadata:
  author: Claude Directory
  ownership: original-workflow
  version: 1.0.0
---

# Department Map Infographic

Create a LinkedIn department or capability map with six grouped role cards arranged around a central topic symbol and color-coded connectors.

## Visual contract

Portrait near-square infographic on white. Bold oversized dark-navy headline at top with the topic phrase in coral. Subtitle gives the exact role count. Central large original thematic symbol. Six rounded pastel department cards arranged as three rows with a left and right column around the central symbol. Each card has a short bold heading capsule, one simple outlined circular icon above it, and three left-aligned bullet roles. Curved dashed colored connectors join the cards to the center. Purple, coral, mint, pink, blue and violet distinguish departments. Keep all connectors out of text. No brand logos, fake credentials or invented people.

Match this layout grammar even when the topic changes. Topic and palette are runtime inputs; example brands and wording are never defaults. Keep a clear hierarchy, repeated spacing and a single obvious reading order. Do not replace the reference pattern with a generic illustration.

## Inputs and content

Accept a normal-language request with topic, audience, exact title, grouped items, optional subtitle, palette, aspect ratio, logo and footer/CTA. The user never needs to edit SKILL.md. Read [four example briefs](references/examples.json) to see contrasting topics using this same pattern. Use their structure, not their topic or wording. Read [worked examples](references/worked-examples.md) when running or adapting a packaged example.

If the user gives only a topic, draft a concise content map and label assumptions before rendering. For external tool capabilities, rankings or statistics, verify supplied facts or use capability labels instead. Do not invent tool logos, data, credentials, affiliations or social performance. A reference screenshot establishes visual style, not truth. Use supplied exact logos only when requested; otherwise use original simple icons. Omit absent logos and footers cleanly. Never insert Claude Directory branding automatically.

Freeze the final copy and count all groups/items before generation. Titles with a number must match the actual item count. For dense copy, shorten with the user's intent preserved or increase canvas space; never silently drop a row. Folder maps must distinguish illustrative files from files actually included in a deliverable.

## Generate from the skill

Create one real raster per requested output using the available image-generation tool. Render the whole infographic with the exact content map and visual contract. A prompt alone is not an output. No particular image provider is guaranteed by installing the skill; explain a missing tool rather than pretending Claude Code can generate images natively. Tool usage charges depend on the user's environment.

Use one independent render per example. Four examples must change the subject, content and associated icons; crops and recolours do not count. A set should preserve the pattern while demonstrating different usable topics. Default to one image for normal requests, four only when requested.

Save every attempt with its prompt, input brief, tool, actual dimensions and skill-source hash. Inspect every word, number, icon, connector and margin at full size and at a readable feed preview. Check row/column alignment, group membership, exact counts, label spelling and unrequested branding. Correct a specific failure with the image tool and keep the rejected attempt. Stop after two unsuccessful corrections to the same issue and report it honestly.

Deliver the accepted image, editable content brief, copyable skill invocation, full generation prompt, alt text and a short review record. These inputs are editable; the raster is not a layered design file. Record measured resolution and any mismatch from the requested size. Do not claim virality, LinkedIn performance or fully verified facts from the visual alone.
