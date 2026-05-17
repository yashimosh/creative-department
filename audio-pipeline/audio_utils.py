"""
Audio Utils — small ffmpeg-based operations that pair with sync_replace.py.

Subcommands:
  normalize   Apply EBU R128 loudness normalization (broadcast standard)
  boost       Apply a simple volume multiplier
  trim        Cut a section out (or keep a section)
  extract     Extract audio from a video file
  split       Split a file at silence (one output per detected segment)
  info        Print peak / RMS / duration / silence-detect summary
"""
import argparse, subprocess, sys, re
from pathlib import Path


def run_ffmpeg(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        print("[FAIL]", " ".join(str(c) for c in cmd))
        print(r.stderr[-1500:])
        sys.exit(1)
    return r


def cmd_normalize(args):
    """EBU R128 loudness normalization (broadcast standard)."""
    out = Path(args.output) if args.output else Path(args.input).with_name(
        f"{Path(args.input).stem}_norm{Path(args.input).suffix}")
    print(f"Normalizing {args.input} -> {out} (target: {args.target} LUFS)")
    cmd = [
        "ffmpeg", "-y", "-i", args.input,
        "-af", f"loudnorm=I={args.target}:TP=-1.5:LRA=11",
        str(out)
    ]
    run_ffmpeg(cmd)
    print(f"Done: {out}")


def cmd_boost(args):
    """Simple volume multiplier."""
    out = Path(args.output) if args.output else Path(args.input).with_name(
        f"{Path(args.input).stem}_boost{Path(args.input).suffix}")
    print(f"Boosting {args.input} by {args.factor}x -> {out}")
    cmd = ["ffmpeg", "-y", "-i", args.input, "-af", f"volume={args.factor}", str(out)]
    run_ffmpeg(cmd)
    print(f"Done: {out}")


def cmd_trim(args):
    """Cut a section. By default keeps the specified range; --remove inverts."""
    out = Path(args.output) if args.output else Path(args.input).with_name(
        f"{Path(args.input).stem}_trim{Path(args.input).suffix}")
    print(f"Trim: {args.input} [{args.from_t}..{args.to_t}] {'(remove)' if args.remove else '(keep)'} -> {out}")
    if not args.remove:
        # Keep the range
        cmd = ["ffmpeg", "-y", "-i", args.input, "-ss", str(args.from_t), "-to", str(args.to_t),
               "-c:a", "copy" if args.copy else "pcm_s16le", str(out)]
    else:
        # Remove the range: take 0..from_t + to_t..end, concat
        import tempfile
        tmp = Path(tempfile.mkdtemp(prefix="trim_"))
        a, b = tmp / "a.wav", tmp / "b.wav"
        run_ffmpeg(["ffmpeg", "-y", "-i", args.input, "-to", str(args.from_t), "-c:a", "pcm_s16le", str(a)])
        run_ffmpeg(["ffmpeg", "-y", "-i", args.input, "-ss", str(args.to_t), "-c:a", "pcm_s16le", str(b)])
        concat = tmp / "c.txt"
        concat.write_text(f"file '{a}'\nfile '{b}'\n")
        cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
               "-c:a", "pcm_s16le", str(out)]
    run_ffmpeg(cmd)
    print(f"Done: {out}")


def cmd_extract(args):
    """Extract audio from a video file."""
    out = Path(args.output) if args.output else Path(args.input).with_suffix(f".{args.format}")
    print(f"Extracting audio: {args.input} -> {out}")
    fmt_args = {
        "wav": ("pcm_s16le", []),
        "mp3": ("libmp3lame", ["-q:a", "2"]),
        "m4a": ("aac", ["-b:a", "256k"]),
        "flac": ("flac", []),
    }
    codec, extra = fmt_args.get(args.format, ("pcm_s16le", []))
    cmd = ["ffmpeg", "-y", "-i", args.input, "-vn", "-c:a", codec] + extra + [str(out)]
    run_ffmpeg(cmd)
    print(f"Done: {out}")


