---
name: task-loop-gif
description: Create looping workflow-demo GIFs for email marketing, inbound lead handling and outbound campaigns, with a fixed headline and CTA around animated requests, results and progress. Exports GIF, MP4, a static fallback and editable source from a fresh brief.
---

# Task Loop Gif

Turn one marketing workflow into a readable animated product demonstration. The visual pattern keeps the promise and CTA visible while the central panel reveals short requests, outcomes and completion states. Accept a normal-language brief; write the JSON inputs for the user. Do not require editing this skill to change their brand, topic or offer.

## Shape the story

Resolve the audience, workflow, brand, destination, CTA and approved product capabilities. Default to a silent 4:5 creative and an email-width GIF. Use 3–5 meaningful beats, such as a trigger, selection, preparation, review and handoff. Give the last result a reading hold before restarting. A campaign about a welcome sequence should show that sequence, not inherit an SDR prospecting script.

Use a fixed two-line headline, a concise promise, an application-like panel, supporting capability chips and one CTA. Pair editorial serif display type with plain sans-serif UI text; use restrained accent color and generous spacing. Choose a palette appropriate to the brand. The bundled renderer offers paper, midnight, forest and plum treatments; these are starting points, not mandatory brand identities. Use the user's exact supplied claims. Omit logo marks when no authorized logo is supplied; a text brand label is supported.

Label fictional demos as illustrative. Do not fabricate verified emails, lead counts, booked meetings, response rates, setup times or live tool execution. A rendered sequence does not perform the workflow. Prefer draft/review/route language when no real execution evidence is supplied. The user-provided reference is inspiration for motion structure only; do not bundle its logo, copy or GIF.

## Build

Read [the input schema](references/schema.md) and write a new brief JSON. Requirements: Python 3.10+, Pillow and FFmpeg/FFprobe with libx264. Fonts and licenses are bundled. No browser automation, image model, API key or paid rendering service is required.

```sh
python3 <installed-skill>/scripts/render.py brief.json --out output/version-01
```

Use a new output directory. The renderer rejects text that cannot fit instead of truncating it. Fix the brief or deliberately revise the layout and rerender. It supports 640–1080px master widths at 4:5, 3–5 beats, 8–24 seconds and 10–30fps MP4. The GIF uses 10fps; this is a workflow demonstration, not character or live-action animation. Arbitrary layouts, alternate aspect ratios, screenshots and logo files require an explicit renderer adaptation.

## Review and deliver

Review the entire playback plus first, middle and final frames. Check spelling, progressive reveals, result timing, CTA persistence, clipping and the loop transition. The first GIF frame must communicate the main promise and CTA without animation. Keep the background stable and animate only the active content. Do not use flashes or pretend the image itself is a clickable interface.

Deliver `workflow.gif`, `email.gif` (600px wide), `workflow.mp4`, `poster.png`, `first-frame.png`, `preview.html`, `email.html`, `brief.json` and `render-report.json`. Inspect actual file sizes. The renderer targets an email GIF under 1MB, reports whether it achieved that target, and does not guarantee every mail provider accepts it. If too large, shorten the story or reduce the GIF color count after reviewing quality. Do not conflate a platform limit with this editorial target.

Read [email delivery notes](references/email.md) when the GIF will go inside a campaign. Set the real CTA URL and image hosting URL before sending; keep meaningful alt text and repeat the action in live HTML text. Preview in the intended email client. The local email snippet is a starting point, not a tested inbox-delivery guarantee. Creating these assets does not send email, connect a CRM or start outreach.

See [worked examples](references/usage-examples.md) for four different briefs, exact render commands and completed exports. Change the brand, narrative, labels and CTA through inputs rather than copying a demo's claims.
