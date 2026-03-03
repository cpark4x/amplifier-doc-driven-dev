---
name: session-close
description: Use when ending any session that used the doc-driven-dev approach — before saying goodbye, wrapping up, or closing the conversation
version: 1.0.0
---

# Session Close

Run this checklist before ending every session. 2 minutes. Prevents doc drift.

## Checklist

**1. Git status clean?**
```bash
git status
```
Any uncommitted changes → commit and push before stopping.

**2. Any epics that shipped but still show "In Progress"?**
Check `docs/02-requirements/epics/`. If something was built this session, update its Status to `Complete`.

**3. Does BACKLOG.md reflect what was built?**
- Move shipped items to Recently Completed with today's date
- Remove shipped items from future work sections
- Update Epic Completion Status percentages
- Update the overall "N specialists shipped" count

**4. Everything pushed?**
```bash
git log origin/main..HEAD
```
Anything listed → push it.

---

## Reflection (1 question)

*Should any of these updates have happened during the work, not now?*

If yes — note which ones. The goal is to build the habit of updating docs as part of shipping, not as cleanup. Session close catches what slipped; it shouldn't be the primary mechanism.

---

## What Session Close Does NOT Cover

- Creating user story files for newly implemented stories → do this manually when the story is fresh
- Updating VISION.md or PRINCIPLES.md → do this when decisions are made, not at session end
- Feedback capture → separate process for reflecting on what worked
