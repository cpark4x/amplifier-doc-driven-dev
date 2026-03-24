---
bundle:
  name: doc-driven-dev-behavior
  version: "2.0.0"
  description: Core doc-driven-dev behavior — session-open doc check, session-close discipline, and decision-logging habits

behaviors:
  - name: session-open-doc-check
    description: At session start, check for VISION.md and BACKLOG.md and offer setup if missing
  - name: session-close-discipline
    description: Before session end, run the session-close checklist to prevent documentation drift
  - name: decision-logging
    description: Log architectural decisions in context rather than leaving them implicit
---

# Doc-Driven Dev Behavior

This behavior bundle injects the doc-driven-dev working habits into every session.

## session-open-doc-check

At the start of a session, check whether the project has:
- `docs/VISION.md` — the *why* behind the project
- `docs/BACKLOG.md` — the *what* in scope

If either is missing, offer to run the `doc-driven-setup` recipe to scaffold them.

## session-close-discipline

Before ending any session, prompt:

> Run `load_skill(skill_name="session-close")` to check for doc drift.

This takes two minutes and prevents the common pattern of undocumented decisions accumulating across sessions.

## decision-logging

When making a significant technical decision (architecture, data model, API shape), note it inline:

> "I chose X over Y because [reason]. This is captured in `docs/epics/[epic].md`."

This keeps future sessions — and future collaborators — from re-litigating settled decisions.
