# Task Loop Gif: four worked examples

The skill and four input briefs were written before rendering. These are original fictional campaign demos, not screen recordings of real email or CRM actions. The same bundled renderer produced all four without changing the skill between topics.

## Reuse

Tell your agent your audience, workflow, brand, approved capabilities and CTA. It writes the brief for you. Change inputs, not SKILL.md. Run from any directory using the renderer’s installed path.

## A welcome sequence with a purpose

Authored request:

```text
Use $task-loop-gif to create a 12-second looping a welcome sequence with a purpose demo for the fictional brand Letterwell. Use the supplied input.json, the paper palette and the CTA "Explore the welcome flow". Export the 720 x 900 GIF/MP4, a 600px email GIF and a static fallback. Keep it labelled illustrative; do not send any messages.
```

Exact renderer invocation (installed paths normalized):

```sh
python3 <installed-skill>/scripts/render.py <installed-skill>/examples/welcome/input.json --out output/welcome
```

[Input JSON](../examples/welcome/input.json) · [GIF](../examples/welcome/output/workflow.gif) · [Email GIF](../examples/welcome/output/email.gif) · [MP4](../examples/welcome/output/workflow.mp4) · [Preview HTML](../examples/welcome/output/preview.html)

12 seconds; 720 × 900 master; 600 × 750 email GIF, 176,470 bytes. Reviewed fixed headline/CTA, ordered reveals, completion states, copy, contrast and final reading hold.

## From a demo request to the right owner

Authored request:

```text
Use $task-loop-gif to create a 12-second looping from a demo request to the right owner demo for the fictional brand Frontdoor. Use the supplied input.json, the forest palette and the CTA "See the inbound playbook". Export the 720 x 900 GIF/MP4, a 600px email GIF and a static fallback. Keep it labelled illustrative; do not send any messages.
```

Exact renderer invocation (installed paths normalized):

```sh
python3 <installed-skill>/scripts/render.py <installed-skill>/examples/inbound/input.json --out output/inbound
```

[Input JSON](../examples/inbound/input.json) · [GIF](../examples/inbound/output/workflow.gif) · [Email GIF](../examples/inbound/output/email.gif) · [MP4](../examples/inbound/output/workflow.mp4) · [Preview HTML](../examples/inbound/output/preview.html)

12 seconds; 720 × 900 master; 600 × 750 email GIF, 182,680 bytes. Reviewed fixed headline/CTA, ordered reveals, completion states, copy, contrast and final reading hold.

## Research before reaching out

Authored request:

```text
Use $task-loop-gif to create a 12-second looping research before reaching out demo for the fictional brand Signaldesk. Use the supplied input.json, the midnight palette and the CTA "Get the research workflow". Export the 720 x 900 GIF/MP4, a 600px email GIF and a static fallback. Keep it labelled illustrative; do not send any messages.
```

Exact renderer invocation (installed paths normalized):

```sh
python3 <installed-skill>/scripts/render.py <installed-skill>/examples/outbound/input.json --out output/outbound
```

[Input JSON](../examples/outbound/input.json) · [GIF](../examples/outbound/output/workflow.gif) · [Email GIF](../examples/outbound/output/email.gif) · [MP4](../examples/outbound/output/workflow.mp4) · [Preview HTML](../examples/outbound/output/preview.html)

12 seconds; 720 × 900 master; 600 × 750 email GIF, 170,255 bytes. Reviewed fixed headline/CTA, ordered reveals, completion states, copy, contrast and final reading hold.

## Reconnect with inactive subscribers

Authored request:

```text
Use $task-loop-gif to create a 12-second looping reconnect with inactive subscribers demo for the fictional brand Rekindle. Use the supplied input.json, the plum palette and the CTA "Explore the reactivation flow". Export the 720 x 900 GIF/MP4, a 600px email GIF and a static fallback. Keep it labelled illustrative; do not send any messages.
```

Exact renderer invocation (installed paths normalized):

```sh
python3 <installed-skill>/scripts/render.py <installed-skill>/examples/reactivation/input.json --out output/reactivation
```

[Input JSON](../examples/reactivation/input.json) · [GIF](../examples/reactivation/output/workflow.gif) · [Email GIF](../examples/reactivation/output/email.gif) · [MP4](../examples/reactivation/output/workflow.mp4) · [Preview HTML](../examples/reactivation/output/preview.html)

12 seconds; 720 × 900 master; 600 × 750 email GIF, 159,959 bytes. Reviewed fixed headline/CTA, ordered reveals, completion states, copy, contrast and final reading hold.

## Limits

Same-agent authored evaluation, not independent customer testing. No real messages sent, account research performed or CRM connected. Email clients were not tested. GIF and MP4 are silent; example CTA URLs are intentionally absent. Fonts are bundled with their OFL licences.
