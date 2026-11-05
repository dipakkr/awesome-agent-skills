# 5 complete comedy reels

These are author-rendered, narrated examples. They are not claims of audience performance or independent customer validation. Each brief contains fresh dialogue, camera directions, prop gags, reactions and pauses.

## New request

Use `$cad-comedy-3d-explainer` to explain [topic] to [audience] in a funny vertical reel. The one takeaway is [fact]. Start with a confident misunderstanding, show a physical gag, teach the idea accurately and end with a callback. Use my configured voice provider and deliver the narrated MP4, script, editable brief and source.

## Cloudy with a chance of files

The roof is not a data center.

- Input: `examples/cloud-weather/brief.json`
- Exact invocation: `examples/cloud-weather/prompt.txt`
- Finished video: `examples/cloud-weather/recorded/film.mp4`
- Duration: 40.7 seconds; 720×1280, 30 fps, two synthetic voices.

```text
Use $cad-comedy-3d-explainer to make a funny vertical 3D explainer about cloud weather. Use a confident wrong assumption, a physical prop gag, a clear correction and a callback. Render the complete narrated MP4 with two original characters, reaction cuts, readable captions and editable source. This worked example follows examples/cloud-weather/brief.json. Generate matching speech with my configured provider and keep the AI voice disclosure.
```

## Where are my cookies?

The least delicious browser feature.

- Input: `examples/cookie-disappointment/brief.json`
- Exact invocation: `examples/cookie-disappointment/prompt.txt`
- Finished video: `examples/cookie-disappointment/recorded/film.mp4`
- Duration: 41.7 seconds; 720×1280, 30 fps, two synthetic voices.

```text
Use $cad-comedy-3d-explainer to make a funny vertical 3D explainer about cookie disappointment. Use a confident wrong assumption, a physical prop gag, a clear correction and a callback. Render the complete narrated MP4 with two original characters, reaction cuts, readable captions and editable source. This worked example follows examples/cookie-disappointment/brief.json. Generate matching speech with my configured provider and keep the AI voice disclosure.
```

## The apology machine

Automation needs a stop button.

- Input: `examples/apology-automation/brief.json`
- Exact invocation: `examples/apology-automation/prompt.txt`
- Finished video: `examples/apology-automation/recorded/film.mp4`
- Duration: 40.0 seconds; 720×1280, 30 fps, two synthetic voices.

```text
Use $cad-comedy-3d-explainer to make a funny vertical 3D explainer about apology automation. Use a confident wrong assumption, a physical prop gag, a clear correction and a callback. Render the complete narrated MP4 with two original characters, reaction cuts, readable captions and editable source. This worked example follows examples/apology-automation/brief.json. Generate matching speech with my configured provider and keep the AI voice disclosure.
```

## Just one tiny change

A small request with very large shoes.

- Input: `examples/tiny-change/brief.json`
- Exact invocation: `examples/tiny-change/prompt.txt`
- Finished video: `examples/tiny-change/recorded/film.mp4`
- Duration: 39.9 seconds; 720×1280, 30 fps, two synthetic voices.

```text
Use $cad-comedy-3d-explainer to make a funny vertical 3D explainer about tiny change. Use a confident wrong assumption, a physical prop gag, a clear correction and a callback. Render the complete narrated MP4 with two original characters, reaction cuts, readable captions and editable source. This worked example follows examples/tiny-change/brief.json. Generate matching speech with my configured provider and keep the AI voice disclosure.
```

## What is AI Evals?

A diploma is not an evaluation.

- Input: `examples/ai-evals/brief.json`
- Exact invocation: `examples/ai-evals/prompt.txt`
- Finished video: `examples/ai-evals/recorded/film.mp4`
- Duration: 53.2 seconds; 720×1280, 30 fps, two synthetic voices.

```text
Read cad-comedy-3d-explainer/SKILL.md and create a funny narrated vertical 3D reel titled "What is AI Evals?" for founders and marketers new to AI. Use Milo and Pip, a self-awarded diploma joke, a practical customer-support example, clear scoring criteria, inspection of failures and a callback ending. Explain that passing a test set is not a guarantee. Follow examples/ai-evals/brief.json for this worked example; generate fresh matching narration using my configured provider. Render the complete MP4 and deliver the readable script, editable brief, captions, poster and source.
```

## Replay without another voice call

Keep the example dialogue unchanged, then:

```sh
python3 scripts/prepare.py examples/cloud-weather/brief.json --out /absolute/output/replay --provider recorded --audio-dir examples/cloud-weather/recorded/audio
cd renderer
npm ci
node render.mjs /absolute/output/replay
```

The replay marks narration as supplied. The original recordings are synthetic OpenAI voices; preserve that disclosure when publishing them. New wording needs new matching speech.
