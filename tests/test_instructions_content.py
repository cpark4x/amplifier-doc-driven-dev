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


def _parse_table_data_rows(content: str) -> list[tuple[str, str]]:
    """Parse markdown table data rows into (question, document) tuples.

    Skips the header row and separator rows (lines with only -/|/space chars).
    Returns a list of (col0, col1) string pairs for each data row.
    """
    rows = []
    for line in content.splitlines():
        stripped = line.strip()
        if "|" not in stripped:
            continue
        # Skip separator rows (e.g. |---|---|)
        if all(c in "-| :" for c in stripped):
            continue
        cells = [c.strip() for c in stripped.split("|") if c.strip()]
        if len(cells) >= 2:
            rows.append((cells[0], cells[1]))
    return rows


def test_alignment_table_has_four_docs():
    """instructions.md must map each of the four alignment docs in a table row."""
    content = _read_instructions()
    rows = _parse_table_data_rows(content)
    doc_cells = [doc for _, doc in rows]
    for doc in ["VISION.md", "OUTCOMES.md", "BACKLOG.md", "AGENTS.md"]:
        assert any(doc in cell for cell in doc_cells), (
            f"instructions.md alignment table must contain '{doc}' in a document column cell"
        )


def test_alignment_table_four_questions():
    """instructions.md must map 4 specific alignment questions to the correct docs."""
    content = _read_instructions()
    rows = _parse_table_data_rows(content)
    # Each entry: (fragment that must appear in the question cell, expected doc)
    expected_mappings = [
        ("why", "VISION.md"),
        ("measurable outcomes", "OUTCOMES.md"),
        ("in scope", "BACKLOG.md"),
        ("agents", "AGENTS.md"),
    ]
    for question_fragment, expected_doc in expected_mappings:
        matching = [
            (q, d)
            for q, d in rows
            if question_fragment.lower() in q.lower() and expected_doc in d
        ]
        assert matching, (
            f"instructions.md alignment table must have a row where the question contains "
            f"'{question_fragment}' and the document is '{expected_doc}'"
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
    """instructions.md must contain exactly Rules 1 through 5 (numbered)."""
    content = _read_instructions()
    for i in range(1, 6):
        assert f"Rule {i}" in content, (
            f"instructions.md must contain 'Rule {i}' — all 5 numbered rules are required"
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
