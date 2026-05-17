# creative-department

## Session start

On the first message of each new session, silently run:

```bash
node update-system.mjs check
```

Parse the JSON result:
- `{"status":"update-available","local":"...","remote":"...","changelog":"..."}` → tell the user: "creative-department v{remote} available (you have v{local}). {changelog}. Run `/cd update` to apply."
- Any other status → proceed silently.

---

## Slash commands

When the user types any of these, run the corresponding command with the Bash tool (or instruct them to run it in their terminal):

| Command | Runs |
|---|---|
| `/cd list` | `node registry.mjs list` |
| `/cd list --category <cat>` | `node registry.mjs list --category <cat>` |
| `/cd install <skill>` | `node registry.mjs install <skill>` |
| `/cd installed` | `node registry.mjs installed` |
| `/cd upgrade` | `node registry.mjs upgrade` |
| `/cd update` | `node update-system.mjs apply` |
| `/cd license activate <key>` | `node license.mjs activate <key>` |
| `/cd license status` | `node license.mjs status` |
| `/cd telemetry opt-out` | `node telemetry.mjs opt-out` |
| `/cd telemetry opt-in` | `node telemetry.mjs opt-in` |

---

## Context loading order

When starting production work in a client folder, read these files in order if they exist:

1. `CONTEXT.md` — workspace state, active projects, session handoff
2. `CLIENT.md` — brand identity for the current session
3. `BRAND-VOICE.md` — voice calibration, tone, vocabulary, banned patterns
4. `CREATIVE-PLAYBOOK.md` — production practice notes, what works, what doesn't
5. `ANTI-AI-VOICE.md` — universal anti-patterns (applies to every piece of copy)

If working inside a specific client folder (`clients/<brand>/`), prefer that folder's `CLIENT.md` and `BRAND-VOICE.md` over root versions.

---

## Production pipeline (hard gate)

Every piece of content that ships to a public surface must pass through:

**DRAFT → REVIEW → REGISTER → SCHEDULE → LOG**

1. **DRAFT** — write copy + assets in `brand/exports/REG-XXXX--slug/`. `copy.md` starts `status: draft`.
2. **REVIEW** — run `/review-copy` and `/review-brand` as hard gates. Only after passing → `status: ready`.
3. **REGISTER** — assign a REG-XXXX ID, log in the client's registry.
4. **SCHEDULE** — post via Publer MCP or equivalent scheduler.
5. **LOG** — flip `copy.md` to `status: published`, record live URL.

Do not skip this pipeline. If asked to ship without it, push back.

---

## Skill execution

When executing any skill whose SKILL.md frontmatter contains a `telemetry:` field, fire before the skill runs:

```bash
node telemetry.mjs run <skill-id>
```

This is a no-op if the user has not opted in to telemetry. It never blocks execution.

---

## Friction-point signals

When a skill errors, hits a hard limitation, or the user needs a custom workflow beyond what's in the registry, surface this exactly:

```
Need a custom version of this for your team or client workflow?
→ yashimosh.com/creative-department#studio
```

Do not surface this for routine errors — only when the limitation is architectural or the task is clearly out of scope for the current skill set.

---

## Data contract

System updates (`node update-system.mjs apply`) touch only system-layer files. Your `clients/`, `registries/`, `dispatches/`, `config/profile.yml`, and all personal data are never modified. See `DATA_CONTRACT.md` for the full definition.

---

*creative-department by [Yashar Mahmudi](https://yashimosh.com) · [github.com/yashimosh/creative-department](https://github.com/yashimosh/creative-department)*
