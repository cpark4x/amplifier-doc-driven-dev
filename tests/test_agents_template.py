"""
Tests for task-9: Create AGENTS_TEMPLATE.md.

Acceptance criteria:
- cat templates/AGENTS_TEMPLATE.md shows correct content
- wc -l shows around 33 lines
- File has YAML frontmatter (last_updated, updated_by)
- 6 sections: What This Is, Current Focus, Key Decisions, Project Structure,
  Docs (with links to VISION.md, OUTCOMES.md, BACKLOG.md), How We Work
- Committed with message: 'feat: add lean AGENTS template for AI session orientation'
"""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "AGENTS_TEMPLATE.md")


def _read_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()


def _count_lines():
    with open(TEMPLATE_PATH, "r") as f:
        return len(f.readlines())


def test_agents_template_exists():
    """The AGENTS_TEMPLATE.md file must exist."""
    assert os.path.isfile(TEMPLATE_PATH), "templates/AGENTS_TEMPLATE.md must exist"


def test_agents_template_is_lean():
    """Template must be around 33 lines."""
    line_count = _count_lines()
    assert line_count <= 45, (
        f"Template must be lean (~33 lines), but found {line_count} lines."
    )
    assert line_count >= 25, (
        f"Template must have at least 25 lines (6 sections + frontmatter), "
        f"found {line_count}"
    )


def test_agents_template_has_yaml_frontmatter():
    """Template must start with YAML frontmatter block."""
    content = _read_template()
    assert content.startswith("---"), "Template must start with YAML frontmatter (---)"
    lines = content.splitlines()
    assert lines[0] == "---", "First line must be --- (YAML frontmatter open)"
    closing_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line == "---":
            closing_idx = i
            break
    assert closing_idx is not None, "Template must have closing --- for YAML frontmatter"


def test_agents_template_frontmatter_has_last_updated():
    """YAML frontmatter must contain last_updated field."""
    content = _read_template()
    assert "last_updated:" in content, (
        "YAML frontmatter must contain 'last_updated:' field"
    )


def test_agents_template_frontmatter_has_updated_by():
    """YAML frontmatter must contain updated_by field."""
    content = _read_template()
    assert "updated_by:" in content, (
        "YAML frontmatter must contain 'updated_by:' field"
    )


def test_agents_template_has_what_this_is_section():
    """Template must have a 'What This Is' section."""
    content = _read_template()
    assert "## What This Is" in content, (
        "Template must have '## What This Is' section"
    )


def test_agents_template_has_current_focus_section():
    """Template must have a 'Current Focus' section."""
    content = _read_template()
    assert "## Current Focus" in content, (
        "Template must have '## Current Focus' section"
    )


def test_agents_template_has_key_decisions_section():
    """Template must have a 'Key Decisions' section."""
    content = _read_template()
    assert "## Key Decisions" in content, (
        "Template must have '## Key Decisions' section"
    )


def test_agents_template_has_project_structure_section():
    """Template must have a 'Project Structure' section."""
    content = _read_template()
    assert "## Project Structure" in content, (
        "Template must have '## Project Structure' section"
    )


def test_agents_template_has_docs_section():
    """Template must have a 'Docs' section."""
    content = _read_template()
    assert "## Docs" in content, "Template must have '## Docs' section"


def test_agents_template_has_how_we_work_section():
    """Template must have a 'How We Work' section."""
    content = _read_template()
    assert "## How We Work" in content, (
        "Template must have '## How We Work' section"
    )


def test_agents_template_docs_links_vision():
    """Docs section must link to VISION.md with a relative path."""
    content = _read_template()
    assert "VISION.md" in content, (
        "Docs section must contain a link to VISION.md"
    )


def test_agents_template_docs_links_outcomes():
    """Docs section must link to OUTCOMES.md with a relative path."""
    content = _read_template()
    assert "OUTCOMES.md" in content, (
        "Docs section must contain a link to OUTCOMES.md"
    )


def test_agents_template_docs_links_backlog():
    """Docs section must link to BACKLOG.md with a relative path."""
    content = _read_template()
    assert "BACKLOG.md" in content, (
        "Docs section must contain a link to BACKLOG.md"
    )


def test_agents_template_has_six_sections():
    """Template must have exactly 6 ## sections."""
    content = _read_template()
    lines = content.splitlines()
    sections = [line for line in lines if line.startswith("## ")]
    assert len(sections) == 6, (
        f"Template must have exactly 6 ## sections, found {len(sections)}: {sections}"
    )
