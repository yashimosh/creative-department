"""
Audio Pipeline — sync standalone mic to phone video, replace audio, optional volume boost.

Cross-correlation alignment using a chunk from the middle of the phone audio
(avoids edge artifacts and silent intros).
"""
import argparse, subprocess, sys, tempfile, shutil
from pathlib import Path

import numpy as np
from scipy.signal import correlate

ap = argparse.ArgumentParser(description="Sync standalone mic to phone video and replace audio")
ap.add_argument("video", help="Phone video (mp4)")
ap.add_argument("mic", help="Standalone mic audio (wav)")
ap.add_argument("--output", help="Output (default: VIDEO_dir/VIDEO_synced.mp4)")
ap.add_argument("--volume", type=float, default=1.0, help="Volume multiplier (default: 1.0)")
ap.add_argument("--chunk-start", type=float, default=10, help="Start of alignment chunk in phone audio (s)")
ap.add_argument("--chunk-len", type=float, default=20, help="Length of alignment chunk (s)")
ap.add_argument("--keep-temps", action="store_true")
args = ap.parse_args()

VIDEO = Path(args.video).resolve()
MIC = Path(args.mic).resolve()
if not VIDEO.exists() or not MIC.exists():
    print(f"Input not found"); sys.exit(1)
OUT = Path(args.output).resolve() if args.output else VIDEO.parent / f"{VIDEO.stem}_synced.mp4"

tmpdir = Path(tempfile.mkdtemp(prefix="audiosync_"))


def load_mono_16k(path: Path) -> np.ndarray:
    """Decode any audio source to 16kHz mono float32 via ffmpeg."""
    r = subprocess.run(
        ["ffmpeg", "-i", str(path), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
        capture_output=True
    )
    if r.returncode != 0:
        print("ffmpeg decode failed:", r.stderr.decode("utf-8", errors="replace")[-500:])
        sys.exit(1)
    return np.frombuffer(r.stdout, dtype=np.float32)


print("Decoding phone audio...")
phone = load_mono_16k(VIDEO)
phone_dur = len(phone) / 16000
print(f"  phone: {phone_dur:.2f}s, peak={np.max(np.abs(phone)):.4f}, RMS={np.sqrt(np.mean(phone**2)):.4f}")

print("Decoding mic audio...")
mic = load_mono_16k(MIC)
mic_dur = len(mic) / 16000
mic_peak = float(np.max(np.abs(mic)))
mic_rms = float(np.sqrt(np.mean(mic**2)))
print(f"  mic:   {mic_dur:.2f}s, peak={mic_peak:.4f}, RMS={mic_rms:.4f}")

if mic_peak < 0.001:
    print("\n[ERROR] Mic audio appears to be silent (peak < 0.001).")
    print("        Check the recording — likely wrong input device or muted mic.")
    sys.exit(2)

# ─── Cross-correlate a chunk from phone against entire mic ────────────────
print(f"\nCross-correlating chunk from phone [{args.chunk_start}s..{args.chunk_start+args.chunk_len}s] against full mic...")
cs = int(args.chunk_start * 16000)
ce = min(cs + int(args.chunk_len * 16000), len(phone))
ph_chunk = phone[cs:ce]
print(f"  Chunk length: {len(ph_chunk)/16000:.2f}s ({len(ph_chunk)} samples)")

if len(ph_chunk) < 16000:
    print("[ERROR] Chunk too short. Try a smaller --chunk-start.")
    sys.exit(1)

corr = correlate(mic, ph_chunk, mode="valid", method="fft")
peak_idx = int(np.argmax(np.abs(corr)))
peak_strength = float(np.max(np.abs(corr)))
peak_in_mic_sec = peak_idx / 16000
offset_sec = peak_in_mic_sec - args.chunk_start  # mic time at phone t=0

print(f"  Phone chunk found at mic time: {peak_in_mic_sec:.3f}s")
print(f"  Inferred offset (mic time at phone t=0): {offset_sec:.3f}s")
print(f"  Correlation peak strength: {peak_strength:.1f}")

if peak_strength < 100:
    print("\n[WARN] Correlation peak is weak — the sync may be unreliable.")
    print("       Try --chunk-start at a moment with clear voice activity.")

# ─── Mux ───────────────────────────────────────────────────────────────────
print(f"\nMuxing phone video + mic audio (offset {offset_sec:+.3f}s, volume {args.volume}x)...")
cmd = ["ffmpeg", "-y", "-i", str(VIDEO)]
if offset_sec >= 0:
    cmd += ["-ss", f"{offset_sec:.4f}", "-i", str(MIC)]
else:
    # Mic started after phone — pad mic with silence at the start
    cmd += ["-itsoffset", f"{-offset_sec:.4f}", "-i", str(MIC)]

cmd += [
    "-map", "0:v:0", "-map", "1:a:0",
    "-c:v", "copy",
]
if args.volume != 1.0:
    cmd += ["-af", f"volume={args.volume}", "-c:a", "aac", "-b:a", "256k"]
else:
    cmd += ["-c:a", "aac", "-b:a", "256k"]
cmd += ["-shortest", str(OUT)]

r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print("[FAIL]", r.stderr[-1500:])
    sys.exit(1)

if not args.keep_temps:
    shutil.rmtree(tmpdir, ignore_errors=True)

print(f"\nDONE: {OUT}")
print(f"Verify by playing — voice should be mic-quality, lips should match video.")
