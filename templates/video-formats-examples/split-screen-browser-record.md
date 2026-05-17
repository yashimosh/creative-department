# Split-screen with browser recording — face-cam + on-screen evidence

**Format slug:** `split-screen-browser-record`
**Length:** 60–120s
**Aspect:** 9:16 vertical

(Renamed from earlier shorthand "split-screen-shortform" — the new name names what it actually shows.)

## Structure

Talking-head face-cam on top half (or one side) + screen recording on the bottom half. The screen side shows the **actual receipt** the spoken side is referencing:

- Open browser tabs of news articles being discussed
- Side-by-side comparison images
- The actual sign / map / typeface / chart in question
- Highlighted quotes from blog posts / press releases / official statements
- Annotated screenshots

The voice narrates while the screen scrolls / highlights / cuts between sources.

**Teleprompter IS allowed and expected** for this format — the screen side carries the visual interest, so the operator's eyes drifting to a teleprompter on the side doesn't break the format the way it would break Mossery.

## When to use

- Observations that need on-screen evidence ("ten news outlets covered this, none read it this way" — show the ten outlets)
- Source-citation moments (a quote from a 2002 blog post, a Zuckerberg statement, a Menlo Ventures chart)
- Anything where the receipt only lands if the audience sees it
- Cultural observation about a specific artifact (the artifact gets the bottom half)
- "Look at this thing in the wild" + commentary

## When NOT to use

- If the speech alone carries the meaning, use Mossery — split-screen adds production cost for no payoff
- If the visual needs motion / animation / B-roll beyond static sources, use explainer
- If you're not willing to source the screen-side materials cleanly, the format fails

## Production cost

**Medium.** 30–60 min per video.

- Talking-head pass (8–15 min, like Mossery)
- Sources gathering + screen capture (10–20 min)
- Layout in CapCut / Premiere / DaVinci with the split (10–20 min)

## Recipe

1. Write the spoken script (target ~80–100s at conversational pace, longer than Mossery to accommodate visual reveals)
2. **List the visual receipts per timecode** — at 18s show Spolsky blog, at 30s show Zuckerberg quote, at 45s show Menlo chart
3. Record the talking-head pass first, single take or two takes
4. Record screen captures separately (browser navigating to each source, scrolling to the highlight, holding for 3–4s)
5. In edit: stack face-cam on top (occupying ~40-50% of vertical) + screen recording on bottom (~50-60% with the highlight area visible)
6. Add 2–3 text callouts overlaid on the screen half at peak moments
7. Volume boost audio 3-4× if phone mic
8. Ship

## Visual production

- **Face-cam framing:** chest-up, lens at eye line, framed for top half of 9:16
- **Screen recording:** 1080×~1100 region of the desktop, ideally a clean Chrome window with bookmarks bar hidden
- **Split:** ~40% face / ~60% screen works for most. If a chart is dense, flip to 30% face / 70% screen
- **Transitions on the screen side:** simple cut OR a brief swipe — no fancy zooms
- **Hold time per source:** 3–4 seconds minimum after a highlight lands, so viewers can read

## Voice rules

Same as Mossery (no triplets / staccato / aphorism closers / written-register patterns). The script can be slightly more structured since the screen side provides the visual rhythm — but err toward conversational.

## Reference example

The original "Hasakah sign" piece used this format: face-cam discussing a Kurdish-to-Arabic signage change, bottom half showing the Reuters article + the actual sign photo + a quick map.

## Output spec

| Property | Value |
|---|---|
| Resolution | 1080×1920 |
| FPS | 30 |
| Codec | H.264 |
| Face area | top 40-50% of frame (430-960px region) |
| Screen area | bottom 50-60% of frame |
| Audio | AAC stereo, mic preferred |
| Length | 60–120s (90s sweet spot) |
| Hook overlay | 0–3s, full-frame on black |
| Text callouts | 2–3, overlaid on screen half, hold 3-4s each |
| Subtitles | Auto-cap, positioned on the face half so they don't overlap screen content |
