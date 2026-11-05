---
name: comic-lab-scenes
description: Create funny narrated 3D explainer reels with a confident misunderstanding, expressive student and deadpan robot, animated prop gags, reaction cuts and a useful takeaway. Includes editable scripts and a local vertical-video renderer.
---

# Comic Lab Scenes

Make the audience laugh at the situation, then understand one idea. This is a short two-character skit, not a lecture with a joke appended. The package is standalone: its original Milo/Pip character geometry and audio pipeline are adapted from Claude Directory's Talking Models, with new comedy staging and scripts.

New to the package? Follow [START-HERE.md](START-HERE.md) for setup and a ready-to-paste AI Evals request.

## Write a fresh skit

Read [comedy-writing.md](references/comedy-writing.md) for the beat structure and [input-contract.md](references/input-contract.md) for renderer controls. Start with the topic, audience and one accurate takeaway. Use supplied product facts for branded work. Invent characters and situations freely, but do not invent product capabilities or results.

Write a confident misunderstanding in the first line. Show its absurd consequence with a prop; let the robot puncture it with one short deadpan line. Explain the idea through dialogue, then return to the opening mistake with a new meaning. Make the joke understandable with sound off. Aim for 90–120 spoken words, usually 35–50 seconds with two voices. Real duration comes from recorded speech.

Use `examples/*/brief.json` as working structure, not text to copy. Five supplied examples cover cloud storage, browser cookies, email automation, freelance scope creep and AI evaluations. Choose fresh content, a relevant prop and different punchlines for a new user. For script-only requests, deliver the dialogue, actions, shot list and takeaway without generating audio.

## Prepare matching narration

Requires Python 3.10+, FFmpeg/FFprobe, Node.js 22+ and npm. New speech needs the user's configured provider; see [audio-setup.md](references/audio-setup.md). Supported adapters: OpenAI, ElevenLabs, Fish Audio, or supplied WAVs. Only OpenAI was live-tested for these examples. The bundled OpenAI Speech adapter has a documented January 2027 compatibility limit; do not silently swap models or providers.

```sh
python3 <skill>/scripts/prepare.py brief.json --out output/my-skit --validate-only
python3 <skill>/scripts/prepare.py brief.json --out output/my-skit --provider openai --env-file /private/path/voices.env
```

Preparation sends the dialogue to the chosen speech service, measures each WAV and derives the timeline, mouth energy, caption JSON and SRT. Credentials stay outside output. `--resume` reuses cached speech for the identical brief/provider; use a fresh directory for changed voices, settings or text. Provider failures stop the run. Never substitute silent footage and describe it as narrated.

For an offline replay, use `--provider recorded --audio-dir <skill>/examples/cloud-weather/recorded/audio`. Keep that example's text unchanged. For a new script, supply matching recordings. Mark synthetic recordings with the appropriate disclosure when adapting the source.

## Render and review

```sh
cd <skill>/renderer
npm ci
node render.mjs /absolute/output/my-skit --stills
node render.mjs /absolute/output/my-skit
```

First setup downloads pinned dependencies and the browser renderer. Local output is 720×1280 at 30 fps. Review the hook, every reaction/diagram and closing card. Check the punchline has a short hold, faces stay visible, captions fit, diagrams explain the actual concept, and the final joke does not undo the lesson. Then render and watch the MP4 with audio. The renderer checks full decode and records source/output hashes.

Deliver `film.mp4`, `poster.png`, `brief.json`, `timeline.json`, `voice.wav`, `captions.json`, `captions.srt`, `preview.html`, `render-report.json` and editable source. Include the fresh invocation and any limits in a short handoff. Keep posting or publishing outside this workflow unless requested.

## What is customizable

Four palettes, four prop animations, five reactions, four camera shots, staged diagrams, tag cards and per-turn comic pauses. Change dialogue, teaching sequence, punchlines and timing in JSON. Add geometry or modify `renderer/src/Film.jsx` for new props, characters or physical actions; the schema does not generate arbitrary 3D scenes from prose.

Mouth movement follows audio energy, not phonemes. Captions follow full dialogue turns, not individual words. English vertical reels are the tested format. Example quality checks are author-executed; no claims of audience success, virality or independent customer validation. Runtime dependencies and speech providers have their own licenses, terms and costs.

See [usage-examples.md](references/usage-examples.md) for the five complete worked outputs and a fresh request pattern.
