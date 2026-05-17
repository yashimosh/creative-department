---
skill: whisper
type: transcription
status: active
last-updated: 2026-04-18
---

# Whisper — Audio Transcription for Video Production

**Purpose:** Local speech-to-text. Converts narration audio into timestamped transcripts that drive Claude-based edit decisions, caption generation, description writing, and chapter markers.

**Role in the CD free agentic edit stack:**

```
OBS (capture) → Whisper (transcribe) → Claude (decide)
             → FFmpeg / Auto-Editor (cut) → DaVinci Resolve (assemble)
             → Remotion (motion graphics overlay) → export
```

The transcript is the text-as-edit-language layer. Everything downstream in Claude-driven editing reads from it.

---

## Install — `faster-whisper` (recommended)

Python package, CTranslate2-backed, fast on CUDA.

```bash
pip install faster-whisper
```

Requirements: Python 3.9+, CUDA 12+ for GPU acceleration. Falls back to CPU if no GPU.

Alternative: `whisper.cpp` (Georgi Gerganov's C++ port) — smaller footprint, no Python dep, same model weights. Use if the Python environment is inconvenient.

---

## Model choice

| Model | Size | Accuracy | Speed (mid-range consumer GPU) |
|---|---|---|---|
| `large-v3` | 1.5 GB | highest | ~5× realtime |
| `distil-large-v3` | 760 MB | near-large | ~10× realtime |
| `turbo` | 809 MB | good | ~15× realtime |
| `medium` | 769 MB | good | ~8× realtime |

**Default:** `large-v3` for production videos where accuracy matters.
**Rehearsal / quick iteration:** `turbo`.

---

## Basic usage

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cuda", compute_type="float16")

segments, info = model.transcribe(
    "audio.wav",
    beam_size=5,
    word_timestamps=True,
    language="en",
)

for segment in segments:
    print(f"[{segment.start:.2f}s → {segment.end:.2f}s] {segment.text}")
```

For the CD pipeline, a wrapper script should:
1. Accept input audio/video file
2. Output timestamped transcript in three formats: `transcript.srt` (captions), `transcript.vtt` (web captions), `transcript.json` (word-level timestamps for Claude-driven cut decisions)
3. Save alongside source using the REG-ID convention

---

## Claude integration — the agentic edit loop

Typical workflow after a narration recording is captured:

1. **Transcribe** → `transcript.json` (word-level timestamps) + `transcript.srt` (captions)
2. **Claude reads the transcript** and produces:
   - **Cut decisions** — which segments to remove (filler words, re-takes, tangents, dead air)
   - **Chapter markers** — timestamped moments worth indexing in the YouTube description
   - **Description draft** — 200–400 word video description in brand voice
   - **Thumbnail caption candidates** — 2–5 words pulled from the transcript
3. **Claude generates FFmpeg commands** or an edit-decision-list from the cut decisions
4. **Run the cuts** → cut video files
5. **Assembly** in DaVinci Resolve, with Remotion motion graphics overlaid where the script calls for typographic reveals or diagram animations

Claude drives steps 2 and 3 agentically. Steps 1, 4, and 5 are CLI or GUI operations Claude can trigger via the session's bash access.

---

## Output conventions (per CD export pattern)

```
brand/exports/REG-XXXX--slug/
├── audio/
│   ├── narration-raw.wav           # OBS output
│   ├── transcript.srt              # captions
│   ├── transcript.vtt              # web captions
│   ├── transcript.json             # word-level timestamps
│   └── cuts.md                     # Claude's cut decisions, human-readable
├── video/
│   ├── screen-capture-raw.mp4      # OBS screen
│   ├── cut.mp4                     # after FFmpeg pass
│   └── final.mp4                   # after Resolve assembly
└── copy.md                         # source essay (per standard CD registry)
```

The REG ID ties transcript, audio, video, and copy to the same content registry entry.

---

## Audio cleanup (upstream of Whisper or post-transcription)

Whisper transcribes cleanly even with room noise. But for the final video output — not the transcript — voice quality matters. The CD recommended audio-cleanup tool is **Resemble Enhance** (open source, runs on GPU, driveable by Claude). Adobe Podcast Enhance Speech is a valid web-based fallback. See future `creative-department/audio-enhance/` skill if added.

---

## Related

- `../remotion-studio/` — motion graphics layer in the same pipeline
- `../PIPELINE.md` — overall CD production flow
- `../clients/<name>/VIDEO-PIPELINE.md` — per-client production SOPs (create as needed)

---

## Future additions

- Wrapper CLI script: `whisper/scripts/transcribe.py` that handles file-in → three-format-out with REG-ID awareness
- Per-client speaker profiles for name-spelling correction
- Streaming-mode support for long recordings
