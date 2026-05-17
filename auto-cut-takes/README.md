# Auto-Cut Takes

Detect repeat-restart patterns in face-cam recordings and cut the bad takes.

## Convention this assumes

When you stumble mid-sentence, **restart at the START of that sentence**, not mid-word. The detector matches the first N words (3-7) of the restart against earlier word sequences and cuts the bad attempt.

## Run

```bash
pip install openai-whisper
python auto_cut.py YOUR_VIDEO.mp4
```

Output: `YOUR_VIDEO_cut.mp4` next to your input.

## What you get

- The cut version of the video (volume preserved or `--volume N` boost)
- Cached transcript JSON (re-runs are fast)
- Cuts JSON listing every detected restart for review

## Verify the cuts

Open the output in [`video-editor`](../video-editor/) to fine-tune any false positives or to add cuts the detector missed.

See `SKILL.md` for full design context.
