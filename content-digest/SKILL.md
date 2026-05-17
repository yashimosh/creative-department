---
skill: content-digest
type: content-ops
status: active
last-updated: 2026-05-17
telemetry: content-digest
---

# Content Digest — gather all content-agent outputs into one reading document

**Purpose:** If you're running a content stack with multiple agents (pitcher, scout, ideation, registry, research), you end up with 5–10 markdown files in different folders that all matter for "what should I make today?" Reading them serially is friction. This skill aggregates everything into ONE long, organized document with checkboxes you tick to mark execution intent.

**No editing, no summarization** — just reorganization, reordering, resorting. The point is that you read it yourself; the digest doesn't paraphrase upstream agents.

**Role in the agentic content stack:**

```
mining-pitch + viral-scout + swanson-bridges + registry → content-digest → you read one file → execute
```

---

## Install

```bash
# No deps beyond the Python standard library
python --version  # 3.9+
```

---

## Configure

Edit `digest_config.yml` to point at your agent output paths:

```yaml
date: today  # or YYYY-MM-DD
output:
  latest: "~/your-brain/content-digest.md"
  archive: "~/your-brain/content-digest-archive/{date}.md"
sources:
  - label: "Top picks (pitcher)"
    path: "~/your-brain/Agents/mining/output/{date}/weekly-topic_pitcher.md"
    section_extract: "Top 5 picks"
  - label: "Full pitch slate"
    path: "~/your-brain/Agents/mining/output/{date}/weekly-topic_pitcher.md"
    section_extract: "Pitches"
  - label: "Viral signals"
    path: "~/your-brain/Agents/viral-scout/stats/{date}.json"
    type: json
  - label: "Opportunity brief"
    path: "~/your-brain/Agents/viral-scout/opportunity-brief-{date}.md"
  - label: "Fresh Swanson bridges"
    glob: "~/your-brain/Agents/swanson/bridges/validated/*.md"
    max_age_days: 14
  - label: "This week (curator)"
    path: "~/your-brain/Agents/mining/output/{date}/weekly-curator.md"
  - label: "Open tensions (debate)"
    path: "~/your-brain/Agents/mining/output/{date}/weekly-debate.md"
registry:
  path: "~/your-brain/registries/your-brand.md"
  exports_glob: "~/your-projects/your-brand/exports/REG-*/copy.md"
  stale_days: 30
```

---

## Run

```bash
python digest.py [YYYY-MM-DD]
```

Default: today. Outputs two files (latest, dated archive).

---

## Output structure

```
# Content Digest — YYYY-MM-DD

## At a glance
Counts: ready REGs, stale REGs, published, parked, fresh bridges, harvests today.

## 1. SHIP NOW (top picks)
## 2. READY REGs (with checkboxes)
## 2b. STALE REGs (needs status review)
## 3. Full pitch slate
## 4. Cross-platform signals
## 5. Opportunity brief
## 6. Fresh ideas / Swanson bridges + B-terms
## 7. Open tensions / debate
## 8. This week — what you worked on
## 9. Positions & evolutions
## 10. Recently done & parked
## Sources (files read vs missing)
```

Each pitch and each ready REG gets a `- [ ]` checkbox you tick to mark execution intent. Strike-through what you reject.

---

## REG-status filter (built in)

Scans `REG-*/copy.md` frontmatter for `status: published | skipped | etc.` and:
- Drops any duplicate "ship this" recommendation for REGs already shipped/skipped
- Flags REGs that have been in `ready` or `draft` status more than `stale_days` (default 30) as needing a status review (probably died quietly)

The stale-REG section is the key insight — content stacks accumulate dead REGs invisibly. Surfacing them prompts a kill / ship / rebuild decision.

---

## Files in this skill

- `digest.py` — the aggregator
- `digest_config.example.yml` — config template
- `README.md`
