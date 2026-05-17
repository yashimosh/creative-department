# HANDOFF → DISPATCH

> **This template is superseded by the Dispatch System.** Skills now communicate via structured dispatch files in `creative-department/dispatches/active/`. See `ARCHITECTURE.md` for the full protocol.

## Dispatch File Format

Save as: `dispatches/active/DISPATCH-{REG-ID}-{skill}-{timestamp}.md`

```markdown
---
reg_id: REG-XXXX
from: {producing-skill}
to: {receiving-skill}
stage: STRATEGY | PRODUCTION | REVIEW | DELIVERY
status: ready-for-next
notion_page: https://www.notion.so/{page-id}
timestamp: {ISO timestamp}
---

## Deliverable
{What was produced — be specific}

## Output
{The actual content, file paths, or links}

## Asset Paths
| Asset | Path / URL | Format |
|---|---|---|
| | | |

## Context for Next Skill
- **Objective:** {What the final thing needs to achieve}
- **Audience:** {Who it's for}
- **Platform/Format:** {Specs}
- **Brand constraints:** {Key constraints}
- **Key message:** {The one takeaway}

## Decisions Made
{Creative decisions the next skill should preserve}

## Open Questions
{Things the next skill might need to decide}
```

## Rules

1. Every production skill creates a dispatch when its work is done
2. Every skill reads dispatches addressed to it before starting
3. The `notion_page` field lets the receiving skill update Notion status
4. After a deliverable reaches `Published` and is registered, dispatches move to `dispatches/archive/`
5. `creative-director` or `campaign-orchestrator` decides routing (who gets the dispatch next)
