# Doc-Driven Dev v2 Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Rebuild the `amplifier-doc-driven-dev` bundle from a documentation scaffolding tool into an alignment system for human-AI collaboration, with 3 living docs, a static project context file, a health check skill, and a properly structured Amplifier bundle.

**Architecture:** The bundle ships 4 lean templates (VISION, OUTCOMES, BACKLOG, AGENTS), a single setup recipe that handles greenfield/undocumented/stale projects through 4 conversational stages, and a health check skill that reads the 3 living docs + git history to keep them honest. The session-close discipline moves out to lifeos (separate effort, not in this plan).

**Tech Stack:** Amplifier bundle (bundle.md with YAML frontmatter), Amplifier recipe (YAML), Amplifier skill (markdown with YAML frontmatter), markdown templates

---

## Context for the Implementer

This is **not a code project**. There is no Python, no tests, no pytest. The entire repo is YAML and markdown files that form an Amplifier bundle. "Validation" here means:

- Checking that YAML files parse correctly
- Verifying markdown renders as expected
- Running `recipes validate` on recipe files
- Confirming the bundle structure follows Amplifier conventions

**The repo lives at:** `/Users/chrispark/Projects/amplifier-doc-driven-dev`

**Current structure (v1 -- what you're replacing):**
```
amplifier-doc-driven-dev/
├── bundle.yaml                      ← WRONG: should be bundle.md
├── README.md                        ← Needs full rewrite
├── context/
│   └── session-close-reminder.md    ← DELETE: moving to lifeos
├── docs/
│   └── plans/
│       └── 2026-03-24-doc-driven-dev-v2-design.md  ← DO NOT TOUCH
├── recipes/
│   ├── doc-driven-setup.yaml        ← REWRITE: 5 stages → 4 stages
│   └── doc-driven-setup-fast.yaml   ← DELETE: one recipe for v2
├── skills/
│   └── session-close.md             ← DELETE: replace with health-check
└── templates/
    ├── BACKLOG_TEMPLATE.md           ← REWRITE
    ├── EPIC_TEMPLATE.md              ← DELETE
    ├── PRINCIPLES_TEMPLATE.md        ← DELETE
    ├── SUCCESS_METRICS_TEMPLATE.md   ← DELETE
    ├── USER_STORY_TEMPLATE.md        ← DELETE
    └── VISION_TEMPLATE.md            ← REWRITE
```

**Target structure (v2 -- what you're building):**
```
amplifier-doc-driven-dev/
├── bundle.md                         ← NEW: proper Amplifier entry point
├── README.md                         ← REWRITTEN
├── behaviors/
│   └── doc-driven-dev.yaml           ← NEW: composable behavior layer
├── context/
│   └── instructions.md               ← NEW: system instructions for AI
├── docs/
│   └── plans/
│       └── 2026-03-24-doc-driven-dev-v2-design.md  ← UNTOUCHED
├── recipes/
│   └── doc-driven-setup.yaml         ← REWRITTEN: 4 stages, 3 project states
├── skills/
│   └── health-check.md               ← NEW: replaces session-close
└── templates/
    ├── AGENTS_TEMPLATE.md             ← NEW
    ├── BACKLOG_TEMPLATE.md            ← REWRITTEN (lean skeleton)
    ├── OUTCOMES_TEMPLATE.md           ← NEW
    └── VISION_TEMPLATE.md            ← REWRITTEN (lean skeleton)
```

---

## Phase 1: Clean Slate -- Delete Obsolete v1 Files

### Task 1: Delete obsolete files

**Files:**
- Delete: `recipes/doc-driven-setup-fast.yaml`
- Delete: `templates/EPIC_TEMPLATE.md`
- Delete: `templates/USER_STORY_TEMPLATE.md`
- Delete: `templates/SUCCESS_METRICS_TEMPLATE.md`
- Delete: `templates/PRINCIPLES_TEMPLATE.md`

**Step 1: Delete all 5 files**

Run these commands from the repo root (`/Users/chrispark/Projects/amplifier-doc-driven-dev`):

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
rm recipes/doc-driven-setup-fast.yaml
rm templates/EPIC_TEMPLATE.md
rm templates/USER_STORY_TEMPLATE.md
rm templates/SUCCESS_METRICS_TEMPLATE.md
rm templates/PRINCIPLES_TEMPLATE.md
```

**Step 2: Verify they're gone**

Run:
```bash
ls recipes/
ls templates/
```

Expected output:
```
recipes/:
doc-driven-setup.yaml

templates/:
BACKLOG_TEMPLATE.md
VISION_TEMPLATE.md
```

Only `doc-driven-setup.yaml` should remain in `recipes/`. Only `BACKLOG_TEMPLATE.md` and `VISION_TEMPLATE.md` should remain in `templates/`.

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add -A && git commit -m "chore: remove v1 files superseded by v2 design

Removed:
- recipes/doc-driven-setup-fast.yaml (redundant fast variant)
- templates/EPIC_TEMPLATE.md (absorbed into BACKLOG.md)
- templates/USER_STORY_TEMPLATE.md (absorbed into BACKLOG.md)
- templates/SUCCESS_METRICS_TEMPLATE.md (absorbed into OUTCOMES.md)
- templates/PRINCIPLES_TEMPLATE.md (folded into VISION.md)"
```

---

## Phase 2: New Foundation -- Bundle Structure

### Task 2: Create bundle.md

This replaces the current `bundle.yaml` with a proper Amplifier bundle entry point. The key difference: `bundle.md` has a markdown body that becomes the system prompt injected into every session.

**Files:**
- Create: `bundle.md`

**Step 1: Create `bundle.md`**

Create the file `bundle.md` at the repo root with this exact content:

```markdown
---
bundle:
  name: doc-driven-dev
  version: 2.0.0
  description: >
    Alignment system for human-AI collaboration. Bootstraps and maintains
    living docs (VISION, OUTCOMES, BACKLOG) so that at any point mid-project,
    you can confirm alignment, see what was built, understand why, and assess
    whether work is accruing to meaningful outcomes.

includes:
  - bundle: git+https://github.com/microsoft/amplifier-foundation@main
  - bundle: doc-driven-dev:behaviors/doc-driven-dev

---

# Doc-Driven Development

@doc-driven-dev:context/instructions.md
```

**Step 2: Verify the file**

Run:
```bash
cat bundle.md
```

Confirm:
- The YAML frontmatter starts and ends with `---`
- `bundle.name` is `doc-driven-dev`
- `bundle.version` is `2.0.0`
- `includes` lists the foundation bundle and the behavior bundle
- The markdown body has a heading and an `@doc-driven-dev:context/instructions.md` reference

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add bundle.md && git commit -m "feat: create bundle.md as proper Amplifier entry point"
```

---

### Task 3: Create the behavior layer

Behaviors are composable capability units that other bundles can include without pulling in your entire bundle. This one registers the skills directory so the health check skill is discoverable.

**Files:**
- Create: `behaviors/doc-driven-dev.yaml`

**Step 1: Create the `behaviors/` directory and the behavior file**

```bash
mkdir -p /Users/chrispark/Projects/amplifier-doc-driven-dev/behaviors
```

Create `behaviors/doc-driven-dev.yaml` with this exact content:

```yaml
bundle:
  name: doc-driven-dev-behavior
  version: 2.0.0
  description: >
    Doc-driven development capability. Provides the health-check skill
    and alignment system context. Compose onto any bundle to add
    doc-driven alignment.

tools:
  - module: tool-skills
    source: git+https://github.com/microsoft/amplifier-module-tool-skills@main
    config:
      skills_dirs:
        - ./skills
      visibility:
        enabled: true
        max_skills_visible: 50

context:
  include:
    - doc-driven-dev:context/instructions.md
```

**Step 2: Verify the file**

Run:
```bash
cat behaviors/doc-driven-dev.yaml
```

Confirm:
- `skills_dirs` points to `./skills` only (no redundant git URL)
- `context.include` references the instructions file via `@doc-driven-dev:` prefix
- No `skills:` key with a remote git URL (that was the v1 bug)

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add behaviors/ && git commit -m "feat: add composable behavior layer for doc-driven-dev"
```

---

### Task 4: Create system instructions

This file gets injected into every session via the `@doc-driven-dev:context/instructions.md` reference in `bundle.md`. It tells the AI what the alignment system is and how to work with it.

**Files:**
- Create: `context/instructions.md`

**Step 1: Create `context/instructions.md`**

Create the file with this exact content:

```markdown
# Doc-Driven Development: Alignment System

This project uses doc-driven development -- an alignment system for human-AI collaboration. The docs exist so that at any point mid-project, the human can confirm alignment, see what was built, understand why, and assess whether work is accruing to meaningful outcomes.

## The 4 Alignment Questions

| Question | Doc |
|----------|-----|
| Is what we're building still what we set out to build? | `docs/VISION.md` |
| Is work accruing to something measurable? | `docs/OUTCOMES.md` |
| What's built, what's not, what's next? | `docs/BACKLOG.md` |
| What does a new session need to know? | `AGENTS.md` (project root) |

## The 80/20 Principle

Docs are **80% for AI context, 20% for human confidence**. Every doc has a summary at the top (the human glance layer) and detail below (the AI context layer).

## How to Work With These Docs

- **Start of session:** Read `AGENTS.md` for project orientation, then check `docs/BACKLOG.md` for current focus.
- **During work:** When making significant decisions, note them. When completing backlog items, update their status.
- **Health check:** Run `load_skill(skill_name="health-check")` periodically (after PRs, on-demand, or when something feels off) to audit alignment across all docs.

## Rules

1. **Update facts automatically, flag judgments for humans.** Backlog status changes are factual. Vision drift is a judgment call -- surface it, don't auto-fix.
2. **Every backlog item must connect to an outcome.** If it doesn't drive an outcome, question why it exists.
3. **Non-Goals are boundaries.** If work drifts into a Non-Goal, stop and flag it.
4. **Learnings are inline, not separate.** Attach learnings to the backlog items or outcome notes that triggered them.
5. **Attribution matters.** Track who drove each completed item (human vs AI) for accountability in autonomous loops.
```

**Step 2: Verify the file**

Run:
```bash
cat context/instructions.md
```

Confirm the file has the heading, the 4 alignment questions table, the 80/20 principle, workflow guidance, and the 5 rules.

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add context/instructions.md && git commit -m "feat: add system instructions for AI alignment context"
```

---

### Task 5: Delete old bundle files

Now that the new bundle structure is in place, remove the old files.

**Files:**
- Delete: `bundle.yaml`
- Delete: `context/session-close-reminder.md`

**Step 1: Delete the old files**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
rm bundle.yaml
rm context/session-close-reminder.md
```

**Step 2: Verify**

Run:
```bash
ls bundle.* context/
```

Expected:
```
bundle.md

context/:
instructions.md
```

Only `bundle.md` at root. Only `instructions.md` in `context/`.

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add -A && git commit -m "feat: remove v1 bundle.yaml and session-close-reminder

Replaced by bundle.md (proper Amplifier entry point) and
context/instructions.md (system prompt). Session-close
discipline will move to lifeos (separate effort)."
```

---

## Phase 3: Templates -- The 4 Lean Skeletons

### Task 6: Rewrite VISION_TEMPLATE.md

The v1 template is 329 lines with writing guidelines, table of contents, strategic positioning, and competitive analysis sections. The v2 template is a lean skeleton: just section headers and frontmatter. All coaching lives in the recipe prompts, not the template.

**Files:**
- Modify: `templates/VISION_TEMPLATE.md`

**Step 1: Replace `templates/VISION_TEMPLATE.md`**

Overwrite the entire file with this exact content:

```markdown
---
last_updated: YYYY-MM-DD
updated_by: [name]
---

# Vision

## Summary

(2-3 sentences: what we're building, the core problem, for whom. Human reads this to confirm alignment.)

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

**Step 2: Verify**

Run:
```bash
wc -l templates/VISION_TEMPLATE.md
```

Expected: around 30 lines (not 329). The file should have YAML frontmatter, then 6 sections: Summary, Problem, Solution, Non-Goals, Who It's For, Principles. No writing guidelines, no table of contents, no competitive analysis.

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add templates/VISION_TEMPLATE.md && git commit -m "feat: replace v1 VISION template with lean v2 skeleton"
```

---

### Task 7: Rewrite BACKLOG_TEMPLATE.md

The v1 template is 133 lines with epic tracking, sprint planning, effort/impact scoring, and emoji conventions. The v2 template is a lean skeleton with 3 sections (Active, Up Next, Done) and tables that tie every item to an outcome.

**Files:**
- Modify: `templates/BACKLOG_TEMPLATE.md`

**Step 1: Replace `templates/BACKLOG_TEMPLATE.md`**

Overwrite the entire file with this exact content:

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

**Step 2: Verify**

Run:
```bash
wc -l templates/BACKLOG_TEMPLATE.md
```

Expected: around 27 lines (not 133). The file should have YAML frontmatter, a Summary section, and 3 table sections: Active, Up Next, Done. The Done table has `Driven By` and `Learnings` columns for accountability.

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add templates/BACKLOG_TEMPLATE.md && git commit -m "feat: replace v1 BACKLOG template with lean v2 skeleton"
```

---

### Task 8: Create OUTCOMES_TEMPLATE.md

This is a brand new template. It replaces the old SUCCESS_METRICS_TEMPLATE (281 lines of V1/V2/V3 metrics, leading/lagging indicators, vanity metrics) with a simple table of outcomes and their status.

**Files:**
- Create: `templates/OUTCOMES_TEMPLATE.md`

**Step 1: Create `templates/OUTCOMES_TEMPLATE.md`**

Create the file with this exact content:

```markdown
---
last_updated: YYYY-MM-DD
updated_by: [name]
---

# Outcomes

## Current Assessment

(1-2 sentences: overall trajectory. What's ahead, what's behind.)

| Outcome | Why It Matters | How We Measure | Status | Last Checked |
|---------|---------------|----------------|--------|-------------|

## Notes

(Context on status changes. "Shifted focus from X to Y because...")
```

**Step 2: Verify**

Run:
```bash
cat templates/OUTCOMES_TEMPLATE.md
wc -l templates/OUTCOMES_TEMPLATE.md
```

Expected: around 19 lines. The file should have YAML frontmatter, a Current Assessment section, one table with 5 columns (Outcome, Why It Matters, How We Measure, Status, Last Checked), and a Notes section.

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add templates/OUTCOMES_TEMPLATE.md && git commit -m "feat: add lean OUTCOMES template (replaces SUCCESS_METRICS)"
```

---

### Task 9: Create AGENTS_TEMPLATE.md

Brand new template. This is the "read me first" file for every AI session. It orients the AI on what the project is, what to focus on, and where the docs live.

**Files:**
- Create: `templates/AGENTS_TEMPLATE.md`

**Step 1: Create `templates/AGENTS_TEMPLATE.md`**

Create the file with this exact content:

```markdown
---
last_updated: YYYY-MM-DD
updated_by: [name]
---

# [Project Name]

## What This Is

(1-2 sentences: what the project does and why it exists.)

## Current Focus

(What we're working on right now. Updated each session or by the health check.)

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

**Step 2: Verify**

Run:
```bash
cat templates/AGENTS_TEMPLATE.md
wc -l templates/AGENTS_TEMPLATE.md
```

Expected: around 33 lines. The file should have YAML frontmatter, then 6 sections: What This Is, Current Focus, Key Decisions, Project Structure, Docs (with links to the 3 living docs), and How We Work.

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add templates/AGENTS_TEMPLATE.md && git commit -m "feat: add lean AGENTS template for AI session orientation"
```

---

## Phase 4: Recipe -- The Biggest Lift

The v1 recipe is 661 lines with 5 stages, hardcoded local paths, tier selection, and epic generation. The v2 recipe has 4 stages, handles 3 project states (greenfield/undocumented/stale), uses bundle-relative template references, and has no tier system.

### Task 10: Write the recipe skeleton

Start with the outer structure: name, description, context variables, and stage declarations with names only. No prompts yet.

**Files:**
- Modify: `recipes/doc-driven-setup.yaml`

**Step 1: Replace `recipes/doc-driven-setup.yaml` with the skeleton**

Overwrite the entire file with this exact content:

```yaml
# Doc-Driven Development Setup Recipe (v2)
# =========================================
#
# Alignment system for human-AI collaboration.
# Bootstraps 3 living docs (VISION, OUTCOMES, BACKLOG) + AGENTS.md
# for any project state: greenfield, undocumented, or stale.
#
# Usage:
#   "Run doc-driven-setup for my project"
#
# 4 stages:
#   1. Discovery   - detect project state, gather context
#   2. Vision      - create or update VISION.md
#   3. Outcomes    - create or update OUTCOMES.md + BACKLOG.md
#   4. Context     - create AGENTS.md

name: "doc-driven-setup"
description: "Bootstrap alignment docs for human-AI collaboration -- handles greenfield, undocumented, and stale projects"
version: "2.0.0"
author: "Chris Park"
tags: ["alignment", "documentation", "setup", "doc-driven"]

context:
  project_path: ""
  project_name: ""
  project_description: ""

stages:
  # Stage 1: Discovery
  - name: "discovery"
    steps:
      - id: "detect-project-state"
        agent: "default"
        prompt: "placeholder -- will be filled in next task"
        output: "discovery_result"
        timeout: 300

  # Stage 2: Vision
  - name: "vision"
    approval:
      required: true
      prompt: |
        DISCOVERY COMPLETE

        {{discovery_result}}

        Ready to work on VISION.md.
        Approve to continue. Deny to revise.
    steps:
      - id: "create-vision"
        agent: "default"
        prompt: "placeholder -- will be filled in next task"
        output: "vision_result"
        timeout: 600

  # Stage 3: Outcomes + Backlog
  - name: "outcomes-backlog"
    approval:
      required: true
      prompt: |
        VISION COMPLETE

        {{vision_result}}

        Ready to work on OUTCOMES.md and BACKLOG.md.
        Approve to continue. Deny to revise.
    steps:
      - id: "create-outcomes-backlog"
        agent: "default"
        prompt: "placeholder -- will be filled in next task"
        output: "outcomes_backlog_result"
        timeout: 600

  # Stage 4: Project Context
  - name: "project-context"
    steps:
      - id: "create-agents-md"
        agent: "default"
        prompt: "placeholder -- will be filled in next task"
        output: "setup_complete"
        timeout: 300
```

**Step 2: Verify the skeleton parses**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
python3 -c "import yaml; yaml.safe_load(open('recipes/doc-driven-setup.yaml')); print('YAML parses OK')"
```

Expected: `YAML parses OK`

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add recipes/doc-driven-setup.yaml && git commit -m "feat: recipe v2 skeleton -- 4 stages, 3 project states, no tiers"
```

---

### Task 11: Write Stage 1 (Discovery) prompt

This stage detects the project state (greenfield, undocumented, or stale) and gathers project info. It replaces the v1 discovery stage which only gathered project info and selected a tier.

**Files:**
- Modify: `recipes/doc-driven-setup.yaml` (replace the discovery placeholder)

**Step 1: Replace the discovery step placeholder**

In `recipes/doc-driven-setup.yaml`, find the line:
```
        prompt: "placeholder -- will be filled in next task"
        output: "discovery_result"
```

Replace the first placeholder prompt (in the `detect-project-state` step) with:

```yaml
        prompt: |
          You are setting up an alignment system for human-AI collaboration on a project.

          ## Current Context

          - Project Path: {{project_path}}
          - Project Name: {{project_name}}
          - Project Description: {{project_description}}

          ## Your Task

          **Step 1: Gather missing info (if needed)**

          If project_path, project_name, or project_description are empty, ask the user:
          1. "Where is your project located? (full path)"
          2. "What's the project name?"
          3. "In one sentence, what does this project do?"

          **Step 2: Detect project state**

          Check the project directory:
          ```bash
          ls -la {{project_path}}/
          ls -la {{project_path}}/docs/ 2>/dev/null
          cat {{project_path}}/AGENTS.md 2>/dev/null
          cat {{project_path}}/docs/VISION.md 2>/dev/null
          cat {{project_path}}/docs/OUTCOMES.md 2>/dev/null
          cat {{project_path}}/docs/BACKLOG.md 2>/dev/null
          ```

          Classify as one of:
          - **Greenfield**: No docs/ directory, no AGENTS.md, no alignment docs
          - **Undocumented**: Project has code but no alignment docs (no docs/VISION.md etc.)
          - **Stale**: Alignment docs exist but may be outdated (check last_updated frontmatter vs recent git activity)

          If the project is undocumented or stale, also scan the codebase to understand what exists:
          ```bash
          find {{project_path}} -maxdepth 2 -type f | head -30
          git -C {{project_path}} log --oneline -10 2>/dev/null
          ```

          **Step 3: Report**

          Provide a structured summary:

          ```
          DISCOVERY SUMMARY
          =================
          Project: [name]
          Path: [path]
          Description: [description]
          State: [Greenfield / Undocumented / Stale]

          Existing Docs:
          - AGENTS.md: [exists/missing]
          - docs/VISION.md: [exists/missing]
          - docs/OUTCOMES.md: [exists/missing]
          - docs/BACKLOG.md: [exists/missing]

          Codebase Summary (if applicable):
          - [brief overview of what exists]

          Plan:
          - [what will be created/updated in the next stages]
          ```
```

**Step 2: Verify YAML still parses**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
python3 -c "import yaml; yaml.safe_load(open('recipes/doc-driven-setup.yaml')); print('YAML parses OK')"
```

Expected: `YAML parses OK`

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add recipes/doc-driven-setup.yaml && git commit -m "feat: recipe Stage 1 (Discovery) -- detect project state"
```

---

### Task 12: Write Stage 2 (Vision) prompt

This stage creates or updates VISION.md through conversation. It uses the lean template skeleton and adapts behavior based on project state (greenfield = interview from scratch, undocumented/stale = read existing state first).

**Files:**
- Modify: `recipes/doc-driven-setup.yaml` (replace the vision placeholder)

**Step 1: Replace the vision step placeholder**

In `recipes/doc-driven-setup.yaml`, find the `create-vision` step and replace its placeholder prompt:

```yaml
        prompt: |
          Create or update the VISION.md document for this project.

          ## Context
          - Project: {{project_name}}
          - Description: {{project_description}}
          - Path: {{project_path}}
          - Discovery: {{discovery_result}}

          ## Template

          Read the vision template for the target structure:
          `@doc-driven-dev:templates/VISION_TEMPLATE.md`

          ## Instructions by Project State

          **If Greenfield (no existing docs):**
          Interview the user to fill in each section. Ask 2-3 focused questions at a time:
          1. "What problem does {{project_name}} solve? Who experiences this pain?"
          2. "What are you building to solve it? High-level, not technical details."
          3. "What are you explicitly NOT building? What boundaries should the AI respect?"
          4. "Who is the primary audience? What do they care about?"
          5. "What standing principles guide how we work? (e.g., 'We value simplicity over features')"

          **If Undocumented (code exists, no docs):**
          Read the codebase and discovery summary to draft VISION.md, then present to the user for validation.
          Ask: "I've drafted a vision based on what I see in the codebase. Does this capture the intent? What's wrong or missing?"

          **If Stale (docs exist but drifted):**
          Read the existing VISION.md, compare against recent git history and codebase state.
          Present what's changed and ask: "Here's what seems to have drifted. Should we update the vision to match reality, or course-correct the work?"

          ## Output

          Write the completed VISION.md to: `{{project_path}}/docs/VISION.md`
          Create the docs/ directory if it doesn't exist: `mkdir -p {{project_path}}/docs`

          Use today's date for `last_updated` in the frontmatter.
          Use the user's name for `updated_by`.

          Fill in every section with real content from the conversation. Remove all placeholder text and parenthetical instructions from the template.

          Report:
          ```
          VISION COMPLETE
          ===============
          File: {{project_path}}/docs/VISION.md
          State: [Created / Updated]

          Summary: [2-3 sentence summary of the vision]
          Non-Goals: [list the boundaries]
          Principles: [list the principles]
          ```
```

**Step 2: Verify YAML parses**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
python3 -c "import yaml; yaml.safe_load(open('recipes/doc-driven-setup.yaml')); print('YAML parses OK')"
```

Expected: `YAML parses OK`

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add recipes/doc-driven-setup.yaml && git commit -m "feat: recipe Stage 2 (Vision) -- create or update VISION.md"
```

---

### Task 13: Write Stage 3 (Outcomes + Backlog) prompt

This stage creates or updates OUTCOMES.md and BACKLOG.md. Outcomes are tied to the vision. Backlog items are tied to outcomes.

**Files:**
- Modify: `recipes/doc-driven-setup.yaml` (replace the outcomes-backlog placeholder)

**Step 1: Replace the outcomes-backlog step placeholder**

In `recipes/doc-driven-setup.yaml`, find the `create-outcomes-backlog` step and replace its placeholder prompt:

```yaml
        prompt: |
          Create or update OUTCOMES.md and BACKLOG.md for this project.

          ## Context
          - Project: {{project_name}}
          - Path: {{project_path}}
          - Discovery: {{discovery_result}}
          - Vision: {{vision_result}}

          ## Templates

          Read both templates for the target structure:
          - `@doc-driven-dev:templates/OUTCOMES_TEMPLATE.md`
          - `@doc-driven-dev:templates/BACKLOG_TEMPLATE.md`

          ## Instructions

          ### OUTCOMES.md

          Based on the vision, interview the user about measurable outcomes:
          1. "What does success look like for this project? What measurable results matter?"
          2. "For each outcome -- why does it matter? How would you know you've achieved it?"
          3. "Where do we stand right now on each outcome? (Not Started / In Progress / Shipped)"

          Fill in the outcomes table. Each outcome should:
          - Connect back to the vision ("Why It Matters")
          - Have a concrete measurement ("How We Measure")
          - Have a current status and last checked date

          Write a Current Assessment (1-2 sentences on overall trajectory).

          **If Undocumented/Stale:** Review what already exists in the codebase to pre-populate outcomes and validate with the user.

          ### BACKLOG.md

          Based on the outcomes, help the user define the initial backlog:
          1. "What are you actively working on right now?" (→ Active section)
          2. "What should come next?" (→ Up Next section)
          3. "What have you already completed?" (→ Done section, if applicable)

          Every backlog item MUST have a "Drives Outcome" value linking it to an outcome from OUTCOMES.md.

          **If Undocumented:** Review recent git history to pre-populate the Done section:
          ```bash
          git -C {{project_path}} log --oneline -20 2>/dev/null
          ```

          ## Output

          Write both files:
          - `{{project_path}}/docs/OUTCOMES.md`
          - `{{project_path}}/docs/BACKLOG.md`

          Use today's date for `last_updated` and the user's name for `updated_by` in both files.
          Remove all placeholder text and parenthetical instructions.

          Report:
          ```
          OUTCOMES + BACKLOG COMPLETE
          ===========================
          Files:
          - {{project_path}}/docs/OUTCOMES.md [Created / Updated]
          - {{project_path}}/docs/BACKLOG.md [Created / Updated]

          Outcomes defined: [count]
          Active backlog items: [count]
          Up next items: [count]
          Done items: [count]
          ```
```

**Step 2: Verify YAML parses**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
python3 -c "import yaml; yaml.safe_load(open('recipes/doc-driven-setup.yaml')); print('YAML parses OK')"
```

Expected: `YAML parses OK`

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add recipes/doc-driven-setup.yaml && git commit -m "feat: recipe Stage 3 (Outcomes + Backlog) -- create or update both docs"
```

---

### Task 14: Write Stage 4 (Project Context) prompt

This stage creates AGENTS.md at the project root. It summarizes everything created in the previous stages into the "read me first" file.

**Files:**
- Modify: `recipes/doc-driven-setup.yaml` (replace the project-context placeholder)

**Step 1: Replace the project-context step placeholder**

In `recipes/doc-driven-setup.yaml`, find the `create-agents-md` step and replace its placeholder prompt:

```yaml
        prompt: |
          Create the AGENTS.md project context file.

          ## Context
          - Project: {{project_name}}
          - Description: {{project_description}}
          - Path: {{project_path}}
          - Discovery: {{discovery_result}}
          - Vision: {{vision_result}}
          - Outcomes + Backlog: {{outcomes_backlog_result}}

          ## Template

          Read the template for the target structure:
          `@doc-driven-dev:templates/AGENTS_TEMPLATE.md`

          ## Instructions

          Create AGENTS.md at the project root (NOT in docs/). This is the first file any AI session reads.

          Fill in each section using information from the previous stages:

          - **What This Is**: Use the project description and vision summary.
          - **Current Focus**: What's in the Active section of BACKLOG.md.
          - **Key Decisions**: Any significant decisions made during this setup (e.g., "We chose to focus on X outcome first because..."). If greenfield, this may be empty.
          - **Project Structure**: Run `find {{project_path}} -maxdepth 2 -type d | head -20` and summarize.
          - **Docs**: Link to the 3 living docs. Adjust the relative paths based on where AGENTS.md lives (project root) vs where the docs live (docs/ subdirectory).
          - **How We Work**: Note any conventions mentioned during the vision/outcomes conversation.

          ## Output

          Write to: `{{project_path}}/AGENTS.md`

          Use today's date for `last_updated` and the user's name for `updated_by`.
          Remove all placeholder text and parenthetical instructions.

          Then provide the final setup summary:

          ```
          DOC-DRIVEN SETUP COMPLETE
          =========================
          Project: {{project_name}}
          Location: {{project_path}}

          Files Created:
          - {{project_path}}/AGENTS.md (read me first)
          - {{project_path}}/docs/VISION.md
          - {{project_path}}/docs/OUTCOMES.md
          - {{project_path}}/docs/BACKLOG.md

          Next Steps:
          1. Review each doc and refine anything that doesn't feel right
          2. Start working -- the docs are your alignment layer
          3. Run health checks periodically: load_skill(skill_name="health-check")
          4. Keep BACKLOG.md updated as you ship work
          ```
```

**Step 2: Verify YAML parses**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
python3 -c "import yaml; yaml.safe_load(open('recipes/doc-driven-setup.yaml')); print('YAML parses OK')"
```

Expected: `YAML parses OK`

**Step 3: Validate the full recipe with Amplifier**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
cat recipes/doc-driven-setup.yaml | python3 -c "
import yaml, sys
data = yaml.safe_load(sys.stdin)
assert data['name'] == 'doc-driven-setup', f'Wrong name: {data[\"name\"]}'
assert data['version'] == '2.0.0', f'Wrong version: {data[\"version\"]}'
assert len(data['stages']) == 4, f'Expected 4 stages, got {len(data[\"stages\"])}'
stage_names = [s['name'] for s in data['stages']]
assert stage_names == ['discovery', 'vision', 'outcomes-backlog', 'project-context'], f'Wrong stages: {stage_names}'
print(f'Recipe validates: {data[\"name\"]} v{data[\"version\"]}')
print(f'Stages: {stage_names}')
for s in data['stages']:
    has_approval = 'approval' in s
    step_count = len(s.get('steps', []))
    print(f'  - {s[\"name\"]}: {step_count} step(s), approval={has_approval}')
print('ALL CHECKS PASS')
"
```

Expected output:
```
Recipe validates: doc-driven-setup v2.0.0
Stages: ['discovery', 'vision', 'outcomes-backlog', 'project-context']
  - discovery: 1 step(s), approval=False
  - vision: 1 step(s), approval=True
  - outcomes-backlog: 1 step(s), approval=True
  - project-context: 1 step(s), approval=False
ALL CHECKS PASS
```

**Step 4: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add recipes/doc-driven-setup.yaml && git commit -m "feat: recipe Stage 4 (Project Context) -- create AGENTS.md

Full v2 recipe complete:
- Stage 1: Discovery (detect greenfield/undocumented/stale)
- Stage 2: Vision (create/update VISION.md)
- Stage 3: Outcomes + Backlog (create/update OUTCOMES.md + BACKLOG.md)
- Stage 4: Project Context (create AGENTS.md)"
```

---

## Phase 5: Skills

### Task 15: Delete session-close skill and create health-check skill

The session-close skill is moving to lifeos (separate effort). It's replaced by the health check skill -- the mechanism that keeps the 3 living docs honest.

**Files:**
- Delete: `skills/session-close.md`
- Create: `skills/health-check.md`

**Step 1: Delete the old skill**

```bash
rm /Users/chrispark/Projects/amplifier-doc-driven-dev/skills/session-close.md
```

**Step 2: Create `skills/health-check.md`**

Create the file with this exact content:

```markdown
---
name: health-check
description: >
  Run a health check on your project's alignment docs. Reads VISION.md,
  OUTCOMES.md, BACKLOG.md, and recent git history, then updates the docs
  to reflect current reality. Use after PRs, periodically, or when
  something feels off.
version: 2.0.0
---

# Health Check

Audit the project's alignment docs against reality. Update facts automatically. Flag judgments for humans.

## When to Run

- After merging a PR
- Periodically (daily if pushing frequently)
- When something feels off ("are we still aligned?")
- At the start of a new session to orient yourself

## Process

### Step 1: Read Current State

Read all alignment docs and recent git history:

```bash
cat AGENTS.md
cat docs/VISION.md
cat docs/OUTCOMES.md
cat docs/BACKLOG.md
git log --oneline --since="$(grep 'last_updated' docs/BACKLOG.md | head -1 | sed 's/.*: //')" 2>/dev/null || git log --oneline -20
```

Note the `last_updated` dates in each file's frontmatter. Check git history since those dates.

### Step 2: Backlog Update (High Confidence -- Auto-update)

Compare recent commits/PRs against the Active and Up Next sections:

- **Move completed items to Done.** Add:
  - `Completed` date (today)
  - `Driven By` (human or AI -- check commit authors)
  - `Learnings` (brief note on what was learned, if anything)
- **Add missing items.** If commits show work that isn't in the backlog, add it to Done with a note: "Not in original backlog -- discovered from git history."
- **Update Active statuses.** If something in Active is clearly done or blocked, update it.

### Step 3: Outcomes Update (Medium-High Confidence -- Auto-update)

For each outcome in the table:

- Update `Status` based on what's been shipped (use simple values: Not Started / In Progress / Shipped)
- Update `Last Checked` to today's date
- Update the **Current Assessment** summary (1-2 sentences on overall trajectory)

Add a note in the Notes section if any status changed: "Shifted from X to Y because..."

### Step 4: Vision Drift Check (Medium Confidence -- Flag Only)

Compare recent work against VISION.md:

- **Non-Goals:** Does any recent work contradict a Non-Goal? If so, **flag it to the human** -- do NOT auto-fix.
- **Principles:** Does any recent work violate a stated principle? Flag it.
- **Problem/Solution:** Has the project's direction shifted from the original problem statement? Flag it.

If drift is detected, present it clearly:
```
VISION DRIFT DETECTED
- Non-Goal says "no mobile" but PR #47 adds mobile auth
- Principle says "simplicity over features" but last 5 PRs added edge-case features

Question: Should we update the vision or course-correct the work?
```

### Step 5: AGENTS.md Update (Medium Confidence -- Semi-auto)

- Update **Current Focus** to match what's in the Active backlog section
- Update **Key Decisions** if any significant decisions were made (may need human input)

### Step 6: Update Frontmatter

For every doc that was modified:
- Set `last_updated` to today's date (YYYY-MM-DD)
- Set `updated_by` to whoever ran the health check

### Step 7: Report

End with a confidence summary so the human knows exactly what was done:

```
HEALTH CHECK COMPLETE
=====================

Confident (auto-updated):
- [list of factual changes made]

Uncertain (needs human review):
- [list of ambiguous items]

Not Checked:
- [anything that couldn't be verified]

Vision Drift:
- [any flags, or "None detected"]
```
```

**Step 3: Verify the skill file**

Run:
```bash
ls skills/
cat skills/health-check.md | head -10
```

Expected: Only `health-check.md` in `skills/`. The first 10 lines should show the YAML frontmatter with `name: health-check` and `description`.

**Step 4: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add -A && git commit -m "feat: replace session-close with health-check skill

Health check reads VISION.md, OUTCOMES.md, BACKLOG.md + git history.
Updates facts automatically, flags judgments for humans.
Reports confidence levels: confident / uncertain / not checked.

Session-close discipline will move to lifeos (separate effort)."
```

---

## Phase 6: Documentation

### Task 16: Rewrite README.md

The v1 README describes a "documentation scaffolding tool" with 3 tiers, 5 stages, session-close discipline, and epic generation. The v2 README frames it as an "alignment system for human-AI collaboration" with 3 living docs, 4 stages, and a health check.

**Files:**
- Modify: `README.md`

**Step 1: Replace `README.md`**

Overwrite the entire file with this exact content:

```markdown
# amplifier-doc-driven-dev

You build fast with AI. The AI does most of the work -- you provide direction, feedback, and judgment. Three weeks in, you open the project and can't tell if what's been built matches what you intended. The AI doesn't know either.

amplifier-doc-driven-dev is an alignment system for human-AI collaboration. It creates 3 living documents that answer the questions you actually need answered mid-project:

| Question | Doc |
|----------|-----|
| Is what we're building still what we set out to build? | **VISION.md** |
| Is work accruing to something measurable? | **OUTCOMES.md** |
| What's built, what's not, what's next? | **BACKLOG.md** |

Plus **AGENTS.md** at the project root -- a static context file every AI session reads first.

## How it works

Run the setup recipe once per project. It walks you through a conversational setup:

1. **Discovery** -- detects if your project is greenfield, undocumented, or has stale docs
2. **Vision** -- interviews you (or validates existing docs) to create VISION.md
3. **Outcomes + Backlog** -- defines measurable outcomes and initial backlog
4. **Project Context** -- creates AGENTS.md linking everything together

Then use the **health check** periodically to keep docs honest:

```
load_skill(skill_name="health-check")
```

The health check reads your docs + git history, updates facts (backlog items completed, outcome statuses), and flags judgment calls (vision drift) for you to decide on.

## The 80/20 principle

Docs are 80% for AI context, 20% for human confidence. Every doc has a summary at the top you can glance at, with detail below for the AI. You scan summaries to confirm alignment. The AI reads everything to make good autonomous decisions.

## Quick start

```bash
amplifier bundle add git+https://github.com/cpark4x/amplifier-doc-driven-dev@main
```

Then in any Amplifier session:

*"Run doc-driven-setup for my project"*

## What's in the bundle

| Piece | Purpose |
|-------|---------|
| **Setup recipe** | 4-stage conversational flow that creates the alignment docs |
| **4 templates** | Lean skeletons for VISION, OUTCOMES, BACKLOG, AGENTS |
| **Health check skill** | Periodic audit that reads docs + git history and updates them |
| **System instructions** | Context injected into sessions explaining the alignment system |

## Built by

[Chris Park](https://www.linkedin.com/in/chrispark) -- Microsoft Office of the CTO, AI Incubation.
```

**Step 2: Verify**

Run:
```bash
wc -l README.md
```

Expected: around 60-65 lines (v1 was 46 lines but the content is completely different now).

**Step 3: Commit**

```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add README.md && git commit -m "docs: rewrite README for v2 -- alignment system framing

Replaces documentation scaffolding framing with alignment system
for human-AI collaboration. Covers: 3 living docs, AGENTS.md,
setup recipe (4 stages, 3 project states), health check skill,
80/20 principle. Removes all references to tiers, epics, user
stories, and session-close."
```

---

## Final Verification

### Task 17: Verify the complete v2 bundle structure

**Step 1: Check the file structure matches the target**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
find . -type f -not -path './.git/*' | sort
```

Expected output (exactly these files):
```
./README.md
./behaviors/doc-driven-dev.yaml
./bundle.md
./context/instructions.md
./docs/plans/2026-03-24-doc-driven-dev-v2-design.md
./docs/plans/2026-03-24-doc-driven-dev-v2-implementation.md
./recipes/doc-driven-setup.yaml
./skills/health-check.md
./templates/AGENTS_TEMPLATE.md
./templates/BACKLOG_TEMPLATE.md
./templates/OUTCOMES_TEMPLATE.md
./templates/VISION_TEMPLATE.md
```

If you see any v1 files (bundle.yaml, session-close.md, session-close-reminder.md, EPIC_TEMPLATE.md, USER_STORY_TEMPLATE.md, SUCCESS_METRICS_TEMPLATE.md, PRINCIPLES_TEMPLATE.md, doc-driven-setup-fast.yaml), something was missed.

**Step 2: Verify no v1 references remain**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
grep -r "structure_tier\|lean.*standard.*full\|epic\|user.story\|session-close\|templates_path\|/Users/chrispark/Projects/toolkit" --include="*.yaml" --include="*.md" . --exclude-dir=.git --exclude-dir=docs/plans 2>/dev/null | grep -v "TEMPLATE" | grep -v "health-check"
```

Expected: No output (or very few false positives). There should be no references to:
- `structure_tier`, `lean/standard/full` tiers
- `epic` or `user story` as doc types (the word "epic" may appear in natural language, that's fine)
- `session-close` (except in the design doc which we don't touch)
- `templates_path` or hardcoded local paths

**Step 3: Verify recipe YAML**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
python3 -c "
import yaml
data = yaml.safe_load(open('recipes/doc-driven-setup.yaml'))
print(f'Name: {data[\"name\"]}')
print(f'Version: {data[\"version\"]}')
print(f'Stages: {len(data[\"stages\"])}')
for s in data['stages']:
    print(f'  - {s[\"name\"]}')
# Check no hardcoded paths
content = open('recipes/doc-driven-setup.yaml').read()
assert '/Users/chrispark/Projects/toolkit' not in content, 'Hardcoded path found!'
assert 'structure_tier' not in content, 'Old tier reference found!'
print('No hardcoded paths or old references. PASS')
"
```

Expected:
```
Name: doc-driven-setup
Version: 2.0.0
Stages: 4
  - discovery
  - vision
  - outcomes-backlog
  - project-context
No hardcoded paths or old references. PASS
```

**Step 4: Verify bundle.md frontmatter**

Run:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
python3 -c "
import yaml
with open('bundle.md') as f:
    content = f.read()
# Extract YAML between --- markers
parts = content.split('---')
frontmatter = yaml.safe_load(parts[1])
print(f'Bundle name: {frontmatter[\"bundle\"][\"name\"]}')
print(f'Bundle version: {frontmatter[\"bundle\"][\"version\"]}')
includes = frontmatter.get('includes', [])
print(f'Includes: {len(includes)} bundles')
for inc in includes:
    print(f'  - {inc[\"bundle\"]}')
print('PASS')
"
```

Expected:
```
Bundle name: doc-driven-dev
Bundle version: 2.0.0
Includes: 2 bundles
  - git+https://github.com/microsoft/amplifier-foundation@main
  - doc-driven-dev:behaviors/doc-driven-dev
PASS
```

**Step 5: Final commit (if any verification fixes were needed)**

If all checks pass with no changes needed:
```bash
echo "All verification checks passed. v2 bundle is complete."
```

If fixes were needed, commit them:
```bash
cd /Users/chrispark/Projects/amplifier-doc-driven-dev
git add -A && git commit -m "fix: address issues found during final verification"
```

---

## Out of Scope (Future Work)

These items were explicitly deferred during design:

1. **Lifeos session-close migration** -- Move the session-close protocol to `~/.lifeos/memory/_protocols/session-close.md`. Separate effort.
2. **Health check as CI step** -- Automate post-merge via GitHub Actions. Not V1.
3. **Superpowers integration** -- Should the setup recipe integrate with brainstorm mode? Revisit after testing.
4. **Fast recipe variant** -- Single recipe for V1. Add fast mode later if needed.
5. **Multi-person repo testing** -- Attribution column (Driven By) helps, but real multi-person usage needs testing.
6. **AGENTS.md Key Decisions pruning** -- When does the list get too long? Solve when it's a problem.
7. **Backlog archiving** -- When does the Done section get unwieldy? Solve when it's a problem.