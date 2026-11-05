# Input contract

UTF-8 JSON with required `brand` (24 characters), `title` (46), `subtitle` (88), `source` (85) and `theme` (chalk, ink, rose, cobalt). Every text value must be nonempty and single-line. Limits are preliminary; measured font width may reject a shorter wide string. Bundled fonts and validation cover Latin-script copy; other writing systems need suitable fonts, validation and fresh review.

## Technique fields

`options`: two objects with `name` (23 characters), `summary` (42). `criteria`: three objects with `label` (18), `left` and `right` (28 each). Keep labels parallel and values comparable. Source every factual competitive claim; examples are explicitly fictional.

## Truth and formatting

The `source` line is visible in the film. Use a real supplied source or clearly label illustrative material. Never convert an example into a claim about a customer or real product. Bar values display up to one decimal; radial values retain supplied final percentages. Dates are authored labels, not a guarantee or a proportional scale. The renderer does not validate real-world truth.

## Output files

`film.mp4`, `poster.png`, `brief.json`, `preview.html`, five review PNGs, encode log and `render-report.json`.  Reports record input, renderer, config, fonts and output hashes, full video decode and exact frame counts. Keep local source assets with the input brief; an external logo file is hashed but is not copied into the output folder automatically.
