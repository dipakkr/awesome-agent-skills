# Brief schema

UTF-8 JSON. The exact examples are under `examples/01` through `examples/04`.

| Field | Required value |
| --- | --- |
| brand | Nonempty text, maximum 24 characters |
| title | Opening completion after “A clearer way to”, maximum 50 characters |
| promise | One product promise, maximum 65 characters |
| cta | Closing headline, maximum 42 characters |
| domain | Destination or closing descriptor, maximum 50 characters |
| disclosure | Accurate source/concept disclosure, maximum 95 characters |
| kind | `product` or `concept`; concept disclosure must include “concept” |
| theme | `ink`, `paper`, `plum`, `forest` |
| audio | `silent` or `original-pulse` |
| chapters | Exactly three objects |

Chapter object: `label` (18 characters), `headline` (42), `detail` (95), `proof` (55), `source` (180), `screen` (local image path relative to the brief, 200), and `focus` ([x,y] fractions from 0 to 1). `source` records where the capture and claim came from. `proof` is a supported summary, not permission to fabricate evidence.

Captures must be at least 1280 × 720, below 25 megapixels and below 30 MB. The camera preserves proportions. Focus refers to the fitted screen panel; review the maximum zoom to ensure the intended detail stays in view. Actual pixel-fit checks can reject wide text below the character limit. English examples are bundled; other writing systems require an appropriate font and fit review.

The chapter card has one input screenshot, not a screen recording or interactive product session. Use genuine recording support only after adapting the renderer. Notes, claims, product names and examples do not connect to any live service.
