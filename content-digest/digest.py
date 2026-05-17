"""
Content Digest — gather all content-agent outputs into ONE reading document.
No editing, no summarization. Pure reorganization.

Config: digest_config.yml (see digest_config.example.yml for the schema).
Usage:  python digest.py [YYYY-MM-DD]
"""
import sys, re, glob, json, os
from pathlib import Path
from datetime import datetime, timedelta

try:
    import yaml
except ImportError:
    print("Install pyyaml: pip install pyyaml")
    sys.exit(1)

# ─── Load config ─────────────────────────────────────────────────────────────
CONFIG_PATH = Path(__file__).parent / "digest_config.yml"
if not CONFIG_PATH.exists():
    print(f"Config not found: {CONFIG_PATH}")
    print(f"Copy digest_config.example.yml -> digest_config.yml and edit paths.")
    sys.exit(1)
cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))

# Resolve date
if len(sys.argv) > 1:
    DATE = sys.argv[1]
elif cfg.get("date", "today") == "today":
    DATE = datetime.now().strftime("%Y-%m-%d")
else:
    DATE = cfg["date"]
TODAY_DATE = datetime.fromisoformat(DATE[:10]).date()


def expand(p: str) -> str:
    return str(Path(os.path.expanduser(p.format(date=DATE))))


LATEST = Path(expand(cfg["output"]["latest"]))
ARCHIVE = Path(expand(cfg["output"]["archive"]))
ARCHIVE.parent.mkdir(parents=True, exist_ok=True)

sources_read = []
sources_missing = []


def read(path, label):
    p = Path(path)
    if p.exists() and p.is_file():
        sources_read.append((label, str(p)))
        return p.read_text(encoding="utf-8", errors="replace")
    sources_missing.append((label, str(p)))
    return None


def parse_frontmatter(text: str) -> dict:
    if not text or not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end < 0: return {}
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def extract_section(text: str, header_pattern: str) -> str:
    if not text: return ""
    m = re.search(rf"^#{{1,4}}\s+{header_pattern}.*?$", text, re.MULTILINE | re.IGNORECASE)
    if not m: return ""
    start = m.end()
    nxt = re.search(r"\n#{1,4}\s+", text[start:])
    end = start + nxt.start() if nxt else len(text)
    return text[start:end].strip()


def section(title: str, body: str) -> str:
    if not body or not body.strip(): return ""
    return f"\n\n---\n\n## {title}\n\n{body.strip()}\n"


# ─── Walk REG exports (if registry configured) ───────────────────────────────
reg_entries = []
stale_days = 30
if cfg.get("registry", {}).get("enable", False):
    reg_cfg = cfg["registry"]
    stale_days = reg_cfg.get("stale_days", 30)
    exports_glob = expand(reg_cfg["exports_glob"])
    for cm in sorted(glob.glob(exports_glob)):
        cm = Path(cm)
        fm = parse_frontmatter(cm.read_text(encoding="utf-8", errors="replace"))
        created_str = fm.get("created", "")
        try:
            created = datetime.fromisoformat(created_str[:10]).date()
            age = (TODAY_DATE - created).days
        except Exception:
            try:
                age = (TODAY_DATE - datetime.fromtimestamp(cm.stat().st_mtime).date()).days
            except Exception:
                age = 0
        reg_entries.append({
            "id": fm.get("reg", cm.parent.name.split("--")[0]),
            "slug": fm.get("slug", ""),
            "status": fm.get("status", "unknown").strip().lower(),
            "format": fm.get("format") or fm.get("formats") or fm.get("type", ""),
            "age_days": age,
            "path": str(cm),
        })

statuses = cfg.get("registry", {}).get("statuses", {})
ready_set = set(statuses.get("ready", ["ready", "draft"]))
shipped_set = set(statuses.get("shipped", ["published", "posted", "live"]))
parked_set = set(statuses.get("parked", ["skipped", "abandoned", "killed"]))

ready_regs = [r for r in reg_entries if r["status"] in ready_set and r["age_days"] <= stale_days]
stale_regs = [r for r in reg_entries if r["status"] in ready_set and r["age_days"] > stale_days]
shipped_regs = [r for r in reg_entries if r["status"] in shipped_set]
parked_regs = [r for r in reg_entries if r["status"] in parked_set]

# ─── Compose digest ──────────────────────────────────────────────────────────
out = []
out.append(f"""# Content Digest — {DATE}

> One document with all content-related agent outputs for {DATE}.
> No summarization, no editing — just gathered and reordered for choosing.
> Tick the boxes next to anything you want to execute, or strike-through what you reject.

---

## At a glance

- **Ready/draft REGs (<= {stale_days}d):** {len(ready_regs)}
- **STALE REGs (needs status review):** {len(stale_regs)}
- **Published:** {len(shipped_regs)}
- **Parked/skipped:** {len(parked_regs)}
""")

