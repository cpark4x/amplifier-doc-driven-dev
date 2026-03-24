# Doc-Driven Dev v2 Design

## Goal

Redesign the `amplifier-doc-driven-dev` bundle from a documentation scaffolding tool into an **alignment system for human-AI collaboration** -- so that at any point mid-project, the human can confirm alignment, see what was built, understand why, and assess whether work is accruing to meaningful outcomes.

## Background

### What exists today (v1)

The current bundle enforces documentation-first development through a setup recipe and session-close discipline. It has:

- **3 tiers** (lean/standard/full) with different folder structures -- too complex, doesn't match how projects are actually organized
- **6 templates** (VISION, EPIC, BACKLOG, PRINCIPLES, SUCCESS_METRICS, USER_STORY) with heavy writing guidelines embedded -- too verbose, guidelines clutter the project docs
- **A 5-stage recipe** that only handles greenfield projects -- too narrow
- **A session-close skill + ambient reminder** that never fires because the bundle isn't loaded in day-to-day sessions -- dead code
- **Hardcoded `templates_path`** pointing to a local machine path -- breaks for all other users
- **`bundle.yaml`** instead of `bundle.md` -- no system prompt injected
- **~90% duplication** between the standard and fast recipe variants

### Why it needs to change

The owner's workflow has evolved:

- Uses **superpowers modes** (brainstorm, write-plan, execute) -- the bundle doesn't integrate with that workflow
- Uses **lifeos** for persistent cross-session memory -- having a second persistence mechanism is redundant
- Works with **AI doing most of the building** -- needs confidence that autonomous work is aligned, not just documented
- Needs this to work for **any project state**: greenfield, undocumented, or stale docs

### The real problem

When working with AI that does most of the building, work accumulates fast. Without a system, you lose the ability to answer: Are we still building what we set out to build? Is the work accruing to something measurable? What was built, what's next, and how does it connect? Where did we go wrong, and what should we reconsider?

## Approach

### Core Philosophy

This is **not project documentation**. It's an alignment and accountability layer for human-AI collaboration. The docs exist so that at any point mid-project, the human can open them and answer four questions:

| Question | Pillar |
|----------|--------|
| Is what we're building still what we set out to build? Have we drifted? | **Vision** |
| Is the work accruing to something measurable? Where do we stand? | **Outcomes** |
| What's built, what's not, what's next -- and how does it connect to vision and outcomes? | **Backlog** |
| Where did we go wrong? What should we reconsider? Are we on the right path? | **Retrospective** |

### The 80/20 Principle

Docs are **80% for AI context, 20% for human confidence**. Every doc has a summary at the top (the human glance layer) and detail below (the AI context layer). The human reads summaries to confirm alignment. The AI reads everything to make good autonomous decisions.

### Chosen Approach: 3-Doc System + Project Context

Three living documents map directly to the alignment questions. A static context file orients every new AI session. A health check skill keeps the docs current. Session-close discipline moves to lifeos where it's always loaded.

This was chosen over two alternatives:
- **Single-doc dashboard** (one PROJECT.md) -- rejected because it gets long fast, is merge-unfriendly, and hard to update one section without re-reading everything
- **Vision + Backlog only** (two docs) -- rejected because the vision doc becomes overloaded, outcomes get buried, and it's hard to separate "where are we going" from "what did we decide and why"

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────┐
│                   This Bundle                        │
│                                                      │
│  Setup Recipe ──→ Creates/updates 3 docs + AGENTS.md │
│  Health Check ──→ Maintains 3 docs over time         │
│  Templates    ──→ Skeletons for the 4 files          │
│                                                      │
└─────────────────────────────────────────────────────┘
         │                              │
         │ Setup (run once)             │ Health check (periodic)
         ▼                              ▼
┌─────────────────────────────────────────────────────┐
│                  Project Docs                        │
│                                                      │
│  AGENTS.md     ← Static context, read first          │
│  VISION.md     ← What, why, for whom, principles     │
│  OUTCOMES.md   ← Measurable results + status          │
│  BACKLOG.md    ← Built, not built, what's next        │
│                                                      │
└─────────────────────────────────────────────────────┘
         │
         │ Session-close (every session)
         ▼
