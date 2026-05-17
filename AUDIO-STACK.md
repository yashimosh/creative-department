# Audio Stack

The four audio skills in this package, in the order you typically use them in a production session. Each is self-contained — use only the ones you need.

```
   Record / capture
        │
        ▼
┌─────────────────────────────┐
│  audio-pipeline             │   sync, replace, normalize, boost,
│  (sync_replace.py +         │   trim, extract, split, info
│   audio_utils.py)           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  audio-enhance              │   voice cleanup: noise removal,
│  (SKILL.md)                 │   reverb, normalization
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  audio-editor               │   transcript-driven word-level
│  (Flask UI on :3029)        │   cutting (Descript-style)
└──────────────┬──────────────┘
               │
               ▼
         Final audio
   (or hand off to video-editor
    for word-precise A+V cuts)
```

## When to use each

### [`audio-pipeline/`](audio-pipeline/SKILL.md) — sync, transform, prep
Use **first**, before any creative editing. Two scripts:

- **`sync_replace.py`** — Sync a standalone mic recording to phone video via cross-correlation. Replace the phone audio with the cleaner mic track. Optional volume boost.
- **`audio_utils.py`** — Subcommands for the smaller ops you constantly need:
  - `normalize` (EBU R128 loudness, podcast standard)
  - `boost` (simple volume multiplier)
  - `trim` (keep or remove a range)
  - `extract` (pull audio from video)
  - `split` (one output per non-silent segment)
  - `info` (peak / RMS / silence-detect — useful for diagnosing silent recordings)

### [`audio-enhance/`](audio-enhance/SKILL.md) — clean the voice
Use **after sync**, before cutting. Voice-specific cleanup:
- Removes room tone, ambient noise, reverb
- Normalizes levels
- Restores clarity to speech recorded on imperfect mics (phone mics, laptop mics, untreated rooms)

If your recording was clean (real mic, treated room), you can skip this step.

### [`audio-editor/`](audio-editor/SKILL.md) — transcript-driven manual cutting
Use **last**, for the creative edit. Local Flask app on `http://localhost:3029`:
- Loads any audio file (wav, mp3, m4a, flac, ogg, opus)
- Transcribes with Whisper (cached)
- Displays transcript — select words, press Delete, those words are cut
- Playback automatically skips cuts
- Waveform overview with kept (blue) / cut (red) coloring
- Export as wav/mp3/m4a/flac/ogg with optional normalize + boost

The audio-only counterpart to [`video-editor`](video-editor/SKILL.md). Use `video-editor` if your source is video+audio and you need to spot bad takes visually; use `audio-editor` for podcasts, voiceover, audio essays.

### [`video-editor/`](video-editor/SKILL.md) (related)
For video sources, video-editor does the same transcript-driven cutting WITH a video preview. Mentioned here because for many vertical-video workflows the audio IS the edit (transcript drives both audio and video cuts).

---

## Typical workflows

### Solo vlog: phone video + standalone mic

```bash
# Sync mic to video, replace phone audio
audio-pipeline/sync_replace.py phone.mp4 mic.wav --volume 1.0

# Clean the voice (optional, if room-sound is bad)
audio-enhance/  # see its SKILL.md

# Then the rest of the video stack
auto-cut-takes/auto_cut.py phone_synced.mp4
video-pipeline/log_to_polished.py phone_synced_cut.mp4 --grade c5
```

### Podcast: 2-mic remote recording

```bash
# Per guest track
audio-pipeline/sync_replace.py host_video.mp4 host_mic.wav    # if host had separate mic
audio-pipeline/audio_utils.py normalize host_clean.wav --target -16
audio-pipeline/audio_utils.py normalize guest_clean.wav --target -16

# Edit each track or mix down
audio-editor/app.py host_clean.wav   # cut host's stumbles
audio-editor/app.py guest_clean.wav  # cut guest's stumbles

# Mix in DAW or use ffmpeg amix for simple cases
```

### Voiceover for an explainer video

```bash
# Record VO in 2-3 long takes, no sync needed
# Just clean + cut
audio-enhance/     # optional cleanup
audio-editor/app.py vo_raw.wav    # cut bad takes word-by-word
audio-pipeline/audio_utils.py normalize vo_edited.wav

# Drop into DaVinci / Premiere / CapCut for the visual assembly
```

### Diagnosing a recording that doesn't sound right

```bash
audio-pipeline/audio_utils.py info recording.wav
# Prints peak / RMS / dBFS / silence regions
# Catches the "wrong input device, captured silence" failure mode
```

---

## What this stack doesn't do

- **Multi-track DAW** — for music production, complex sound design, multi-instrument mixing, use Reaper / Logic / Pro Tools / Audacity. This stack is for spoken-word + voiceover content.
- **Real-time effects** — everything here is offline / non-realtime.
- **Mastering** — basic EBU R128 normalization is there, but for full mastering use a dedicated tool.

For those, the stack steps aside; for spoken-word post-production, the four skills here cover the workflow end-to-end without paid software.
