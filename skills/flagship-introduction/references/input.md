# Editable input

See the exact validation in `renderer/src/model.mjs` and the three authored briefs. All times are seconds on a 30fps timeline. Landscape is 1920×1080, portrait 1080×1920, square 1080×1080.

- `brand` max16, `category` max30, `hook`/`promise` max42 with intentional newline breaks, `cta` max28, `url` max32, `task` max60 characters.
- `words`, `steps`, `projects`: exactly three labels, each max20 characters.
- `theme`: black or white. `accent`: hex supporting >=4.5 contrast with black text. Accent is used for surfaces and graphic motifs; readable text uses the appropriate ink color.
- `motif`: rings, ribbons or grid. `seed`: nonnegative integer for synthesized score. `concept`: true for fictional examples.
- Optional portfolio `images`: three local paths relative to renderer/public. Supply images with valid usage rights; these replace procedural project art. Image content still needs manual review.

Typography and shot lengths are authored defaults. Longer content, additional features, voiceover or a different narrative need source adaptation and a fresh review. Formats change layout, not merely output geometry.
