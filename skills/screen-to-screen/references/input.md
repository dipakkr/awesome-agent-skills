# Input and art direction

mode:handoff; format:landscape1920x1080, portrait1080x1920 or square1080x1080 at30fps. brand1-16; headline/ending1-34; cta1-25; url1-32; item1-22; chapters:three strings1-26 characters; accent:six-digit hex; concept:boolean. subject:notes or design. Optional screens: three local public image basenames. Real demonstrations require these captures and concept:false. Device geometry is generic; no hardware brand is implied.

Keep one recognizable item across all screens. Hand-off moments at4-8s and12-16s use a shared accent card, not a random scene cut. The final device family should communicate continuity. Preserve legibility when camera perspective moves.

Change src/Handoff.jsx for choreography, src/model.mjs for timeline and validation. All animation is frame-driven. New dimensions and assets require independent visual review.

## Stage theme

Optional theme: light or dark. Omitted means dark for compatibility with earlier briefs. Light uses a white stage, dark headings and soft shadows; accent panels and supplied screen images retain their colors. Start from examples/03-white-landscape.json for the white variation. Formats and theme are independent.

## Delivery

The agent edits the brief and scene source, checks scene samples, then runs the renderer. The result is film.mp4 plus the input brief, poster, encoded review frames, render receipt and MUSIC-CREDITS.txt when music was supplied. Reusable source is included in this skill. Without --music the film is silent. For your own app, supply three screen captures; use concept:true for illustrative mockups.

The four earlier dark recordings preserve their original source hashes. Their renderer snapshot is in examples/recorded/source-dark-v1; the current renderer adds optional theme support.
