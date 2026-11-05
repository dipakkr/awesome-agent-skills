# Make your own Device Handoff video

After installing, open the project where you want the new video in your coding agent. Ask the agent to use this skill by name. This happens in the agent chat, not a marketplace comment. There is no separate customization form on the marketplace today.

## Paste this prompt

Use $screen-to-screen to make a NEW video for [PRODUCT NAME].
- Purpose and audience: [what the product helps people do, and who it is for].
- Appearance: [white/light or black/dark] background, [bright accent color].
- Format: [landscape 16:9, portrait 9:16, square 1:1, or all three].
- Opening headline: [short headline].
- Item carried between devices: [short project or idea name].
- Story: capture on phone, develop on laptop, present on tablet. Use [your actual steps and approved wording].
- Screen files: [phone image path], [laptop image path], [tablet image path]. If I do not supply screens, use clearly labelled fictional mockups.
- Ending headline: [short ending]. Call to action: [CTA]. URL: [URL].
- Music: [authorized music path and publishing credit, or silent].
Create a new output folder. Show me scene previews first, check every requested format, then render the complete MP4 and include editable source, the input brief and music credits.

You can write this in ordinary language; the agent maps it into a JSON brief. You do not need to edit code or JSON yourself. If skill-name invocation is not recognized by your agent, reference the installed SKILL.md file path and ask the agent to read and use it.

## What can change?

| Choice | Supported directly | When source adaptation is needed |
| --- | --- | --- |
| Background | theme:light or theme:dark; omitted means dark | Other stage designs or custom materials |
| Output shape | landscape, portrait, square at1080p30fps | Other sizes or frame rates |
| Brand and copy | brand, opening, ending, CTA, URL, item and chapter captions | Longer copy or different languages may need new layout/font checks |
| Accent | Six-digit hex color, used for cards and CTA | Dark accents need adjusted text contrast |
| Device screens | Three local PNG/JPG/WebP files; image aspect ratios preserved | Screen recordings, animated UI states, extra devices or custom hardware |
| Built-in concept | Notes or design-board interface | Other mockup interfaces and workflows |
| Length and scenes | Current authored timeline is24seconds, six scenes | Shorter/longer films or different choreography require source/timeline edits |
| Sound | Supply cleared music + a credit file, or render silent | Narration, sound effects or beat-specific cuts require an extra audio pass |
| Logo | Text brand name | Graphic logo placement requires a scene edit |

The agent may adapt the included source for these requests, but should disclose the extra work and verify the new result. The skill provides a reusable starting structure, not arbitrary video generation from any prompt.

## What you receive

A new film.mp4 and editable project, brief.json, poster.png, scene review frames and render-report.json. MUSIC-CREDITS.txt accompanies supplied music. The downloadable examples are references; your new film is generated from your brief. Existing accepted examples should not be overwritten.

The renderer requires Node22+, FFmpeg/FFprobe and the pinned Remotion dependencies. Ask your agent to check these before rendering. Remotion and agent usage have separate terms. The included recorded films use credited music; standalone tracks are not bundled.
