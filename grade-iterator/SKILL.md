---
skill: grade-iterator
type: video-post
status: active
last-updated: 2026-05-17
telemetry: grade-iterator
---

# Grade Iterator — converge on a LOG-to-Rec.709 grade through iteration, then export as preset or LUT

**Purpose:** Going from raw LOG footage to a polished look usually takes 15-30 minutes of fiddling in DaVinci. This skill turns that into a fast, structured human-in-the-loop iteration: extract a frame, generate N grade variations, pick the best one, generate N variations from that base, repeat until convergence. Each iteration is ~5 seconds of compute.

When you're done, export the locked recipe as:
- A preset in `video-pipeline/`'s grade preset library (one line in Python)
- A standalone `.cube` LUT for use in DaVinci / Premiere / CapCut / any pro tool

**Role in the free agentic edit stack:**

```
Phone (LOG capture) → grade-iterator (converge on the grade)
                   ↓ locks recipe → preset or .cube
Phone (LOG capture) → video-pipeline (apply locked grade + matting + blur) → ...
```

You run grade-iterator ONCE per shoot setup (same room, same light, same camera). The locked grade then becomes the default for every subsequent video shot in that setup.

---

## Install

```bash
pip install pillow numpy
```

ffmpeg + ffprobe on PATH.

---

## The iteration workflow

### Step 1 — Extract a representative frame

```bash
python iterate_grade.py extract YOUR_LOG_VIDEO.mp4 --at 5 --out frame.jpg
```

Picks a single frame 5 seconds in. Use a frame with both shadows and highlights (face + background) so the grade decisions generalize.

### Step 2 — Generate the first batch of grade variations

```bash
python iterate_grade.py variations frame.jpg \
  --base "default" \
  --variations weak,medium,strong,very-strong,cinematic \
  --out grades/round1/
```

Outputs `grades/round1/weak.jpg`, `medium.jpg`, etc. Each labeled with the recipe applied.

### Step 3 — Open the folder. Look at all variations side-by-side. Pick one.

The skill doesn't pick for you. This is the human step. Open them in any image viewer and compare.

### Step 4 — Generate the next round, varying around your pick

```bash
python iterate_grade.py variations frame.jpg \
  --base "strong" \
  --variations more-sat,more-contrast,warmer,cooler,gentler \
  --out grades/round2/
```

The `--variations` arg names recipes from `recipes.yml`. Each is a delta from the base.

### Step 5 — Pick again. Iterate.

In practice 2-4 rounds of 5 variations converges on a locked grade. The session that produced the bundled `c5` recipe took 3 rounds and ~15 minutes.

### Step 6 — Lock the recipe

```bash
python iterate_grade.py lock "strong+more-sat+pull-highlights" --name my-locked-grade
```

This:
- Writes the resolved ffmpeg filter chain to `locked/my-locked-grade.json`
- Optionally exports a `.cube` LUT: `--export-lut locked/my-locked-grade.cube`
- Optionally appends it to `video-pipeline/log_to_polished.py`'s `GRADE_PRESETS` dict: `--export-to-pipeline /path/to/video-pipeline/`

---

## What's in `recipes.yml`

The library of recipe deltas. Each entry is an ffmpeg filter string fragment:

```yaml
weak:
  description: "Mild log-to-rec709, gentle contrast"
  filter: "eq=contrast=1.18:saturation=1.25:gamma=0.93"

medium:
  description: "Standard S-curve + saturation boost"
  filter: "curves=all='0/0 0.25/0.18 0.5/0.5 0.75/0.85 1/1',eq=saturation=1.5:contrast=1.05"

strong:
  description: "Aggressive S-curve, +85% saturation"
  filter: "curves=all='0/0 0.2/0.10 0.5/0.5 0.8/0.92 1/1',eq=saturation=1.85:contrast=1.10:gamma=1.02"

more-sat:
  description: "Pushes saturation further (+15% on top of base)"
  delta: "eq=saturation=2.5"  # additive — appended to base filter chain

more-contrast:
  description: "Steeper S-curve, more dramatic shadows"
  delta: "curves=all='0/0 0.08/0 0.4/0.42 0.72/1 1/1'"

warmer:
  description: "Midtone red lift, slight blue drop in highlights"
  delta: "colorbalance=rm=0.04:bm=-0.02"

cooler:
  description: "Cool shadows, slight green in highlights"
  delta: "colorbalance=rs=-0.04:bs=0.06:gh=0.02"

pull-highlights:
  description: "Recover blown highlights"
  delta: "curves=all='0/0 0.1/0 0.4/0.4 0.7/0.85 1/1'"
```

The bundled `recipes.yml` ships with ~20 useful primitives. Add your own.

---

## LUT export

```bash
python iterate_grade.py lock "your+recipe+chain" --name brand-grade --export-lut grades/brand.cube
```

How LUT export works internally:

1. Generate a Hald CLUT identity image (8x8x8 = 64×64 image where each pixel encodes one input RGB value)
2. Apply the ffmpeg filter chain to the Hald CLUT
3. Read the modified pixels back
4. Write a standard `.cube` LUT file (Adobe LUT format, works in DaVinci / Premiere / CapCut / Photoshop)

LUT size defaults to 33×33×33 (the common middle ground — small enough to load fast, large enough to preserve detail). Use `--lut-size 65` for higher precision.

**Why export to LUT:** the LUT is portable. Once you have `brand.cube`, you can grade in DaVinci or any pro tool without re-implementing the recipe. The locked preset in video-pipeline is for the agentic stack; the .cube LUT is for everything else.

---

## Why this exists

Most LUT-building tools are either (a) interactive grading suites (DaVinci, Premiere) that have a 1-2 hour learning curve, or (b) automatic AI-generated grades that don't give you control. This skill is the middle: structured iteration with a recipe library, fast preview, deterministic output.

The pattern came from a real session converging on a Samsung Galaxy Pro Video LOG grade. ~15 variations across 3 rounds, locked as the bundled `c5` preset in `video-pipeline`.

---

## Files

- `iterate_grade.py` — CLI for extract / variations / lock
- `recipes.yml` — bundled recipe library
- `README.md`
