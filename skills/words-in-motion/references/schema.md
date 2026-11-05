# Input schema

All inputs are UTF-8 JSON. Required strings: `brand` (24 characters), `title` (38), `subtitle` (90), `cta` (28), `disclosure` (72). No control characters. Use `theme`: paper, night, lavender or ocean. These maximum lengths are preliminary; actual pixel-fit checks can reject shorter wide text. The bundled fonts support these English examples; unsupported scripts need suitable fonts and a new fit review.

Pattern fields (only the skill's configured pattern is used):

| Pattern | Fields |
| --- | --- |
| Kinetic | `beats`: exactly three strings, up to32characters each |
| Chat | `context`: three lines up to54characters; `conversation`: question and answer, each up to110 |
| Chart | `labels`: five strings up to10; `series_names`: two up to18; `series`: two arrays of five finite numbers from0to100; `unit`: up to20characters |
| Morph | `steps`: four strings up to42 for button/prompt/option/result; `sessions`: six names up to20. Keep button text especially short. |
| Wall | `filters`: three up to18; `media`:3–12local image paths relative to the brief JSON. The second image is the expanded selection. |
| Crew | `roles`: three up to18; `tasks`: three up to50 |

The renderer never follows URLs or sends messages. Do not place secrets in briefs. Keep example data labelled illustrative. Charts require an explicit unit and values matching that unit. Presenter modes require the command-line `--presenter` input, which is never synthesized or inferred from a portrait.
