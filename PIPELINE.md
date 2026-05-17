# Creative Pipeline — Stage Gates

Every deliverable flows through this pipeline. Stages are sequential — each must be completed before the next begins. No stage can be skipped.

---

## The Pipeline

```
INTAKE → STRATEGY → PRODUCTION → REVIEW → REVISION → APPROVAL → DELIVERY → REGISTRY
```

---

## Stage 1: INTAKE

**Owner:** Creative Director (`/creative-director`) or whoever receives the request
**Gate:** A filled brief exists

| Action | Details |
|---|---|
| Receive request | Raw idea, client ask, or internal initiative |
| Fill the brief | Use `BRIEF-TEMPLATE.md` — all required fields must be complete |
| Load client context | Read `CLIENT.md`, `BRAND-VOICE.md`, `DESIGN-RATIONALE.md`, `CREATIVE-PLAYBOOK.md` |
| Confirm scope | Deliverables, platforms, timeline, constraints are clear |
| **Create Notion row** | Create entry in Content Registry — Status: `Idea` or `Brief`, fill Title, Project, Format, Platform |

**Exit criteria:** A complete brief with all required fields filled. Notion row exists. If the brief is incomplete, push back before proceeding.

**Notion update:** `notion-create-pages` → Content Registry row with Status = `Idea` or `Brief`

---

## Stage 2: STRATEGY

**Owner:** Creative Director + Art Director + Marketer (as needed)
**Gate:** Creative direction is defined

| Action | Details |
|---|---|
| Research | Competitor analysis (`/competitive-creative-audit`), trend research, audience insights |
| Define direction | Visual approach, messaging angle, content structure |
| Plan deliverables | What gets made, in what order, by which skill |
| Create content calendar | If multi-post campaign, map out the schedule |
| **Update Notion** | Status → `Draft`, add direction notes |

**Exit criteria:** Clear creative direction documented. Production skills know what to make and why. Notion updated.

**Notion update:** `notion-update-page` → Status = `Draft`
**Dispatch:** Create `dispatches/active/DISPATCH-{REG-ID}-strategy-{timestamp}.md` for production

---

## Stage 3: PRODUCTION

**Owner:** Specialist skills (copywriter, graphic-designer, video-editor, etc.)
**Gate:** Deliverables are complete

| Action | Details |
|---|---|
| Copy first | `/copywriter` produces all text — headlines, body, CTAs |
| Design second | `/graphic-designer`, `/ui-designer`, `/carousel-builder` build on copy |
| Motion/video third | `/video-editor`, `/motion-designer`, `/logo-motion` compose with copy + design |
| Marketing last | `/marketer` wraps distribution around finished assets |
| **Update Notion on start** | Status → `In Progress` |
| **Update Notion if blocked** | Status → `Blocked` + add blocker note |

**Sequencing rule:** Copy informs design. Design informs motion. Marketing wraps everything. Independent deliverables can be produced in parallel.

**Dispatch:** Each skill creates a dispatch in `dispatches/active/DISPATCH-{REG-ID}-{skill}-{timestamp}.md` when passing work to the next specialist.

**Exit criteria:** All deliverables exist in draft form. Assets are exported in correct formats and dimensions (reference `PLATFORM-SPECS.md`). Dispatch created for review.

**Notion update:** `notion-update-page` → Status = `In Progress` (on start), `Blocked` (if stuck)
**Dispatch:** Create `dispatches/active/DISPATCH-{REG-ID}-production-{timestamp}.md` for review

---

## Stage 4: REVIEW

**Owner:** Review skills
**Gate:** All review checks pass or issues are documented

| Review Type | Skill | When |
|---|---|---|
| Brand compliance | `/review-brand` | Every deliverable |
| Copy quality | `/review-copy` | Every deliverable with text |
| UI/UX review | `/review-ui` | UI screens, components |
| Web review | `/review-web` | Live websites, landing pages |
| Print review | `/review-print` | Print-ready files |
| Digital PDF review | `/review-digital-pdf` | Reports, decks |
| Report layout review | `/review-report` | Analytical reports, white papers |
| Brand compliance score | `/brand-compliance-score` | When quantitative scoring is needed |
| Final gate | `/final-review` | Always — dispatches appropriate specialists |

**Swarm reviews (optional, for high-stakes work — convene Quality Council):**
- `/design-critic-swarm` — adversarial critique from 5 specialists
- `/design-disagreement` — surfaces genuinely contested decisions
- `/design-ab-test` — multi-variant testing with persona agents

**Exit criteria:** Review report exists. All critical issues are flagged. Deliverable is either approved or sent back to revision. Notion updated.

**Notion update:** `notion-update-page` → Status = `Review` (on entry)
**If issues found:** Dispatch back to production + Notion Status = `Revisions`
**If passed:** Dispatch to approval + Notion Status = `Approved`

---

## Stage 5: REVISION

**Owner:** Original production skill(s)
**Gate:** All flagged issues are addressed

| Action | Details |
|---|---|
| Address critical issues | Fix everything marked "must fix" in review |
| Address warnings | Fix or justify every warning |
| Re-review if needed | Major changes trigger another review pass |

**Exit criteria:** All critical issues resolved. Review report updated. Ready for approval.

**Notion update:** Status stays at `Revisions` until re-review passes → then `Approved`
**Dispatch:** Re-dispatch to review via `dispatches/active/`

---

## Stage 6: APPROVAL