┌─────────────────────────────────────────────────────┐
│                    Lifeos                             │
│                                                      │
│  session-close protocol ← Commit, push, hygiene      │
│  (always loaded, always fires)                       │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Responsibility Split

| Concern | Owner | Lifecycle |
|---------|-------|-----------|
| Setup recipe (bootstrap docs) | This bundle | Run once per project |
| Templates | This bundle | Referenced during setup |
| Health check skill | This bundle | Run periodically / on demand |
| Session-close discipline | Lifeos (protocol) | Every session, forever |
| Doc maintenance | Health check + session-close | Ongoing |

## Components

### Living Documents

#### VISION.md

What we're building, why, for whom. Includes principles and non-goals. Changes rarely -- the health check may flag drift but doesn't auto-fix.

```markdown
---
last_updated: YYYY-MM-DD
updated_by: [name]
---

# Vision

## Summary
(2-3 sentences: what we're building, the core problem, for whom.
Human reads this to confirm alignment.)

## Problem
(What pain exists. Why the status quo is broken.)

## Solution
(What we're building to solve it. High-level, no implementation details.)

## Non-Goals
(What we are explicitly NOT building. Boundaries for AI autonomy.)

## Who It's For
(Primary audience. What they care about.)

## Principles
(Standing decisions that guide all work. "We value X over Y." Updated rarely.)
```

Design decisions:
- **Non-Goals** is the most important section for AI alignment -- knowing what we're NOT building prevents drift into adjacent territory
- **Principles** lives here (not as a separate doc) because standing principles that rarely change are part of the vision, not a separate concern
- No implementation details -- this is about intent, not how

#### OUTCOMES.md

Measurable results we're driving toward, plus current status. Updated by the health check after PRs.

```markdown
---
last_updated: YYYY-MM-DD
updated_by: [name]
---

# Outcomes

## Current Assessment
(1-2 sentences: overall trajectory, what's ahead, what's behind.)

| Outcome | Why It Matters | How We Measure | Status | Last Checked |
|---------|---------------|----------------|--------|-------------|

## Notes
(Context on status changes. "Shifted focus from X to Y because...")
```

Design decisions:
- **Why It Matters** connects each outcome back to the vision -- the AI can trace any outcome to "why do we care about this"
- **Last Checked** gives both human and AI a staleness signal -- if an outcome hasn't been checked in 2 weeks, something's wrong
- **Notes** captures the "why" behind status changes -- this is where learnings about outcomes live
- Status values should be simple and factual: Not Started / In Progress / Shipped -- not subjective like "On Track / At Risk"

#### BACKLOG.md

What's built, what's not, what's next, tied to outcomes. The most frequently updated doc.

```markdown
---
last_updated: YYYY-MM-DD
updated_by: [name]
---

# Backlog

## Summary
(1-2 sentences: current focus, what just shipped.)

## Active
| Item | Drives Outcome | Status | Assigned |
|------|---------------|--------|----------|

## Up Next
| Item | Drives Outcome | Priority |
|------|---------------|----------|

## Done
| Item | Drives Outcome | Completed | Driven By | Learnings |
|------|---------------|-----------|-----------|-----------|
```

Design decisions:
- **Drives Outcome** ties every item to an outcome, which ties to vision -- the AI can trace any item back to "why are we doing this"
- **Driven By** tracks human vs AI-driven changes -- critical for autonomous loops where the human needs to audit AI decisions (e.g., "AI drove 8 of the last 10 changes -- let me audit those")
- **Learnings** captures what we learned on completed items without a separate doc -- if a learning is significant enough to change how we work, the health check surfaces it and pushes it into VISION.md (principles) or OUTCOMES.md
- **Backlog will grow** over time; the health check can archive old Done items if it gets unwieldy -- solve that problem when it's actually a problem, not preemptively

#### AGENTS.md

Static project context file. "Read me first" for every AI session. Changes rarely.

