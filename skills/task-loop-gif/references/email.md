# Email delivery

Use `email.gif` as an image block and give the block the campaign's real link. The animation itself has no working buttons. The export is silent; do not depend on narration. Include live text for the message and action because recipients may disable image loading or motion.

The first frame contains the headline, explanation, first request and CTA. `poster.png` shows the completed workflow; `first-frame.png` is the actual fallback. `email.html` is a minimal table-based local snippet with escaped copy, meaningful alt text, image dimensions, responsive width and optional linked CTA. Host the GIF through your email platform and replace its relative source. The script does not upload it or send a message.

Aim for a short loop and a modest payload. This workflow uses a 600px-wide, 10fps, 96-color GIF and reports a 1MB editorial target. Client support and provider limits vary; test the actual campaign in your audience's clients. Avoid cropping or resizing the animation through an editor that may flatten it.

Sources checked 2026-10-28:
- [Mailchimp image design guidance](https://templates.mailchimp.com/design/images/): GIF support and first-frame fallback.
- [Mailchimp image upload guidance](https://mailchimp.com/help/upload-add-and-edit-images-in-campaigns/): supported file formats and hosting through the content studio.
- [ActiveCampaign GIF troubleshooting](https://help.activecampaign.com/hc/en-us/articles/360021835899-My-GIF-isn-t-working): provider-specific limits and static-frame behavior in older clients.
