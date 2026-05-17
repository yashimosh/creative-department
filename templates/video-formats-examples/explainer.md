# Explainer — VO-driven with heavy B-roll / motion / archival

**Format slug:** `explainer`
**Length:** 60–90s vertical (also works as 5–15min long-form on YouTube with a vertical cut downstream)
**Aspect:** 9:16 vertical (or 16:9 for long-form parent)

## Structure

Voiceover drives. **No talking head** — or very brief talking-head bookends (intro 3-5s, outro 3-5s). The screen is doing the work: B-roll footage, animation, maps, side-by-side visuals, typography motion, archival footage, screen capture.

The argument is structured: hook → setup → tension → reveal → close. Tight pacing — but the cuts serve the argument, not retention metrics.

Teleprompter for the VO is standard. Multiple takes per line are normal. The audio is comped together in post.

## When to use

- Anything with a strong visual subject that benefits from *showing* rather than narrating
  - Typography breakdown ("the typeface of X")
  - Design system reveal ("here's what this brand does that others don't")
  - Geographic / political argument ("here's where X happened on a map")
  - Infrastructure visualization ("here's the stack underneath the thing you use")
  - Archival comparison ("here's how this looked in 1995 vs now")
- Topics where the audience needs to *see* what's being explained
- Topics where the operator being off-screen actually serves the piece (the no-protagonist rule benefits from literal absence)
- Long-form essays ported to vertical — the long-form lives on YouTube, the vertical is the 60-90s cut

## When NOT to use

- Conversational / thinking-aloud content — Mossery is the right shape
- "I noticed a thing, here's the source" — split-screen-browser-record is faster
- Anything where you can't source / shoot the B-roll cleanly. This format fails badly without strong visuals — talking over a poorly-chosen stock clip looks worse than a clean Mossery shot.
- Anything you need to ship this week — the production cost is 5-15× a Mossery

## Reference creators

- **Johnny Harris** — geography/politics explainers, dense visual stacking, archival + map work
- **Nolan Perkins (@_radnolan)** — designer's eye for typography motion + visual rhythm, current peer-scale reference
- **Cleo Abram (Huge If True)** — tech-optimist explainers, clean animation, tight VO scripts, accessible without being shallow
- **Every Frame a Painting** (vertical cuts of long-form) — for video analysis pacing
- **Sebastian Lague** — builder-narrator with code + visualization (when the topic is build-shaped)

## Production cost

**Highest.** 4–15 hours per vertical piece. Long-form parent: 40–80 hours.

Not weekly — monthly at most for solo operators. With an editor, twice-monthly is feasible.

## Recipe

1. **Write the script first** — explainer pieces fail when they're improvised. 800-1500 words for a long-form, 150-200 for a vertical cut. Argument structure: hook → setup → tension → reveal → close.
2. **Storyboard / shot list** — for each paragraph, name the visual that supports it. If you can't name one, the paragraph is too abstract or the topic is wrong for this format.
3. **Source B-roll** — public-domain archival, your own footage, screen captures, stock from Pexels/Pixabay, paid stock if budget allows
4. **Motion design** — minimal but consistent. Type animations, simple map zooms, highlighted callouts. Keep a small library you reuse across pieces.
5. **Record VO** — multiple takes per line, in a quiet room, with a real mic. Use auto-cut-takes to pick the best takes.
6. **Edit** — VO on the timeline first, then drop visuals beat by beat. Tight but not retention-bait. Music is OK here (unlike Mossery / split-screen) — subtle bed, not a hook.
7. **Color grade** — use video-pipeline with the locked `c5` grade or a brand-specific LUT
8. **Export** — long-form parent (16:9, 1080p, 4-8 Mbps) AND vertical cut (9:16, 1080×1920)

## Visual production

- **No face** is the default. If face appears, it's a 3-5s bookend.
- **Aspect strategy:** shoot wide for the 16:9 long-form, crop to 9:16 for vertical. Keep important content in the center vertical strip.
- **Visual cadence:** 1 cut every 2-4s on average. Faster for hooks, slower for reveals.
- **Type:** consistent across all your explainers. Pick a display face + a body face + a mono. Don't mix per video.
- **Color:** the locked grade should apply uniformly — your explainers should be color-recognizable as a family.

## Voice rules

The same brand voice rules apply (no triplets / aphorism closers / written-register patterns). But explainer scripts CAN be more written-register than Mossery because the operator can re-record any line until it flows. The trail-off closer style of Mossery doesn't always work in explainer — the argument structure usually needs a more definite landing.

## Output spec

| Property | Vertical | Long-form parent |
|---|---|---|
| Resolution | 1080×1920 | 1920×1080 |
| FPS | 30 | 30 or 24 |
| Codec | H.264 | H.264 or HEVC |
| Audio | AAC stereo, mic + music bed | AAC stereo, mic + music bed |
| Length | 60-90s | 5-15min |
| Music | Subtle bed, low (-20 to -25 dB under VO) | Same |
| Subtitles | Burned-in for vertical | Toggle for long-form |
