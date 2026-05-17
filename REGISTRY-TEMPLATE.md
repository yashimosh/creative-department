# Registry — {Client/Brand Name}

**Client:** {name}
**Created:** {YYYY-MM-DD}
**Status:** active
**Content archive:** {path to content files — use `private: {your-path}` if stored outside this package}

---

<!-- REGISTRY ENTRIES — newest month on top -->

## YYYY-MM

_No entries yet._

---

# Entry Template

Copy this block and append it under the correct month heading above.

```markdown
### [REG-XXXX] slug — Title

- **Date:** YYYY-MM-DD
- **Type:** text | image | carousel | video | reel | thread | article
- **Platform(s):** X | LinkedIn | Instagram | Threads | YouTube | Facebook
- **Pillar:** 1 | 2 | 3 | 4
- **Tags:** [tag, tag]
- **Campaign:** [campaign-slug] or standalone
- **Status:** idea | draft | ready | exported | published | removed
- **Scheduled:** YYYY-MM-DD HH:MM [timezone] or ~
- **Brief:** [one-line angle — what's the take]
- **File:** [path to content file, or ~]
- **Assets:** [path to exported files — images, video, etc. — or ~]
- **Created by:** [skills/agents that produced it]
- **Reviewed by:** [review skills or client — or "none"]
- **Published:**
  - X: ~
  - LinkedIn: ~
  - Instagram: ~
  - Threads: ~
- **Performance:** ~
- **Notes:** [voice corrections, decisions, what worked, what didn't]
```

---

## Field Guide

| Field | Required | Notes |
|---|---|---|
| REG-XXXX | Yes | Sequential per client. Check last entry and increment. |
| slug | Yes | Short identifier matching the content file slug |
| Title | Yes | Short, descriptive |
| Date | Yes | Date published — or date created if not yet published |
| Type | Yes | Pick one. Carousel of images is "carousel", not "image". |
| Platform(s) | Yes | All platforms this piece is intended for |
| Pillar | Yes | Content pillar number |
| Tags | Yes | Searchable keywords |
| Campaign | Yes | Campaign slug if part of a series, otherwise "standalone" |
| Status | Yes | See status flow below |
| Scheduled | Optional | Target publish date/time if known |
| Brief | Yes | The angle — what's the take or concept |
| File | Yes | Path to the content file in the brain/workspace |
| Assets | Optional | Exported image/video files ready to upload |
| Created by | Yes | Which skills/agents produced it |
| Reviewed by | Optional | Review skills applied, or client name |
| Published | Yes | Per-platform live URLs once posted, ~ if not yet |
| Performance | Optional | Engagement notes — filled in post-publish |
| Notes | Optional | Voice corrections, decisions, learnings |

---

## Status Flow

```
idea → draft → ready → exported → published
                                ↘ removed
```

| Status | Meaning |
|---|---|
| `idea` | Raw concept captured — no copy written yet |
| `draft` | Copy in progress — not finished |
| `ready` | Copy finished and approved — waiting to publish |
| `exported` | Assets rendered/exported — images/video files ready to upload |
| `published` | Live on platform(s) — add links to Published field |
| `removed` | Taken down or archived — note reason in Notes |

---

## Session Rules

Every session that touches content for this client MUST:

1. **Before producing** — check this registry for existing ideas and drafts. Don't duplicate.
2. **After producing** — create a registry entry immediately. Not at session end.
3. **After publishing** — update status to `published`, add live URLs to Published field.
4. **After any post is removed** — update status to `removed`, note reason.

The registry is the master record. The content file is the content. Both must exist.
