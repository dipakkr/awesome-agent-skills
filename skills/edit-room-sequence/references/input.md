# Supported inputs

mode: `creative`. format: `landscape` (1920×1080) or `square` (1080×1080). Both are 30fps and18seconds. brand:1–18 characters; headline and ending:1–42; cta:1–24; item:1–26; source:1–65. labels:three strings of1–20 characters; details:three strings of1–38. accent and ink:six-digit hex colors. variant:0or1 controls secondary composition details. concept:true is required because default scenes illustrate authored content. brandKind:fictional or real. Optional logo:local public SVG/PNG/WebP basename; place it in renderer/public. Preserve actual brand geometry and inspect its sizing.

For a real brand, brandAudit must contain sourceUrl (official HTTPS website), colors (observed palette including accent and ink), evidence (what was observed) and any user override. The renderer validates the URL and palette membership; the agent must verify that the evidence actually matches the website. A schema check is not a brand audit.

The labels and details map to the three principal elements shown in the scene. Edit the source when you need a different count or different actions.

Do not put secrets or private customer data into example briefs. Different lengths, portrait layout, variable duration, voiceover, live product captures and new scene structures require source adaptation and fresh visual review. They are not hidden automatic options.
