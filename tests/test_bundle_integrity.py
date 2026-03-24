"""
Bundle integrity tests for doc-driven-dev.

Validates that bundle.md frontmatter parses correctly,
required fields are present, and all local path references resolve.
"""

import os
import re

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE_MD = os.path.join(REPO_ROOT, "bundle.md")


def _parse_bundle_md():
    """Parse bundle.md and return (frontmatter_dict, body_text)."""
    with open(BUNDLE_MD, encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        raise ValueError("bundle.md does not start with YAML frontmatter")

    # Find the closing ---
    end = content.index("---", 3)
    frontmatter_text = content[3:end].strip()
    body = content[end + 3 :].strip()

    return yaml.safe_load(frontmatter_text), body


def _extract_bundle_refs(fm: dict) -> list[str]:
    """Extract bundle ref strings from frontmatter includes list."""
    return [
        item.get("bundle", "")
        for item in fm.get("includes", [])
        if isinstance(item, dict)
    ]


def _behavior_bundle_path(ref: str) -> str:
    """Resolve a doc-driven-dev: bundle include ref to a filesystem path."""
    # ref is like "doc-driven-dev:behaviors/doc-driven-dev"
    local_path = ref.split("doc-driven-dev:", 1)[-1]
    return os.path.join(REPO_ROOT, local_path)


def _parse_behavior_bundle_md():
    """Parse behaviors/doc-driven-dev/bundle.md and return (frontmatter_dict, body_text)."""
    path = os.path.join(REPO_ROOT, "behaviors", "doc-driven-dev", "bundle.md")
    with open(path, encoding="utf-8") as f:
        content = f.read()

    if not content.startswith("---"):
        raise ValueError(
            "behaviors/doc-driven-dev/bundle.md does not start with YAML frontmatter"
        )

    end = content.index("---", 3)
    frontmatter_text = content[3:end].strip()
    body = content[end + 3 :].strip()

    return yaml.safe_load(frontmatter_text), body


# ---------------------------------------------------------------------------
# Frontmatter structure tests
# ---------------------------------------------------------------------------


def test_bundle_md_exists():
    assert os.path.isfile(BUNDLE_MD), "bundle.md must exist at repo root"


def test_frontmatter_parses():
    fm, _ = _parse_bundle_md()
    assert fm is not None, "frontmatter must be non-empty YAML"


def test_bundle_name():
    fm, _ = _parse_bundle_md()
    assert fm.get("bundle", {}).get("name") == "doc-driven-dev"


def test_bundle_version():
    fm, _ = _parse_bundle_md()
    assert fm.get("bundle", {}).get("version") == "2.0.0"


def test_description_present():
    fm, _ = _parse_bundle_md()
    desc = fm.get("bundle", {}).get("description", "")
    assert desc, "bundle.description must not be empty"


def test_includes_foundation_bundle():
    fm, _ = _parse_bundle_md()
    bundle_refs = _extract_bundle_refs(fm)
    assert any("amplifier-foundation" in ref for ref in bundle_refs), (
        "includes must reference the amplifier-foundation bundle"
    )


def test_includes_behavior_bundle():
    fm, _ = _parse_bundle_md()
    bundle_refs = _extract_bundle_refs(fm)
    assert any("behaviors/doc-driven-dev" in ref for ref in bundle_refs), (
        "includes must reference doc-driven-dev:behaviors/doc-driven-dev"
    )


def test_body_has_heading():
    _, body = _parse_bundle_md()
    assert body.startswith("# Doc-Driven Development"), (
        "markdown body must start with '# Doc-Driven Development'"
    )


def test_body_references_instructions():
    _, body = _parse_bundle_md()
    assert "@doc-driven-dev:context/instructions.md" in body, (
        "markdown body must contain @doc-driven-dev:context/instructions.md reference"
    )


# ---------------------------------------------------------------------------
# Local path resolution tests
# ---------------------------------------------------------------------------


def _extract_local_references(body: str) -> list[str]:
    """Extract @bundle-name:path references from markdown body."""
    return re.findall(r"@doc-driven-dev:([^\s\n]+)", body)


def test_context_instructions_exists():
    """@doc-driven-dev:context/instructions.md must resolve to a real file."""
    path = os.path.join(REPO_ROOT, "context", "instructions.md")
    assert os.path.isfile(path), (
        f"context/instructions.md must exist (referenced by bundle.md body); "
        f"not found at {path}"
    )


def test_context_instructions_content():
    """context/instructions.md must contain the expected heading and key sections."""
    path = os.path.join(REPO_ROOT, "context", "instructions.md")
    with open(path, encoding="utf-8") as f:
        content = f.read()

    assert "# Doc-Driven Development" in content, (
        "context/instructions.md must contain a '# Doc-Driven Development' heading"
    )
    assert "## What this means" in content, (
        "context/instructions.md must contain a '## What this means' section"
    )
    assert "### At session start" in content, (
        "context/instructions.md must contain a '### At session start' section"
    )
    assert "### Before session close" in content, (
        "context/instructions.md must contain a '### Before session close' section"
    )


def test_behavior_bundle_exists():
    """doc-driven-dev:behaviors/doc-driven-dev must resolve to a real path."""
    fm, _ = _parse_bundle_md()
    bundle_refs = _extract_bundle_refs(fm)
    behavior_refs = [ref for ref in bundle_refs if "behaviors/doc-driven-dev" in ref]
    assert behavior_refs, "No behavior bundle ref found in includes"

    full_path = _behavior_bundle_path(behavior_refs[0])
    # Accept either a directory (with bundle.md inside) or a direct .md file
    dir_exists = os.path.isdir(full_path)
    file_exists = os.path.isfile(full_path + ".md") or os.path.isfile(
        os.path.join(full_path, "bundle.md")
    )
    assert dir_exists or file_exists, (
        f"behaviors/doc-driven-dev must exist as a directory or .md file; "
        f"checked {full_path}"
    )


def test_behavior_bundle_structure():
    """behaviors/doc-driven-dev/bundle.md must have valid frontmatter with all three behaviors."""
    fm, _ = _parse_behavior_bundle_md()
    assert fm is not None, (
        "behaviors/doc-driven-dev/bundle.md must have valid YAML frontmatter"
    )

    behaviors = fm.get("behaviors", [])
    assert behaviors, (
        "behaviors/doc-driven-dev/bundle.md must have a non-empty 'behaviors' section"
    )

    expected_names = {
        "session-open-doc-check",
        "session-close-discipline",
        "decision-logging",
    }
    actual_names = {b.get("name") for b in behaviors if isinstance(b, dict)}
    assert expected_names == actual_names, (
        f"Expected behaviors {expected_names}, found {actual_names}"
    )

    for behavior in behaviors:
        assert behavior.get("description"), (
            f"Behavior '{behavior.get('name')}' must have a non-empty description"
        )


def test_all_body_local_refs_resolve():
    """Every @doc-driven-dev:path reference in body must point to an existing file."""
    _, body = _parse_bundle_md()
    refs = _extract_local_references(body)
    missing = []
    for ref in refs:
        path = os.path.join(REPO_ROOT, ref)
        if not os.path.isfile(path):
            missing.append(ref)
    assert not missing, f"Unresolved local references in bundle.md body: {missing}"
