---
name: talking-models
description: Create a vertical Instagram explainer with an original 3D student and robot tutor, a progressive whiteboard analogy, two synthetic voices, reaction shots and timed captions. Use for short beginner lessons, educational reels and technical explainers with editable source and an actual MP4.
---

# Talking Models

Turn one beginner question into a short conversation between Milo, a curious student, and Pip, a small robot tutor. Teach through a concrete analogy, map it to the real concept, state one limitation, and finish with a light joke. The supplied video is a structural reference; do not copy its characters, restaurant dialogue, creator handle, watermark or footage.

## Start with the lesson

Read [the example guide](references/usage-examples.md), [input contract](references/input-contract.md) and [audio setup](references/audio-setup.md). Ask only for information that is missing: topic, audience, approved facts, language and preferred audio provider. If the user supplied a reference, inspect its visuals and narration first. Reuse established preferences and available authorized configuration. Never ask for a secret in chat.

Write a fresh brief. Use 8–20 short turns and at most 180 words. Give the student real questions and the tutor useful explanations. Avoid making the learner appear foolish. Keep the analogy accurate and say where it stops working. Verify niche or changing claims with primary documentation and save the sources. The included lessons are educational simplifications, not complete implementation guides.

Use the built-in visual grammar when it fits: four room palettes, wide/student/tutor/board shots, one to three diagram nodes, flow/cycle/queue diagrams and twelve icon types. Board states should change as the explanation develops. Change the subject, analogy, diagram, dialogue and palette across examples; a recolored duplicate is not a new worked example. For anatomy, detailed machinery, new characters or a different scene, extend the editable React/Three.js source deliberately instead of pretending the fixed renderer supports it.

## Generate the audio first

Claude, Codex or Cursor orchestrates the script and rendering. This skill does not add a speech model to the host agent. Select a configured TTS service or supplied recordings. No API keys are included.

```sh
python3 <skill>/scripts/prepare.py my-brief.json --out output/lesson-01 --provider elevenlabs --env-file /private/path/voices.env
```

Supported provider arguments: `elevenlabs`, `fish`, `openai`, `recorded`. The four bundled examples use OpenAI's `marin` and `cedar` voices. ElevenLabs and Fish adapters are documented integrations; they have not been live-tested in this package. The OpenAI Speech adapter uses a currently available but deprecated model; read the dated note in audio setup before selecting it for a new installation.

Generate each dialogue turn separately, measure its actual duration and build the timeline from the result. The renderer uses measured speech energy to open the speaking character's mouth. This is simple amplitude-based animation, not phoneme-accurate lip synchronization. Captions are timed by turn, not word. Review pronunciation, pacing and wording before accepting the film. Do not silently switch providers when a call fails.

Preparation refuses an existing nonempty directory. `--resume` reuses cached turns only for the same input file and provider. To change a voice, model or script, use a fresh output directory. `--validate-only` checks a brief without making calls. For existing narration, provide `--provider recorded --audio-dir /path/to/turn-wavs`; name the files `00.wav`, `01.wav`, and so on. Keep the script consistent with those files. This mode displays “Supplied narration” rather than claiming it is AI-generated.

## Render and inspect

Requires Python 3.10+, Node.js 22+, npm, FFmpeg/FFprobe and the pinned dependencies. Initial setup needs network access for npm packages and Remotion's Chromium renderer. Rendering happens locally. Remotion has its own [license and plans](https://www.remotion.dev/license); the original skill source does not grant rights to third-party software or speech services.

```sh
cd <skill>/renderer
npm ci
node render.mjs /absolute/path/to/output/lesson-01 --stills
# Inspect the review images, then render the full film:
node render.mjs /absolute/path/to/output/lesson-01
```

Stills cover every turn and the ending. Inspect title/board separation, diagram legibility, caption length, framing, speaking character, hands and pointer. All animation must remain driven by the frame clock; do not use uncontrolled timers or a live render loop. Use normal-speed cuts and a small camera drift. Keep captions away from the right-side social controls and the bottom action area. The layout is a practical safe-area guide, not a guarantee for every Instagram crop or overlay.

The default film is 720×1280 at 30 fps, matching the supplied reference resolution. Duration follows the actual narration, typically 50–60 seconds for these examples. Render a higher resolution by updating the composition and proportional typography together, then review again. Do not upscale and call it newly rendered detail.

## Deliver the complete result

Deliver `film.mp4` with audible narration, `poster.png`, `voice.wav`, per-turn audio, `captions.srt`, `brief.json`, `timeline.json`, `preview.html`, review frames and `render-report.json`, plus the editable source. The receipt records hashes, dimensions, actual duration, audio codec and provider/model/voice names. It never contains the key.

For a catalogue addition, run four distinct briefs and include each exact prompt, editable input and finished output. Record which providers were actually tested. Author-executed rendering does not establish independent agent/customer reuse or audience performance. Keep synthetic-voice disclosure visible. Use only authorized voices; no reference voice cloning is needed. Keep outputs local until the user requests publishing.
