# Additions — 2026-05-17

Branch: `feat/2026-05-17-video-pipeline-and-voice-system`

A production session extracted into 7 new skills + 3 templates (incl. 3 worked format examples) + 5 playbook patterns + 1 stack overview. All files are generic / template-ready. Nothing brand-specific leaked in.

---

## File tree (added/modified)

```
creative-department/
├── CREATIVE-PLAYBOOK.md                       ← appended 5 pattern sections
├── AUDIO-STACK.md                             ★ NEW — overview tying the 4 audio skills together
│
├── video-pipeline/                            ★ NEW skill — LOG color grade + RVM matting + bg blur
│   ├── SKILL.md
│   ├── log_to_polished.py
│   ├── luts/README.md                          (drop .cube files here)
│   └── README.md
│
├── video-editor/                              ★ NEW skill — Descript-style transcript editor (intelligent editor)
│   ├── SKILL.md
│   ├── app.py                                  (Flask single-file)
│   └── README.md
│
├── auto-cut-takes/                            ★ NEW skill — detect repeat-restart, cut bad takes
│   ├── SKILL.md
│   ├── auto_cut.py
│   └── README.md
│
├── audio-pipeline/                            ★ NEW skill — sync, replace, normalize, boost, trim, extract, split, info
│   ├── SKILL.md
│   ├── sync_replace.py                         (sync standalone mic to phone video, replace audio)
│   ├── audio_utils.py                          (normalize/boost/trim/extract/split/info subcommands)
│   └── README.md
│
├── audio-editor/                              ★ NEW skill — transcript-driven audio editing (Descript-style, audio-only)
│   ├── SKILL.md
│   ├── app.py                                  (Flask UI on :3029)
│   └── README.md
│
├── audio-enhance/                             (existing — voice cleanup, predates this session, now grouped)
│
├── grade-iterator/                            ★ NEW skill — iterate LOG grades, lock as preset or .cube LUT
│   ├── SKILL.md
│   ├── iterate_grade.py
│   ├── recipes.yml                             (20+ recipe primitives bundled)
│   └── README.md
│
├── content-digest/                            ★ NEW skill — gather all content-agent outputs into one doc
│   ├── SKILL.md
│   ├── digest.py
│   ├── digest_config.example.yml
│   └── README.md
│
├── templates/
│   ├── VIDEO-FORMATS-template.md              ★ NEW
│   ├── REVIEW-LOG-template.md                 ★ NEW
│   └── video-formats-examples/                ★ NEW — three worked formats
│       ├── README.md
│       ├── mossery.md                          (single-take face-cam)
│       ├── split-screen-browser-record.md      (face-cam + browser recording)
│       └── explainer.md                        (VO + B-roll, Johnny Harris shape)
│
└── skills/
    └── mining-pitch.md                        ★ NEW skill manifest
```

**Stats:**
- **7 new skills** (top-level dirs with SKILL.md): video-pipeline, video-editor, auto-cut-takes, audio-pipeline, audio-editor, grade-iterator, content-digest
- **2 new templates** (VIDEO-FORMATS, REVIEW-LOG)
- **3 worked format examples** under templates/video-formats-examples/
- **1 new skill manifest** (skills/mining-pitch.md)
- **1 modified file** (CREATIVE-PLAYBOOK.md — appended ~140 lines)
- **1 new overview doc** (AUDIO-STACK.md — ties the 4 audio skills together)
- **0 brand-specific leaks**

---

## Naming notes

