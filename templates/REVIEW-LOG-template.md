---
brand: your-brand-here
layer: voice-review-log
status: active
last-updated: YYYY-MM-DD
purpose: Persistent, accumulating log of voice and content reviews the operator has given. Every correction lives here. Loaded by every content-generating skill before producing copy. Grows over time like a child learning — newer entries compound, they do not replace older ones.
---

# Voice Review Log — your-brand-here

This file is the accumulated personal review. It grows whenever the operator gives a correction. Newer entries don't replace older ones — they compound. If a new rule contradicts an older one, mark the older one `superseded` with a date and reason, but keep it in the log for context.

**Every content-generating skill (mining-pitch, content-brief, content-engine, any script-writing) MUST read this file before producing copy. Apply the active rules below BEFORE the operator has to tell you.**

---

## ⚠️ Instructions for Claude (you, reading this)

If the operator just gave you a content correction in any session:

1. **Apply the fix to the content first** (don't make them wait).
2. **Append a new entry to the "Review log (chronological)" section below** before ending your turn. Include: date, the quote (verbatim), the distilled rule, what it applies to.
3. **If the new entry surfaces a pattern not already in "Active rules,"** update that section too.
4. **Commit the change to git** so it persists across machines.

This file is how the brand operator teaches the system. Don't break the loop.

---

## Active rules (rolled-up — read these first)

> **Replace this section's contents with your own rules as they emerge.** The structure below is a suggested set of buckets — keep what serves you, delete what doesn't.

### Goal and method
- **The goal of content for this brand:** [income / reputation / community / awareness / etc.]
- **The constraint that limits which content gets made:** [integrity / safety / time / etc.]
- **The method for deciding what ships:** [cadence floors / case-by-case scoring / committee approval / etc.]

### Register — the spine
- The narrator stance: [authority / searcher / observer / advocate / etc.]
- Audience layers: [who must be able to follow / who must recognize depth]
- Protagonist rule: [is the operator the subject? when?]

### Voice — banned patterns
- List patterns the operator has explicitly rejected
- Each with a one-line example
- Examples to consider banning by default: triplets, staccato lists, aphorism closers, written-register patterns in spoken scripts, em-dash appositions where a period would breathe, `and...and` clusters, LinkedIn-bro / manifesto, motivational quotes, hashtag walls, identity labels

### Voice — required patterns
- Patterns the operator has explicitly demanded
- Examples to consider requiring by default: connective tissue ("so", "because", "which means"), speech-not-prose, state the observation don't imply it, time anchors, trail-off closers when the question stays open

### Structure — what every piece needs
1. Hook anchored to [what]
2. The problem
3. The thought
4. The close

### Format defaults
- Primary formats by surface
- Video opt-in vs opt-out
- Cadence philosophy

### Research / fact-check
- For empirical claims: cite source, year, finding
- What you must NOT claim without evidence
- What's defensible vs hand-wave

---

## Review log (chronological — newest first, never delete)

### YYYY-MM-DD — [Short title of the correction]
**Operator:** "[Verbatim quote of the correction]"
**Distilled rule:** [The rule in your own words, applicable beyond the specific instance]
**Applies to:** [Which content types / contexts]
**Pattern added to Active Rules:** [Which section of Active Rules was updated, or "new section" if it created a new bucket]

### YYYY-MM-DD — [Next correction]
...

---

## How this file grows

- Every time the operator gives a content correction → new entry in "Review log" with date, quote, distilled rule.
- If the entry surfaces a new pattern → also update "Active rules."
- Older rules stay even when superseded — mark them `~~superseded YYYY-MM-DD: reason~~` but keep them visible.
- Commit and push immediately after appending.
- After 50+ entries, consider a quarterly synthesis pass that consolidates patterns without losing the source quotes.

---

## Wiring this into your stack

Reference REVIEW-LOG.md from:

1. **STRATEGY.md** — list it in "Session load order" so it's loaded early
2. **mining-pitch skill** — make it a REQUIRED read in the source-gathering step
3. **content-brief skill** — read before drafting any brief
4. **CLAUDE.md** (global instructions) — add a hook: "if the user gives a content correction during the session, append it to REVIEW-LOG.md before ending the turn"

The combination of (a) Claude reading it on every content session and (b) Claude appending to it on every correction is what makes the file accumulate value over time. Either alone breaks the loop.
