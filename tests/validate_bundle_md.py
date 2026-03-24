#!/usr/bin/env python3
"""Validation test for bundle.md - task-2 acceptance criteria."""
import sys
from pathlib import Path

BUNDLE_MD = Path(__file__).parent.parent / "bundle.md"


def fail(msg):
    print(f"  FAIL: {msg}", file=sys.stderr)
    return False


def ok(msg):
    print(f"  PASS: {msg}")
    return True


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None, content
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    frontmatter_str = content[3:end].strip()
    body = content[end + 4:].strip()
    return frontmatter_str, body


def test_bundle_md_exists():
    if not BUNDLE_MD.exists():
        return fail(f"bundle.md not found at {BUNDLE_MD}")
    return ok("bundle.md exists")


def test_frontmatter_delimiters():
    if not BUNDLE_MD.exists():
        return fail("bundle.md does not exist")
    content = BUNDLE_MD.read_text()
    if not content.startswith("---"):
        return fail("bundle.md does not start with ---")
    if "\n---" not in content[3:]:
        return fail("bundle.md does not have closing --- delimiter")
    return ok("YAML frontmatter has opening and closing ---")


def test_bundle_name():
    import yaml
    if not BUNDLE_MD.exists():
        return fail("bundle.md does not exist")
    content = BUNDLE_MD.read_text()
    fm_str, _ = parse_frontmatter(content)
    if fm_str is None:
        return fail("Could not parse frontmatter")
    fm = yaml.safe_load(fm_str)
    name = fm.get("bundle", {}).get("name")
    if name != "doc-driven-dev":
        return fail(f"bundle.name is '{name}', expected 'doc-driven-dev'")
    return ok(f"bundle.name = {name}")


def test_bundle_version():
    import yaml
    if not BUNDLE_MD.exists():
        return fail("bundle.md does not exist")
    content = BUNDLE_MD.read_text()
    fm_str, _ = parse_frontmatter(content)
    if fm_str is None:
        return fail("Could not parse frontmatter")
    fm = yaml.safe_load(fm_str)
    version = fm.get("bundle", {}).get("version")
    if str(version) != "2.0.0":
        return fail(f"bundle.version is '{version}', expected '2.0.0'")
    return ok(f"bundle.version = {version}")


def test_includes_foundation():
    import yaml
    if not BUNDLE_MD.exists():
        return fail("bundle.md does not exist")
    content = BUNDLE_MD.read_text()
    fm_str, _ = parse_frontmatter(content)
    if fm_str is None:
        return fail("Could not parse frontmatter")
    fm = yaml.safe_load(fm_str)
    includes = fm.get("includes", [])
    foundation_url = "git+https://github.com/microsoft/amplifier-foundation@main"
    for item in includes:
        if isinstance(item, dict) and item.get("bundle") == foundation_url:
            return ok(f"includes foundation bundle: {foundation_url}")
    return fail(f"includes does not contain bundle: {foundation_url}")


def test_includes_behavior():
    import yaml
    if not BUNDLE_MD.exists():
        return fail("bundle.md does not exist")
    content = BUNDLE_MD.read_text()
    fm_str, _ = parse_frontmatter(content)
    if fm_str is None:
        return fail("Could not parse frontmatter")
    fm = yaml.safe_load(fm_str)
    includes = fm.get("includes", [])
    behavior_ref = "doc-driven-dev:behaviors/doc-driven-dev"
    for item in includes:
        if isinstance(item, dict) and item.get("bundle") == behavior_ref:
            return ok(f"includes behavior bundle: {behavior_ref}")
    return fail(f"includes does not contain bundle: {behavior_ref}")


def test_markdown_heading():
    if not BUNDLE_MD.exists():
        return fail("bundle.md does not exist")
    content = BUNDLE_MD.read_text()
    _, body = parse_frontmatter(content)
    if "# Doc-Driven Development" not in body:
        return fail("Markdown body does not contain '# Doc-Driven Development' heading")
    return ok("Markdown body has '# Doc-Driven Development' heading")


def test_instructions_reference():
    if not BUNDLE_MD.exists():
        return fail("bundle.md does not exist")
    content = BUNDLE_MD.read_text()
    _, body = parse_frontmatter(content)
    if "@doc-driven-dev:context/instructions.md" not in body:
        return fail("Markdown body does not contain @doc-driven-dev:context/instructions.md")
    return ok("Markdown body has @doc-driven-dev:context/instructions.md reference")


def test_description_alignment():
    import yaml
    if not BUNDLE_MD.exists():
        return fail("bundle.md does not exist")
    content = BUNDLE_MD.read_text()
    fm_str, _ = parse_frontmatter(content)
    if fm_str is None:
        return fail("Could not parse frontmatter")
    fm = yaml.safe_load(fm_str)
    desc = fm.get("bundle", {}).get("description", "")
    if not desc:
        return fail("bundle.description is missing")
    desc_lower = desc.lower()
    if "alignment" not in desc_lower and "human" not in desc_lower:
        return fail(f"description doesn't mention alignment/human-AI: '{desc}'")
    return ok(f"bundle.description mentions alignment/human-AI collaboration")


if __name__ == "__main__":
    tests = [
        test_bundle_md_exists,
        test_frontmatter_delimiters,
        test_bundle_name,
        test_bundle_version,
        test_includes_foundation,
        test_includes_behavior,
        test_markdown_heading,
        test_instructions_reference,
        test_description_alignment,
    ]

    passed = 0
    failed = 0
    print("Running bundle.md validation tests...")
    print()
    for test in tests:
        name = test.__name__
        print(f"[{name}]")
        result = test()
        if result:
            passed += 1
        else:
            failed += 1
        print()

    print(f"Results: {passed} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)
