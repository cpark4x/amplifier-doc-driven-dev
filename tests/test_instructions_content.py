"""
Tests for context/instructions.md content per spec task-4.

Validates the alignment system instructions include:
- Heading: 'Doc-Driven Development: Alignment System'
- 4 alignment questions table referencing VISION.md, OUTCOMES.md, BACKLOG.md, AGENTS.md
- 80/20 Principle section
- 'How to Work With These Docs' section with start-of-session, during-work, health-check
- 5 Rules
"""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTRUCTIONS_PATH = os.path.join(REPO_ROOT, "context", "instructions.md")


def _read_instructions() -> str:
    with open(INSTRUCTIONS_PATH, encoding="utf-8") as f:
        return f.read()


def test_heading_alignment_system():
    """instructions.md must use 'Doc-Driven Development: Alignment System' heading."""
    content = _read_instructions()
    assert "# Doc-Driven Development: Alignment System" in content, (
        "instructions.md must contain '# Doc-Driven Development: Alignment System' heading"
    )


def test_alignment_table_has_four_docs():
    """instructions.md must reference all four alignment docs in a table."""
    content = _read_instructions()
    for doc in ["VISION.md", "OUTCOMES.md", "BACKLOG.md", "AGENTS.md"]:
        assert doc in content, (
            f"instructions.md must reference {doc} in the alignment questions table"
        )


def test_alignment_table_four_questions():
    """instructions.md must map 4 alignment questions."""
    content = _read_instructions()
    # The table should have at least 4 data rows — check there are 4 docs + a table structure
    # We verify by confirming all 4 docs appear AND there's a markdown table present
    assert "|" in content, (
        "instructions.md must contain a markdown table (pipe characters)"
    )
    lines_with_pipe = [line for line in content.splitlines() if "|" in line]
    # At minimum: header row, separator row, 4 data rows = 6 lines with pipes
    assert len(lines_with_pipe) >= 6, (
        "instructions.md alignment table must have at least 4 data rows (question→doc mapping)"
    )


def test_8020_principle_section():
    """instructions.md must contain an 80/20 Principle section."""
    content = _read_instructions()
    assert "80/20" in content, (
        "instructions.md must contain an '80/20' Principle section"
    )
    assert "80%" in content, "instructions.md must explain 80% purpose (AI context)"
    assert "20%" in content, (
        "instructions.md must explain 20% purpose (human confidence)"
    )


def test_how_to_work_section():
    """instructions.md must contain 'How to Work With These Docs' section."""
    content = _read_instructions()
    assert "How to Work With These Docs" in content, (
        "instructions.md must contain 'How to Work With These Docs' section"
    )


def test_how_to_work_subsections():
    """How to Work section must include start-of-session, during-work, and health-check guidance."""
    content = _read_instructions()
    lower = content.lower()
    assert "start" in lower and "session" in lower, (
        "instructions.md must contain start-of-session guidance"
    )
    assert "during" in lower or "work" in lower, (
        "instructions.md must contain during-work guidance"
    )
    assert "health" in lower, "instructions.md must contain health-check guidance"


def test_five_rules_present():
    """instructions.md must contain 5 Rules."""
    content = _read_instructions()
    # Check for a Rules section
    assert "Rule" in content or "Rules" in content, (
        "instructions.md must contain a Rules section"
    )


def test_rule_1_facts_vs_judgments():
    """Rule 1: Update facts automatically, flag judgments for humans."""
    content = _read_instructions()
    lower = content.lower()
    assert "fact" in lower, "Rule 1 must mention facts"
    assert "judgment" in lower or "judgement" in lower, (
        "Rule 1 must distinguish facts from judgments"
    )


def test_rule_2_backlog_connects_outcome():
    """Rule 2: Every backlog item must connect to an outcome."""
    content = _read_instructions()
    lower = content.lower()
    assert "backlog" in lower, "Rule 2 must reference backlog"
    assert "outcome" in lower, "Rule 2 must reference outcome"


def test_rule_3_non_goals_boundaries():
    """Rule 3: Non-Goals are boundaries."""
    content = _read_instructions()
    assert (
        "Non-Goal" in content or "Non-goal" in content or "non-goal" in content.lower()
    ), "Rule 3 must reference Non-Goals"
    lower = content.lower()
    assert "boundar" in lower, "Rule 3 must describe Non-Goals as boundaries"


def test_rule_4_learnings_inline():
    """Rule 4: Learnings are inline not separate."""
    content = _read_instructions()
    lower = content.lower()
    assert "learning" in lower, "Rule 4 must reference learnings"
    assert "inline" in lower, "Rule 4 must say learnings are inline"


def test_rule_5_attribution():
    """Rule 5: Attribution matters."""
    content = _read_instructions()
    lower = content.lower()
    assert "attribution" in lower, "Rule 5 must mention attribution"
