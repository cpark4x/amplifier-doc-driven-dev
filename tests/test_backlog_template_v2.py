"""
Tests for task-7: Rewrite BACKLOG_TEMPLATE.md as lean v2 skeleton.

Acceptance criteria:
- wc -l shows around 27 lines (not 133)
- File has YAML frontmatter (last_updated, updated_by)
- 3 table sections: Active, Up Next, Done
- Done table has Driven By and Learnings columns
- No epic tracking, sprint planning, effort/impact scoring, emoji conventions
"""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "BACKLOG_TEMPLATE.md")


def _read_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()


def _count_lines():
    with open(TEMPLATE_PATH, "r") as f:
        return len(f.readlines())


def test_backlog_template_exists():
    """The BACKLOG_TEMPLATE.md file must exist."""
    assert os.path.isfile(TEMPLATE_PATH), "templates/BACKLOG_TEMPLATE.md must exist"


def test_backlog_template_is_lean():
    """Template must be around 27 lines, not the v1 133 lines."""
    line_count = _count_lines()
    assert line_count <= 40, (
        f"Template must be lean (~27 lines), but found {line_count} lines. "
        "Remove epic tracking, sprint planning, effort/impact scoring."
    )
    assert line_count >= 20, (
        f"Template must have at least 20 lines (3 table sections + frontmatter), "
        f"found {line_count}"
    )


def test_backlog_template_has_yaml_frontmatter():
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


def test_backlog_template_frontmatter_has_last_updated():
    """YAML frontmatter must contain last_updated field."""
    content = _read_template()
    assert "last_updated:" in content, (
        "YAML frontmatter must contain 'last_updated:' field"
    )


def test_backlog_template_frontmatter_has_updated_by():
    """YAML frontmatter must contain updated_by field."""
    content = _read_template()
    assert "updated_by:" in content, (
        "YAML frontmatter must contain 'updated_by:' field"
    )


def test_backlog_template_has_summary_section():
    """Template must have a Summary section."""
    content = _read_template()
    assert "## Summary" in content, "Template must have '## Summary' section"


def test_backlog_template_has_active_section():
    """Template must have an Active table section."""
    content = _read_template()
    assert "## Active" in content, "Template must have '## Active' section"


def test_backlog_template_has_up_next_section():
    """Template must have an Up Next table section."""
    content = _read_template()
    assert "## Up Next" in content, "Template must have '## Up Next' section"


def test_backlog_template_has_done_section():
    """Template must have a Done table section."""
    content = _read_template()
    assert "## Done" in content, "Template must have '## Done' section"


def test_active_table_has_item_column():
    """Active table must have an Item column."""
    content = _read_template()
    assert "Item" in content, "Active table must have 'Item' column"


def test_active_table_has_drives_outcome_column():
    """Active table must have a Drives Outcome column."""
    content = _read_template()
    assert "Drives Outcome" in content, "Active table must have 'Drives Outcome' column"


def test_active_table_has_status_column():
    """Active table must have a Status column."""
    content = _read_template()
    # Check that Status appears in a table context (after Active heading)
    active_idx = content.find("## Active")
    up_next_idx = content.find("## Up Next")
    active_section = content[active_idx:up_next_idx]
    assert "Status" in active_section, "Active table must have 'Status' column"


def test_active_table_has_assigned_column():
    """Active table must have an Assigned column."""
    content = _read_template()
    active_idx = content.find("## Active")
    up_next_idx = content.find("## Up Next")
    active_section = content[active_idx:up_next_idx]
    assert "Assigned" in active_section, "Active table must have 'Assigned' column"


def test_up_next_table_has_priority_column():
    """Up Next table must have a Priority column."""
    content = _read_template()
    up_next_idx = content.find("## Up Next")
    done_idx = content.find("## Done")
    up_next_section = content[up_next_idx:done_idx]
    assert "Priority" in up_next_section, "Up Next table must have 'Priority' column"


def test_done_table_has_driven_by_column():
    """Done table must have a Driven By column for accountability."""
    content = _read_template()
    done_idx = content.find("## Done")
    done_section = content[done_idx:]
    assert "Driven By" in done_section, (
        "Done table must have 'Driven By' column for accountability"
    )


def test_done_table_has_learnings_column():
    """Done table must have a Learnings column for accountability."""
    content = _read_template()
    done_idx = content.find("## Done")
    done_section = content[done_idx:]
    assert "Learnings" in done_section, (
        "Done table must have 'Learnings' column for accountability"
    )


def test_done_table_has_completed_column():
    """Done table must have a Completed column."""
    content = _read_template()
    done_idx = content.find("## Done")
    done_section = content[done_idx:]
    assert "Completed" in done_section, "Done table must have 'Completed' column"


def test_no_epic_tracking():
    """Template must NOT contain epic tracking."""
    content = _read_template()
    assert "Epic" not in content, (
        "Template must not contain epic tracking — lean v2 removes this"
    )


def test_no_sprint_planning():
    """Template must NOT contain sprint planning sections."""
    content = _read_template()
    assert "Sprint" not in content, (
        "Template must not contain sprint planning — lean v2 removes this"
    )


def test_no_effort_impact_scoring():
    """Template must NOT contain effort/impact scoring."""
    content = _read_template()
    assert "Effort" not in content, (
        "Template must not contain effort/impact scoring — lean v2 removes this"
    )
    assert "Impact" not in content, (
        "Template must not contain impact scoring — lean v2 removes this"
    )


def test_no_emoji_conventions():
    """Template must NOT contain emoji status conventions block."""
    content = _read_template()
    assert "Status Emoji Convention" not in content, (
        "Template must not contain emoji status conventions — lean v2 removes this"
    )
