# LOG → Polished Pipeline

Color-grade Samsung Pro Video LOG footage + replace background with blur, in one command.

## What it does

1. **Color grade** — apply a 3D LUT if you have one, or sensible default curves (contrast +18%, saturation +25%, gamma 0.93) to bring LOG back to viewable contrast.
2. **Background blur** — runs [Robust Video Matting (RVM)](https://github.com/PeterL1n/RobustVideoMatting) to separate you from the background, then Gaussian-blurs the background while keeping you sharp. This is what "Portrait mode" does live on the phone — done in post means better quality and adjustable blur.
3. **Audio passthrough** — original audio kept, optional volume boost.

## Install (one-time)

```bash
pip install torch torchvision av opencv-python tqdm
```

(Torch should already be present from Whisper install.)

The RVM model downloads automatically the first run (~13 MB for mobilenetv3, cached in `~/.cache/torch/hub`).

## Usage

```bash
python log_to_polished.py INPUT.mp4
```

Output lands at `INPUT_dir/polished.mp4` by default.

### Common variations

```bash
# Skip background blur (just color-grade)
python log_to_polished.py raw.mp4 --no-blur

# Heavier background blur
python log_to_polished.py raw.mp4 --blur 50

# Use a specific LUT for grading
python log_to_polished.py raw.mp4 --lut luts/samsung_log_to_rec709.cube

# Skip grading entirely (LOG passes through unchanged)
python log_to_polished.py raw.mp4 --no-grade

# Boost audio 3x (phone audio is often quiet)
python log_to_polished.py raw.mp4 --volume 3.0

# Faster matting (lower quality, useful for proofs)
python log_to_polished.py raw.mp4 --downsample 0.25

# Force CPU (if CUDA is broken)
python log_to_polished.py raw.mp4 --device cpu
```

## Tips

- **Matting quality** depends on subject/background contrast. Plain wall behind you = perfect. Busy bookshelf = some edge artifacts.
- **Blur radius** sweet spot: 25–40 for natural Portrait-like blur, 50–80 for dramatic shallow-depth-of-field look.
- **First run takes longer** because it downloads the RVM model.
- **GPU vs CPU:** With an RTX 5070 Ti, expect ~30–60 seconds for a 90-second 1080p clip. CPU-only is ~10× slower.
- **LUT priority:** If you find a Samsung Galaxy LOG LUT online (.cube format), put it in `luts/` and reference with `--lut`. Otherwise the default curves are a reasonable starting point — tweak in `log_to_polished.py` if they're off.

## Pipeline order

```
input LOG MP4
    ↓ (1) ffmpeg lut3d or eq filter
graded MP4
    ↓ (2) RVM matting + Gaussian blur + composite, per frame
matted+blurred MP4 (video only, no audio)
    ↓ (3) ffmpeg mux original audio + volume boost
polished MP4
```

Intermediate files live in a temp dir and are deleted unless `--keep-temps`.

## When to skip a step

- `--no-grade`: if your footage is already graded (e.g. you exported from DaVinci with a LUT applied)
- `--no-blur`: if you shot with a real background (no blur needed) and only want color correction