```markdown
---
last_updated: YYYY-MM-DD
updated_by: [name]
---

# [Project Name]

## What This Is
(1-2 sentences: what the project does and why it exists.)

## Current Focus
(What we're working on right now. Updated each session.)

## Key Decisions
(Running list of big calls that shaped the project. Brief -- decision + rationale.)

## Project Structure
(Key directories and what they contain.)

## Docs
- [VISION.md](docs/VISION.md) -- What we're building and why
- [OUTCOMES.md](docs/OUTCOMES.md) -- Measurable results and status
- [BACKLOG.md](docs/BACKLOG.md) -- What's built, what's next

## How We Work
(Key conventions the AI needs for autonomous decisions.)
```

Design decisions:
- **Current Focus** tells every new session what to care about -- no wasted time exploring
- **Key Decisions** gives the AI the big calls without reading the full VISION.md -- "we chose Postgres over Mongo because X"
- **Project Structure** gives the AI a map so it doesn't waste tokens exploring the filesystem
- This is the lightest doc -- could exist for any project, even small ones

### Templates

Templates are **skeletons, not guides**. Just section headers, frontmatter, and minimal structure. All coaching on how to fill them in lives in the recipe prompts -- used once during setup and then gone, not cluttering the actual project docs.

The bundle ships 4 templates:

| Template | Location |
|----------|----------|
| `VISION_TEMPLATE.md` | `@doc-driven-dev:templates/` |
| `OUTCOMES_TEMPLATE.md` | `@doc-driven-dev:templates/` |
| `BACKLOG_TEMPLATE.md` | `@doc-driven-dev:templates/` |
| `AGENTS_TEMPLATE.md` | `@doc-driven-dev:templates/` |

Templates are referenced via `@doc-driven-dev:templates/` -- no hardcoded local paths.

### Setup Recipe

Handles **3 project states**, not just greenfield:

| State | What the recipe does |
|-------|---------------------|
| **Greenfield** (no docs) | Creates AGENTS.md + 3 docs from scratch through conversation |
| **Undocumented** (existing project, no docs) | Reads the codebase first, then creates docs that reflect what already exists |
| **Stale** (docs exist but drifted) | Reads existing docs + codebase, updates docs to reflect current reality |

**4 stages** (down from 5 in v1):

| Stage | What happens |
|-------|-------------|
| **1. Discovery** | Detect project state (greenfield/undocumented/stale). Read existing docs and code if present. |
| **2. Vision** | Interview user about what they're building and why -- or validate/update existing VISION.md. |
| **3. Outcomes + Backlog** | Define measurable outcomes and initial backlog -- or update existing ones. |
| **4. Project Context** | Create AGENTS.md -- the "read me first" file for AI sessions. |

Design decisions:
- No separate "structure" stage -- just create the docs folder
- No separate "navigation" stage -- AGENTS.md replaces the docs/README.md hub
- Stage 1 does detection -- subsequent stages update rather than create if docs already exist
- One recipe for V1 -- no fast variant; add that later if needed

### Health Check Skill

The mechanism that keeps the 3 living docs current over time. A skill in this bundle loaded via `load_skill(skill_name="health-check")`.

**What it reads:**

- VISION.md, OUTCOMES.md, BACKLOG.md
- Recent git history (commits, PRs since `last_updated`)

**What it does (in order):**

| Step | Action | Confidence |
|------|--------|-----------|
| 1 | Read all 3 docs + recent commits/PRs since `last_updated` | -- |
| 2 | **Backlog update** -- move completed items to Done with `Driven By` and `Learnings`. Add new items discovered from commits that aren't in the backlog. | High (factual) |
| 3 | **Outcomes update** -- update Status and Last Checked for each outcome. Update Current Assessment summary. | Medium-High (factual statuses) |
| 4 | **Vision drift check** -- flag if recent work contradicts Problem, Solution, Non-Goals, or Principles. Don't auto-fix -- surface to human. | Medium (judgment call) |
| 5 | **AGENTS.md update** -- update Current Focus from active backlog. Update Key Decisions if significant decisions were made. | Medium (may need human input) |
| 6 | Update `last_updated` and `updated_by` frontmatter on every doc that changed. | High (mechanical) |

