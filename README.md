# amplifier-doc-driven-dev

[Amplifier](https://github.com/microsoft/amplifier) recipes and templates for doc-driven development.

## What is Doc-Driven Development?

A documentation-first approach where you define the "why" and "what" before the "how":

1. **Vision first** - Define problems before solutions
2. **Epics describe WHAT** - User-focused, not technical
3. **User stories for IMPLEMENTED features only** - No speculative docs
4. **Templates ensure consistency** - Same structure across projects

## Quick Start

```bash
# In an Amplifier session
"run doc-driven-setup for my new project"

# Or with full context
amplifier tool invoke recipes operation=execute \
  recipe_path=~/Projects/toolkit/recipes/doc-driven-setup.yaml \
  context='{"project_path": "/path/to/project", "project_name": "my-project"}'
```

## Recipes

| Recipe | Description |
|--------|-------------|
| `doc-driven-setup.yaml` | Interactive setup with approval gates |
| `doc-driven-setup-fast.yaml` | Fast setup, no approval gates |

## Templates

| Template | Purpose |
|----------|---------|
| `VISION_TEMPLATE.md` | Problems, positioning, V1/V2/V3 roadmap |
| `EPIC_TEMPLATE.md` | User-focused epic specification |
| `USER_STORY_TEMPLATE.md` | For implemented features only |
| `PRINCIPLES_TEMPLATE.md` | Decision framework for trade-offs |
| `SUCCESS_METRICS_TEMPLATE.md` | How to measure success |
| `BACKLOG_TEMPLATE.md` | Strategic planning view — epics, priorities, sprint status |

## Structure Tiers

The recipe supports three documentation tiers based on project size:

| Tier | Use For | Structure |
|------|---------|-----------|
| **lean** | Small tools (murmur) | 01-vision, 02-requirements/epics, templates |
| **standard** | Medium projects | + PRINCIPLES, SUCCESS-METRICS, user-stories, BACKLOG |
| **full** | Large projects (workspaces2) | + BACKLOG, 03-technical, 04-guides, 05-design, 06-research |

## Related Tools

Part of the cpark4x Amplifier tool collection:

- **amplifier-doc-driven-dev** (this repo) - Doc-driven development
- **amplifier-session-insights** - Session analysis and insights
- **murmur** - Local speech-to-text

## License

MIT
