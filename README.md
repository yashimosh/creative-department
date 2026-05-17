# creative-department

An opinionated framework for running agentic creative production in [Claude](https://claude.com). Treat brand voice, design, review, and publishing as a pipeline — not a toolkit.

This package is the frame + patterns + docs + a few bundled skills + one worked example client. It is extracted from the real rig that shipped campaigns for civil-society brands, multilingual publications, and editorial design systems. The conventions are opinionated on purpose: every piece of content goes through `DRAFT → REVIEW → REGISTER → SCHEDULE → LOG`. No orphan files. No skipped gates.

Most agentic design tooling is horizontal — neutral infrastructure for anyone. This is vertical — specific structure for people who already have taste and stakes.

---

## Tiers

| Tier | What you get |
|---|---|
| **Free** | Full core system, all bundled skills, registry, update tether |
| **Pro** | Premium skills, priority updates — [yashimosh.com/creative-department](https://yashimosh.com/creative-department) |
| **Studio** | Team seats, custom skill config, white-label builds — same link |
| **Community** | Skills contributed by others, reviewed and approved by the maintainer |

Pro and Studio licenses are activated with `node license.mjs activate <key>`. Free tier requires nothing.

---

## What's in the package

```
creative-department/
├── ARCHITECTURE.md        System model: how skills, clients, and pipelines compose
├── PIPELINE.md            The DRAFT → REVIEW → REGISTER → SCHEDULE → LOG flow
├── INTEGRATION.md         How this package pairs with a private knowledge system
├── CREATIVE-PLAYBOOK.md   Practice notes for using the package
├── BRAND-VOICE.md         Pattern for calibrating a brand's voice
├── BRIEF-TEMPLATE.md      Brief format for new work
├── PLATFORM-SPECS.md      Social platform specs (dimensions, character limits, etc.)
├── DECISIONS.md           Architectural decision log
├── DESIGN-RATIONALE.md    Design rationale conventions
├── DESIGN-TOKENS.json     Token schema
├── HANDOFF.md             Session-to-session handoff conventions
├── REGISTRY.md            Content registry pattern
├── REGISTRY-TEMPLATE.md   Template for per-client registries
│
├── remotion-studio/       Bundled skill — motion graphics (Remotion, React video)
├── whisper/               Bundled skill — local audio transcription (faster-whisper)
├── audio-enhance/         Bundled skill — voice cleanup (Resemble Enhance)
│
├── clients/
│   └── example-brand/     Worked example client — fork this to start
│
├── registries/            Per-client content registries
└── dispatches/            Session dispatch notes (active / archive)
```

### Bundled vs. bring-your-own

The three skill folders above (`remotion-studio`, `whisper`, `audio-enhance`) ship with the package — they cover video assembly and audio production for the long-form pipeline. The other skills referenced throughout the docs (brand-voice calibration, review gates, graphic design, social scheduling) are **patterns you implement or add**. The framework tells you how to compose them; you bring the specific skill implementations that fit your work.

## How it composes

```
┌─ skills ──────────────────────────────────┐
│  BUNDLED                                  │  Each skill is a folder with
│   remotion-studio / whisper /             │  SKILL.md + assets. Skills are
│   audio-enhance                           │  composable, opinionated, docu-
│                                           │  mented. Bring additional skills
│  BYO patterns                             │  from your own ecosystem.
│   brand-voice calibration                 │
│   review gates (copy, brand, UI)          │
│   graphic design / layout / carousels     │
│   social scheduling (Publer / Buffer /…)  │
└───────────────────────────────────────────┘
          │
          ▼
┌─ clients/<brand>/ ────────┐
│  CLIENT.md                │  Each client has a load order:
│  STRATEGY.md              │  STRATEGY → PERSONALITY → CLIENT → BRAND-VOICE.
│  PERSONALITY.md           │
│  BRAND-VOICE.md           │
└───────────────────────────┘
          │
          ▼
┌─ registries/<brand>.md ───┐  Content registry per brand. Every shippable
└───────────────────────────┘  piece gets a REG-XXXX ID and a status trail.
          │
          ▼
     DRAFT → REVIEW → REGISTER → SCHEDULE → LOG
```

See `ARCHITECTURE.md` for the full model.

---

## The pipeline in practice

A single brand brief enters the system. A typical flow:

1. **Draft** copy against the brand-voice calibration file in `clients/<brand>/BRAND-VOICE.md` (via your copywriter skill of choice)
2. **Review** through the review gates defined in your session (patterns documented in `CREATIVE-PLAYBOOK.md`)
3. **Register** the piece in `registries/<brand>.md` with a REG-XXXX ID and full entry block (see `REGISTRY-TEMPLATE.md`)
4. **Export** the assets — the bundled `remotion-studio` for motion, `whisper` for transcription, `audio-enhance` for voice cleanup; add your own for static design output
5. **Schedule** through your social platform skill (bring your own — Publer, Buffer, direct API, etc.)
6. **Log** the published URLs and any performance notes back into the registry entry

Each step is a skill or pattern. Skills compose. Clients compose. Pipelines compose.

---

## Install

```bash
git clone https://github.com/yashimosh/creative-department
cd creative-department
```

Per-skill install notes live in each skill folder's `SKILL.md`:

- `remotion-studio/` — requires Node
- `whisper/` — requires Python, CUDA recommended
- `audio-enhance/` — requires Python, CUDA recommended

Then in a Claude session (Claude Code, Desktop, or Workbench with MCP), load the client folder for the brand you're producing for. The session reads the files in load order and applies them to every production task.

Start with the `clients/example-brand/` client to see the pipeline run end-to-end.

---

## What this is

- A reference implementation for running agentic creative production with Claude
- Opinionated and documented — every skill has a SKILL.md explaining why
- Extensible — add skills, add clients, add review gates; don't add scope creep
- Designed to be forked and modified; not everything will fit every brand

## What this is not

- A platform or SaaS
- A general-purpose AI framework
- Beginner tutorial content
- Zero-config — you will edit `CLIENT.md`, `BRAND-VOICE.md`, and the skills to match your work

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). Bug fixes and documentation improvements are welcome. Feature PRs require an issue first.

## License

MIT. See [`LICENSE`](LICENSE).

---

Maintained by [@yashimosh](https://github.com/yashimosh).