# Source sections (per config)
for src_cfg in cfg.get("sources", []):
    label = src_cfg.get("label", "Unknown")
    body = None
    if "path" in src_cfg:
        text = read(expand(src_cfg["path"]), label)
        if text:
            if src_cfg.get("type") == "json":
                try:
                    data = json.loads(text)
                    lines = []
                    for k, v in (data.items() if isinstance(data, dict) else []):
                        if isinstance(v, (str, int, float)):
                            lines.append(f"- **{k}:** {v}")
                        elif isinstance(v, list):
                            lines.append(f"- **{k}:** {', '.join(str(x) for x in v[:10])}")
                    body = "\n".join(lines) or text[:2000]
                except Exception:
                    body = "```\n" + text[:2000] + "\n```"
            elif "section_extract" in src_cfg:
                body = extract_section(text, src_cfg["section_extract"]) or text
            else:
                body = text
            if "truncate" in src_cfg and body and len(body) > src_cfg["truncate"]:
                body = body[: src_cfg["truncate"]] + "\n\n_...truncated_\n"
    elif "glob" in src_cfg:
        files = sorted(glob.glob(expand(src_cfg["glob"])), reverse=True)
        if src_cfg.get("max_age_days"):
            cutoff = TODAY_DATE - timedelta(days=src_cfg["max_age_days"])
            files = [f for f in files if datetime.fromtimestamp(Path(f).stat().st_mtime).date() >= cutoff]
        if files:
            sources_read.append((label, f"{len(files)} files"))
            lines = []
            for f in files[:20]:
                content = Path(f).read_text(encoding="utf-8", errors="replace")
                if src_cfg.get("extract_titles"):
                    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                    title = m.group(1) if m else Path(f).stem
                    lines.append(f"- **{title}** — `{Path(f).name}`")
                elif src_cfg.get("section_extract"):
                    sec = extract_section(content, src_cfg["section_extract"])
                    if sec:
                        bullets = [l for l in sec.splitlines() if l.startswith("### ")][:5]
                        lines.append(f"\n_From `{Path(f).name}`:_")
                        for b in bullets:
                            lines.append(f"  - {b.replace('### ', '')}")
            body = "\n".join(lines) if lines else None
    out.append(section(label, body or "_Not present._"))

# REG sections
if reg_entries:
    if ready_regs:
        body = "Drafted/ready — tick to execute:\n\n"
        for r in ready_regs:
            body += f"- [ ] **{r['id']}** ({r['status']}, {r['age_days']}d) — `{r['slug']}` — {r['format']}\n  - File: `{r['path']}`\n"
        out.append(section("READY REGs", body))
    if stale_regs:
        body = f"REGs at ready/draft status for more than {stale_days} days. Decide: ship, kill, or rebuild.\n\n"
        for r in sorted(stale_regs, key=lambda x: -x["age_days"]):
            body += f"- [ ] **{r['id']}** ({r['status']}, **{r['age_days']}d old**) — `{r['slug']}`\n  - File: `{r['path']}`\n"
        out.append(section(f"STALE REGs — needs status review (>{stale_days}d)", body))
    done_block = ""
    if shipped_regs:
        done_block += "**Published recently:**\n\n"
        for r in shipped_regs[-10:]:
            done_block += f"- ✓ {r['id']} — `{r['slug']}`\n"
    if parked_regs:
        done_block += "\n**Parked / skipped:**\n\n"
        for r in parked_regs[-10:]:
            done_block += f"- ✗ {r['id']} — `{r['slug']}` ({r['status']})\n"
    if done_block:
        out.append(section("Recently done & parked", done_block))

# Sources block
src_block = "**Files read:**\n\n"
for label, path in sources_read:
    src_block += f"- {label} -> `{path}`\n"
if sources_missing:
    src_block += "\n**Missing (run the relevant agent to populate):**\n\n"
    for label, path in sources_missing:
        src_block += f"- {label} -> `{path}`\n"
out.append(section("Sources", src_block))

out.append(f"\n\n---\n\n_Generated at {datetime.now().isoformat(timespec='seconds')}_\n")

final = "".join(out)
LATEST.write_text(final, encoding="utf-8")
ARCHIVE.write_text(final, encoding="utf-8")

print(f"Digest written:")
print(f"  Latest:  {LATEST}")
print(f"  Archive: {ARCHIVE}")
print(f"  Sources read: {len(sources_read)} / missing: {len(sources_missing)}")
if reg_entries:
    print(f"  REGs: {len(reg_entries)} ({len(ready_regs)} ready, {len(stale_regs)} STALE, {len(shipped_regs)} done, {len(parked_regs)} parked)")
