"""
LOG video -> polished output pipeline.

Steps:
  1. Apply color grading — strong S-curve + saturation boost (or LUT if provided).
  2. Run Robust Video Matting (RVM) to separate subject from background.
  3. Extend foreground mask with a "keep-region" rectangle so the mic/hands/desk
     in the lower part of frame stay sharp (mic-stand setups).
  4. Feather the alpha matte for smooth blur transitions.
  5. Blur background, composite over sharp foreground.
  6. Mux original audio back in (with optional volume boost).

Usage:
  python log_to_polished.py INPUT.mp4 [options]
"""
import argparse, subprocess, sys, os, tempfile, shutil
from pathlib import Path

# ─── Grade presets ────────────────────────────────────────────────────────────
GRADE_PRESETS = {
    # Each preset is the -vf filter string applied after LOG decoding.
    # 'curves' uses ffmpeg curves filter with explicit S-curve points;
    # then eq adds final saturation/contrast nudge.
    "weak": "eq=contrast=1.18:saturation=1.25:gamma=0.93",
    "medium": (
        "curves=all='0/0 0.25/0.18 0.5/0.5 0.75/0.85 1/1',"
        "eq=saturation=1.5:contrast=1.05"
    ),
    "strong": (
        "curves=all='0/0 0.2/0.10 0.5/0.5 0.8/0.92 1/1',"
        "eq=saturation=1.85:contrast=1.10:gamma=1.02"
    ),
    "very-strong": (
        "curves=all='0/0 0.15/0.05 0.5/0.5 0.85/0.95 1/1',"
        "eq=saturation=2.1:contrast=1.15:gamma=1.05"
    ),
    # C5 — locked grade for REG-0017 (and likely future Samsung Pro Video LOG).
    # Iterated through ~15 variations to arrive at this. Strong S-curve, aggressive saturation,
    # protected highlights (top capped at 0.985), shadow lift to 0.025 for detail retention.
    "c5": (
        "curves=all='0/0 0.11/0.025 0.42/0.42 0.72/0.85 1/0.985',"
        "eq=saturation=2.7:contrast=1.125:gamma=1.05"
    ),
}

def run(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        print("[CMD FAIL]", " ".join(str(c) for c in cmd))
        print("[STDERR]", r.stderr[-1500:])
        sys.exit(1)
    return r

def ffmpeg_grade(input_path, output_path, lut=None, preset="strong", warm=False):
    """Apply color grading. LUT overrides preset."""
    if lut:
        vf = f"lut3d=file='{lut}'"
        print(f"  Applying LUT: {lut}")
    else:
        vf = GRADE_PRESETS[preset]
        print(f"  Applying grade preset: {preset}")
    if warm:
        # Lift reds, drop blues slightly — adds warmth often missing from LOG
        vf += ",colorbalance=rh=0.06:bh=-0.04"
        print("  + warmth tweak (+6% red, -4% blue in highlights)")
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-vf", vf,
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:a", "copy",
        str(output_path)
    ]
    run(cmd)


