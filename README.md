# amplifier-doc-driven-dev

Amplifier recipes and templates for doc-driven development — a documentation-first approach where you define the "why" and "what" before the "how."

Used across all cpark4x projects. The discipline that keeps AI-generated code aligned with product intent.

## What is Doc-Driven Development?

1. **Vision first** — define the problem before the solution
2. **Epics describe WHAT** — user-focused, not technical
3. **User stories for implemented features only** — no speculative docs
4. **Templates ensure consistency** — same structure across every project

## Quick Start

```bash
# In any Amplifier session
"run doc-driven-setup for my new project"

# Or invoke directly
amplifier tool invoke recipes operation=execute \
  recipe_path=git+https://github.com/cpark4x/amplifier-doc-driven-dev@main#subdirectory=recipes/doc-driven-setup.yaml \
  context='{"project_path": "/path/to/project", "project_name": "my-project"}'
```

## Recipes

| Recipe | Description |
|---|---|
| `doc-driven-setup.yaml` | Interactive setup with approval gates |
| `doc-driven-setup-fast.yaml` | Fast setup, no approval gates |

## Templates

| Template | Purpose |
|---|---|
| `VISION_TEMPLATE.md` | Problems, positioning, V1/V2/V3 roadmap |
| `EPIC_TEMPLATE.md` | User-focused epic specification |
| `USER_STORY_TEMPLATE.md` | For implemented features only |
| `PRINCIPLES_TEMPLATE.md` | Decision framework for trade-offs |
| `SUCCESS_METRICS_TEMPLATE.md` | How to measure success |
| `BACKLOG_TEMPLATE.md` | Strategic planning — epics, priorities, sprint status |

## Structure Tiers

Three documentation tiers based on project size:

| Tier | Use For | Structure |
|---|---|---|
| **lean** | Small tools | 01-vision, 02-requirements/epics, templates |
| **standard** | Medium projects | + PRINCIPLES, SUCCESS-METRICS, user-stories, BACKLOG |
| **full** | Large projects | + 03-technical, 04-guides, 05-design, 06-research |

The recipe asks which tier during setup.

## Related

Part of the cpark4x Amplifier tool collection:

- **amplifier-doc-driven-dev** (this repo) — doc-driven development recipes and templates
- **[amplifier-session-capture](https://github.com/cpark4x/amplifier-session-capture)** — per-session AI collaboration insights
- **[amplifier-usage-insights](https://github.com/cpark4x/amplifier-usage-insights)** — weekly aggregate analytics

---

## Built by

**Chris Park** — Senior PM, Microsoft Office of the CTO, AI Incubation group.
Engineering degree from Waterloo. 17 years shipping product.

[LinkedIn](https://www.linkedin.com/in/chrispark1/) · [GitHub](https://github.com/cpark4x)

---

MIT License
