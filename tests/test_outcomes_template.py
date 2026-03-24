"""
Tests for task-8: Create OUTCOMES_TEMPLATE.md lean skeleton.

Acceptance criteria:
- wc -l shows around 19 lines
- File has YAML frontmatter (last_updated, updated_by)
- Current Assessment section (1-2 sentences: overall trajectory)
- One table with 5 columns: Outcome, Why It Matters, How We Measure, Status, Last Checked
- Notes section for context on status changes
- Replaces old SUCCESS_METRICS_TEMPLATE (V1/V2/V3 metrics, leading/lagging indicators, vanity metrics)
"""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(REPO_ROOT, "templates", "OUTCOMES_TEMPLATE.md")


def _read_template():
    with open(TEMPLATE_PATH, "r") as f:
        return f.read()


def _count_lines():
    with open(TEMPLATE_PATH, "r") as f:
        return len(f.readlines())


def test_outcomes_template_exists():
    """The OUTCOMES_TEMPLATE.md file must exist."""
    assert os.path.isfile(TEMPLATE_PATH), "templates/OUTCOMES_TEMPLATE.md must exist"


def test_outcomes_template_is_lean():
    """Template must be around 19 lines, not the v1 281 lines."""
    line_count = _count_lines()
    assert line_count <= 30, (
        f"Template must be lean (~19 lines), but found {line_count} lines. "
        "Remove V1/V2/V3 metrics, leading/lagging indicators, vanity metrics."
    )
    assert line_count >= 14, (
        f"Template must have at least 14 lines (frontmatter + sections + table), "
        f"found {line_count}"
    )


def test_outcomes_template_has_yaml_frontmatter():
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


def test_outcomes_template_frontmatter_has_last_updated():
    """YAML frontmatter must contain last_updated field."""
    content = _read_template()
    assert "last_updated:" in content, (
        "YAML frontmatter must contain 'last_updated:' field"
    )


def test_outcomes_template_frontmatter_has_updated_by():
    """YAML frontmatter must contain updated_by field."""
    content = _read_template()
    assert "updated_by:" in content, (
        "YAML frontmatter must contain 'updated_by:' field"
    )


def test_outcomes_template_has_current_assessment_section():
    """Template must have a Current Assessment section."""
    content = _read_template()
    assert "## Current Assessment" in content, (
        "Template must have '## Current Assessment' section"
    )


def test_outcomes_template_has_outcomes_table():
    """Template must have a table with the 5 required columns."""
    content = _read_template()
    assert "Outcome" in content, "Table must have 'Outcome' column"
    assert "Why It Matters" in content, "Table must have 'Why It Matters' column"
    assert "How We Measure" in content, "Table must have 'How We Measure' column"
    assert "Status" in content, "Table must have 'Status' column"
    assert "Last Checked" in content, "Table must have 'Last Checked' column"


def test_outcomes_table_is_markdown_table():
    """Table must be a proper markdown table (has | separators)."""
    content = _read_template()
    lines = content.splitlines()
    table_lines = [line for line in lines if "|" in line]
    assert len(table_lines) >= 2, (
        "Template must contain a markdown table with at least header and separator rows"
    )


def test_outcomes_table_has_all_five_columns_in_header():
    """The table header row must contain all 5 required columns."""
    content = _read_template()
    lines = content.splitlines()
    header_line = None
    for line in lines:
        if "Outcome" in line and "Why It Matters" in line and "|" in line:
            header_line = line
            break
    assert header_line is not None, (
        "Could not find a table header row containing all required columns: "
        "Outcome, Why It Matters, How We Measure, Status, Last Checked"
    )
    assert "How We Measure" in header_line, (
        "Table header must contain 'How We Measure' column"
    )
    assert "Status" in header_line, "Table header must contain 'Status' column"
    assert "Last Checked" in header_line, "Table header must contain 'Last Checked' column"


def test_outcomes_template_has_notes_section():
    """Template must have a Notes section."""
    content = _read_template()
    assert "## Notes" in content, "Template must have '## Notes' section"


def test_outcomes_template_no_v1_v2_v3_metrics():
    """Template must NOT contain V1/V2/V3 metrics language."""
    content = _read_template()
    assert "V1 Metrics" not in content, "Template must not contain 'V1 Metrics'"
    assert "V2 Metrics" not in content, "Template must not contain 'V2 Metrics'"
    assert "V3 Metrics" not in content, "Template must not contain 'V3 Metrics'"


def test_outcomes_template_no_leading_lagging_indicators():
    """Template must NOT contain leading/lagging indicator sections."""
    content = _read_template()
    assert "Leading Indicator" not in content, (
        "Template must not contain leading indicator sections"
    )
    assert "Lagging Indicator" not in content, (
        "Template must not contain lagging indicator sections"
    )


def test_outcomes_template_no_vanity_metrics():
    """Template must NOT contain vanity metrics sections."""
    content = _read_template()
    assert "Vanity" not in content, (
        "Template must not contain vanity metrics — lean template removes this"
    )
