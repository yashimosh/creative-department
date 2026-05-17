# Integration — Optional Patterns

The Creative Department is designed to **work standalone**. You can drop it into a fresh machine, point it at a client folder, and it will produce, review, and register content without any other systems.

This file documents **optional integration patterns** that some operators use to pair the CD with a private knowledge system, a local asset workspace, or a live pipeline dashboard. None of these are required. If you use the CD by itself, skip this file.

---

## Pattern 1 — Brain + CD (private knowledge system pairing)

**What it is:** Pair the public CD skill with a private, git-synced markdown knowledge base ("the Brain") that holds personal notes, infrastructure context, project files, and anything too sensitive or too operator-specific to ship in a public package.

**When to use it:** You already keep a structured personal knowledge system in markdown, and you want your creative work to coexist with your project/infra notes without entangling the two.

**Rules for the pairing to stay clean:**

1. **The CD is the source of truth for creative work.** Brand files, registry, dispatches, production output — all live inside `creative-department/`.
2. **The Brain is the source of truth for everything else.** Infra, project specs, personal notes, private context.
3. **Cross-links go one direction only: Brain → CD.** The Brain may contain `see: ~/claude-code-projects/claude-skills/creative-department/clients/{slug}/STRATEGY.md`-style pointers. The CD MUST NOT contain any path that points into the Brain — those paths would leak if the CD is released publicly.
4. **Private paths referenced from inside the CD use prefixes, never absolute paths:**
   - `private: your-workspace/social-content/...` — file inside a private knowledge system
   - `local-assets: your-brand/exports/...` — file inside a local asset workspace outside any repo
   These prefixes carry the signal that "something lives here" without exposing the operator's file system layout.
5. **Drift is the enemy.** If the same fact lives in both systems, one will go stale. Pick one system as the canonical home for each type of fact. Typical pattern: brand strategy and voice live in the CD (e.g. `clients/your-brand/STRATEGY.md`); a separate private knowledge system, if you use one, holds a pointer file only.

**Example operator setup:** One working configuration — a private "Brain" repo synced to a private GitHub remote, and a public claude-skills repo that contains this Creative Department package. The Brain's per-project files hold short pointer stubs that tell any Brain-reading session to load canonical strategy/brand files from the CD client folder instead. The CD files never mention the Brain by name or by path — they're written so a cold reader with no Brain can use them standalone.

---

## Pattern 2 — Local asset workspace

**What it is:** A local directory outside any git repo that holds large binary assets (exported images, carousel frames, video renders, mockups) keyed by registry ID.

**When to use it:** You produce image/video assets that are too heavy or too numerous to commit, but you want them traceable from the registry.

**Convention:**
- Directory structure: `{asset-workspace}/exports/REG-XXXX--{slug}/`
- Referenced from registry entries as `local-assets: {brand}/exports/REG-XXXX--{slug}/`
- One folder per registered deliverable, named after the REG ID

**Why not commit assets:** Binary churn, file size, and private/unpublished work all argue against putting exports in the skills repo.

---

## Pattern 3 — Live pipeline dashboard (Notion or similar)

**What it is:** A database (most commonly a Notion Content Registry) that mirrors the file registry and gives a real-time dashboard of what's in the pipeline at any stage.

**When to use it:** You want non-technical visibility into pipeline status — a board where you can see every piece in Idea/Brief/Draft/Review/Scheduled/Published without cracking open markdown files.

**Rules:**
- The **file registry** (`registries/{client}.md`) is the source of truth for content files.
- The **dashboard** is the source of truth for live status.
- They must stay in sync within a session — when a session updates one, it updates the other.
- Configuration (workspace URL, page ID, API keys) lives in a **local config file outside this package**, never committed.

**Schema for Notion Content Registry** (if you adopt this pattern): see `PIPELINE.md` → "Live Pipeline Visibility — Optional Notion Dashboard".

---

## Pattern 4 — Private per-client notes

**What it is:** Private annotations attached to a client folder that should stay out of any public release of the CD.

**Convention:** Use filenames that match a `.gitignore` pattern — e.g. `PRIVATE-*.md` or `*.private.md` inside `clients/{slug}/`. Never reference these files from any public file in the CD.

**Example use cases:** a private pricing sheet, a list of prospects, sensitive client feedback, internal political context.

If you adopt this pattern, make sure your repo's `.gitignore` excludes the private filename pattern before adding any private content.

---

## What the CD does NOT require

The CD works without any of the above. Specifically, you do NOT need:

- A private knowledge system of any kind
- Notion, Airtable, or any dashboard tool
- Any MCP servers beyond the ones the CD skill itself needs
- A local asset workspace (you can commit small assets inside the CD if the repo is private)
- Any external config files

A fresh user should be able to clone the skills repo, open `creative-department/`, read `ARCHITECTURE.md` and `PIPELINE.md`, and start producing content for a new client immediately.

---

## Path Convention Reference

When a CD file needs to reference something outside the package, use one of these prefixes:

| Prefix | Meaning | Example |
|---|---|---|
| (plain/relative) | Inside the CD package | `../clients/example-brand/STRATEGY.md` |
| `private: ...` | Private knowledge system outside the package | `private: your-workspace/social-content/post.md` |
| `local-assets: ...` | Local asset workspace outside any repo | `local-assets: your-brand/exports/REG-XXXX/` |

**Never write absolute paths** (e.g. operator home directories, Windows user folders, or references to a specific private knowledge system by name) in any CD file. Those are operator-specific and will leak when the CD ships publicly. Use the prefixes above instead.

---

## Related

- `DECISIONS.md` — architectural decisions including the 2026-04-12 standalone-safety pass
- `ARCHITECTURE.md` — how the CD is organized internally
- `PIPELINE.md` — the 8-stage pipeline all deliverables flow through
- `REGISTRY.md` — output registry and session rules
