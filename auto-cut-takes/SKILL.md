---
skill: auto-cut-takes
type: video-post
status: active
last-updated: 2026-05-17
telemetry: auto-cut-takes
---

# Auto-Cut Takes — detect repeat-restart patterns and cut the bad takes

**Purpose:** When you record a face-cam piece in one sit and re-record a sentence after stumbling, the bad take is followed immediately by the good take of the same sentence. This skill transcribes the video with Whisper, finds those repeated phrases automatically, and cuts the bad takes — leaving only the clean version.

It's the difference between "scrub through 90 minutes of takes hunting for stumbles" and "open the auto-cut version, watch it back, manually fix anything the detector missed."

**Convention that makes this work** (you adopt this for it to land cleanly):

> When you mess up a sentence mid-record, immediately go back to the *start of that sentence* and re-record it. Don't restart mid-word. The detector keys on the first N words of the restart matching the first N words of the original attempt.

**Role in the free agentic edit stack:**

```
video-pipeline (grade + matte + blur) → auto-cut-takes (cut stumbles) → video-editor (fine-tune remaining cuts) → export
```

Or use auto-cut-takes first to get most of the way there, then open the result in video-editor for manual cleanup.

---

## How the detection works

For each word position `i`, look for a matching N-word sequence (3 ≤ N ≤ 7) starting later in the transcript, within a ~12 second window. When found, mark the range from `i` through the start of the match as a cut. This captures:

- The bad take itself (the words you said wrong)
- The inter-take silence (the pause before you restarted)

Detection prefers **longer matches first** — a 7-word repeat is more confident than a 3-word repeat, so 7-word matches take priority.

---

## Install

```bash
pip install openai-whisper
```

ffmpeg must be on `PATH`.

---

## Run

```bash
python auto_cut.py INPUT.mp4 [options]
```

Options:
```
--output PATH         Output file (default: INPUT_dir/INPUT_cut.mp4)
--volume X            Audio volume multiplier (default: 1.0)
--whisper MODEL       Whisper model size (default: base; try 'small' or 'medium' for harder accents)
--pad SECONDS         Clip boundary padding (default: 0.05)
--gap SECONDS         Merge adjacent kept clips closer than this (default: 0.4)
--min-match WORDS     Minimum word-sequence length to consider a restart (default: 3)
--max-match WORDS     Maximum length (default: 7)
--window SECONDS      Search window for restart pattern (default: 12)
```

Outputs:
- `INPUT_cut.mp4` — the cut version
- `INPUT.words.json` — word-level transcript (cached; reused on re-run)
- `INPUT.cuts.json` — the list of cuts that were made

---

## Tips

- **The transcript cache** makes re-runs fast — if you change `--gap` or `--pad`, only the cut + render step re-runs.
- **For non-English** or accented speech, try `--whisper small` or `--whisper medium`. Slower but more accurate.
- **False positives** are rare but possible — e.g. if you naturally repeat a phrase ("not just X, but X"). Open the cut version in `video-editor` to verify and restore any false cuts.
- **Missed stumbles** — short fragments that don't pass the 3-word minimum. Use `video-editor` to clean up manually.

---

## Files in this skill

- `auto_cut.py` — the detection + render script
- `README.md`
