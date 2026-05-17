# Creative Department — Output Registry

Every deliverable that leaves this department gets registered. No exceptions.

Each client/brand has its own registry file in `creative-department/registries/`.

---

## Client Registries

| Client/Brand | Registry File | Status | Brand Files | Content Archive |
|---|---|---|---|---|
| Example Brand | `registries/example-brand.md` | example | `clients/example-brand/` | `local: example-archive/` |

> **Path conventions:**
> - Plain/relative paths live inside this skill package (public, standalone)
> - `private: ...` references a private knowledge system outside this package (see `INTEGRATION.md` for the optional pattern)
> - `local: ...` references a local-only workspace outside any repo (brand assets, archives)
>
> The `example-brand/` row is a placeholder — when you fork this package, replace it with your real clients.

---

## How to Register a Deliverable

1. Identify the client/brand
2. If no registry file exists yet, create one from `REGISTRY-TEMPLATE.md` at `registries/{client-slug}.md`
3. Copy the **entry block** from the template
4. Fill in all required fields
5. Append under the correct month heading (newest first)
6. Update the table above if this is a new client
7. Commit and push to GitHub

## How to Onboard a New Client

1. Create `registries/{client-slug}.md` using the header from `REGISTRY-TEMPLATE.md`
2. Add the client row to the table above
3. Fill in the client's `CLIENT.md` (or a per-client variant)
4. Set up the content archive path in the registry header

---

## Session Rules

These apply to every session that touches client content:

| Trigger | Action |
|---|---|
| Starting a production session | Read the client registry first — check what exists, what's ready, what's in progress |
| After producing any content | Create a registry entry immediately — not at session end |
| Content status changes | Update the registry entry in the same session |
| After publishing | Add live URLs to the Published field, set status to `published` |
| After any post is removed | Set status to `removed`, note reason in Notes |

**The registry is the master record for status. The content file is the content. Both must exist.**

---

## Live Status — Optional Notion Dashboard

**Optional integration.** If the operator uses Notion as a pipeline dashboard, every content piece should have a row there in addition to its file registry entry. Otherwise this section can be ignored — the file registry is sufficient on its own.

- **Pattern:** A "Content Registry" database per operator, keyed on the same REG-XXXX IDs used in the file registry
- **Sync rule:** When status changes in the file registry, update the Notion row in the same session. They must stay in sync.
- **Configuration:** The Notion page URL and workspace ID are operator-specific and should be stored in a local config file outside this package (e.g. `local: notion-config.md` or an env var), not committed.

Operator-specific Notion workspace URLs and credentials live in each operator's local setup, not in this package.

---

## Status Flow

```
idea → draft → ready → exported → published
                               ↘ removed
```

Notion equivalent: `Idea → Brief → Draft → Review → Scheduled → Published`

---

## Rules

- **One registry per client/brand** — never mix brands in a single file
- **Register immediately** after publish/deliver — not at session end
- **Sequential IDs** per client — each client's entries start at `REG-0001`
- **If it shipped, it gets registered**
- **If it exists as a file, it has a registry entry** — no orphan content files
