# Render input

The agent writes this file from the user's request. The user does not need to edit a template.

```json
{
  "width": 1080,
  "height": 1920,
  "background": "#152020",
  "shots": [
    {"file": "artwork/hook.png", "duration": 2},
    {"file": "footage/demo.mp4", "start": 1, "duration": 4},
    {"file": "artwork/cta.png", "duration": 2}
  ],
  "audio": "audio/licensed-eight-second-edit.wav"
}
```

These paths describe a schema example, not bundled media. Omit audio when none was supplied. start applies only to video; it defaults to zero. All paths are local and relative to the manifest unless absolute. Only one video stream is used per shot; clip audio is removed. A soundtrack must cover the entire requested duration and is trimmed to it. Create an intentional audio edit upstream when needed. Outputs are H.264, 30 fps, yuv420p MP4. Preview GIFs use 12 fps and a 480px width. The renderer pads assets rather than cropping or stretching.

Review placement-specific safe areas. A 9:16 shape alone does not establish eligibility. TikTok's June 2026 non-Spark specification lists a vertical minimum of 540 x 960; safe zones depend on language, caption and add-ons. The separate April 2026 policy also discusses audio, dynamic content and functional destinations. Check both for the selected region and ad type instead of assuming every silent slideshow is runnable:

- https://ads.tiktok.com/resources/help/article/tiktok-auction-in-feed-ads?lang=en
- https://ads.us.tiktok.com/resources/help/article/tiktok-ads-policy-ad-format-and-functionality
- https://www.facebook.com/business/ads-guide/

Verification date: 2026-10-28. Meta's detailed guide can require login. Use the actual account's preview before publishing. Prefer MP4 for vertical video ads; GIF is an optional preview or a destination-specific creative format, not a universal paid-social upload.
