# Creative Department — Organizational Architecture

*Skills as employees. Notion as the nervous system. Workflows as muscle memory.*

---

## The Problem Today

The creative department has 30+ specialist skills and 7 swarm architectures — but they operate as freelancers, not as an organization. Every skill is user-invoked. No skill talks to another skill automatically. No skill writes to Notion. The pipeline exists on paper (PIPELINE.md) but nothing enforces it. HANDOFF.md is a template nobody fills in. The result: Yash is the routing layer, the state tracker, the handoff messenger, and the quality gate — all manually.

## The Vision

Each skill is an employee with a role, a team, and a communication protocol. Work flows through the department like it would in a real creative agency: someone takes a brief, a team plans the approach, specialists produce the work, reviewers check it, and the final output is delivered and registered — with Notion updated at every step. The human (Yash) is the Creative Director who makes the hard calls. Everything else is automated.

---

## Org Chart

```
                        CREATIVE DIRECTOR (Yash)
                               |
                    creative-director (routing)
                               |
        ┌──────────┬───────────┼───────────┬──────────┐
        |          |           |           |          |
    STRATEGY    PRODUCTION   QUALITY    RESEARCH   OPERATIONS
    --------    ----------   -------    --------   ----------
    strategist  copywriter   final-     competitive context-
    art-        graphic-     review     -creative-  assembler
    director    designer     review-    audit       campaign-
    campaign-   motion-      brand      reference-  orchestrator
    planner     designer     review-    hunter      creative-
                video-       copy       design-     monitor
                editor       review-    historian   creative-
                carousel-    ui                     dashboard
                builder      review-
                ui-designer  web
                ux-designer  review-
                layout-      print
                designer     review-
                slides-      report
                designer     review-
                poster       digital-
                3d-designer  pdf
                             brand-
                             compliance
                             -score
```

### Decision Councils (Swarm Teams)

These are cross-functional teams that convene for specific decision types. They are not permanently active — they're assembled when a decision requires collective intelligence.

| Council | Skills Involved | Convenes When |
|---------|----------------|---------------|
| **Direction Council** | design-stigmergy, design-murmuration, art-director | New brand voice needed, creative direction unknown, brief is ambiguous |
| **Quality Council** | design-critic-swarm, design-disagreement, final-review | High-stakes deliverables, contested review decisions, campaign-level QA |
| **Layout Council** | design-negotiator, design-evolution, layout-designer | Complex layout decisions, design system creation, multi-format adaptation |
| **Innovation Lab** | design-telephone, design-evolution, generative-designer | Creative rut, need radical new directions, exploring unfamiliar territory |

---

## Work Modes

Not every project runs the full pipeline. The creative department operates in distinct modes, each activating a different team with a different workflow.

### Content Mode
**What:** Social posts, articles, videos, threads, captions
**Pipeline:** Brief → Copy → Design → Review → Publish → Register
**Team:** copywriter, caption-*, graphic-designer, video-editor, carousel-builder, marketer
**Strategy skills (when the brief is strategy-led, not just execution):** content-marketing, permission-marketing, viral-marketing
**Councils:** Quality Council only for campaign-level content
**Notion:** Yes — every piece tracked in Content Registry
**Typical scope:** 1 session, 1-3 deliverables

```
INTAKE → PRODUCTION → REVIEW → DELIVERY → REGISTRY
         (copy → design)
```

Skips: Strategy (direction is usually known), Approval (lightweight — Yash reviews inline)

### Branding Mode
**What:** Brand identity, voice discovery, design system, brand book, visual language
**Pipeline:** Discovery → Strategy → Production → Review → Delivery
**Team:** design-stigmergy, design-murmuration, art-director, brand-book, design-system, typestyle, iconography, copywriter (for voice), generative-designer
**Councils:** Direction Council (almost always), Layout Council (for design system), Innovation Lab (for visual exploration)
**Notion:** No — branding projects are not individual content pieces. Track in project file instead.
**Typical scope:** Multi-session, spans days/weeks

```
DISCOVERY → STRATEGY → PRODUCTION → REVIEW → DELIVERY
(stigmergy)  (direction   (brand book,   (critic    (files,
              council)     design system)  swarm)    guidelines)
```

Skips: Registry (no REG-ID — this isn't content, it's infrastructure)

### Design Mode
**What:** UI/UX for websites, apps, components, prototypes
**Pipeline:** Research → Wireframes → Prototypes → Review → Handoff
**Team:** user-research, ux-designer, ui-designer, design-system, design-handoff, review-ui, accessibility-review
**Councils:** Layout Council (for complex layouts), Quality Council (for final UI review)
**Notion:** No — track in project file. Design deliverables aren't "content."
**Typical scope:** Multi-session project

