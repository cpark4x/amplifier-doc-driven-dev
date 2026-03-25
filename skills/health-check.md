---
name: health-check
description: Run a doc-driven-dev alignment audit -- updates BACKLOG, OUTCOMES, checks vision drift, updates AGENTS.md, and reports confidence levels
version: 1.0.0
---

# Health Check

Alignment audit for the doc-driven-dev system. Reads the 3 living docs + recent git history, updates what's factual, flags what needs human judgment.

**Trigger:** "run a health check", "check alignment", "are the docs current?", or after merging a PR.

## Process

**Step 1: Gather context**

Read all 4 docs and recent activity:

```
1. Read VISION.md, OUTCOMES.md, BACKLOG.md, AGENTS.md
2. Read git log since the earliest `last_updated` date across the docs:
   git log --oneline --since="YYYY-MM-DD"
3. If PRs were merged, read their titles and descriptions too
```

Note any commits or PRs that don't map to a backlog item -- these are signals of undocumented work.

**Step 2: Update BACKLOG.md** (confidence: high -- factual)

- Move completed items from Active to Done with `Completed` date, `Driven By` attribution (human or AI), and `Learnings`
- Add new items discovered from commits that aren't already in the backlog
- Reorder Up Next if completed work changes priorities
- Update the Summary to reflect current focus

**Step 3: Update OUTCOMES.md** (confidence: medium-high -- factual statuses)

- Update Status for each outcome based on what shipped
- Update Last Checked to today
- Update Current Assessment summary
- Add Notes for any status changes with rationale

**Step 4: Check vision drift** (confidence: medium -- judgment call)

- Compare recent work against VISION.md Non-Goals and Principles
- Flag any work that appears to contradict stated boundaries
- Do NOT auto-fix -- surface drift to the human with specific evidence:
  - "Commit X appears to add [feature] which is listed as a Non-Goal"
  - "Recent work on [area] may conflict with Principle: [principle]"
- If no drift detected, say so explicitly

**Step 5: Update AGENTS.md** (confidence: medium -- may need human input)

- Update Current Focus from the active backlog
- Add to Key Decisions if significant decisions were made this cycle
- Update Project Structure if new directories were added

**Step 6: Update frontmatter**

For every doc that changed:
- Set `last_updated` to today's date
- Set `updated_by` to "health-check"

**Step 7: Report with confidence levels**

End with a transparency summary using three categories:

```
HEALTH CHECK COMPLETE
=====================

Confident: [changes made with high certainty]
  - Moved 3 backlog items to Done
  - Updated 2 outcome statuses to "Shipped"
  - Updated AGENTS.md Current Focus

Uncertain: [items that need human review]
  - PR #52 doesn't map to any backlog item -- new work or missing item?
  - Outcome "Reduce setup time" has no recent activity -- still relevant?

Not checked: [areas skipped this run]
  - Haven't compared codebase against Non-Goals (no code analysis this run)
  - No PR descriptions available for attribution

Drift flags: [potential vision misalignment]
  - None detected (or: specific flags listed)
```

## Rules

- **Update facts automatically; flag judgments for humans.** Steps 2-3 are auto. Step 4 is flag-only.
- **Every change must have evidence.** Cite the commit, PR, or observation that drove the update.
- **Don't fabricate learnings.** If you don't know what was learned from a completed item, leave the Learnings column as "---" rather than guessing.
- **Don't skip the report.** The confidence summary is the deliverable -- it tells the human what to trust and what to verify.
