# DATA_CONTRACT.md

This file defines the boundary between the system layer and the user layer.

The rule is simple: **system updates pull only system-layer files. The user layer is never touched.**

---

## System layer — auto-updatable

`node update-system.mjs apply` may modify any of these:

| Path | Description |
|---|---|
| `ANTI-AI-VOICE.md` | Universal anti-AI-voice rules |
| `ARCHITECTURE.md` | System model documentation |
| `BRIEF-TEMPLATE.md` | Brief format template |
| `CHANGELOG.md` | Release changelog |
| `CODE_OF_CONDUCT.md` | Contributor code of conduct |
| `CONTRIBUTING.md` | Contribution guidelines |
| `DATA_CONTRACT.md` | This file |
| `DECISIONS.md` | Architectural decision log |
| `DESIGN-RATIONALE.md` | Design rationale conventions |
| `DESIGN-TOKENS.json` | Token schema |
| `HANDOFF.md` | Session handoff conventions |
| `INTEGRATION.md` | Private knowledge system pairing guide |
| `LICENSE` | License |
| `PIPELINE.md` | Production pipeline stages |
| `PLATFORM-SPECS.md` | Platform dimensions + character limits |
| `README.md` | Main documentation |
| `REGISTRY.md` | Content registry pattern |
| `REGISTRY-TEMPLATE.md` | Per-client registry template |
| `TOOLS.md` | Tool inventory |
| `CLAUDE.md` | Session behavior + slash commands |
| `VERSION` | Semantic version string |
| `registry.json` | Skill registry index |
| `package.json` | Node.js manifest |
| `update-system.mjs` | Update tether |
| `registry.mjs` | Skill registry client |
| `telemetry.mjs` | Telemetry client |
| `license.mjs` | License client |
| `setup.mjs` | First-run setup wizard |
| `scripts/` | Sync and utility scripts |
| `audio-enhance/` | Bundled skill: audio enhancement |
| `whisper/` | Bundled skill: transcription |
| `remotion-studio/` | Bundled skill: motion graphics |
| `templates/` | Shared production templates |
| `config/profile.example.yml` | Profile template (example only) |

---

## User layer — never touched by updates

These paths are owned by the operator. `update-system.mjs apply` will abort if any of these are modified.

| Path | Description |
|---|---|
| `config/profile.yml` | Your personal/team profile |
| `config/license.json` | Your license key + tier (gitignored) |
| `config/telemetry.json` | Your telemetry preference + install ID (gitignored) |
| `config/installed.json` | Your installed skill manifest |
| `clients/` | Your client brand folders |
| `registries/` | Your per-client content registries |
| `dispatches/` | Your session dispatch notes |
| `data/` | Your production data |
| `output/` | Your generated output |
| `CONTEXT.md` | Your operational workspace context |
| `CLIENT.md` | Your brand identity file |
| `BRAND-VOICE.md` | Your brand voice calibration |
| `CREATIVE-PLAYBOOK.md` | Your production practice notes |

Any locally created skills (not installed via registry) live outside the above paths and are also never touched.

---

## Enforcement

The updater enforces this contract at runtime. If a system update checkout modifies a user-layer path, it aborts immediately and rolls back that file before exiting. User data loss from updates is not possible by design.

To verify the contract is intact: `node update-system.mjs check`  
To apply an update: `node update-system.mjs apply`  
To roll back: `node update-system.mjs rollback`
