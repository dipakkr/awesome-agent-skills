# Editable inputs

`brief.json` contains single-line strings: brand≤22characters, claim≤62, hinge≤26, turn≤20(two words), invocation≤14, prompt≤85, closer≤65, thesis≤64, cta≤30, source_label≤26. Pixel-fit validation may require shorter wide text. `theme` is blueprint, aubergine, copper or tidal. `posts` is exactly three strings≤135characters each; each must include the exact hinge. `data` points to a local JSON file relative to the brief.

`data.json` has `records`: exactly four objects with nonempty single-line `title`≤30characters, `detail`≤72 and `status`≤20. The exact status `Ready` is counted as ready; all other values count as review-needed. Use the sample's `Needs review` for clarity. These values appear unchanged in the proof HTML and output cards. Counts and source findings are computed, not supplied as promotional claims.

No network requests occur. Do not include secrets or private records in public examples. The bundled fonts support the English samples; other scripts need suitable fonts and a new text-fit review.
