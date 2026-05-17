# Creative Department — Decisions Log

A rolling log of architectural decisions about the Creative Department itself. Not content decisions (those live in per-client files) — decisions about how the CD is structured, what conventions it follows, and why.

Newest entries on top.

---

## 2026-04-12 — Standalone-safe path conventions

**What changed:** Introduced `private: ...` and `local-assets: ...` path prefixes for references to files outside this package. Scrubbed all absolute paths from client files, registry files, and templates. Replaced Notion URLs with optional-pattern language.

**Why:** The CD is structured to eventually go public as a standalone skill package. Private paths (personal knowledge systems, local asset workspaces, specific Notion pages) must not leak into files that will ship in a public repo. The convention preserves the signal that "this references something" without leaking Yash's file system structure or account IDs.

**Impact:** All new content added to this package must follow the convention. Any path that points outside `creative-department/` (or outside the parent `claude-skills/` package) must use one of these prefixes:
- Plain/relative → inside this package (public, standalone)
- `private: ...` → private knowledge system outside the package
- `local-assets: ...` → local asset workspace outside any repo

**Related:** INTEGRATION.md explains the optional pattern for pairing this package with a private knowledge system on the operator's local setup.

---

## 2026-04-12 — Strategy layer merged into client folder (Option A)

**What changed:** Added a strategy layer (`STRATEGY.md`) as a peer of `PERSONALITY.md`, `CLIENT.md`, and `BRAND-VOICE.md` inside each client folder. Wired it into the session load order as the first file loaded.

**Why:** Drift risk. When brand strategy lives in a separate private knowledge system and production files live in the CD, the two can diverge inside a single session. Every production session would then pull whichever frame got loaded first, not necessarily the latest strategic intent. Merging the strategy layer into the CD eliminates the drift surface — one source of truth, loaded automatically by every session.

**Impact:** The strategy layer is now part of the CD. Future positioning shifts get written directly into `clients/{brand}/STRATEGY.md` and take effect on the next session without any separate-system sync step.

**Considered but rejected:**
- **Merge CD into private knowledge system (Option C):** rejected because the CD needs to eventually ship as a standalone public package.
- **Keep systems separate (Option B status quo):** rejected because drift had already been demonstrated.

---

## Earlier entries (pre-2026-04-12)

Earlier architectural decisions were not logged in this file — they live in git history and in individual file change notes. This decisions log starts on 2026-04-12. Future architectural changes should be recorded here as they happen, not after the fact.