**Critical design principle: Update facts automatically. Flag judgments for human decision.**

- Steps 2-3 are automatic (items are done or they aren't, metrics moved or they didn't)
- Step 4 is a flag, not a fix (the AI surfaces drift, the human decides whether to update the vision or course-correct the work)

**Confidence summary:** The health check ends with a transparency report:

```
Confident: Moved 3 backlog items to Done, updated 2 outcome statuses
Uncertain: PR #52 doesn't map to any backlog item -- new work or missing item?
Not checked: Haven't compared against Non-Goals (no code analysis this run)
```

**When it runs:**

| Trigger | Description |
|---------|-------------|
| Post-PR | Triggered manually ("run a health check") after merging |
| On-demand | When something feels off |
| Future | Could be automated as a CI step (not V1) |

**What it produces:** No separate artifact. The docs themselves get updated. The health check reports to the human what it changed and what it flagged.

### Session-Close Protocol (Moves to Lifeos)

The session-close discipline is the anti-drift mechanism, but it's currently dead code because the bundle isn't loaded in day-to-day sessions.

**Solution:** Move to lifeos as a protocol at `~/.lifeos/memory/_protocols/session-close.md`. Lifeos is always loaded, so the discipline always fires.

**What moves:** One protocol file + one line in lifeos ambient context.
**What stays in this bundle:** The setup recipe, the templates, the health check skill.

**The distinction:**

| Mechanism | Where | What it does | When |
|-----------|-------|-------------|------|
| **Session-close** | Lifeos | Commit changes, push -- mechanical hygiene | Every session |
| **Health check** | This bundle | Alignment audit -- strategic assessment | Periodically / on demand |

## Data Flow

### Setup Flow (Run Once Per Project)

```
User triggers "run doc-driven-setup"
  │
  ├─ Stage 1: Discovery
  │    ├─ Scan for existing docs
  │    ├─ Scan codebase (if undocumented/stale)
  │    └─ Determine project state: greenfield / undocumented / stale
  │
  ├─ Stage 2: Vision
  │    ├─ Interview user (greenfield) OR validate existing (stale)
  │    └─ Write/update VISION.md
  │
  ├─ Stage 3: Outcomes + Backlog
  │    ├─ Define outcomes tied to vision
  │    ├─ Create initial backlog tied to outcomes
  │    └─ Write OUTCOMES.md + BACKLOG.md
  │
  └─ Stage 4: Project Context
       └─ Write AGENTS.md (links to all 3 docs, project structure)
```

### Health Check Flow (Periodic)

```
User triggers "run a health check"
  │
  ├─ Read VISION.md, OUTCOMES.md, BACKLOG.md
  ├─ Read git log since last_updated
  │
  ├─ Backlog: move completed → Done, add missing items  [auto]
  ├─ Outcomes: update statuses, Current Assessment       [auto]
  ├─ Vision: flag drift against Non-Goals/Principles     [flag only]
  ├─ AGENTS.md: update Current Focus, Key Decisions      [semi-auto]
  │
  ├─ Update frontmatter (last_updated, updated_by)
  └─ Report: confident / uncertain / not checked
```

### Session Flow (Every Session)

```
AI session starts
  │
  ├─ Read AGENTS.md (project context)
  ├─ Work happens (AI builds, human directs)
  │
  └─ Session ends
       └─ Lifeos session-close protocol fires
            ├─ git status → commit if needed
            └─ git push
```

## Error Handling

