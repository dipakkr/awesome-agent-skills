# Four complete worked examples

All four use the same renderer and original characters. The theme, analogy, diagrams, camera sequence and dialogue vary. Each example includes its exact invocation in `prompt.txt`, editable `brief.json`, finished film and supporting output in `recorded/`. The recorded voices use OpenAI `marin` for Milo and `cedar` for Pip.

| Example | Teaching idea | Visual pattern |
| --- | --- | --- |
| caching | A library book copied to a desk; stale copies need refreshing. | Mint study; library/desk/source diagram. |
| webhooks | A doorbell announces an event; verify the sender and handle repeats. | Peach workshop; polling cycle becomes an event flow. |
| rate-limits | A turnstile paces traffic; backoff prevents a retry storm. | Violet room; gate, 429 response and retry clock. |
| job-queues | Cafe tickets separate ordering from doing the work; retries need care. | Night studio; moving queue indicators and worker flow. |

## Reproduce an example

```sh
python3 <skill>/scripts/prepare.py <skill>/examples/caching/brief.json --out output/cache-replay --provider recorded --audio-dir <skill>/examples/caching/recorded/audio
cd <skill>/renderer
npm ci
node render.mjs /absolute/path/to/output/cache-replay
```

This uses the recorded audio and does not call a voice API. It is a source-reproducibility test, not a fresh narration test.

## Ask for a new lesson

> Use $cad-3d-dialogue-explainer to explain DNS to nontechnical ecommerce founders. Build a new address-book analogy and a clear three-node diagram. Use the peach room, Milo and Pip, two configured ElevenLabs voices and a short final joke. Verify the facts, write a fresh brief, generate matching narration, derive timing from the real audio and render the full vertical MP4. Keep captions readable, include the synthetic-voice disclosure and deliver the editable input, source, captions and render receipt. Keep everything local.

Change the topic and provider to suit the request. The DNS prompt is an invocation example, not one of the four recorded outputs. Exact prompts for the actual tested topics are stored alongside their briefs.

## Why the prompts work

They specify the audience, teaching scope, analogy, scene, voices, output and verification. The user supplies intent; the agent converts it into a valid brief, selects a configured provider, generates audio before timing the picture, checks every shot, then renders. The agent should learn the pattern from the examples, not recycle their dialogue for an unrelated topic.
