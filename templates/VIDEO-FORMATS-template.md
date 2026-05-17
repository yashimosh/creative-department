---
brand: your-brand-here
layer: format-reference
status: active
last-updated: YYYY-MM-DD
purpose: Canonical list of vertical video formats this brand uses. Every video pitch declares which one. Read by mining-pitch, content-brief, content-engine.
---

# Vertical Video Formats — your-brand-here

> **The point of this file:** instead of "let's make a Reel," every video pitch must name *which* format. Limit yourself to 2–4 distinct formats with clear definitions. This kills format drift, sets production cost expectations, and matches the right shape to the right idea.

## Why limit yourself?

Most creators flail across every format the algorithm offers. Picking 2–4 and naming them does three things:

1. **Production cost gets predictable** — you know "this is a 15-min mossery" vs "this is a 4-hour explainer" before you start
2. **The pitcher proposes a format alongside the pitch** — no more "what format should this be?" stalling
3. **The audience develops a shape recognition** for your work — same kind of shape across uploads compounds into recognizability

---

## Format N — [Name]

**Format slug:** `slug-name` (used in pitch frontmatter)
**Length:** 45–90s (or whatever range fits)
**Aspect:** 9:16 vertical

### Structure

Describe the visual + structural rules in 2–3 sentences. Example: "Single take. Desk-cam. One thought, finished. Talking-head face-cam, eyes at lens."

### What it isn't

- List 3–5 things this format DOESN'T do
- Often more useful than what it does
- Examples: "No B-roll", "No music", "No retention-bait pacing"

### When to use

Bullet list of pitch types that fit this format. Example: "Question-register / thinking-aloud", "Reference-share posts", "Anytime the medium is meant to perform what it's describing"

### Reference creators

List 3–5 specific creators whose output exemplifies this format. Helps the pitcher (and you) recognize the shape.

### Production cost

Low / Medium / High + estimated minutes per piece.

### Examples in registry

Link to REG-XXXX entries where this format was used.

---

## Format selection — quick decision matrix

| Pitch shape | Likely format |
|---|---|
| Question-register / thinking-aloud | Format 1 |
| Reference-share | Format 1 |
| Cultural observation about a specific artifact | Format 2 |
| Source-quotation piece | Format 2 |
| Visual subject that needs showing | Format 3 |
| Anything Yash is the literal subject of | **NONE — fails no-protagonist** |

---

## Rules

1. Every video pitch MUST have a `video_preset:` line in its frontmatter set to one of the slugs above.
2. The pitcher MUST propose the format alongside the pitch — don't make you choose blind.
3. New format ideas are written down here BEFORE shipping. No format drift without an explicit update to this file.
4. One format is the default for short-turnaround / weekly cadence. The heavier formats are reserved.

---

## Worked example: yashimosh's three formats

See `clients/example-brand/VIDEO-FORMATS.md` for a worked example with three formats (mossery / split-screen-shortform / explainer) and full production notes.
