# amplifier-doc-driven-dev

You build fast with AI. Three weeks later, no one can explain why the caching layer uses Redis instead of Memcached, or why the API is REST instead of GraphQL. The AI that made those choices didn't write down the reasoning. The next AI that touches the code won't know either.

amplifier-doc-driven-dev fixes this by making documentation the first step, not the last. A conversational recipe interviews you about the vision, problems, and audience, then scaffolds a complete docs structure that both humans and AI can reference from day one.

## What you get

Run `"run doc-driven-setup for my new project"` in an Amplifier session. A 5-stage conversational setup walks you through:

1. **Discovery** — project name, description, structure tier
2. **Structure** — creates the docs directory with templates
3. **Vision** — interviews you, writes `VISION.md` (problems, positioning, V1/V2/V3 roadmap)
4. **First epic** — interviews you, writes the first epic spec
5. **Navigation** — creates a `docs/README.md` hub linking everything together

Three tiers to match your project's size:

| Tier | For | What you get |
|------|-----|-------------|
| **lean** | Small tools | Vision + epics + templates |
| **standard** | Medium projects | + principles, success metrics, backlog |
| **full** | Large projects | + technical docs, guides, design, research |

## The session-close discipline

Documentation drift happens because "later" never comes. Every session auto-reminds you: before ending, run the session-close checklist. Two minutes:

- Uncommitted changes? Commit and push.
- Epics that shipped but still show "In Progress"? Update them.
- Backlog reflect what was built? Update it.
- Unpushed commits? Push them.

## Quick start

```bash
amplifier bundle add git+https://github.com/cpark4x/amplifier-doc-driven-dev@main
```

Then in any Amplifier session:

*"Run doc-driven-setup for my new project"*

## Built by

[Chris Park](https://www.linkedin.com/in/chrispark) — Microsoft Office of the CTO, AI Incubation. Building the tools he actually uses.
