# Workflow brief

All copy is supplied at runtime. The script has no campaign brand, headline or workflow baked into it. UTF-8 text supported by the bundled fonts is drawn as text; emojis and unsupported scripts require a suitable font adaptation.

Required JSON fields:

| Field | Contract |
| --- | --- |
| brand | Short text brand, up to 28 characters |
| eyebrow | Short campaign label, up to 32 characters |
| headline | Array of exactly two short lines, up to 28 characters each; second line uses the accent |
| subtitle | Up to 100 characters, wrapped to two lines |
| panel_title | Up to 36 characters |
| beats | 3–5 objects with `request` (up to 78 characters) and `result` (up to 78 characters) |
| chips | 2–4 short capability labels, up to 24 characters each |
| cta | Up to 36 characters |
| alt | Meaningful image alternative text, up to 220 characters |
| disclosure | Short visible evidence label, up to 70 characters |

Optional: `theme` (`paper`, `midnight`, `forest`, `plum`, default `midnight`), `duration` (8–24 seconds, default 12), `width` (even 640–1080, default 720), `fps` (10–30, default 24), `cta_url` (HTTPS URL, default empty). Height is width × 1.25 rounded to an even number. Width affects export size, not the content grid.

The layout checks actual text bounds against allotted rectangles at render time. Character limits are a preliminary check, not a guarantee of fit. The script writes a receipt with geometry checks, SHA-256 hashes, decoded dimensions, durations and measured bytes.

The optional URL becomes an anchor only in preview/email HTML. It is never fetched by the renderer. Without a URL, the email snippet contains the image and plain CTA text, without a fake destination. Replace the local `email.gif` source with the URL supplied by your email platform before sending.
