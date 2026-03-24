"""
Tests for task-6: Rewrite VISION_TEMPLATE.md as lean v2 skeleton.

Acceptance criteria:
- wc -l shows around 30 lines (not 329)
- File has YAML frontmatter (last_updated, updated_by)
- 6 sections: Summary, Problem, Solution, Non-Goals, Who It's For, Principles
- No writing guidelines, table of contents, or competitive analysis
"""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "VISION_TEMPLATE.md")


def _read_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()


def _count_lines():
    with open(TEMPLATE_PATH, "r") as f:
        return len(f.readlines())


def test_vision_template_exists():
    """The VISION_TEMPLATE.md file must exist."""
    assert os.path.isfile(TEMPLATE_PATH), "templates/VISION_TEMPLATE.md must exist"


def test_vision_template_is_lean():
    """Template must be around 30 lines, not the v1 329 lines."""
    line_count = _count_lines()
    assert line_count <= 40, (
        f"Template must be lean (~30 lines), but found {line_count} lines. "
        "Remove writing guidelines, table of contents, competitive analysis."
    )
    assert line_count >= 20, (
        f"Template must have at least 20 lines (6 sections + frontmatter), found {line_count}"
    )


def test_vision_template_has_yaml_frontmatter():
    """Template must start with YAML frontmatter block."""
    content = _read_template()
    assert content.startswith("---"), "Template must start with YAML frontmatter (---)"
    # Find the closing --- of frontmatter
    lines = content.splitlines()
    assert lines[0] == "---", "First line must be --- (YAML frontmatter open)"
    closing_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line == "---":
            closing_idx = i
            break
    assert closing_idx is not None, "Template must have closing --- for YAML frontmatter"


def test_vision_template_frontmatter_has_last_updated():
    """YAML frontmatter must contain last_updated field."""
    content = _read_template()
    assert "last_updated:" in content, (
        "YAML frontmatter must contain 'last_updated:' field"
    )


def test_vision_template_frontmatter_has_updated_by():
    """YAML frontmatter must contain updated_by field."""
    content = _read_template()
    assert "updated_by:" in content, (
        "YAML frontmatter must contain 'updated_by:' field"
    )


def test_vision_template_has_summary_section():
    """Template must have a Summary section."""
    content = _read_template()
    assert "## Summary" in content, "Template must have '## Summary' section"


def test_vision_template_has_problem_section():
    """Template must have a Problem section."""
    content = _read_template()
    assert "## Problem" in content, "Template must have '## Problem' section"


def test_vision_template_has_solution_section():
    """Template must have a Solution section."""
    content = _read_template()
    assert "## Solution" in content, "Template must have '## Solution' section"


def test_vision_template_has_non_goals_section():
    """Template must have a Non-Goals section."""
    content = _read_template()
    assert "## Non-Goals" in content, "Template must have '## Non-Goals' section"


def test_vision_template_has_who_its_for_section():
    """Template must have a 'Who It's For' section."""
    content = _read_template()
    assert "## Who It's For" in content, "Template must have \"## Who It's For\" section"


def test_vision_template_has_principles_section():
    """Template must have a Principles section."""
    content = _read_template()
    assert "## Principles" in content, "Template must have '## Principles' section"


def test_vision_template_no_writing_guidelines():
    """Template must NOT contain writing guidelines."""
    content = _read_template()
    assert "Writing Guidelines" not in content, (
        "Template must not contain writing guidelines — coaching lives in recipe prompts"
    )


def test_vision_template_no_table_of_contents():
    """Template must NOT contain a table of contents."""
    content = _read_template()
    assert "Table of Contents" not in content, (
        "Template must not contain a table of contents"
    )


def test_vision_template_no_competitive_analysis():
    """Template must NOT contain competitive analysis section."""
    content = _read_template()
    assert "Competitive" not in content, (
        "Template must not contain competitive analysis — this is a lean v2 skeleton"
    )


def test_vision_template_no_strategic_positioning():
    """Template must NOT contain strategic positioning section."""
    content = _read_template()
    assert "Strategic Positioning" not in content, (
        "Template must not contain strategic positioning section"
    )