def matte_and_blur(input_path, output_path, blur_radius, downsample, device,
                   feather_px, keep_bottom_pct, keep_region):
    """Run RVM + composite with extended foreground mask."""
    import torch, av, cv2, numpy as np
    from torchvision.transforms import functional as TF
    from tqdm import tqdm

    print(f"  Loading RVM model on {device}…")
    model = torch.hub.load("PeterL1n/RobustVideoMatting", "mobilenetv3", trust_repo=True).eval()
    if device == "cuda":
        model = model.cuda()

    in_container = av.open(str(input_path))
    in_stream = in_container.streams.video[0]
    fps = in_stream.average_rate or 30
    width = in_stream.codec_context.width
    height = in_stream.codec_context.height
    total_frames = in_stream.frames or 0

    out_container = av.open(str(output_path), mode="w")
    out_stream = out_container.add_stream("libx264", rate=fps)
    out_stream.width = width
    out_stream.height = height
    out_stream.pix_fmt = "yuv420p"
    out_stream.options = {"crf": "18", "preset": "fast"}

    rec = [None, None, None, None]

    # Build static keep-region mask (same every frame)
    keep_mask = np.zeros((height, width), dtype=np.float32)
    if keep_bottom_pct > 0:
        cutoff = int(height * (1 - keep_bottom_pct / 100))
        # Soft top edge — gradient over 40px so it doesn't look like a hard horizontal line
        feather_top = max(10, height // 40)
        for y in range(cutoff, min(cutoff + feather_top, height)):
            keep_mask[y, :] = (y - cutoff) / feather_top
        keep_mask[cutoff + feather_top:, :] = 1.0
        print(f"  Keep-bottom mask: bottom {keep_bottom_pct}% kept sharp (cutoff y={cutoff}, feather {feather_top}px)")
    if keep_region:
        x1, y1, x2, y2 = keep_region
        keep_mask[y1:y2, x1:x2] = 1.0
        print(f"  Keep-region rectangle: ({x1},{y1})-({x2},{y2}) kept sharp")

    # Blur kernel — Gaussian, kernel size must be odd
    k = max(3, int(blur_radius) * 2 + 1)
    feather_k = max(3, int(feather_px) * 2 + 1)

    print(f"  Processing frames: blur={blur_radius}px, feather={feather_px}px, downsample={downsample}, mode={device}…")
    pbar = tqdm(total=total_frames or None, unit="fr")

    with torch.no_grad():
        for frame in in_container.decode(in_stream):
            img = frame.to_ndarray(format="rgb24")
            tensor = TF.to_tensor(img).unsqueeze(0)
            if device == "cuda":
                tensor = tensor.cuda()
            fgr, pha, *rec = model(tensor, *rec, downsample_ratio=downsample)

            fg_np = (fgr[0].clamp(0, 1).cpu().numpy().transpose(1, 2, 0) * 255).astype(np.uint8)
            alpha_rvm = pha[0, 0].clamp(0, 1).cpu().numpy()

            # Combine RVM alpha with keep-region mask (take maximum — union of foregrounds)
            alpha = np.maximum(alpha_rvm, keep_mask)

            # Feather the combined alpha for smooth transition
            if feather_px > 0:
                alpha = cv2.GaussianBlur(alpha, (feather_k, feather_k), feather_px)

            # Blur the ORIGINAL frame for background
            bg_blurred = cv2.GaussianBlur(img, (k, k), blur_radius)

            # Composite
            alpha3 = alpha[..., None]
            composite = (alpha3 * fg_np + (1 - alpha3) * bg_blurred).astype(np.uint8)

            out_frame = av.VideoFrame.from_ndarray(composite, format="rgb24")
            for packet in out_stream.encode(out_frame):
                out_container.mux(packet)
            pbar.update(1)

    for packet in out_stream.encode():
        out_container.mux(packet)
    out_container.close()
    in_container.close()
    pbar.close()
    print(f"  Wrote: {output_path}")


def mux_audio(video_path, audio_source_path, output_path, volume=1.0):
    af = f"volume={volume}" if volume != 1.0 else None
    cmd = ["ffmpeg", "-y",
           "-i", str(video_path),
           "-i", str(audio_source_path),
           "-map", "0:v:0", "-map", "1:a:0",
           "-c:v", "copy"]
    if af:
        cmd += ["-af", af, "-c:a", "aac", "-b:a", "256k"]
    else:
        cmd += ["-c:a", "copy"]
    cmd += ["-shortest", str(output_path)]
    run(cmd)


def parse_region(s):
    if not s:
        return None
    parts = [int(p) for p in s.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("Region must be X1,Y1,X2,Y2")
    return tuple(parts)


def main():
    ap = argparse.ArgumentParser(description="LOG -> polished pipeline (color grade + bg blur with foreground extension)")
    ap.add_argument("input")
    ap.add_argument("--output", help="Output path (default: <input_dir>/polished.mp4)")

    # Grading
    ap.add_argument("--lut", help="3D LUT .cube file (overrides --grade)")
    ap.add_argument("--grade", choices=list(GRADE_PRESETS.keys()), default="strong",
                    help="Grade preset (default: strong)")
    ap.add_argument("--warm", action="store_true", help="Add warmth (red lift, blue drop)")
    ap.add_argument("--no-grade", action="store_true")

    # Matting + blur
    ap.add_argument("--no-blur", action="store_true")
    ap.add_argument("--blur", type=int, default=18,
                    help="Bg blur radius in px (default: 18 — softer/more natural)")
    ap.add_argument("--feather", type=int, default=4,
                    help="Feather radius on alpha matte (default: 4)")
    ap.add_argument("--keep-bottom", type=int, default=35,
                    help="Keep bottom N%% of frame sharp (default: 35 — covers desk mic + hands)")
    ap.add_argument("--keep-region", type=parse_region,
                    help="Extra rectangle X1,Y1,X2,Y2 to keep sharp")
    ap.add_argument("--downsample", type=float, default=0.4)
    ap.add_argument("--device", choices=["cuda", "cpu", "auto"], default="auto")

    # Audio
    ap.add_argument("--volume", type=float, default=1.0)

    ap.add_argument("--keep-temps", action="store_true")
    args = ap.parse_args()

    inp = Path(args.input).resolve()
    if not inp.exists():
        print(f"Input not found: {inp}")
        sys.exit(1)
    out = Path(args.output).resolve() if args.output else inp.parent / "polished.mp4"

    device = args.device
    if device == "auto":
        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            device = "cpu"

    print(f"== LOG -> polished pipeline ==")
    print(f"Input:  {inp}")
    print(f"Output: {out}")
    print(f"Device: {device}")
    print(f"Grade:  {'LUT '+str(args.lut) if args.lut else args.grade}{' + warm' if args.warm else ''}{'  [SKIPPED]' if args.no_grade else ''}")
    print(f"Blur:   {'SKIPPED' if args.no_blur else f'{args.blur}px (feather {args.feather}px, keep-bottom {args.keep_bottom}%)'}")

    tmpdir = Path(tempfile.mkdtemp(prefix="lp_"))
    try:
        if args.no_grade:
            graded = inp
            print("[1/3] Grading: SKIPPED")
        else:
            graded = tmpdir / "graded.mp4"
            print(f"[1/3] Color grading -> {graded.name}")
            ffmpeg_grade(inp, graded, lut=args.lut, preset=args.grade, warm=args.warm)

        if args.no_blur:
            matted_video = graded
            print("[2/3] Matting + blur: SKIPPED")
        else:
            matted_video = tmpdir / "matted.mp4"
            print(f"[2/3] Matting + blur -> {matted_video.name}")
            matte_and_blur(graded, matted_video, args.blur, args.downsample, device,
                          args.feather, args.keep_bottom, args.keep_region)

        print(f"[3/3] Muxing audio (volume {args.volume}x) -> {out.name}")
        mux_audio(matted_video, inp, out, volume=args.volume)

    finally:
        if args.keep_temps:
            print(f"Kept temp files at: {tmpdir}")
        else:
            shutil.rmtree(tmpdir, ignore_errors=True)

    print(f"\nDONE: {out}")

if __name__ == "__main__":
    main()