| Scenario | Handling |
|----------|---------|
| Setup recipe finds existing docs | Switch to update mode (don't overwrite) |
| Health check can't map a commit to a backlog item | Report as "Uncertain" in confidence summary |
| Health check detects vision drift | Flag to human, don't auto-fix |
| AGENTS.md Key Decisions grows too long | Health check prunes or the human decides (open question) |
| Backlog Done section grows unwieldy | Archive old items when it becomes a problem |
| Templates path is wrong / missing | Use `@doc-driven-dev:templates/` bundle references (no hardcoded paths) |

## Testing Strategy

| What to test | How |
|-------------|-----|
| Setup recipe -- greenfield | Run on a new empty project, verify all 4 files created with correct structure |
| Setup recipe -- undocumented | Run on an existing project with code but no docs, verify docs reflect codebase |
| Setup recipe -- stale | Run on a project with outdated docs, verify docs get updated not overwritten |
| Health check -- backlog updates | Make commits, run health check, verify Done items appear with correct attribution |
| Health check -- outcomes update | Ship work tied to an outcome, run health check, verify status updates |
| Health check -- vision drift | Make changes that contradict Non-Goals, run health check, verify drift is flagged (not fixed) |
| Health check -- confidence summary | Run health check with ambiguous commits, verify uncertain items are reported |
| Template references | Verify templates load via `@doc-driven-dev:templates/` from any machine |
| Bundle structure | Verify `bundle.md` injects system prompt, behaviors compose correctly |

## Bundle Structure

```
amplifier-doc-driven-dev/
├── bundle.md                          # Markdown with YAML frontmatter (replaces bundle.yaml)
├── behaviors/
│   └── doc-driven-dev.yaml            # Behavior layer (tools + context config)
├── context/
│   └── instructions.md                # System instructions for AI
├── recipes/
│   └── doc-driven-setup.yaml          # Single setup recipe (handles all 3 project states)
├── skills/
│   └── health-check.md               # Health check skill
├── templates/
│   ├── VISION_TEMPLATE.md
│   ├── OUTCOMES_TEMPLATE.md
│   ├── BACKLOG_TEMPLATE.md
│   └── AGENTS_TEMPLATE.md
├── docs/
│   └── plans/                         # Design docs
└── README.md
```

### What Changed from v1

| Removed | Why |
|---------|-----|
| 3-tier system (lean/standard/full) | Over-engineered. Every project gets the same 4 docs. |
| `EPIC_TEMPLATE.md` | Absorbed into BACKLOG.md items |
| `USER_STORY_TEMPLATE.md` | Absorbed into BACKLOG.md items |
| `SUCCESS_METRICS_TEMPLATE.md` | Absorbed into OUTCOMES.md |
| `PRINCIPLES_TEMPLATE.md` | Folded into VISION.md as a section |
| Writing guidelines in templates | Coaching lives in recipe prompts, not in project docs |
| `session-close.md` skill + ambient reminder | Moves to lifeos (always loaded) |
| Fast recipe variant (`doc-driven-setup-fast.yaml`) | One recipe for V1. Add fast mode later if needed. |
| Hardcoded `templates_path` | Templates referenced via `@doc-driven-dev:templates/` |
| Redundant `skills:` git URL in bundle config | `skills_dirs: ./skills` is sufficient |
| `bundle.yaml` | Replaced by `bundle.md` (markdown body becomes system prompt) |

| Added | Why |
|-------|-----|
| `bundle.md` | Canonical Amplifier entry point with system prompt |
| `behaviors/doc-driven-dev.yaml` | Composable behavior layer |
| `context/instructions.md` | System instructions referenced via @mention |
| `OUTCOMES_TEMPLATE.md` | New doc replacing SUCCESS_METRICS with simpler "where do we stand" format |
| `AGENTS_TEMPLATE.md` | New static context file for AI session orientation |
| `health-check.md` skill | New mechanism for ongoing doc maintenance |

## Open Questions

1. **AGENTS.md "Key Decisions" growth** -- Should this be the last N decisions? All decisions? Should the health check prune it? Defer to real-world testing.
2. **Backlog archiving** -- When does the Done section get too long? Solve when it's actually a problem, not preemptively.
3. **Health check as CI step** -- Could run automatically post-merge and open a PR with doc updates. Future work, not V1.
4. **Superpowers integration** -- Should the setup recipe integrate with brainstorm mode? Or is it a standalone recipe you run when needed? Current decision: standalone recipe, revisit after testing.
5. **Multi-person repos** -- Attribution (Driven By) helps, but how does the health check work when multiple people push? Current decision: the health check reads all commits regardless of author. The Driven By column distinguishes. Test in practice.