**Owner:** Creative Director or client (Yash)
**Gate:** Human sign-off

| Action | Details |
|---|---|
| Present final deliverable | Show the work with review report |
| Get sign-off | Creative Director or client approves |
| Note any final tweaks | Minor adjustments before delivery |

**Exit criteria:** Explicit approval. "Ship it."

**Notion update:** `notion-update-page` → Status = `Approved` (confirmed)
**Dispatch:** Create `dispatches/active/DISPATCH-{REG-ID}-delivery-{timestamp}.md`

---

## Stage 7: DELIVERY

**Owner:** Marketer or Creative Director
**Gate:** Deliverable is published/sent/delivered

| Action | Details |
|---|---|
| Publish or deliver | Post to platform, send to client, export final files |
| Confirm delivery | Verify the post is live, the file was received, etc. |
| Capture link/proof | Save the live URL or delivery confirmation |
| **Update Notion** | Status → `Scheduled` (if scheduled) or `Published` (if live), add Publish Date |

**Exit criteria:** Deliverable is in the hands of the audience or client. Notion updated.

**Notion update:** `notion-update-page` → Status = `Scheduled` or `Published`, Publish Date set

---

## Stage 8: REGISTRY

**Owner:** Whoever delivered
**Gate:** Entry exists in both the file registry and the Notion Content Registry

| Action | Details |
|---|---|
| Register the output | Add entry to `registries/{project-slug}.md` |
| Fill all required fields | Date, type, platform, created by, status, link |
| Confirm Notion | Verify Content Registry row shows `Published` with REG ID, platform, publish date |
| Update playbook | Add insights to `CREATIVE-PLAYBOOK-{project}.md` if learnings emerged |
| Archive dispatch | Move all dispatches for this REG ID from `dispatches/active/` to `dispatches/archive/` |

**Exit criteria:** Registry entry committed and pushed to GitHub. Notion row confirmed at Published. Dispatches archived.

---

## Live Pipeline Visibility — Optional Notion Dashboard

**Optional integration.** Some operators maintain a Notion Content Registry as a live dashboard for all in-flight and published content. If you use this pattern, it gives a real-time view of what's in the pipeline at any stage. If you don't, the file registry (`registries/{client}.md`) is sufficient on its own.

- **Pattern:** A single "Content Registry" database per operator, keyed on the REG-XXXX IDs used in the file registry
- **Configuration:** The Notion URL, workspace ID, and page ID are operator-specific. Store them in a local config file outside this package, not committed. Yash's private config lives in his local setup.
- **Updated by:** Every session that produces, reviews, schedules, or publishes content

### When to update Notion

| Trigger | Action |
|---|---|
| New idea or brief | Create a row, set status to `Idea` or `Brief` |
| Draft started | Update status to `Draft` |
| In review | Update status to `Review` |
| Scheduled on Publer | Update status to `Scheduled`, add publish date |
| Published | Update status to `Published`, add publish date |

### Schema

| Field | Values |
|---|---|
| Title | Content piece name |
| Status | Idea → Brief → Draft → Review → Scheduled → Published |
| Platform | X, LinkedIn, Instagram, Threads, YouTube, Behance |
| Format | Post, Thread, Carousel, Video, Article |
| Project | One per brand you work with — set the options list to your own clients |
| REG ID | Links to file registry entry (e.g. REG-0002) |
| Publish Date | Scheduled or actual publish date |
| Notes | Anything relevant |

**The file registry (`registries/{client}.md`) remains the source of truth for content files. Notion is the source of truth for status.**

---

## Retrospective (Optional — for campaigns)

After a campaign is fully delivered, run `/creative-retrospective` to:
- Compare deliverables against original brief
- Document what worked and what didn't
- Update the client's `CREATIVE-PLAYBOOK.md`
- Generate prompt/guideline improvements for future work

---

## Quick Reference — Who Owns What

| Stage | Primary Owner | Skills Involved | Notion Status |
|---|---|---|---|
| Intake | Creative Director | `/creative-director`, `/onboard-client` | `Idea` → `Brief` |
| Strategy | Creative Director | `/art-director`, `/marketer`, `/competitive-creative-audit` | `Draft` |
| Production | Specialists | `/copywriter`, `/graphic-designer`, `/video-editor`, etc. | `In Progress` / `Blocked` |
| Review | Review team | `/final-review`, `/review-brand`, `/review-copy`, etc. | `Review` |
| Revision | Original producer | Same as production | `Revisions` |
| Approval | Creative Director (Yash) | Human decision | `Approved` |
| Delivery | Marketer / CD | Platform MCPs, publer, email tools | `Scheduled` → `Published` |
| Registry | Deliverer | File registry + Notion confirmation | `Published` (confirmed) |

## Dispatch System

Skills communicate through structured dispatch files in `creative-department/dispatches/active/`. Each dispatch follows the format defined in `ARCHITECTURE.md`. When a deliverable is fully registered, its dispatches move to `dispatches/archive/`.

## Decision Councils

For hard decisions, convene the appropriate swarm team:

| Council | When | Skills |
|---------|------|--------|
| Direction Council | Creative direction unknown | stigmergy → murmuration → art-director |
| Quality Council | High-stakes review | critic-swarm → disagreement → final-review |
| Layout Council | Complex layout | evolution → negotiator → layout-designer |
| Innovation Lab | Creative rut | telephone → evolution → generative-designer |
