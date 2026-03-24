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
    with open(BUNDLE_MD) as f:
        content = f.read()

    if not content.startswith("---"):
        raise ValueError("bundle.md does not start with YAML frontmatter")

    # Find the closing ---
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
    includes = fm.get("includes", [])
    bundle_refs = [
        item.get("bundle", "") for item in includes if isinstance(item, dict)
    ]
    assert any("amplifier-foundation" in ref for ref in bundle_refs), (
        "includes must reference the amplifier-foundation bundle"
    )


def test_includes_behavior_bundle():
    fm, _ = _parse_bundle_md()
    includes = fm.get("includes", [])
    bundle_refs = [
        item.get("bundle", "") for item in includes if isinstance(item, dict)
    ]
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


def _behavior_bundle_path(ref: str) -> str:
    """Resolve a doc-driven-dev: bundle include ref to a filesystem path."""
    # ref is like "doc-driven-dev:behaviors/doc-driven-dev"
    local_path = ref.split("doc-driven-dev:", 1)[-1]
    return os.path.join(REPO_ROOT, local_path)


def test_context_instructions_exists():
    """@doc-driven-dev:context/instructions.md must resolve to a real file."""
    path = os.path.join(REPO_ROOT, "context", "instructions.md")
    assert os.path.isfile(path), (
        f"context/instructions.md must exist (referenced by bundle.md body); "
        f"not found at {path}"
    )


def test_behavior_bundle_exists():
    """doc-driven-dev:behaviors/doc-driven-dev must resolve to a real path."""
    fm, _ = _parse_bundle_md()
    includes = fm.get("includes", [])
    behavior_refs = [
        item.get("bundle", "")
        for item in includes
        if isinstance(item, dict)
        and "behaviors/doc-driven-dev" in item.get("bundle", "")
    ]
    assert behavior_refs, "No behavior bundle ref found in includes"

    ref = behavior_refs[0]
    local_path = ref.replace("doc-driven-dev:", "")
    full_path = os.path.join(REPO_ROOT, local_path)
    # Accept either a directory (with bundle.md inside) or a direct .md file
    dir_exists = os.path.isdir(full_path)
    file_exists = os.path.isfile(full_path + ".md") or os.path.isfile(
        os.path.join(full_path, "bundle.md")
    )
    assert dir_exists or file_exists, (
        f"behaviors/doc-driven-dev must exist as a directory or .md file; "
        f"checked {full_path}"
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
