"""
Tests for task-5: Delete v1 bundle.yaml and session-close-reminder.md.

Acceptance criteria:
- ls bundle.* shows only bundle.md (no bundle.yaml)
- ls context/ shows only instructions.md (no session-close-reminder.md)
- Replacement files (bundle.md, context/instructions.md) remain intact
"""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_bundle_yaml_does_not_exist():
    """bundle.yaml must NOT exist — replaced by bundle.md."""
    path = os.path.join(REPO_ROOT, "bundle.yaml")
    assert not os.path.exists(path), (
        "bundle.yaml must be deleted; it is replaced by bundle.md"
    )


def test_session_close_reminder_does_not_exist():
    """context/session-close-reminder.md must NOT exist — session-close discipline moves to lifeos."""
    path = os.path.join(REPO_ROOT, "context", "session-close-reminder.md")
    assert not os.path.exists(path), (
        "context/session-close-reminder.md must be deleted; "
        "session-close discipline moves to lifeos (separate effort)"
    )


def test_bundle_md_remains():
    """bundle.md must still exist at repo root (the v1 replacement)."""
    path = os.path.join(REPO_ROOT, "bundle.md")
    assert os.path.isfile(path), "bundle.md must exist at repo root"


def test_context_instructions_md_remains():
    """context/instructions.md must still exist (the v1 replacement)."""
    path = os.path.join(REPO_ROOT, "context", "instructions.md")
    assert os.path.isfile(path), "context/instructions.md must exist"


def test_context_dir_has_only_instructions():
    """context/ directory must contain only instructions.md."""
    context_dir = os.path.join(REPO_ROOT, "context")
    files = [
        f for f in os.listdir(context_dir) if os.path.isfile(os.path.join(context_dir, f))
    ]
    assert files == ["instructions.md"], (
        f"context/ must contain only instructions.md, found: {sorted(files)}"
    )
