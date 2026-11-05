# Inputs and limits

Common fields: `brand` (24 characters), `title` (46), `subtitle` (88), `source` (85), and `theme` (chalk, ink, rose, cobalt). Text is Latin-script with a limited punctuation set; geometry measurement may reject copy that is within the character cap but does not fit. Do not silently truncate.

`seconds`: integer 3..60. The film lasts seconds + 2, including the zero hold. `ending`: up to 22 characters. This is a prerecorded opening cue; it is not a countdown to a live date.
