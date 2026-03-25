# doc-driven-dev

An alignment system for human-AI collaboration.

When AI does most of the building, work accumulates fast. Three weeks in, no one can explain why the caching layer uses Redis instead of Memcached, whether the project is actually on track, or what was decided last Tuesday. The AI that made those choices didn't write down the reasoning. The next AI that touches the code won't know either.

doc-driven-dev keeps humans and AI aligned by maintaining four living documents that answer the only questions that matter mid-project:

| Question | Document |
|----------|----------|
| Is what we're building still what we set out to build? | **VISION.md** |
| Is the work accruing to something measurable? | **OUTCOMES.md** |
| What's built, what's not, what's next? | **BACKLOG.md** |
| What does a new AI session need to know first? | **AGENTS.md** |

## Three project states, one recipe

The setup recipe detects your project's state and adapts:

| State | What happens |
|-------|-------------|
| **Greenfield** -- no docs, no code | Interviews you, creates all 4 docs from scratch |
| **Undocumented** -- existing code, no alignment docs | Reads the codebase first, creates docs that reflect what exists |
| **Stale** -- docs exist but drifted | Reads existing docs + codebase, updates to reflect current reality |

## The health check

Docs drift because "later" never comes. The health check skill audits alignment on demand:

1. Reads all 4 docs + recent git history
2. Updates BACKLOG.md with completed work (auto)
3. Updates OUTCOMES.md statuses (auto)
4. Flags vision drift against non-goals and principles (human decision)
5. Updates AGENTS.md current focus (auto)
6. Reports with confidence levels -- what it's sure about, what needs human review

Run it after merging a PR: `load_skill(skill_name="health-check")`

## Quick start

```bash
amplifier bundle add git+https://github.com/cpark4x/amplifier-doc-driven-dev@main
```

Then in any Amplifier session:

```
"run doc-driven-setup"
```

The 4-stage recipe walks you through discovery, vision, outcomes + backlog, and project context -- with approval gates between each stage.

## The 80/20 principle

Docs are **80% for AI context, 20% for human confidence**. Every doc has a summary at the top (the human glance layer) and detail below (the AI context layer). The human reads summaries to confirm alignment. The AI reads everything to make good autonomous decisions.

## Built by

[Chris Park](https://www.linkedin.com/in/chrispark) -- Microsoft Office of the CTO, AI Incubation. Building the tools he actually uses.
