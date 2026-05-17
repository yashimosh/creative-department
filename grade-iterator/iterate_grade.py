"""
Grade Iterator — converge on a LOG-to-Rec.709 grade through human-in-the-loop iteration.

Commands:
  extract    Pull a single representative frame from a video
  variations Apply N grade variations to a frame, output labeled images
  lock       Resolve a recipe chain, optionally export as preset + .cube LUT

See SKILL.md for the full workflow.
"""
import argparse, subprocess, sys, json
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Install pyyaml: pip install pyyaml"); sys.exit(1)

SCRIPT_DIR = Path(__file__).parent
RECIPES_PATH = SCRIPT_DIR / "recipes.yml"
RECIPES = yaml.safe_load(RECIPES_PATH.read_text(encoding="utf-8"))


def resolve_chain(spec: str) -> tuple[str, list[str]]:
    """
    Resolve a recipe chain like "strong+more-sat+pull-highlights" into a single
    ffmpeg -vf filter string. Returns (filter_string, list_of_recipe_names_used).
    """
    parts = spec.split("+")
    used = []
    chains = []
    for name in parts:
        name = name.strip()
        if name not in RECIPES:
            print(f"[ERR] recipe not found: {name}")
            print(f"      available: {', '.join(RECIPES.keys())}")
            sys.exit(1)
        r = RECIPES[name]
        used.append(name)
        if "filter" in r:
            # 'filter' replaces the chain (typically a base grade)
            chains = [r["filter"]]
        elif "delta" in r:
            chains.append(r["delta"])
    return ",".join(chains), used


def cmd_extract(args):
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-ss", str(args.at), "-i", args.video,
        "-vframes", "1", "-update", "1", str(out)
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("[ERR]", r.stderr[-500:]); sys.exit(1)
    print(f"Extracted frame at {args.at}s -> {out}")


def cmd_variations(args):
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    variations = [v.strip() for v in args.variations.split(",")]
    base = args.base.strip() if args.base else None

    print(f"Base recipe: {base or '(none)'}")
    print(f"Variations: {variations}")
    print()

    manifest = {"frame": args.frame, "base": base, "variations": []}

    for var in variations:
        chain_spec = f"{base}+{var}" if base else var
        try:
            vf, used = resolve_chain(chain_spec)
        except SystemExit:
            continue
        out_file = out_dir / f"{var}.jpg"
        cmd = ["ffmpeg", "-y", "-i", args.frame]
        if vf and vf != "null":
            cmd += ["-vf", vf]
        cmd += ["-update", "1", str(out_file)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  [ERR] {var}: {r.stderr[-300:]}"); continue
        desc = RECIPES[var].get("description", "")
        print(f"  OK  {var}.jpg  ({desc})")
        manifest["variations"].append({"name": var, "chain": chain_spec, "filter": vf, "description": desc})

    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"\nManifest -> {manifest_path}")
    print(f"\nNext: open {out_dir}/ and pick one. Then iterate:")
    print(f"  python iterate_grade.py variations FRAME --base \"<picked>\" --variations <next-five> --out grades/roundN/")


def cmd_lock(args):
    vf, used = resolve_chain(args.recipe)
    name = args.name
    locked_dir = SCRIPT_DIR / "locked"
    locked_dir.mkdir(exist_ok=True)

    # Save recipe JSON
    recipe_json = locked_dir / f"{name}.json"
    recipe_json.write_text(json.dumps({
        "name": name,
        "chain": args.recipe,
        "recipes_used": used,
        "filter": vf,
    }, indent=2), encoding="utf-8")
    print(f"Locked recipe JSON -> {recipe_json}")

    # Export LUT?
    if args.export_lut:
        lut_path = Path(args.export_lut)
        lut_path.parent.mkdir(parents=True, exist_ok=True)
        export_cube_lut(vf, lut_path, size=args.lut_size)

    # Append to video-pipeline GRADE_PRESETS?
    if args.export_to_pipeline:
        pipe_path = Path(args.export_to_pipeline) / "log_to_polished.py"
        if not pipe_path.exists():
            print(f"[WARN] log_to_polished.py not found at {pipe_path} — skipped")
        else:
            text = pipe_path.read_text(encoding="utf-8")
            # Insert before the closing brace of GRADE_PRESETS dict
            insert = f'    "{name}": (\n        "{vf}"\n    ),\n'
            if f'"{name}":' in text:
                print(f"[WARN] preset '{name}' already exists in pipeline — skipped")
            else:
                text = text.replace("}\n\ndef run", insert + "}\n\ndef run", 1)
                pipe_path.write_text(text, encoding="utf-8")
                print(f"Appended preset '{name}' to {pipe_path}")
                print(f"  Use via: python log_to_polished.py video.mp4 --grade {name}")


