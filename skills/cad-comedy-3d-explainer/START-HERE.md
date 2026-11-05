# Make your first video

Unzip `cad-comedy-3d-explainer`, then open its parent working folder in a coding agent such as Claude Code, Cursor or Codex. You can explicitly point the agent at the file without installing the skill globally.

Tell the agent:

```text
Read cad-comedy-3d-explainer/SKILL.md. Check that Python 3.10+,
Node.js 22+, npm, FFmpeg and FFprobe are available, and help me
set up anything missing. Install the pinned renderer dependencies.
```

New narration needs your own supported voice-provider account or matching recordings. Follow `references/audio-setup.md`. Store credentials in a private environment file outside this skill and public folders. Give the agent the file path, not the secret. The included synthetic recordings can replay the supplied examples without new API calls.

## A new AI Evals reel

Paste this, replacing the bracketed voice settings:

```text
Read cad-comedy-3d-explainer/SKILL.md and create a new funny
narrated 3D reel titled “What is AI Evals?”

Audience: founders and marketers who are new to AI.
Length: roughly 40–55 seconds; prioritize clarity over rushing.
Use Milo and Pip, expressive reactions and readable captions.

Opening joke: Milo says his AI passed every test. Pip asks who
wrote the tests. Milo admits the AI did and awarded itself a diploma.

Explain evaluations with a customer-support example: realistic
test cases, clear criteria, inspecting failures and comparing
versions. Explain that a passing test set is not a guarantee.
End with a callback and one useful takeaway.

Write fresh dialogue. Use examples/ai-evals/brief.json as a
structural reference, not wording that must be copied.
Voice provider: [openai, elevenlabs, fish, or supplied recordings].
Private configuration file: [absolute path to my voice environment file].

Create the script and editable brief, generate matching narration,
review the shots and render the full video into output/my-ai-evals/.
Deliver the MP4, script, captions, poster and source.
```

The agent runs preparation and rendering using the commands in SKILL.md. Open the resulting `preview.html` or `film.mp4`; then request changes to the dialogue, pace or visuals. A changed script needs matching new audio. The existing characters, camera controls, palettes and props are reusable; new geometry requires source changes.

## Watch the included example first

Open `examples/ai-evals/recorded/preview.html` or `film.mp4`. Its exact invocation is in `examples/ai-evals/prompt.txt`, readable dialogue in `script.md`, editable input in `brief.json` and factual notes in `references/ai-evals-notes.md`.

For script-only work, explicitly request “script only; do not generate audio or render.”
