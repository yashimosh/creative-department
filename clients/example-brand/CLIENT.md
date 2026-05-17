# CLIENT — Meridian (example brand)

This is a worked example client for the `creative-department` package. It's a fictional independent editorial platform. Fork it, rename it, and edit it to match your real work.

## Client
- **Name:** Meridian
- **Handle:** @meridian (fictional, for example purposes)
- **Website:** meridian.example
- **Primary contact:** (fictional)
- **Industry:** Independent editorial — long-form essays on typography, translation, and publication history
- **Context:** Example client. A small independent editorial that publishes one long essay per month plus weekly short-form notes. One-person operation. Taste-lane positioning.

## Brand Identity
- **Tagline:** (none — deliberately no tagline)
- **Mission:** Publish editorial work on typography, translation, and publication history that rewards close reading.
- **Archetype:** Quiet authority. Flat tone. Undersold.
- **Tone of voice:** Editorial. Analytical. Warm but not chatty. 70% practitioner / 30% historical perspective. See `BRAND-VOICE.md`.
- **Languages:** English (primary). Open to bilingual pieces when the subject requires it (e.g., a translation essay may quote in source + English).

## Visual Identity
- **Typography:**
  - **Display:** GT Sectra (or a similar editorial serif with personality)
  - **Body:** Source Serif Pro
  - **Labels / numerals:** JetBrains Mono
- **Colors:**
  - **Ink:** `#1A1A1A` — primary text
  - **Accent:** `#8B4513` — warm brown, used sparingly
  - **Paper:** `#F7F3ED` — light cream background
- **Palette logic:** Warm neutrals. No saturated color. Accent brown used for emphasis in pull quotes and section rules only.
- **Visual style:** Editorial-magazine sensibility. Column-driven. Serifs do the emotional work. Minimal imagery unless the essay requires it.
- **Avoid:** Stock photos, sans-serif display type, saturated color, emoji, social-media optimization signals.

## Content

### Lane
Editorial taste-lane. Every piece is a long essay or a curated note. See `STRATEGY.md`.

### Platforms
- **Spine:** meridian.example — the slow venue. Monthly long-form.
- **Secondary:** one short-form newsletter (bi-weekly).
- **Social:** a single presence on one platform (example: a monthly index post on a chosen social).
- **Dropped:** all other social platforms. Editorial publications don't sprawl.

### Post frequency
- **Long-form essay:** monthly
- **Short notes:** bi-weekly
- **Social index post:** monthly, summarizing what ran that month

### Content pillars
1. **Typography history.** How type shapes reading. Specific typefaces, their designers, their contexts.
2. **Translation as craft.** How a translator's choices change a text. Side-by-side readings.
3. **Publication history.** How small independent publications survived or didn't; lessons still useful.

### Formats
- Long-form essays (2000–5000 words)
- Short notes (300–800 words)
- Curated annotated bibliography entries
- Occasional interview in Q&A transcript format

## Assets
- **Logo:** (a wordmark in the display serif is usually enough)
- **Brand kit:** fonts, colors, rules — see this file and `BRAND-VOICE.md`
- **Export pipeline:** HTML → print-ready PDF for essays; HTML → PNG for social cards

## Session Load Order

Every production session for this client loads files in this order:

1. `STRATEGY.md` — lane, priorities, what to publish and why
2. `PERSONALITY.md` — editorial posture, beliefs, audience
3. `CLIENT.md` — this file — operational detail
4. `BRAND-VOICE.md` — voice rules, structural patterns
5. `../../registries/example-brand.md` — content registry (create this when you fork)

## Notes
- No hashtags in social posts (editorial publications earn their audience through the work)
- No AI-sounding copy — every piece should read like a person wrote it
- No manifesto energy — editorial voice is by nature restrained
- No clickbait — headlines describe, don't tease
- No engagement-farming — one monthly index post is the whole social strategy

## How to use this as your starting point

1. Fork this folder: `cp -r clients/example-brand clients/your-brand`
2. Edit the four files (`CLIENT.md`, `STRATEGY.md`, `PERSONALITY.md`, `BRAND-VOICE.md`) to match your real brand
3. Create `registries/your-brand.md` from `REGISTRY-TEMPLATE.md`
4. Load the folder in a Claude session and start a brief

The `clients/example-brand/` files are deliberately simple — just enough to show the pattern. Your real brand files will be more specific and longer.
