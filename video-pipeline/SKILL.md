---
skill: video-pipeline
type: video-post
status: active
last-updated: 2026-05-17
telemetry: video-pipeline
---

# Video Pipeline — LOG color grade + background blur (post-process Portrait mode)

**Purpose:** Take a LOG-profile vertical video shot on a phone (Samsung Pro Video LOG, S-Log, etc.) and produce a polished, gradeable, talking-head-ready output in one command. Handles three things most phone footage needs after the fact:

1. **Color grading** — LOG is intentionally flat; this restores normal contrast and saturation with tunable presets or your own LUT.
2. **Background blur** — runs [Robust Video Matting (RVM)](https://github.com/PeterL1n/RobustVideoMatting) to separate subject from background, Gaussian-blurs the background while keeping subject sharp. Replicates phone Portrait mode in post — but with adjustable blur radius and a `--keep-bottom` mask that preserves foreground objects (desk mic, hands, gesture) that RVM treats as "not-person."
3. **Audio passthrough** — original audio kept; optional volume boost for quiet phone mics.

**Role in the free agentic edit stack:**

```
Phone (LOG capture) → video-pipeline (grade + matte + blur) → auto-cut-takes (cut stumbles) → DaVinci / CapCut (final assembly) → export
```

---

## Install (one-time)

```bash
pip install torch torchvision av opencv-python tqdm
```

RVM model auto-downloads on first run (~14 MB cached at `~/.cache/torch/hub/`).

**GPU strongly recommended** — CPU runs ~10× slower. If you have an NVIDIA card, install CUDA-enabled torch:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

---

## Usage

```bash
python log_to_polished.py INPUT.mp4
```

Output: `INPUT_dir/polished.mp4` by default.

### Common variations

```bash
# Use a stronger grade preset (defaults to 'strong')
python log_to_polished.py raw.mp4 --grade very-strong

# Skip background blur (just grade)
python log_to_polished.py raw.mp4 --no-blur

# Heavier blur
python log_to_polished.py raw.mp4 --blur 30

# Custom 3D LUT for grading
python log_to_polished.py raw.mp4 --lut luts/my_log_to_rec709.cube

# Boost quiet audio
python log_to_polished.py raw.mp4 --volume 3.0

# Cover the desk + mic in the lower half (default: 35%, increase if mic is taller)
python log_to_polished.py raw.mp4 --keep-bottom 50

# Force CPU
python log_to_polished.py raw.mp4 --device cpu
```

---

## Grade presets

| Preset | When |
|---|---|
| `weak` | Already lightly graded footage; just needs a nudge |
| `medium` | Standard log-to-rec709 conversion |
| `strong` (default) | Aggressive S-curve, +85% saturation — most LOG footage from phones |
| `very-strong` | Even more aggressive — flat S-Log2-style footage |
| `c5` | Custom recipe iterated for Samsung Galaxy Pro Video LOG. Strong S-curve with protected highlights (top capped at 0.985), shadow lift to 0.025 for detail, saturation 2.7, contrast 1.125 |

LUTs override presets entirely. Put `.cube` files in `luts/` and reference with `--lut`.

---

## The `--keep-bottom` mask

RVM is a person-segmentation model — it only knows "person" vs "not-person." A desk mic on a stand in front of you is "not-person," so it gets blurred along with the background. The `--keep-bottom N%` mask forces the lower N% of the frame to stay sharp, with a soft 40px gradient at the top edge so the transition isn't a hard horizontal line.

Default 35% covers a typical talking-head + desk mic shot. Increase to 50% if the mic body extends higher; decrease to 25% if your hands rarely come into frame.

For non-rectangular foreground objects, use `--keep-region X1,Y1,X2,Y2` for arbitrary rectangles.

---

## Pipeline stages

```
input LOG MP4
    ↓ (1) ffmpeg curves + eq (or lut3d)
graded MP4
    ↓ (2) RVM matting + alpha feather + Gaussian blur + composite, per frame
matted+blurred MP4 (video only)
    ↓ (3) ffmpeg mux original audio + optional volume boost
polished MP4
```

Intermediate files live in a temp dir and are deleted unless `--keep-temps`.

---

## Tips

- **Matting quality** depends on subject/background contrast. Plain wall behind you = perfect. Busy bookshelf = some edge artifacts on hair/shoulders. Use `--feather 8` for a softer edge if the cutout looks unnatural.
- **Blur radius** sweet spot: 15–25 for natural Portrait-like blur, 30–50 for dramatic shallow-depth-of-field look.
- **First run** takes longer because of RVM model download.
- **GPU**: ~30–60 seconds for a 90-second 1080p clip. CPU: 15–25 minutes.

---

## Files in this skill

- `log_to_polished.py` — main script (single CLI entry point)
- `luts/` — drop your `.cube` LUT files here
- `README.md` — quick-start usage examples
