# Portable deck schema v1

JSON object: `title` (string), `font` (installed family, default Arial), `disclosure` (string), `slides` (1–80).
Each slide: `background` (#RRGGBB), `notes` (nonempty string), `objects` (painted in order).
All objects: `kind`, `x`, `y`, `w`, `h` in a 1280 × 720 coordinate space, inside the canvas.
- text: `text`, `size` (12–160 px), `color`, optional `bold`, `italic`, `font` (per-object family), `align` (left/center/right). Newlines allowed. Fixed boxes do not auto-fit. Inspect browser overflow.
- rect/ellipse: `fill`, optional `stroke`, `strokeWidth`; rectangles also support `radius` for rounded corners.
- image: `src` local relative PNG/JPEG/WebP path inside the JSON folder, or embedded image data URI; `alt`. Object-fit cover, centered crop. Match the box to the source ratio for uncropped artwork.

Example:
```json
{"title":"A fresh idea","font":"Arial","slides":[{"background":"#F6F1E7","notes":"Explain the decision this slide supports.","objects":[{"kind":"text","text":"Make the next step clear.","x":64,"y":100,"w":1100,"h":250,"size":76,"bold":true,"color":"#182A35"}]}]}
```

HTML is self-contained. Saved JSON from the HTML includes embedded images and can be rendered again. Output overwrite is refused unless `--force` is explicitly supplied. Receipt records input and output SHA-256 hashes. No API calls occur in the renderer.
