# cpark4x-toolkit

Personal collection of Amplifier recipes, bundles, skills, and templates for development workflows.

## Contents

### Bundles (`bundles/`)

Custom bundle configurations and behaviors.

| Bundle | Description |
|--------|-------------|
| `canvas-dev` | Development bundle for Canvas/Workspaces2 with outcome-driven patterns |

### Recipes (`recipes/`)

Reusable multi-step workflows.

| Recipe | Description |
|--------|-------------|
| `doc-driven-setup.yaml` | Bootstrap docs for new projects (interactive, with approval gates) |
| `doc-driven-setup-fast.yaml` | Bootstrap docs for new projects (fast, no approval gates) |
| `canvas-epic-workflow.yaml` | Complete epic development lifecycle following Canvas iteration philosophy |
| `canvas-verification.yaml` | Verification-driven development workflow |

### Templates (`templates/`)

Document templates for doc-driven development.

| Template | Description |
|----------|-------------|
| `VISION_TEMPLATE.md` | Project vision (problems, positioning, roadmap) |
| `EPIC_TEMPLATE.md` | Epic specification (user-focused) |
| `USER_STORY_TEMPLATE.md` | User story (for implemented features only) |
| `PRINCIPLES_TEMPLATE.md` | Decision framework for controversial choices |
| `SUCCESS_METRICS_TEMPLATE.md` | How to measure success |

### Skills (`skills/`)

Domain-specific knowledge and patterns for Canvas development.

| Skill | Description |
|-------|-------------|
| `canvas-philosophy` | Canvas development principles: outcome-driven, verification-first |
| `workspaces-patterns` | Common patterns for Workspaces2 architecture |

## Usage

### Using Bundles

Use the canvas-dev bundle directly from GitHub:

```bash
amplifier run --bundle git+https://github.com/cpark4x/cpark4x-toolkit@main:bundles/canvas-dev/bundle.md
```

Or set as default in `~/.amplifier/settings.yaml`:

```yaml
bundle: git+https://github.com/cpark4x/cpark4x-toolkit@main:bundles/canvas-dev/bundle.md
```

### Using Recipes

Reference recipes directly from GitHub:

```bash
amplifier recipes execute git+https://github.com/cpark4x/cpark4x-toolkit@main:recipes/canvas-epic-workflow.yaml \
  --context '{"epic_number": "12", "epic_name": "my-epic", "epic_path": "docs/02-requirements/epics/12-my-epic.md"}'
```

Or clone locally and reference by path.

### Using Skills

Skills are cognitive frameworks - reference them in your prompts:

```
"Using canvas-philosophy principles, implement the outcome definition UI"
"Apply workspaces-patterns to this agent chat feature"
```

## Quick Setup

```bash
# Clone locally
git clone https://github.com/cpark4x/cpark4x-toolkit.git
cd cpark4x-toolkit

# Set as your default bundle
echo "bundle: $(pwd)/bundles/canvas-dev/bundle.md" >> ~/.amplifier/settings.yaml
```

## Canvas Context

This toolkit is designed for working on:
- **Project:** Canvas (Workspaces 2.0)
- **Repo:** https://github.com/microsoft/workspaces2
- **Local:** ~/amplifier.workspaces2
- **Philosophy:** Outcome-driven development, verification-first iteration

## License

MIT
