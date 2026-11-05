# After installing

Paste into your coding agent's chat:

> Use $schedule-shuffle for [product URL or fictional concept]. My message is [one sentence]. Show [three relevant actions or elements]. Use the official website's colors and logo on a white background. Make a [landscape or square]18-second video, ending with [call to action]. Review the scenes and deliver the MP4 plus editable brief. Use [my licensed music file] with [publishing credit], or render silently.

The agent should inspect your website, copy an example JSON and adapt the fields in references/input.md. You can change brand, headline, ending, call to action, labels, details, accent, ink, logo and format.  Choreography lives in the named component and can be edited for a new story. There is no marketplace comment field that configures the renderer; you give these instructions to your agent after installation.

Command from renderer: `npm ci`, then `node render.mjs ../examples/01-landscape.json /absolute/new-output --stills`. Review, then render without --stills. Deliverable files include film.mp4, brief.json, storyboard.json and render-report.json. The package includes two recorded examples and their exact prompts; raw licensed music is not included.
