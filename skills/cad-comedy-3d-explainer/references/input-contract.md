# Editable brief

Copy a supplied `brief.json` into a new location and give it a new lowercase hyphenated `id`.

| Field | Contract |
|---|---|
| `title`, `subtitle`, `takeaway` | 1–34, 1–48, 1–76 characters respectively |
| `theme` | `citrus`, `candy`, `cobalt`, `plum` |
| `boards` | 1–8 board states |
| `turns` | 8–20 turns, total <=180 words |
| `turn.speaker` | `student` (Milo) or `tutor` (Pip) |
| `turn.text` | 1–108 characters; split longer lines |
| `turn.board` | Zero-based existing board index |
| `turn.shot` | `student`, `tutor`, `wide`, `board` |
| `turn.gag` | `none` (default), `cloud`, `cookie`, `mail`, `box` |
| `turn.reaction` | `neutral`, `proud`, `shock`, `think`, `deadpan` |
| `turn.tag` | Optional 0–32-character visual joke label |
| `turn.pause` | 0.1–1.2 seconds after the measured speech; default 0.2 |

Prop shots automatically use the wide camera so the object and both characters stay visible. The prop temporarily replaces the whiteboard. `reaction` poses the student (proud lean, surprise bounce, thinking tilt) and the tutor (deadpan eyes/tilt). It does not add spoken words. Tag cards are visual text, not narration.

Each board needs a heading <=30 characters, note <=56 characters, 1–3 nodes and optional kind `flow`, `cycle` or `queue`. Nodes have labels <=16 characters and one icon from: `book`, `shelf`, `bell`, `shop`, `phone`, `gate`, `ticket`, `worker`, `tray`, `clock`, `database`, `lightning`.

Captions use the JSON Caption shape: `text`, `startMs`, `endMs`, `timestampMs: null`, `confidence: null`. Times derive from measured turn WAV lengths; these are scripted captions, not speech recognition confidence or word alignment. `timeline.json` also stores the shot, reaction, prop and energy envelope for each turn.

The last 2.4 seconds hold the takeaway. All animation uses video time, so stills and full renders are deterministic at the same frame. No live physics, browser-time CSS transitions or uncontrolled animation loop is used.
