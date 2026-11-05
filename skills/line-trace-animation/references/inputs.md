# Inputs and limits

Common fields: `brand` (24 characters), `title` (46), `subtitle` (88), `source` (85), and `theme` (chalk, ink, rose, cobalt). Text is Latin-script with a limited punctuation set; geometry measurement may reject copy that is within the character cap but does not fit. Do not silently truncate.

`segments`: one to four cubic segments. Each segment is four [x,y] control points in 0..1. The last point of each segment must equal the next segment’s first point. `caption`: up to 30 characters. Very short paths fail validation. Arbitrary SVG import, geographic accuracy and shape morphing are not included.
