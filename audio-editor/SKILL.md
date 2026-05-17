---
skill: audio-editor
type: audio-post
status: active
last-updated: 2026-05-17
telemetry: audio-editor
---

# Audio Editor — transcript-driven manual audio editing (local, free)

**Purpose:** The audio-only counterpart to [`video-editor`](../video-editor/SKILL.md). Same transcript-as-edit workflow — select words, press Delete, those words are cut from the audio. Playback automatically skips deleted sections. Designed for podcasts, voiceover passes, audio essays, and any case where you're editing audio without an associated video track.

**When to use this** (vs video-editor):
- The source is audio-only (.wav, .mp3, .m4a, .flac, .ogg)
- You're producing a podcast / VO / audio essay
- You're prepping a voiceover that gets dropped into a video editor later
- The source is video but you only care about cutting the audio (and will re-attach the video manually)

For video-with-audio editing, use [`video-editor`](../video-editor/SKILL.md) — it has the video preview that helps you spot bad takes faster.

**Role in the free agentic edit stack:**

```
Recording → audio-enhance (cleanup) → audio-pipeline (sync/trim if needed) → audio-editor (transcript-driven cutting) → export
```

For podcasts:
```
Record each guest separately → audio-pipeline (sync) → audio-enhance (per track) → audio-editor (cut)
```

---

## What it does

- **Streams your audio** with HTML5 + range requests (local, no upload)
- **Transcribes** with Whisper (word-level timestamps cached as JSON)
- **Displays transcript** as clickable word spans — green when kept, strikethrough grey when cut
- **Waveform display** at the bottom — kept regions in blue, cut regions in dark red — click to seek
- **Selection** works like a text editor: click + drag, or click then shift-click
- **Delete key** cuts selected words (and the surrounding silence)
- **R key** restores cut words
- **Ctrl+Z / Ctrl+Shift+Z** undo / redo
- **Auto-skip on playback** — what you hear in the timeline is the final cut
- **Quick edits**: one-click filler removal (um/uh/hmm), short-take removal, restore-all
- **Render** runs ffmpeg, outputs cut audio in your chosen format + optional volume boost / normalize

---

## Install

```bash
pip install flask openai-whisper
```

ffmpeg on `PATH`.

---

## Run

```bash
python app.py [audio_file]
```

Opens at `http://localhost:3029` (different port from video-editor so you can run both).

Supports: `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.opus`, anything ffmpeg decodes.

---

## Workflow

1. **Load** — paste audio path, click Open
2. **Transcribe** — Whisper runs; for English use `base`, for accented speech bump to `small` or `medium`
3. **Read and listen** — click any word to seek; transcript scrolls with playback
4. **Edit** — select stumbles, ums, repeated phrases; press Delete
5. **Quick clean** — "Remove fillers" kills all um/uh/hmm at once
6. **Export** — choose output format (`.wav`, `.mp3`, `.m4a`), optional volume / normalize

---

## Why it exists

Most audio editors are timeline-based (Audacity, Reaper, GarageBand). You scrub looking for stumbles. For long-form spoken content, the transcript IS the natural map — "select the bad take in the words, not in the waveform." This brings Descript's audio-edit UX to local, free, no-quota.

For pure waveform editing (music, sound design, complex multi-track), use Audacity or Reaper. This is for spoken-word content.

---

## Files

- `app.py` — single-file Flask app
- `README.md`