def export_cube_lut(vf: str, out_path: Path, size: int = 33):
    """
    Export an ffmpeg filter chain as a .cube LUT.

    Method: generate a Hald CLUT identity image, apply the filter, write .cube.
    """
    print(f"Exporting {size}x{size}x{size} LUT -> {out_path}")
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        print("[ERR] LUT export needs Pillow + numpy: pip install Pillow numpy")
        return

    # Generate identity Hald CLUT via ffmpeg
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="luttmp_"))
    hald_in = tmp / "hald.png"
    hald_out = tmp / "hald_graded.png"

    # ffmpeg has a haldclutsrc source for generating identity Hald CLUTs
    # level = cube-root-ish; level=8 -> 512x512 Hald which corresponds to 8^2=64 per axis
    # For a 33x33x33 LUT we need a Hald that can represent at least 33 levels per axis.
    # level=6 -> 216x216 image, encoding 6^3=216 cube indices per axis? No — Hald level N
    # creates a 2D image of size (N^3 x N^3), encoding N^2 levels per channel.
    # So level=6 -> 216x216 image, 36 levels per channel — enough for size=33.
    # For size=65, use level=8 -> 512x512 image, 64 levels per channel.
    hald_level = 8 if size > 36 else 6
    levels_per_channel = hald_level ** 2

    gen_cmd = [
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"haldclutsrc=level={hald_level}",
        "-frames:v", "1", str(hald_in)
    ]
    r = subprocess.run(gen_cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ERR] Hald CLUT gen failed: {r.stderr[-500:]}"); return

    # Apply the grade filter to the Hald CLUT
    apply_cmd = [
        "ffmpeg", "-y", "-i", str(hald_in),
        "-vf", vf, str(hald_out)
    ]
    r = subprocess.run(apply_cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[ERR] Grade application failed: {r.stderr[-500:]}"); return

    # Read graded Hald and convert to .cube format
    img = Image.open(hald_out).convert("RGB")
    arr = np.asarray(img, dtype=np.float32) / 255.0  # H W 3 in [0,1]
    n = levels_per_channel  # samples per channel in the Hald

    # Hald CLUT layout: pixels are arranged so that (r, g, b) input maps to
    # an (x, y) coordinate. For level=N (image NxN where N=hald_level^3):
    #   img[y, x] gives output for input (r, g, b) where:
    #     r = (x % N^2) / (N^2 - 1)... actually use the standard formula:
    #   For Hald level L: width = height = L^3, and:
    #     x = b * L^2 + r
    #     y = g * L + (b // L) ... no, this varies by tool.
    #
    # Standard: Hald[y*W+x] = (
    #     r = x % (L^2),
    #     g = (y % L) * L + (x // L^2),
    #     b = y // L
    # ) ... this is implementation-specific.
    #
    # ffmpeg's haldclutsrc layout: rows enumerate (b, g) pairs, cols enumerate r.
    # For level L, image is (L^3, L^3). The mapping is:
    #   r_index = x % L^2
    #   g_index = (y % L^2) ... actually ffmpeg uses level^3 not level^2.
    #
    # Simplest reliable approach: resample the graded Hald to a size^3 line
    # by iterating the 3D grid and looking up the corresponding pixel.

    L = hald_level
    img_size = L ** 3  # ffmpeg haldclutsrc produces L^3 x L^3 image
    assert arr.shape[0] == img_size and arr.shape[1] == img_size, \
        f"Unexpected Hald size {arr.shape}, expected {img_size}x{img_size}"

    # Hald formula (ffmpeg/Adobe standard):
    #   For input (r, g, b) each in [0, L^2 - 1]:
    #     index = b * L^4 + g * L^2 + r
    #     y = index // (L^3)
    #     x = index %  (L^3)
    samples_per_axis = L ** 2  # = 64 when L=8, = 36 when L=6

    # Build the .cube data: enumerate (r,g,b) at `size` levels, look up in Hald
    cube_data = np.zeros((size, size, size, 3), dtype=np.float32)
    for b_i in range(size):
        for g_i in range(size):
            for r_i in range(size):
                # Map size-level index to Hald-level index (0 to samples_per_axis-1)
                r_h = round(r_i / (size - 1) * (samples_per_axis - 1))
                g_h = round(g_i / (size - 1) * (samples_per_axis - 1))
                b_h = round(b_i / (size - 1) * (samples_per_axis - 1))
                idx = b_h * samples_per_axis * samples_per_axis + g_h * samples_per_axis + r_h
                y = idx // img_size
                x = idx % img_size
                cube_data[b_i, g_i, r_i] = arr[y, x]

    # Write .cube file (Adobe Cube LUT format)
    lines = [
        f"# LUT exported by grade-iterator from filter chain:",
        f"# {vf}",
        f"",
        f"LUT_3D_SIZE {size}",
        f"DOMAIN_MIN 0.0 0.0 0.0",
        f"DOMAIN_MAX 1.0 1.0 1.0",
        f"",
    ]
    # .cube convention: r varies fastest, then g, then b
    for b_i in range(size):
        for g_i in range(size):
            for r_i in range(size):
                r, g, b = cube_data[b_i, g_i, r_i]
                lines.append(f"{r:.6f} {g:.6f} {b:.6f}")

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  Wrote LUT: {out_path}")
    print(f"  Use in DaVinci / Premiere / CapCut by loading it as a 3D LUT.")

    # cleanup
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)