def cmd_split(args):
    """Split at silence regions. One output file per detected non-silent segment."""
    print(f"Detecting silence in {args.input} (threshold {args.threshold} dB, min duration {args.min_silence}s)...")
    detect = subprocess.run([
        "ffmpeg", "-i", args.input,
        "-af", f"silencedetect=noise={args.threshold}dB:d={args.min_silence}",
        "-f", "null", "-"
    ], capture_output=True, text=True)
    log = detect.stderr
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", log)]
    ends = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", log)]
    # Build segment list: between silences
    # Get total duration
    dur_r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                            "-of", "default=noprint_wrappers=1:nokey=1", args.input],
                           capture_output=True, text=True)
    total = float(dur_r.stdout.strip())

    segments = []
    last = 0.0
    for s, e in zip(starts, ends):
        if s - last > args.min_segment:
            segments.append((last, s))
        last = e
    if total - last > args.min_segment:
        segments.append((last, total))

    out_dir = Path(args.output) if args.output else Path(args.input).parent / f"{Path(args.input).stem}_splits"
    out_dir.mkdir(exist_ok=True)
    print(f"Detected {len(segments)} segments. Writing to {out_dir}/")
    for i, (s, e) in enumerate(segments):
        out = out_dir / f"seg_{i:03d}.wav"
        run_ffmpeg(["ffmpeg", "-y", "-i", args.input, "-ss", str(s), "-to", str(e),
                    "-c:a", "pcm_s16le", str(out)])
        print(f"  seg {i:03d}: {s:.2f}s -> {e:.2f}s ({e-s:.2f}s) -> {out.name}")


def cmd_info(args):
    """Print stats and silence-detect summary."""
    import numpy as np
    print(f"Analyzing {args.input}...")
    r = subprocess.run(["ffmpeg", "-i", args.input, "-ac", "1", "-ar", "16000",
                        "-f", "f32le", "-"], capture_output=True)
    arr = np.frombuffer(r.stdout, dtype=np.float32)
    if not len(arr):
        print("[ERR] Could not decode audio"); sys.exit(1)
    dur = len(arr) / 16000
    peak = float(np.max(np.abs(arr)))
    rms = float(np.sqrt(np.mean(arr**2)))
    print(f"  Duration:       {dur:.2f}s")
    print(f"  Peak amplitude: {peak:.4f}  ({20*np.log10(peak+1e-10):.1f} dBFS)")
    print(f"  RMS:            {rms:.4f}  ({20*np.log10(rms+1e-10):.1f} dBFS RMS)")
    if peak < 0.01:
        print("  [WARN] Very low signal — possibly silent or wrong input recorded")
    # Silence detect
    print(f"\nSilence regions (threshold -30 dB, min 0.5s):")
    detect = subprocess.run(["ffmpeg", "-i", args.input,
                             "-af", "silencedetect=noise=-30dB:d=0.5",
                             "-f", "null", "-"], capture_output=True, text=True)
    starts = re.findall(r"silence_start: ([\d.]+)", detect.stderr)
    ends = re.findall(r"silence_end: ([\d.]+)", detect.stderr)
    for s, e in zip(starts, ends):
        print(f"  {float(s):.2f}s -> {float(e):.2f}s ({float(e)-float(s):.2f}s)")
    if not starts:
        print("  (no extended silences detected)")


def main():
    p = argparse.ArgumentParser(description="Audio Utils — ffmpeg-based audio operations")
    sp = p.add_subparsers(dest="command", required=True)

    p_n = sp.add_parser("normalize", help="EBU R128 loudness normalize")
    p_n.add_argument("input")
    p_n.add_argument("--output")
    p_n.add_argument("--target", type=float, default=-16, help="Target LUFS (default: -16, podcast standard)")
    p_n.set_defaults(func=cmd_normalize)

    p_b = sp.add_parser("boost", help="Simple volume multiplier")
    p_b.add_argument("input")
    p_b.add_argument("factor", type=float)
    p_b.add_argument("--output")
    p_b.set_defaults(func=cmd_boost)

    p_t = sp.add_parser("trim", help="Cut a section (keep or remove)")
    p_t.add_argument("input")
    p_t.add_argument("--from", dest="from_t", type=float, required=True)
    p_t.add_argument("--to", dest="to_t", type=float, required=True)
    p_t.add_argument("--remove", action="store_true", help="Remove this range (default: keep this range)")
    p_t.add_argument("--copy", action="store_true", help="Copy codec instead of re-encoding")
    p_t.add_argument("--output")
    p_t.set_defaults(func=cmd_trim)

    p_e = sp.add_parser("extract", help="Extract audio from video")
    p_e.add_argument("input")
    p_e.add_argument("--format", default="wav", choices=["wav", "mp3", "m4a", "flac"])
    p_e.add_argument("--output")
    p_e.set_defaults(func=cmd_extract)

    p_s = sp.add_parser("split", help="Split at silence")
    p_s.add_argument("input")
    p_s.add_argument("--threshold", type=int, default=-30, help="Silence threshold dB (default: -30)")
    p_s.add_argument("--min-silence", type=float, default=1.0, help="Minimum silence duration to split on")
    p_s.add_argument("--min-segment", type=float, default=2.0, help="Drop segments shorter than this")
    p_s.add_argument("--output", help="Output directory")
    p_s.set_defaults(func=cmd_split)

    p_i = sp.add_parser("info", help="Print stats + silence detect")
    p_i.add_argument("input")
    p_i.set_defaults(func=cmd_info)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
