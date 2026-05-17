# Content Digest

One reading document, gathered from every content agent in your stack.

## Why

You're running mining-pitch, viral-scout, swanson, registry tools. They each write to their own folder. Reading them serially is friction. This gathers everything into ONE long document, sorted by actionability.

**No editing, no summarization** — pure reorganization. You read it yourself.

## Setup

```bash
pip install pyyaml
cp digest_config.example.yml digest_config.yml
# Edit digest_config.yml to point at your agent output paths
```

## Run

```bash
python digest.py [YYYY-MM-DD]
```

Default: today. Writes both a latest version (always overwritten) and a dated archive.

## Output sections

1. SHIP NOW (top picks)
2. READY REGs (with checkboxes)
3. STALE REGs (status review needed)
4. Full pitch slate
5. Viral signals
6. Opportunity brief
7. Fresh ideas / Swanson bridges
8. Open tensions
9. This week
10. Recently done

Plus a Sources section listing every file read and any missing.

See `SKILL.md` for design context.