- **"intelligent editor"** = `video-editor/` (Flask Descript-style with word-level cuts + auto-skip playback)
- **"yashar style" renamed** → `split-screen-browser-record` (the name now describes what's actually on screen)
- **"sound tools and pipeline"** = `audio-pipeline/` (sync + replace + boost) and the existing `audio-enhance/` (voice cleanup, predates this session). Both belong to the same audio post stage.
- **LUT-building pipeline with iteration** = `grade-iterator/` — the structured human-in-the-loop iteration we did interactively in the session, now packaged as a reusable CLI. Locks recipes as both pipeline presets AND portable `.cube` LUTs.

---

## What each addition does (one-line each)

### Skills (6)

| Skill | One-line |
|---|---|
| **video-pipeline** | One command: LOG video → color-graded + background blur (post-process Portrait mode with `--keep-bottom` for desk mic / hands) |
| **video-editor** | Free local Descript clone — transcript IS the edit, Delete cuts words from video, playback skips them |
| **auto-cut-takes** | Detects "I stumbled and restarted" patterns in face-cam recordings, cuts the bad takes automatically |
| **audio-pipeline** | Sync standalone mic to phone video, replace audio, plus a utility for normalize/boost/trim/extract/split/info |
| **audio-editor** | Free local Descript-style transcript editor for audio-only files (podcasts, voiceover, audio essays). Audio counterpart of video-editor. |
| **grade-iterator** | Iterate LOG grades through 5-variation rounds, lock the result as a pipeline preset and/or portable `.cube` LUT |
| **content-digest** | Gathers every content-agent output into ONE long reading document with checkboxes for execution intent |
| **mining-pitch** (manifest) | Weekly content pitcher with no-protagonist hard gate, REG-status filter, Belief×Money×Cost framework |

### Templates (2 + 3 examples)

| File | What it provides |
|---|---|
| **VIDEO-FORMATS-template.md** | Schema for naming 2–4 distinct video formats + decision matrix |
| **REVIEW-LOG-template.md** | Persistent voice-review log structure (active rules + chronological log + Claude instructions for the auto-append loop) |
| **video-formats-examples/mossery.md** | Worked example: single-take face-cam, no teleprompter, no B-roll |
| **video-formats-examples/split-screen-browser-record.md** | Worked example: face-cam + browser recording of sources |
| **video-formats-examples/explainer.md** | Worked example: VO + B-roll / motion (Johnny-Harris shape) |

### Playbook patterns (5, appended to CREATIVE-PLAYBOOK.md)

1. **No-protagonist content** — world is subject, operator is observer. Hard gate on pitcher.
2. **Belief × Money-connection × Cost** — pitch evaluation that replaces cadence floors.
3. **Persistent voice review loop** — REVIEW-LOG.md that Claude reads before content sessions AND appends to after corrections.
4. **Named-formats discipline for video** — pick 2–4 formats, name them, no drift.
5. **REG-status filter** — drop pitches for already-shipped/skipped REGs at topic level. Auto-detect stale REGs.

---

## Why this matters (the through-line)

These additions are one coherent system, not a grab bag:

```
                    ┌───────────────────────────────┐
                    │   CREATIVE-PLAYBOOK patterns  │
                    │  (no-protagonist, belief×$×$, │
                    │   review-log loop, formats,   │
                    │   REG-status filter)          │
                    └────────────┬──────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
              ▼                  ▼                  ▼
       ┌───────────┐      ┌────────────┐     ┌──────────┐
       │ templates │      │   mining-  │     │ content- │
       │ + 3       │ ───→ │   pitch    │ ──→ │ digest   │
       │ examples  │      │   skill    │     │ skill    │
       └───────────┘      └────────────┘     └──────────┘
                                 │
                                 ▼
            ┌──────────────────────────────────────────────┐
            │  PRODUCTION TOOLCHAIN                        │
            │                                              │
            │  Record (LOG video + standalone mic)         │
            │    → audio-pipeline (sync + normalize)       │
            │    → audio-enhance (voice cleanup)           │
            │    → audio-editor (transcript-driven cut)    │
            │       (OR pass through to video-editor)      │
            │    → grade-iterator (lock LUT, one-time)     │
            │    → video-pipeline (grade + bg blur)        │
            │    → auto-cut-takes (cut stumbles)           │
            │    → video-editor (fine-tune A+V)            │
            │    → export                                  │
            │                                              │
            │  See AUDIO-STACK.md for the audio path,      │
            │  ADDITIONS§Naming for video.                 │
            └──────────────────────────────────────────────┘
```

The patterns are the philosophy. The templates are the substrate the patterns sit in. The mining-pitch skill enforces the patterns at the pitch-generation stage. The content-digest reads everything back to the operator in one document. The 6 production tools execute the pitches without paid software — together they form a full edit stack: audio sync → voice cleanup → color grading → background blur → stumble cutting → fine-tune cutting → export.

---

## What was NOT added (kept private)

- The actual REG-0014 / REG-0015 / REG-0017 copy.md scripts
- The yashimosh STRATEGY.md (money goal, intersection, mic + desk setup)
- The yashimosh REVIEW-LOG.md entries (specific quotes from real corrections)
- The Swanson config with yashimosh's specific fields/pairs
- The yashimosh.md content registry

The Samsung Galaxy Pro Video LOG-tuned `c5` recipe IS included as a preset in `video-pipeline` and in `grade-iterator/recipes.yml` as `aggressive-protected` — it's broadly useful and not personally-identifying.

---

## Verify before merging

1. Read this doc top to bottom — it should match what you remember from the session.
2. Open each new SKILL.md and scan the description.
3. Check `CREATIVE-PLAYBOOK.md` end of file (lines ~140 onward) — the 5 pattern sections.
4. Spot-check 1–2 of the templates for tone and genericness.
5. Open `templates/video-formats-examples/` and verify the three formats read as worked examples not prescriptive specs.
6. Read `grade-iterator/SKILL.md` workflow — the iteration loop description should match what we actually did in the session.

If anything reads as too brand-specific or too prescriptive for a framework, flag and I'll edit.

---

## Branch + commit plan

Currently on branch `feat/2026-05-17-video-pipeline-and-voice-system`. Nothing committed yet — all files are unstaged. Once approved:

```bash
cd creative-department
git add .
git commit -m "feat: video + audio pipeline + grade iterator + voice review system

- 6 new skills (video-pipeline, video-editor, auto-cut-takes, audio-pipeline,
  grade-iterator, content-digest)
- 2 new templates (VIDEO-FORMATS, REVIEW-LOG) + 3 worked format examples
  (mossery, split-screen-browser-record, explainer)
- mining-pitch skill manifest with no-protagonist + REG-status filter + Belief×Money×Cost
- CREATIVE-PLAYBOOK: 5 pattern sections added (no-protagonist, scoring framework,
  voice review loop, named-formats discipline, REG-status filter)
- ADDITIONS-2026-05-17.md summary doc"

git push -u origin feat/2026-05-17-video-pipeline-and-voice-system
gh pr create --title "Video + audio pipeline + grade iterator + voice review system" --body "See ADDITIONS-2026-05-17.md"
```

Or merge to main directly if no PR review step needed.

---

## Next conversation (queued)

Once these are merged, the user wants to discuss **integrating content agents (or their outputs) into the creative-department repo** — i.e. how to bring the mining stack, viral-scout, swanson, etc. into this public framework without leaking private content. That's its own design conversation.
