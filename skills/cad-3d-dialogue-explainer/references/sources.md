# Sources and provenance

The private user-supplied video was inspected and transcribed locally. It shows a student and a branded star-shaped tutor explaining an API through a restaurant analogy. Its media, dialogue, branding, watermark and audio are not bundled. This package uses independently authored Milo/Pip geometry, scripts, room models, icons and motion.

The implementation follows the [Remotion ThreeCanvas contract](https://www.remotion.dev/docs/three-canvas): frame-driven animation with React Three Fiber and proper lighting. npm dependencies are pinned in the lockfile, installed separately and governed by their own licenses. No upstream gallery asset or purchased template is included. Fonts use the renderer environment's Arial/sans-serif fallback; no commercial font file is redistributed.

Teaching references, checked 2026-10-29:

- [MDN HTTP caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Caching): stored responses, reuse, freshness and revalidation. The film uses a broader beginner cache analogy.
- [Shopify webhooks](https://shopify.dev/docs/apps/build/webhooks): event subscriptions as an alternative to continuous polling; event identifiers and delivery behavior.
- [MDN HTTP 429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/429): too many requests and optional Retry-After timing.
- [Amazon SQS at-least-once delivery](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html): possible duplicate processing and idempotent handling.

Audio API sources and the dated OpenAI compatibility limit are documented in audio-setup.md. Short analogies omit protocol details. They do not imply every cache, webhook service or queue has identical behavior.
