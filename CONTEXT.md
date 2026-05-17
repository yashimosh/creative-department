# CONTEXT.md — Your Standalone Brain

This file is the creative department's self-contained context layer. Fill it in once. Every skill in this department reads it before doing anything.

If you have a central brain (a markdown OS like `~/claude-brain/`), you don't need this — your brain already provides this context. If you don't, this file is what replaces it.

**How to use:** Delete the instructions in brackets. Fill in the rest. Keep it honest and specific — agents perform better with real specifics than polished summaries.

---

## About You

```
Name: [Your name or handle]
Role: [e.g. designer, developer, founder, writer, creator]
Based in: [City, country]
Background: [2-3 sentences — what you've done, where you come from, what you're building toward]
```

This is the "receipt" layer. Skills use it to make your content specific to you, not generic.

---

## Your Projects & Products

List what exists — things you might reference in content as receipts, not as subjects to promote directly.

| Name | What it is | Status | URL (if live) |
|---|---|---|---|
| [Project name] | [One line: what it does, who it's for] | [building / live / paused] | |
| | | | |

**The rule:** projects are receipts, not subjects. "I used X while building Y" is content. "Here's why you should use Y" is a product pitch. Your skills know this distinction — they just need to know what Y is.

---

## Your Platforms

Where you publish. Skills use this to calibrate tone, length, and format.

| Platform | Handle | Frequency | Primary format |
|---|---|---|---|
| Instagram | @[handle] | [e.g. 4 Reels/week] | Reels, carousels |
| X / Twitter | @[handle] | [e.g. daily] | posts, occasional threads |
| LinkedIn | [URL] | [e.g. 1/week max] | long-form posts |
| YouTube | [URL] | [e.g. 2 Shorts/week] | Shorts, monthly long-form |
| [Other] | | | |

---

## Your Tools

What you actually use. Skills reference tools specifically when they're part of your process — a "brain-peek" works better if the agent knows what's in the brain.

| Category | Tool(s) |
|---|---|
| AI / agents | [e.g. Claude Code, Cursor, Windsurf] |
| Design | [e.g. Figma, Canva, Framer] |
| Video | [e.g. CapCut, Canva, Premiere] |
| Writing / notes | [e.g. Obsidian, Notion, plain markdown] |
| Code | [e.g. VS Code, Neovim] |
| Publishing | [e.g. Publer, Buffer, manual] |
| Infrastructure | [e.g. Hetzner, Vercel, Supabase] |
| Other | [anything you reference in content] |

---

## Your Content History

What you've shipped recently. Prevents agents from pitching ideas you've already covered.

Add a line each time you publish. Newest first. Keep the last 20.

| Date | Platform | What it was | REG / link |
|---|---|---|---|
| [YYYY-MM-DD] | [IG / X / etc] | [one-line description] | [REG-ID or URL] |
| | | | |

---

## Your Current Focus

What you're working on right now. Helps agents generate content that's actually timely and relevant.

```
Building: [What you're in the middle of making]
Thinking about: [The question or problem you're chewing on]
Shipping next: [What's close to done]
Not working on right now: [What's paused or deprioritised]
```

---

## Decisions Already Made

Context agents shouldn't try to re-open. Include decisions that inform content and creative choices.

| Decision | Date | Why it matters |
|---|---|---|
| [e.g. No Notion in personal workflow] | [date] | [agents won't suggest Notion-based workflows] |
| [e.g. Video: no post-processing, Canva only] | [date] | [video skills won't suggest complex audio chains] |
| | | |

---

## What You're Figuring Out

Open questions you haven't resolved. Agents use this for "thinking-aloud" and "open question" content shapes — your best content often comes from here.

- [e.g. Whether to open-source the brain or keep it private]
- [e.g. How to make the agent setup transferable to people without my infrastructure]
- [e.g. When to go long-form vs staying short-form]

---

## Your Workspace

Where things live. Agents need this when creating or referencing files.

```
Content exports: [e.g. ~/brand/exports/ or ./exports/]
Brain / notes: [e.g. ~/Documents/notes/ or none]
Design files: [e.g. Figma team / local folder]
Video files: [e.g. local folder path]
Registry: [e.g. ideas.md in this repo / Notion / none]
```

If you have no structured workspace, write: "No structured workspace — I work from this directory."

---

## Gaps in This File

Things you haven't filled in yet. Agents will flag if they need something missing.

- [ ] Projects table
- [ ] Content history (start fresh — add as you publish)
- [ ] Current focus
- [ ] Workspace paths

---

## Notes for Skills

> **Skills:** Read this file before CLIENT.md and BRAND-VOICE.md. It provides the operational context those files assume. If a section is empty or marked with `[fill this]`, don't fabricate — ask the user or proceed without it and note what's missing.
>
> **If a skill references `~/claude-brain/`:** substitute the path in the Workspace section above. If no equivalent path exists, skip the brain read and work from this file + CLIENT.md + BRAND-VOICE.md only.
>
> **Notion references:** If the skill references Notion and the user has no Notion setup, skip Notion writes and log to a local `registry.md` instead. Fail gracefully — don't block the pipeline.
