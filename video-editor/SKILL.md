---
skill: video-editor
type: video-post
status: active
last-updated: 2026-05-17
telemetry: video-editor
---

# Video Editor — Descript-style transcript-driven cutting (local, free)

**Purpose:** A free local alternative to Descript for transcription-driven video editing. The transcript IS the edit: select words, press Delete, those words are cut from the video. Playback automatically skips over cut sections. Designed for face-cam / talking-head Reels and short-form video where you want word-precise control without paying for a subscription.

**Role in the free agentic edit stack:**

```
video-pipeline (grade + matte + blur) → video-editor (transcript-driven cut) → DaVinci / CapCut (final assembly) → export
```

Or standalone for any clip that just needs precise stumble removal.

---

## What it does

- **Streams your video** with HTML5 + range requests (no upload, all local)
- **Transcribes** with Whisper (word-level timestamps cached as JSON)
- **Displays transcript** as clickable word spans — green when kept, strikethrough grey when cut
- **Selection** works like a text editor: click + drag across words, or click-then-shift-click
- **Delete key** cuts the selected words (and the inter-word silence around them)
- **R key** restores cut words
- **Ctrl+Z / Ctrl+Shift+Z** for full undo / redo
- **Playback auto-skips** deleted regions — what you see in the timeline is what the final video will be
- **Mini waveform** on the right shows the full clip with kept (blue) vs cut (red) overview
- **Quick edits**: one-click filler word removal (um/uh/hmm), short-take removal, restore-all
- **Render** button runs ffmpeg, outputs cut version with optional volume boost

---

## Install

```bash
pip install flask
```

Whisper is required for transcription (likely already installed if you use the rest of the stack):
```bash
pip install openai-whisper
```

ffmpeg must be on `PATH`.

---

## Run

```bash
python app.py [video_file]
```

Opens at `http://localhost:3028`. The optional positional arg auto-loads a video; otherwise paste a path in the UI.

---

## Workflow

1. **Load** — paste video path, click Open
2. **Transcribe** — click button (top header), wait ~30s–2min depending on length + Whisper model
3. **Listen and read** — click any word to seek the video; transcript scrolls with playback
4. **Edit** — select stumbles, ums, repeated phrases; press Delete. They cross out, video skips them on playback
5. **Quick clean** — "Remove fillers" button kills all um/uh in one click
6. **Export** — top-right, choose filename, render. Output saves to the same folder as your input by default

---

## Why it exists

Descript costs ~$15–30/month for the same workflow. This is the same idea in ~600 lines of Python — runs locally, no upload, no quota, no monthly fee. You sacrifice the polish of Descript's UI and some features (Studio Sound, Overdub, multi-track) — but for solo creators making vertical short-form, the transcript-as-edit workflow is the 80%.

---

## Files in this skill

- `app.py` — single-file Flask server + HTML UI
- `README.md` — quick-start