```
RESEARCH → WIREFRAMES → PROTOTYPES → REVIEW → HANDOFF
(user       (ux-designer)  (ui-designer)  (review-ui)  (design-handoff
research)                                               → developer)
```

Skips: Content Registry, copy-first sequencing, marketing/delivery

### Campaign Mode
**What:** Multi-deliverable marketing push across platforms
**Pipeline:** Full 8-stage pipeline
**Team:** campaign-orchestrator manages everything, all teams involved
**Strategy skills:** guerrilla-marketing, community-building, content-marketing, public-relations, viral-marketing, permission-marketing, marketer, strategist, campaign-planner
**Councils:** Direction Council (for strategy), Quality Council (for review), Innovation Lab (if stale)
**Notion:** Yes — one Content Registry entry per deliverable
**Typical scope:** Multi-session, parallel workstreams

```
INTAKE → STRATEGY → PRODUCTION → REVIEW → REVISION → APPROVAL → DELIVERY → REGISTRY
                     (parallel                                     (per
                      dispatch)                                     platform)
```

Uses everything. campaign-orchestrator sequences and tracks.

### Publication Mode
**What:** Reports, magazines, books, white papers, designed PDFs
**Pipeline:** Brief → Layout → Content → Design → Review → Export
**Team:** layout-designer, copywriter, graphic-designer, review-print, review-digital-pdf, review-report
**Councils:** Layout Council (almost always), Quality Council (for final)
**Notion:** Optional — track if it will be published/distributed, skip if internal-only
**Typical scope:** Multi-session

```
BRIEF → LAYOUT → CONTENT → DESIGN → REVIEW → EXPORT
         (council   (copy fills    (graphics,   (review-print/
          layout)    the layout)    images)      review-pdf)
```

Skips: Marketing/delivery (unless being distributed), often skips Strategy

### Quick Mode
**What:** Single-skill tasks — "write me a caption," "review this copy," "make a thumbnail"
**Pipeline:** None — just invoke the skill directly
**Team:** Single skill
**Councils:** None
**Notion:** No — too small to track. Unless it's part of a tracked piece (then update existing entry).
**Typical scope:** 1 message

No dispatches. No pipeline. Just do the thing.

---

### How creative-director Selects the Mode

The creative-director reads the request and selects the mode before routing:

| Signal in the request | Mode |
|----------------------|------|
| "post," "caption," "article," "thread," "reel," "video for [platform]" | Content |
| "brand," "identity," "voice," "design system," "brand book," "logo" | Branding |
| "website," "app," "UI," "UX," "prototype," "wireframe," "component" | Design |
| "campaign," "launch," "multi-platform," "content calendar" | Campaign |
| "report," "magazine," "book," "white paper," "PDF," "publication" | Publication |
| Single skill request, simple task | Quick |

If ambiguous, ask: "Is this content for publishing, a branding project, a design project, or a campaign?"

The mode determines:
1. Which skills to involve
2. Which pipeline stages to run (and which to skip)
3. Whether to create a Content Registry entry
4. Whether to use dispatches or just invoke directly
5. Which councils might be needed

---

## Communication Protocol — The Dispatch System

### Current Problem
Skills don't talk to each other. A copywriter produces copy and... nothing happens. Someone (Yash) has to manually invoke the graphic designer, paste in the copy, and explain the context.

### Solution: Structured Dispatches

Every skill that produces output creates a **dispatch** — a structured message that the next skill in the pipeline can consume. Dispatches are stored in a standard location and follow a standard format.

#### Dispatch Format

```markdown
<!-- DISPATCH-{REG-ID}-{stage}-{timestamp}.md -->
---
reg_id: REG-XXXX
from: copywriter
to: graphic-designer
stage: PRODUCTION
status: ready-for-next
notion_page: https://www.notion.so/{page-id}
timestamp: 2026-04-12T14:30:00Z
---

## Deliverable
[What was produced — specific, not vague]

## Output
[The actual content or file paths]

## Context for Next Skill
- **Objective:** [What the final deliverable needs to achieve]
- **Audience:** [Who it's for]
- **Platform/Format:** [Specs]
- **Brand constraints:** [Key constraints]
- **Key message:** [The one takeaway]

## Decisions Made
[Important creative decisions the next skill should preserve]

## Open Questions
[Things the next skill might need to decide]
```

#### Dispatch Directory

```
creative-department/
  dispatches/
    active/          ← current dispatches awaiting pickup
    archive/         ← completed dispatches (auto-moved after pickup)
```

#### Dispatch Rules

