---
skill: audio-enhance
type: audio-post
status: active
last-updated: 2026-04-18
---

# Audio Enhance — Voice Cleanup for Video Production

**Purpose:** Clean up voice recordings after capture. Removes room tone, ambient noise, and reverb; normalizes levels; restores clarity to speech recorded on imperfect mics (phone mics, laptop mics, untreated rooms).

**Role in the CD free agentic edit stack:**

```
OBS (capture) → Audio Enhance (clean voice) → Whisper (transcribe)
             → Claude (decide) → FFmpeg / Auto-Editor (cut)
             → DaVinci Resolve (assemble) → Remotion (motion graphics)
             → export
```

Runs between capture and transcription. A cleaner signal gives Whisper fewer errors and produces a cleaner final output for viewers.

---

## Primary tool — Resemble Enhance

Open-source AI voice enhancement. Two-stage model: denoise → enhance (super-resolution on the voice signal). Runs on GPU locally. Driveable by Claude via CLI.

**GitHub:** `resemble-ai/resemble-enhance`

### Install

```bash
pip install resemble-enhance --upgrade
```

Requirements: Python 3.10+, CUDA 11.8+ for GPU. Falls back to CPU but is slow there.

Models download on first run (~1 GB).

### Basic usage

```bash
# Denoise only (fast, preserves more of the original character)
resemble_enhance input_dir/ output_dir/ --denoise_only

# Full enhance (denoise + super-resolution, best quality)
resemble_enhance input_dir/ output_dir/
```

Input: directory of `.wav` / `.mp3` / `.flac` files.
Output: enhanced files in target directory, same filenames.

**Recommendation:** use full enhance by default for production videos. Switch to `--denoise_only` if the full enhance introduces artifacts on a specific recording.

---

## Why this over Adobe Podcast / Supertone Clear

| Tool | Runs locally | Scriptable | Free | Notes |
|---|---|---|---|---|
| **Resemble Enhance** | ✅ | ✅ (CLI) | ✅ | Open source. Drives from Claude. Fits the agentic stack. |
| Adobe Podcast Enhance Speech | ❌ (web) | ❌ | ✅ (free tier, 1h/mo) | Excellent quality. Web upload friction. |
| Supertone Clear | ✅ (desktop app) | ❌ (GUI) | ✅ (free tier) | Often edges Adobe on voice naturalness. Not agentic. |
| iZotope RX | ✅ | Limited | ❌ ($400+) | Industry standard. Overkill for YouTube. |

**Call for the CD pipeline:** Resemble Enhance. Fits the local-GPU-with-Claude pattern the same way Whisper and Ollama do.

**Fallback for one-offs or if Resemble setup fails:** Adobe Podcast (manual, web upload, works every time).

---

## When to use

Every narration recording before transcription and edit, if:
- Recorded on phone mic, laptop mic, or imperfect USB mic
- Background noise present (fan, traffic, keyboard, street, HVAC)
- Room has noticeable reverb / echo
- Levels are inconsistent across takes

Skip the enhance pass if:
- Recording was made on a treated-room + studio-mic setup (e.g. the Beyerdynamic Fox in a quiet room) — the raw signal is already clean and enhancement can introduce artifacts
- A specific creative take requires the unprocessed character of the room

---

## Claude integration

Typical agentic post-record step:

1. OBS outputs raw audio track alongside screen recording
2. Claude detects new recording in `brand/exports/REG-XXXX--slug/audio/`
3. Claude runs `resemble_enhance audio/ audio/enhanced/ --denoise_only` (or full enhance)
4. Claude feeds the enhanced audio into Whisper for transcription
5. Pipeline continues downstream

Claude can A/B compare raw vs enhanced with a loudness/spectrum check and decide which version to pass downstream.

---

## Output conventions (per CD export pattern)

```
brand/exports/REG-XXXX--slug/
├── audio/
│   ├── narration-raw.wav           # OBS output, untouched
│   ├── narration-enhanced.wav      # Resemble Enhance output
│   ├── transcript.srt              # Whisper, from enhanced
│   ├── transcript.vtt
│   ├── transcript.json
│   └── cuts.md
```

Always keep `narration-raw.wav` — enhancement is destructive and the raw signal is the ground truth. The enhanced version is derived.

---

## Failure modes

1. **Over-processing on already-clean audio.** Running full enhance on a studio-mic recording can flatten voice character. Fix: use `--denoise_only` or skip the step when the raw is clean.
2. **Model artifacts on whisper or sibilants.** Rare with Resemble Enhance, more common with some alternatives. If a specific word sounds robotic post-enhance, fall back to Adobe Podcast on that single file.
3. **VRAM contention.** If a local LLM runtime (Ollama, LM Studio, etc.) is running alongside at full load, Resemble Enhance may OOM on the shared GPU. Resolution: enhance in a separate pass when the LLM runtime is idle, or unload it temporarily. A 16 GB consumer GPU generally has headroom for two concurrent models, not three.

---

## Related

- `../whisper/SKILL.md` — transcription, runs on the enhanced output
- `../remotion-studio/` — motion graphics layer
- `../PIPELINE.md` — overall CD production flow

---

## Future additions

- Wrapper script: `audio-enhance/scripts/clean.py` that handles REG-ID-aware input/output with quality comparison between raw and enhanced
- Batch mode for processing all narration takes in a session
- Per-voice profile tuning (if Resemble Enhance exposes this at the CLI level)
