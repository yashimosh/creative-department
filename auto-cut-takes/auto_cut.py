"""
Auto-Cut Takes — detect repeat-restart patterns in face-cam recordings and
cut the bad takes.

Convention: when you stumble, immediately restart at the START of the sentence.
The detector finds repeats of the first N words and cuts the bad attempt.
"""
import subprocess, pathlib, json, re, tempfile, argparse, sys
from typing import List, Tuple

# ─── CLI ─────────────────────────────────────────────────────────────────────
ap = argparse.ArgumentParser(description="Auto-cut: detect repeat-restart patterns and cut bad takes")
ap.add_argument("input", help="Input video file")
ap.add_argument("--output", help="Output video (default: INPUT_dir/INPUT_cut.mp4)")
ap.add_argument("--volume", type=float, default=1.0, help="Audio volume multiplier (default: 1.0)")
ap.add_argument("--whisper", default="base", help="Whisper model size (default: base)")
ap.add_argument("--pad", type=float, default=0.05, help="Clip boundary padding seconds (default: 0.05)")
ap.add_argument("--gap", type=float, default=0.4, help="Merge clips closer than this in seconds (default: 0.4)")
ap.add_argument("--min-match", type=int, default=3, help="Min repeat length in words (default: 3)")
ap.add_argument("--max-match", type=int, default=7, help="Max repeat length in words (default: 7)")
ap.add_argument("--window", type=float, default=12.0, help="Restart search window seconds (default: 12)")
args = ap.parse_args()

SOURCE = pathlib.Path(args.input).resolve()
if not SOURCE.exists():
    print(f"Input not found: {SOURCE}"); sys.exit(1)

FINAL = pathlib.Path(args.output).resolve() if args.output else SOURCE.parent / f"{SOURCE.stem}_cut.mp4"
WORDS_JSON = SOURCE.parent / f"{SOURCE.stem}.words.json"
CUTS_JSON = SOURCE.parent / f"{SOURCE.stem}.cuts.json"

print(f"Input:  {SOURCE}")
print(f"Output: {FINAL}")
print(f"Volume: {args.volume}x · Whisper: {args.whisper} · Match: {args.min_match}-{args.max_match} words · Window: {args.window}s")
print()

# ─── Step 1: Transcribe (cached) ────────────────────────────────────────────
if not WORDS_JSON.exists():
    print("Transcribing with Whisper...")
    import whisper
    model = whisper.load_model(args.whisper)
    result = model.transcribe(str(SOURCE), word_timestamps=True)
    words = []
    for seg in result["segments"]:
        for w in seg.get("words", []):
            words.append({
                "start": round(w["start"], 3),
                "end":   round(w["end"], 3),
                "word":  w["word"].strip(),
            })
    WORDS_JSON.write_text(json.dumps(words, indent=2), encoding="utf-8")
    print(f"  Wrote {len(words)} words -> {WORDS_JSON.name}")
else:
    words = json.loads(WORDS_JSON.read_text(encoding="utf-8"))
    print(f"Loaded {len(words)} words from cached {WORDS_JSON.name}")

print(f"\nFull transcript:\n{' '.join(w['word'] for w in words)}\n")

# ─── Step 2: Detect repeat-and-restart patterns ─────────────────────────────
def normalize(word: str) -> str:
    return re.sub(r"[^\w]", "", word.lower())

normed = [normalize(w["word"]) for w in words]
cuts: List[Tuple[int, int]] = []
covered = set()

i = 0
while i < len(words):
    if i in covered:
        i += 1; continue
    best_match = None  # (j, n)
    for n in range(args.max_match, args.min_match - 1, -1):
        if i + n > len(words): continue
        seq = tuple(normed[i:i+n])
        if any(not s for s in seq): continue
        for j in range(i + n, len(words) - n + 1):
            if words[j]["start"] - words[i]["start"] > args.window:
                break
            if tuple(normed[j:j+n]) == seq:
                best_match = (j, n); break
        if best_match: break
    if best_match:
        j, n = best_match
        cuts.append((i, j - 1))
        for k in range(i, j): covered.add(k)
        print(f"  REPEAT '{' '.join(w['word'] for w in words[i:i+n])}'")
        print(f"    bad:  words {i}..{j-1} ({words[i]['start']:.2f}s..{words[j-1]['end']:.2f}s)")
        print(f"    keep: words {j}..{j+n-1} ({words[j]['start']:.2f}s..{words[j+n-1]['end']:.2f}s)")
        i = j
    else:
        i += 1

CUTS_JSON.write_text(json.dumps([
    {"start_idx": s, "end_idx": e,
     "start_sec": words[s]["start"], "end_sec": words[e]["end"],
     "text": " ".join(w["word"] for w in words[s:e+1])}
    for s, e in cuts], indent=2), encoding="utf-8")
print(f"\n  {len(cuts)} cut(s) detected -> {CUTS_JSON.name}")

# ─── Step 3: Build clip list (runs of kept words) ───────────────────────────
cut_words = {k for s, e in cuts for k in range(s, e + 1)}

clips = []
in_clip = False; cs = ce = 0.0
for idx, w in enumerate(words):
    if idx not in cut_words:
        if not in_clip:
            cs = max(0, w["start"] - args.pad); in_clip = True
        ce = w["end"] + args.pad
    else:
        if in_clip:
            clips.append((round(cs, 3), round(ce, 3))); in_clip = False
if in_clip:
    clips.append((round(cs, 3), round(ce, 3)))

# Merge adjacent clips
merged = []
for cs, ce in clips:
    if merged and cs - merged[-1][1] < args.gap:
        merged[-1] = (merged[-1][0], ce)
    else:
        merged.append((cs, ce))
clips = merged

print(f"\n  {len(clips)} clip(s) to render:")
total = 0
for k, (cs, ce) in enumerate(clips):
    dur = ce - cs; total += dur
    print(f"    clip {k+1}: {cs:.2f}s -> {ce:.2f}s ({dur:.2f}s)")
print(f"  Total kept: {total:.2f}s")

# ─── Step 4: Render ─────────────────────────────────────────────────────────
print(f"\nRendering...")
tmpdir = pathlib.Path(tempfile.mkdtemp(prefix="autocut_"))
clip_files = []
for idx, (cs, ce) in enumerate(clips):
    out = tmpdir / f"c{idx:03d}.mp4"
    r = subprocess.run([
        "ffmpeg", "-y", "-i", str(SOURCE),
        "-ss", str(cs), "-to", str(ce),
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "aac", "-b:a", "192k",
        "-avoid_negative_ts", "make_zero", str(out)
    ], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ERR] clip {idx+1}: {r.stderr[-400:]}"); sys.exit(1)
    clip_files.append(out)

concat = tmpdir / "concat.txt"
concat.write_text("\n".join(f"file '{p}'" for p in clip_files), encoding="utf-8")
af = ["-af", f"volume={args.volume}"] if args.volume != 1.0 else []
cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat)] + af + \
      ["-c:v", "copy", str(FINAL)]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print(f"[ERR] concat: {r.stderr[-400:]}"); sys.exit(1)

for f in clip_files: f.unlink()
concat.unlink()
tmpdir.rmdir()

dur = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                      "-of", "default=noprint_wrappers=1:nokey=1", str(FINAL)],
                     capture_output=True, text=True).stdout.strip()
print(f"\nDONE: {FINAL}")
print(f"Final duration: {float(dur):.2f}s")
print(f"Words: {WORDS_JSON} (cached for next run)")
print(f"Cuts: {CUTS_JSON}")