def main():
    p = argparse.ArgumentParser(description="Grade Iterator — iterate LOG grades via human-in-the-loop")
    sp = p.add_subparsers(dest="command", required=True)

    p_ext = sp.add_parser("extract", help="Pull a frame from a video")
    p_ext.add_argument("video")
    p_ext.add_argument("--at", type=float, default=5, help="Time in seconds (default: 5)")
    p_ext.add_argument("--out", default="frame.jpg")
    p_ext.set_defaults(func=cmd_extract)

    p_var = sp.add_parser("variations", help="Apply N variations to a frame, output labeled images")
    p_var.add_argument("frame", help="Path to the frame to grade")
    p_var.add_argument("--base", default=None, help="Base recipe (or chain like 'strong+more-sat')")
    p_var.add_argument("--variations", required=True, help="Comma-sep list of recipe names to apply")
    p_var.add_argument("--out", required=True, help="Output directory")
    p_var.set_defaults(func=cmd_variations)

    p_lock = sp.add_parser("lock", help="Resolve a recipe chain, optionally export as LUT / preset")
    p_lock.add_argument("recipe", help="Recipe chain like 'strong+more-sat+pull-highlights'")
    p_lock.add_argument("--name", required=True, help="Name for the locked recipe")
    p_lock.add_argument("--export-lut", help="Path to write .cube LUT")
    p_lock.add_argument("--lut-size", type=int, default=33, choices=[17, 33, 65], help="LUT resolution (default: 33)")
    p_lock.add_argument("--export-to-pipeline", help="Path to video-pipeline/ — appends preset to log_to_polished.py")
    p_lock.set_defaults(func=cmd_lock)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
