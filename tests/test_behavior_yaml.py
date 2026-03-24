"""
Tests for behaviors/doc-driven-dev.yaml — the composable behavior layer.

Validates structure, required fields, and absence of v1 anti-patterns.
"""

import os

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEHAVIOR_YAML = os.path.join(REPO_ROOT, "behaviors", "doc-driven-dev.yaml")


def _load_behavior_yaml() -> dict:
    """Parse behaviors/doc-driven-dev.yaml and return the data dict."""
    with open(BEHAVIOR_YAML, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data is not None, "behaviors/doc-driven-dev.yaml must not be empty"
    return data


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------


def test_behavior_yaml_exists():
    """behaviors/doc-driven-dev.yaml must exist."""
    assert os.path.isfile(BEHAVIOR_YAML), (
        f"behaviors/doc-driven-dev.yaml must exist; not found at {BEHAVIOR_YAML}"
    )


def test_behavior_yaml_parses():
    """behaviors/doc-driven-dev.yaml must be valid YAML."""
    data = _load_behavior_yaml()
    assert isinstance(data, dict), "top-level YAML must be a mapping"


# ---------------------------------------------------------------------------
# bundle section
# ---------------------------------------------------------------------------


def test_bundle_name():
    """bundle.name must be 'doc-driven-dev-behavior'."""
    data = _load_behavior_yaml()
    assert data.get("bundle", {}).get("name") == "doc-driven-dev-behavior", (
        "bundle.name must be 'doc-driven-dev-behavior'"
    )


def test_bundle_version():
    """bundle.version must be '2.0.0'."""
    data = _load_behavior_yaml()
    assert data.get("bundle", {}).get("version") == "2.0.0", (
        "bundle.version must be '2.0.0'"
    )


def test_bundle_description_present():
    """bundle.description must be non-empty."""
    data = _load_behavior_yaml()
    desc = data.get("bundle", {}).get("description", "")
    assert desc, "bundle.description must not be empty"


# ---------------------------------------------------------------------------
# tools section — module reference
# ---------------------------------------------------------------------------


def test_tools_section_present():
    """A 'tools' section must be present."""
    data = _load_behavior_yaml()
    assert "tools" in data, "A 'tools' section is required"
    assert isinstance(data["tools"], list), "'tools' must be a list"
    assert len(data["tools"]) > 0, "'tools' must not be empty"


def test_tool_skills_module_present():
    """tools must include the tool-skills module from the expected git URL."""
    data = _load_behavior_yaml()
    tools = data.get("tools", [])
    modules = [t.get("module", "") for t in tools if isinstance(t, dict)]
    expected = "git+https://github.com/microsoft/amplifier-module-tool-skills@main"
    assert any(expected in m for m in modules), (
        f"tools must include module '{expected}'; found: {modules}"
    )


def test_skills_dirs_points_to_local_only():
    """config.skills_dirs must contain './skills' and no remote git URLs."""
    data = _load_behavior_yaml()
    tools = data.get("tools", [])
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        config = tool.get("config", {})
        skills_dirs = config.get("skills_dirs", [])
        if skills_dirs:
            # Must contain ./skills
            assert "./skills" in skills_dirs, (
                f"skills_dirs must contain './skills'; found: {skills_dirs}"
            )
            # Must NOT contain any remote git URLs
            for entry in skills_dirs:
                assert not entry.startswith("git+"), (
                    f"skills_dirs must not contain remote git URLs; found: {entry}"
                )


def test_visibility_enabled():
    """visibility.enabled must be true."""
    data = _load_behavior_yaml()
    tools = data.get("tools", [])
    found = False
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        visibility = tool.get("visibility", {})
        if visibility:
            found = True
            assert visibility.get("enabled") is True, "visibility.enabled must be true"
    assert found, "At least one tool entry must have a 'visibility' section"


def test_max_skills_visible_50():
    """visibility.max_skills_visible must be 50."""
    data = _load_behavior_yaml()
    tools = data.get("tools", [])
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        visibility = tool.get("visibility", {})
        if visibility:
            assert visibility.get("max_skills_visible") == 50, (
                "visibility.max_skills_visible must be 50"
            )


# ---------------------------------------------------------------------------
# context section
# ---------------------------------------------------------------------------


def test_context_include_present():
    """context.include must reference instructions file via @doc-driven-dev: prefix."""
    data = _load_behavior_yaml()
    context = data.get("context", {})
    includes = context.get("include", [])
    assert any(
        "@doc-driven-dev:context/instructions.md" in str(item) for item in includes
    ), (
        "context.include must reference '@doc-driven-dev:context/instructions.md'; "
        f"found: {includes}"
    )


# ---------------------------------------------------------------------------
# Anti-pattern guard — no v1 'skills:' key with remote git URL
# ---------------------------------------------------------------------------


def test_no_top_level_skills_with_git_url():
    """Must NOT have a top-level 'skills:' key containing a remote git URL (v1 bug)."""
    data = _load_behavior_yaml()
    skills = data.get("skills")
    if skills is None:
        return  # No skills key at all — that's correct

    # If 'skills' key exists, it must not contain any git+ URLs
    skills_str = yaml.dump(skills)
    assert "git+" not in skills_str, (
        "The 'skills:' key must not contain remote git URLs (v1 anti-pattern); "
        f"found: {skills_str}"
    )
