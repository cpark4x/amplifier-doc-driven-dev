# Doc-Driven Development: Alignment System

You are operating in a **doc-driven development** session. This system keeps humans and AI aligned across every session by treating documentation as the primary source of truth.

## The Alignment System

Four documents answer the four questions that matter most for every decision made in this project:

| Alignment Question | Document |
|--------------------|----------|
| Why does this project exist and what does success look like? | `VISION.md` |
| What measurable outcomes are we driving toward? | `OUTCOMES.md` |
| What work is in scope, prioritized, and in progress? | `BACKLOG.md` |
| How is this project structured and how do we work in it? | `AGENTS.md` |

Before taking action, locate the answer in one of these documents. If the answer is missing, surface the gap rather than guessing.

## The 80/20 Principle

These documents are written **80% for AI context, 20% for human confidence**.

- **80% for AI**: Dense, structured, unambiguous. Written so an AI can restore full project context in a single read without needing to ask clarifying questions.
- **20% for human confidence**: Readable enough that a human can scan and trust that the AI has what it needs.

This means: prefer completeness over brevity, precision over prose, and facts over interpretation.

## How to Work With These Docs

### At start of session

1. Read `VISION.md` to understand why this project exists and what done looks like.
2. Read `OUTCOMES.md` to understand the measurable targets currently in play.
3. Read `BACKLOG.md` to understand what is in scope and what is next.
4. Read `AGENTS.md` if the work involves multiple roles or agents.
5. If any of these files are missing, surface the gap and offer to create them using the `doc-driven-setup` recipe.

### During work

- Every decision you make should be traceable to one of the four documents.
- If a decision requires information not in the docs, note it — it belongs in the relevant document before the session closes.
- When scope creep appears, consult `VISION.md` non-goals and `BACKLOG.md` priorities before proceeding.
- Update docs in place as you learn — don't defer to "clean up later."

### Health check

Use this checklist to verify alignment before closing a session:

- [ ] Does `BACKLOG.md` reflect what was actually built?
- [ ] Are active backlog items updated with current status?
- [ ] Did any decisions surface that belong in `VISION.md` or `OUTCOMES.md`?
- [ ] Are all learnings recorded inline (not deferred)?
- [ ] Is attribution clear for any AI-generated content?

## Rules

**Rule 1: Update facts automatically; flag judgments for humans.**
Facts (status changes, file paths, completed tasks) can be updated without asking. Judgments (priority changes, scope decisions, outcome targets) must be flagged to a human before updating.

**Rule 2: Every backlog item must connect to an outcome.**
A task without an outcome connection is undirected effort. Before adding or working on a backlog item, confirm it traces to a measurable outcome in `OUTCOMES.md`.

**Rule 3: Non-Goals are boundaries, not suggestions.**
Non-goals defined in `VISION.md` and scope boundaries recorded in `BACKLOG.md` are hard constraints. Do not work around them, suggest alternatives that violate them, or treat them as negotiable without explicit human approval.

**Rule 4: Learnings are inline, not separate.**
Discoveries, corrections, and context updates belong in the document they affect — not in a separate "learnings" file or deferred to the end of the session. Inline learnings compound; separate files decay.

**Rule 5: Attribution matters.**
When AI generates content that will persist (decisions, rationale, doc updates), note that it was AI-generated. This preserves human confidence that docs reflect real understanding, not fabricated consensus.
