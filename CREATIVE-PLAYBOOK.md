# CREATIVE PLAYBOOK
<!-- Per-client document. A living record of what works, what doesn't, and how to approach this client. -->
<!-- Copy this template and save as CREATIVE-PLAYBOOK-[client-slug].md for multi-client work. -->

## Client
- **Name:** [Client / Brand Name]
- **Started:** [YYYY-MM-DD]
- **Last updated:** [YYYY-MM-DD]

---

## What Works

Approaches, formats, styles, and tactics that have performed well or received positive feedback. Update after every project.

### Content Formats
| Format | Platform | Why It Works | Example |
|---|---|---|---|
| | | | |

### Visual Approaches
| Approach | Why It Works | Example |
|---|---|---|
| | | |

### Copy Patterns
| Pattern | Why It Works | Example |
|---|---|---|
| | | |

### Posting & Timing
| Insight | Source |
|---|---|
| | |

---

## What Doesn't Work

Approaches that failed, underperformed, or received negative feedback. Document so they're never repeated.

| What Was Tried | Why It Failed | Date |
|---|---|---|
| | | |

---

## Recurring Feedback

Patterns in client/audience feedback that should inform all future work.

| Feedback Theme | Frequency | How to Address |
|---|---|---|
| | | |

---

## Client Preferences & Quirks

Things you learn about the client over time that aren't in the brand guidelines but matter.

- [e.g. "Client always wants to see 3 options, not 1"]
- [e.g. "Client is very particular about headline capitalization — always sentence case"]
- [e.g. "Revision rounds: rarely more than 1 if copy is reviewed first"]
- [e.g. "Client prefers Canva for minor edits — always export editable format"]

---

## Audience Insights

What you've learned about the client's audience through engagement data, comments, and research.

| Insight | Source | Date |
|---|---|---|
| | | |

---

## Skill-Specific Notes

Notes for specific skills when working on this client.

### /copywriter
- [e.g. "Keep sentences under 15 words. This audience scans."]

### /graphic-designer
- [e.g. "Always include the logo watermark on carousel slides"]

### /video-editor
- [e.g. "Hook must be in first 2 seconds — audience drops off fast"]

### /caption-instagram
- [e.g. "Hashtag set A performs better than set B — use A unless seasonal"]

<!-- Add sections for any skill that has client-specific notes -->

---

## Campaign History

Quick reference to past campaigns and their outcomes.

| Campaign | Date | Platforms | Result | Registry Entries |
|---|---|---|---|---|
| | | | | REG-XXXX to REG-XXXX |

---

## Patterns added 2026-05-17

The following patterns were extracted from a real production session and merged into the playbook. They're listed here because they're proven, not because they're prescriptive — adopt the ones that fit your operation.

### No-protagonist content

**The world is the subject. The operator is the observer.**

The temptation in personal-brand content is to be the subject — talk about what you built, how you work, what your system does. This produces "showing off" energy that filters out the audience you actually want (taste-led practitioners, prospective clients, peer creators) and attracts the audience you don't (general curiosity, brand-watchers).

The shape that works is observation, reading, or question — applied to something *in the world*. Receipts (what the operator has built, who they've worked with) leak through implicitly by what they notice and how they handle it.

**Three shapes that pass:**
1. **Observation** — "Here's a thing I noticed about X" (X is external)
2. **Reading** — "I read this and here's what struck me" (source is the anchor)
3. **Question** — "I keep wondering about Y" (searcher, not authority)

**Four shapes to suppress by default:**
- "Brain peek" / "show your system" — makes the operator the protagonist
- "Working in public" as the *subject* (vs. as a side effect of subject choice)
- "Agent peek" / "process moment" — self as subject
- "Mini case study" on the operator's own projects — receipt becomes flex

**Wire this into mining-pitch** as a hard gate: pitches whose subject is the operator/system get capped at 1 per week total. The bar is `if the first sentence starts with "I" or "my," rebuild`.

---

### Belief × Money-connection × Cost pitch framework

Replaces cadence floors ("you must ship 4 Reels/week"). Cadence floors produce compulsion-content the operator doesn't believe in, which doesn't compound — it produces noise that fills calendars.

Every pitch is scored on three axes before shipping:

| Axis | Question | Hard requirements |
|---|---|---|
| **Belief** | Does the operator genuinely believe in this enough to ship without faking? | HIGH required, non-negotiable |
| **Money-connection** | Does this plausibly reach people who hire, buy, or recommend? | Medium or High preferred |
| **Cost** | Production weight in formats the operator can actually execute now | Lower is better |

**Ship rule:** belief MUST be HIGH. Then ship if money is medium+ OR cost is low. Skip otherwise.

**Anti-perfectionism:** any pitch alive >14 days without shipping forces a decision (ship / kill / rebuild). No quiet death.

This framework respects the integrity constraint (no disbelieved content) without surrendering the discipline that floor-based cadences provide (the 14-day decision-force).

---

### Persistent voice review loop

A `REVIEW-LOG.md` file in the brand folder that accumulates every voice/content correction the operator has ever given, with a rolled-up "Active rules" section at the top.

**Two parts make it work:**

1. **Claude reads it before any content session.** Loaded via STRATEGY.md's "Session load order" and reinforced in mining-pitch (REQUIRED read). Active rules apply automatically without the operator restating them.

2. **Claude appends to it whenever the operator gives a correction.** Hooked via global CLAUDE.md: "if the operator gives a content correction, apply the fix, then append a new entry to REVIEW-LOG.md before ending the turn." Entry includes date, the verbatim quote, the distilled rule, what it applies to.

Newer entries don't replace older ones — they compound. The rolled-up Active Rules section is the synthesized current state; the chronological log preserves the source quotes for context.

After ~50 entries, a quarterly synthesis pass consolidates patterns without losing the source material.

See `templates/REVIEW-LOG-template.md` for the structure.

---

### Named-formats discipline for video

Most creators flail across every format the algorithm offers. The discipline: pick 2–4 distinct video formats, name them, define them in `VIDEO-FORMATS.md`, and require every video pitch to declare which one it is.

Three things this gives you:

1. **Production cost gets predictable** — you know "this is a 15-min single-take" vs "this is a 4-hour explainer" before you start
2. **The pitcher proposes a format alongside the pitch** — no "what format should this be?" stalling
3. **The audience develops shape recognition** — same kind of shape across uploads compounds into recognizability

New format ideas are written down in VIDEO-FORMATS.md BEFORE shipping. No format drift without an explicit update.

See `templates/VIDEO-FORMATS-template.md`.

---

### REG-status filter (drop already-shipped or killed REGs at topic level)

The mining pitcher reads upstream agent outputs. Upstream agents are written at different times and can be stale — they may recommend "ship REG-0011 today" when REG-0011 was published yesterday.

The filter, run at the start of every pitcher invocation:

1. Scan all `REG-*/copy.md` exports
2. Read `status:` frontmatter from each
3. Build `shipped` and `skipped` sets
4. **Drop any pitch that recommends or references a REG in either set** before it enters the slate
5. **Topic-level filter:** for each shipped REG, extract its subject. Drop any pitch substantively about the same subject — even framed as "extended/long-form/follow-up." Re-treads require explicit operator opt-in.

Same filter detects **stale REGs** — those in `ready` or `draft` status more than N days (default 30). These probably died quietly. Surface them as "needs status review" so the operator decides ship/kill/rebuild instead of letting them rot.

Built into both `content-digest` and `content-hub` skills.

---