1. **Every production skill** must create a dispatch when its work is done
2. **Every skill** reads dispatches addressed to it before starting work
3. **creative-director** or **campaign-orchestrator** routes dispatches (decides who's next)
4. Dispatches reference the Notion page — the receiving skill can pull additional context from Notion

---

## Notion as the Nervous System

### Current Problem
Notion is disconnected. The Content Registry exists but nothing writes to it automatically. Skills track state in local markdown files that nobody else reads.

### Solution: Notion-Integrated Pipeline

Every stage transition in the pipeline triggers a Notion update. Every skill that starts or finishes work updates the Content Registry.

#### When Skills Write to Notion

| Event | Notion Action | Who Does It |
|-------|---------------|-------------|
| New idea/brief created | Create row in Content Registry, status = `Idea` or `Brief` | creative-director or campaign-orchestrator |
| Strategy complete | Update status to `Draft` | strategist or art-director |
| Production started | Update status to `In Progress` | production skill (copywriter, designer, etc.) |
| Production blocked | Update status to `Blocked`, add note | any production skill |
| Ready for review | Update status to `Review` | production skill |
| Revisions requested | Update status to `Revisions`, add review notes | review skill |
| Approved | Update status to `Approved` | final-review |
| Scheduled | Update status to `Scheduled`, add publish date | marketer or publer |
| Published | Update status to `Published`, add publish date and links | delivery skill |

#### How Skills Write to Notion

Add this to every skill that participates in the pipeline:

```markdown
## Notion Integration

After completing your work:
1. Read the dispatch to get the `notion_page` URL
2. Use `notion-update-page` to update the Status field
3. Add a comment via `notion-create-comment` with a brief summary of what you did
4. If you created assets, add file paths to the Notes field
```

#### Content Registry Schema (canonical)

| Field | Values |
|-------|--------|
| Title | Content piece name |
| Status | Idea / Brief / Draft / In Progress / Blocked / Review / Revisions / Approved / Scheduled / Published |
| Platform | X, LinkedIn, Instagram, Threads, YouTube, Behance |
| Format | Post, Thread, Carousel, Video, Article, Report |
| Project | One per brand you work with — set the options list to your own clients |
| REG ID | Links to file registry entry (e.g. REG-0005) |
| Publish Date | Scheduled or actual publish date |
| Current Owner | Which skill currently has the work |
| Notes | Running log of activity |

---

## Workflow Automation — Pipeline as Code

### The Full Pipeline (Automated)

```
1. INTAKE
   creative-director receives request
   → Creates Notion row (Status: Idea/Brief)
   → Invokes context-assembler to build context manifest
   → Dispatches to STRATEGY

2. STRATEGY
   art-director / strategist / campaign-planner
   → Defines creative direction
   → Updates Notion (Status: Draft)
   → If direction is uncertain → convene Direction Council
   → Dispatches to PRODUCTION with direction brief

3. PRODUCTION
   Sequenced by campaign-orchestrator:
   a. copywriter → dispatch to graphic-designer
   b. graphic-designer → dispatch to motion-designer (if needed)
   c. Each skill updates Notion (Status: In Progress)
   d. If blocked → updates Notion (Status: Blocked) + Telegram alert
   e. When complete → dispatch to REVIEW + Notion (Status: Review)

4. REVIEW
   final-review dispatches to appropriate specialists:
   → review-brand (always)
   → review-copy (if text)
   → review-ui / review-web / review-print (by format)
   → For high-stakes: convene Quality Council
   → If issues found → dispatch back to REVISION + Notion (Status: Revisions)
   → If passed → dispatch to APPROVAL + Notion (Status: Approved)

5. REVISION
   Original production skill(s) fix issues
   → Re-dispatch to REVIEW
   → Notion stays at Revisions until re-review passes

6. APPROVAL
   Human sign-off (Yash)
   → Notion (Status: Approved)

7. DELIVERY
   marketer / publer / platform-specific skills
   → Publish or schedule
   → Notion (Status: Scheduled or Published)
   → Add publish links

8. REGISTRY
   → Update file registry (registries/{project}.md)
   → Notion confirmed at Published
   → Git sync
```

### Who Orchestrates?

**campaign-orchestrator** is the production manager. It:
- Tracks which skills are working on what
- Manages the dispatch queue
- Sequences production skills (copy before design before motion)
- Escalates blockers
- Triggers review when production is complete

**creative-director** handles routing:
- Decides which skills to involve for a given request
- Makes strategic calls (when to use swarms, when to skip steps)
- Approves or redirects at decision points

**creative-monitor** is the watchdog:
- Every 4 hours, checks Notion for stuck/overdue items
- Sends Telegram alerts for items needing attention
- Tracks days-in-status for SLA enforcement

---

## Team Decision-Making — When to Convene Councils

### Direction Council
**Trigger:** Brief is ambiguous, brand voice needs discovery, creative direction is unknown
**Process:**
1. design-stigmergy runs first — discovers latent brand character through 15 rounds of mark-and-react
2. design-murmuration takes the stigmergy output and generates 12 creative variants, clusters them into 3-4 directions
3. art-director reviews the clusters and either picks a direction or presents options to Yash
**Output:** A creative direction document that all production skills reference

### Quality Council
**Trigger:** High-stakes deliverable (client-facing, campaign-level, brand launch), or a contested review decision
**Process:**
1. design-critic-swarm runs 5 specialist critics in parallel
2. design-disagreement runs 5 independent agents on the contested questions
3. final-review synthesizes: GREEN decisions are auto-resolved, RED decisions are escalated to Yash
**Output:** A review verdict with clear action items + decision points for human judgment

### Layout Council
**Trigger:** Complex multi-format layout, design system creation, publication design
**Process:**
1. design-evolution parameterizes the design space and evolves solutions over 5-7 generations
2. design-negotiator gives each element agency and negotiates equilibrium layouts
3. layout-designer receives the winning parameters and produces the actual layout
**Output:** Layout specifications with stable decisions (locked) and contested decisions (for Yash)

### Innovation Lab
**Trigger:** Creative rut, need genuinely new directions, want to stress-test a concept
**Process:**
1. design-telephone runs the work through radical transformations (era/medium/audience/scale chains)
2. design-evolution takes the "essential elements" from telephone and evolves new variants
3. generative-designer explores the possibility space
**Output:** Novel creative directions that no single skill would have produced

---

## Implementation Plan

### Phase 1: Foundation (Do First)
1. **Add Notion write-back to PIPELINE.md** — make it explicit that every stage transition updates Notion
2. **Update creative-director** — add dispatch creation to its routing logic
3. **Update campaign-orchestrator** — track pipeline state in Notion instead of local markdown
4. **Create dispatch directory** — `creative-department/dispatches/active/` and `archive/`

### Phase 2: Production Skills (Next)
5. **Update copywriter, graphic-designer, motion-designer** — add dispatch output + Notion status update
6. **Update review skills** — add dispatch routing + Notion status update
7. **Update delivery skills** (marketer, publer) — add Notion status update on publish

### Phase 3: Decision Councils (Then)
8. **Create council-direction skill** — orchestrates stigmergy → murmuration → art-director pipeline
9. **Create council-quality skill** — orchestrates critic-swarm → disagreement → final-review pipeline
10. **Create council-layout skill** — orchestrates evolution → negotiator → layout-designer pipeline
11. **Create council-innovation skill** — orchestrates telephone → evolution → generative-designer pipeline

### Phase 4: Automation (Finally)
12. **Update creative-monitor** — detect Notion status changes and trigger appropriate next steps
13. **Add webhook/polling** — creative-monitor detects new Content Registry entries and alerts
14. **End-to-end test** — run a complete project through the automated pipeline

---

## Remotion Studio — Video Production Infrastructure

The creative department has a programmatic video production studio at `creative-department/remotion-studio/`.

### Architecture

```
remotion-studio/
  src/
    brand/          ← tokens.ts (colors, fonts, motion), theme.ts (derived styles)
    components/     ← shared building blocks (TextReveal, BrandFrame, Transition, LowerThird, DividerLine, Counter)
    templates/      ← props-driven social video compositions (TextPost, CaptionReel, Listicle, BeforeAfter, Announcement)
    productions/    ← custom/complex compositions (Explainer, DataViz, BrandFilm, DemoVideo)
  public/
    fonts/          ← brand font files
    assets/         ← images, logos, screenshots for compositions
```

### How It Plugs Into the Pipeline

**Content Mode:** caption skill produces copy → dispatch → video-editor selects Remotion template → feeds copy as props → renders → dispatch → review → delivery

**Campaign Mode:** campaign-orchestrator dispatches multiple video renders in parallel — one template, many platform variants (Reel + Short + TikTok from the same composition)

**Branding Mode:** BrandFilm production for brand launch videos. Brand tokens in `src/brand/tokens.ts` are the single source of truth.

### Rendering

- **Local:** render on a capable GPU for iteration (Remotion is CPU-light but faster with GPU acceleration)
- **Cloud:** `@remotion/lambda` available for batch rendering (>5 videos)
- **video-editor** skill orchestrates: picks template or production, feeds props, renders, dispatches output

### Brand Tokens

All compositions import from `src/brand/tokens.ts`. The shipped token file contains generic placeholder values — replace them with your brand's real colors, typography, spacing, and motion parameters before rendering. To support multiple brands, create additional token files and parameterize the import.

---

## What Changes for the User

**Before:** "Run /copywriter, then manually copy the output, then run /graphic-designer, paste the copy, then run /review-brand..."

**After:** "Run /creative-director with a brief. The system plans the approach, sequences the skills, passes work between them automatically, updates Notion at every step, convenes councils when decisions are hard, and delivers the final output — with a complete audit trail in Notion."

The human remains the Creative Director — the one who makes the hard calls, approves the work, and sets the strategic direction. Everything else is the department doing its job.
