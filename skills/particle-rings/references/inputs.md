# Inputs and limits

Common fields: `brand` (24 characters), `title` (46), `subtitle` (88), `source` (85), and `theme` (chalk, ink, rose, cobalt). Text is Latin-script with a limited punctuation set; geometry measurement may reject copy that is within the character cap but does not fit. Do not silently truncate.

`shape`: sphere, torus, helix or wave. `density`: integer 180..700. `caption`: up to 35 characters. This is a locally rendered projected 3D point field, not an interactive WebGL shader or a physical simulation.
