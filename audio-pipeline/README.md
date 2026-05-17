# Audio Pipeline

Sync standalone mic to phone video, replace audio, optional volume boost.

## When you need this

You recorded video on a phone but audio on a separate device (laptop sound recorder, dedicated audio recorder). The two timelines don't match. This finds the offset via cross-correlation and replaces the phone audio with the cleaner mic track.

If your mic plugs into the phone directly — you don't need this; the phone records mic audio natively.

## Run

```bash
pip install numpy scipy
python sync_replace.py phone.mp4 mic.wav
```

Output: `phone_synced.mp4` next to the input.

## Options

```bash
--volume 3.0           Boost output audio 3x (for quiet sources)
--chunk-start 30       Take alignment chunk from 30s into the phone audio
--chunk-len 15         15-second alignment chunk
--output OUT.mp4       Custom output path
--keep-temps           Keep intermediate files
```

## Verifying

After the sync runs it prints a "correlation peak strength" number. If it's < 100, the sync is unreliable — try `--chunk-start` at a moment with clear voice activity (not silence, not music).

If the printed `peak / RMS` for the mic is essentially zero, the mic file is silent and re-recording is needed before this can work. See SKILL.md for diagnosis steps.
