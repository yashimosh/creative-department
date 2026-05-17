# Grade Iterator

Converge on a LOG color grade through human-in-the-loop iteration. Export the result as a `.cube` LUT or as a preset in [`video-pipeline`](../video-pipeline/).

## Why

Going from raw LOG footage to "this looks right" usually means 15-30 min in DaVinci. This is the same outcome via 3-4 rounds of 5-variation comparison, each round taking ~5 seconds of compute + the time to look at 5 images and pick one.

## Run

```bash
pip install pyyaml pillow numpy
```

### Three-step workflow

```bash
# 1. Pull a representative frame
python iterate_grade.py extract YOUR_VIDEO.mp4 --at 5 --out frame.jpg

# 2. Generate 5 variations
python iterate_grade.py variations frame.jpg \
  --variations weak,medium,strong,very-strong,cinematic \
  --out grades/round1/

# 3. Look at grades/round1/ — pick one, then iterate
python iterate_grade.py variations frame.jpg \
  --base "strong" \
  --variations more-sat,more-contrast,warmer,pull-highlights,shoulder-rolloff \
  --out grades/round2/

# ...repeat until convergence...

# Lock it
python iterate_grade.py lock "strong+more-sat+pull-highlights" \
  --name my-grade \
  --export-lut grades/my-grade.cube \
  --export-to-pipeline ../video-pipeline/
```

## What you get

- `grades/roundN/*.jpg` — labeled comparison images
- `grades/roundN/manifest.json` — recipe-per-image for reproducibility
- `locked/my-grade.json` — locked recipe definition
- `grades/my-grade.cube` — portable LUT for DaVinci/Premiere/CapCut
- `video-pipeline/log_to_polished.py` — appended GRADE_PRESETS entry (use via `--grade my-grade`)

## Adding your own recipes

Edit `recipes.yml` — add entries with either `filter:` (full chain) or `delta:` (appended after base). 20+ primitives ship bundled (saturation, contrast, color balance, shoulder rolloff, teal-orange split-tone, etc.).

See SKILL.md for the full workflow + LUT-export internals.
