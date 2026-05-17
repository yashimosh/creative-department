---
skill: audio-pipeline
type: audio-post
status: active
last-updated: 2026-05-17
telemetry: audio-pipeline
---

# Audio Pipeline — sync standalone mic to phone video, replace audio, boost volume

**Purpose:** When you record video on a phone and audio on a standalone mic (because the phone mic is too distant / room-sound is bad), this skill aligns the two recordings using cross-correlation and replaces the phone audio with the cleaner mic track. Optionally boosts volume for quiet sources.

**Companion to [`audio-enhance`](../audio-enhance/SKILL.md)** which handles voice cleanup *after* the sync step.

**Role in the free agentic edit stack:**

```
Phone (video + reference audio) + standalone mic (clean audio)
    → audio-pipeline (sync + replace)
    → audio-enhance (optional voice cleanup)
    → video-pipeline (color grade + background blur)
    → auto-cut-takes (cut stumbles)
    → video-editor (fine-tune cuts)
    → export
```

If your mic plugs directly into the phone (USB-C / Lightning), you don't need this skill — the phone records mic audio directly. This skill is for the case where the mic is on its own recorder (laptop's standalone recording app, dedicated audio recorder, etc.) and you need to sync after.

---

## Install

```bash
pip install numpy scipy
```

ffmpeg + ffprobe on PATH.

---

## Usage

```bash
python sync_replace.py VIDEO.mp4 MIC.wav [options]
```

Options:
```
--output PATH           Output file (default: VIDEO_dir/VIDEO_synced.mp4)
--volume X              Audio volume multiplier (default: 1.0)
--chunk-start SECONDS   Time in video to take alignment chunk from (default: 10s)
--chunk-len SECONDS     Length of alignment chunk (default: 20s)
--keep-temps            Keep intermediate files for debug
```

How the sync works:

1. Extracts a 20-second chunk from 10s into the phone audio
2. Cross-correlates that chunk against the entire mic audio
3. Finds the peak — that's where the chunk starts in the mic timeline
4. Computes the offset: mic time at phone t=0 = peak_in_mic - chunk_start_in_phone
5. ffmpeg muxes phone video + mic audio (seek-offset applied) into the output

The chunk-from-middle approach avoids two common failure modes:
- Both files starting with silence (correlation peak lands in noise)
- Search window cutting off the true offset (peak hits the boundary)

---

## Common variations

```bash
# Phone audio is quiet — boost the mic 3x in the output
python sync_replace.py phone.mp4 mic.wav --volume 3.0

# Phone clip is shorter and starts mid-conversation — adjust chunk start
python sync_replace.py phone.mp4 mic.wav --chunk-start 2 --chunk-len 10

# Debug a bad sync — keep the intermediate files
python sync_replace.py phone.mp4 mic.wav --keep-temps
```

---

## What to do if sync fails

**Symptom: cross-correlation peak strength reported as 0 or very low.**

Likely cause: the mic file actually contains silence (mic muted, wrong input selected). Verify with:

```bash
python -c "
import subprocess, numpy as np
r = subprocess.run(['ffmpeg','-i','MIC.wav','-ac','1','-ar','16000','-f','f32le','-'], capture_output=True)
a = np.frombuffer(r.stdout, dtype=np.float32)
print(f'Peak: {np.max(np.abs(a)):.4f}, RMS: {np.sqrt(np.mean(a**2)):.4f}')
"
```

If peak/RMS = 0, the recording captured no signal. Re-record after checking:
- Windows Settings → System → Sound → Input — correct device selected
- Right-click sound icon → Open Sound settings → input bar moves when you speak
- Cable / USB connection
- Mic gain not set to 0

**Symptom: sync works but voice is slightly off-lip.**

The cross-correlation found a near-peak (not the global maximum). Try a different chunk:

```bash
python sync_replace.py phone.mp4 mic.wav --chunk-start 30 --chunk-len 15
```

Picking a chunk with clear voice activity (no music, no silence) improves accuracy.

---

## When to skip this skill

- Mic plugs directly into the phone — phone records mic audio natively, no sync needed
- You're filming a one-take with no mistakes — phone audio + a volume boost is often fine
- The mic recording is unusable (silent, clipped, noisy) — re-record before processing

---

---

## Beyond sync — additional audio operations (`audio_utils.py`)

The same skill ships a small utility for ffmpeg-based audio ops you'll often want before or after sync:

```bash
# EBU R128 loudness normalize (podcast standard, -16 LUFS by default)
python audio_utils.py normalize input.wav --target -14

# Simple volume multiplier (no loudness math)
python audio_utils.py boost input.wav 3.0

# Trim — keep a range OR --remove a range
python audio_utils.py trim input.wav --from 5 --to 60
python audio_utils.py trim input.wav --from 12 --to 18 --remove

# Extract audio track from a video file
python audio_utils.py extract video.mp4 --format wav

# Split at silence — one output file per non-silent segment
python audio_utils.py split podcast.wav --threshold -30 --min-silence 1.5

# Print peak / RMS / dBFS / silence-detect summary
python audio_utils.py info recording.wav
```

`info` is especially useful for diagnosing "is this recording actually silent?" before you waste time on a sync that can't work.

---

## Files

- `sync_replace.py` — the sync + replace script
- `audio_utils.py` — normalize, boost, trim, extract, split, info
- `README.md`
