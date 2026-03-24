# Doc-Driven Development — Session Instructions

You are operating in a **doc-driven development** session.

## What this means

Documentation is the first step, not the last. Before writing code, we write the *why*. Before closing a session, we update the docs. This keeps humans and AI aligned across every session.

## Your responsibilities

### At session start
- Check for `docs/VISION.md` and `docs/BACKLOG.md`. If they don't exist, offer to run the `doc-driven-setup` recipe.
- Read existing docs to restore context before touching code.

### During the session
- Treat `VISION.md` as the source of truth for *why* the project exists and what success looks like.
- Treat `BACKLOG.md` as the source of truth for *what* is in scope.
- When making decisions that aren't in the docs, note them — they belong in an ADR or the relevant epic.

### Before session close
- Run the `session-close` skill: `load_skill(skill_name="session-close")`
- Commit uncommitted changes.
- Update any epics that shipped from "In Progress" to done.
- Verify the backlog reflects what was actually built.

## The quick-start command

If the user says anything like *"set up docs for my project"* or *"run doc-driven-setup"*, execute the `doc-driven-setup` recipe. It will interview the user and scaffold everything.

## Philosophy

> Documentation drift happens because "later" never comes.

Every AI session that touches code without updating docs makes the next session harder. Two minutes of doc hygiene per session compounds into a codebase that stays understandable for months.
