# cpark4x Amplifier Toolkit

Personal [Amplifier](https://github.com/microsoft/amplifier) recipes, bundles, skills, and templates for doc-driven development workflows.

## Quick Start

```bash
# Clone locally
git clone https://github.com/cpark4x/cpark4x-toolkit.git ~/Projects/toolkit

# Run a recipe
"run doc-driven-setup from my toolkit"

# Or reference directly
amplifier tool invoke recipes operation=execute \
  recipe_path=~/Projects/toolkit/recipes/doc-driven-setup.yaml
```

## Contents

### Recipes (`recipes/`)

Multi-step Amplifier workflows with agent orchestration.

| Recipe | Description |
|--------|-------------|
| `doc-driven-setup.yaml` | Bootstrap docs for new projects (interactive, approval gates) |
| `doc-driven-setup-fast.yaml` | Bootstrap docs for new projects (fast, no gates) |
| `canvas-epic-workflow.yaml` | Epic development lifecycle for Canvas |
| `canvas-verification.yaml` | Verification-driven development workflow |

### Templates (`templates/`)

Document templates for doc-driven development pattern.

| Template | Purpose |
|----------|---------|
| `VISION_TEMPLATE.md` | Problems, positioning, V1/V2/V3 roadmap |
| `EPIC_TEMPLATE.md` | User-focused epic specification |
| `USER_STORY_TEMPLATE.md` | For implemented features only |
| `PRINCIPLES_TEMPLATE.md` | Decision framework for trade-offs |
| `SUCCESS_METRICS_TEMPLATE.md` | How to measure success |

### Bundles (`bundles/`)

Amplifier bundle configurations.

| Bundle | Description |
|--------|-------------|
| `canvas-dev` | Development bundle for Canvas/Workspaces2 |

### Skills (`skills/`)

Domain knowledge for Amplifier agents.

| Skill | Description |
|-------|-------------|
| `canvas-philosophy` | Outcome-driven, verification-first principles |
| `workspaces-patterns` | Common patterns for Workspaces2 |

## Doc-Driven Development

The core philosophy behind this toolkit:

1. **Vision first** - Define problems before solutions
2. **Epics describe WHAT** - User-focused, not technical
3. **User stories for IMPLEMENTED features only** - No speculative docs
4. **Templates ensure consistency** - Same structure across projects

### Structure Tiers

| Tier | Use For | Folders |
|------|---------|---------|
| **lean** | Small tools | 01-vision, 02-requirements/epics, templates |
| **standard** | Medium projects | + PRINCIPLES, SUCCESS-METRICS, user-stories |
| **full** | Large projects | + 03-technical, 04-guides, 05-design, 06-research |

## License

MIT
