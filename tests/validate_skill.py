"""Validate the actual release's skill metadata and shipped relative links."""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/plan-first-ab-test"
text = (SKILL / "SKILL.md").read_text()
match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
assert match, "Missing YAML frontmatter"
meta = yaml.safe_load(match.group(1))
assert meta["name"] == SKILL.name
assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", meta["name"])
assert 1 <= len(meta["name"]) <= 64
assert isinstance(meta["description"], str) and 1 <= len(meta["description"]) <= 1024
assert meta["license"] == "MIT" and (ROOT / "LICENSE").is_file()
assert (SKILL / "LICENSE.txt").read_bytes() == (ROOT / "LICENSE").read_bytes()
assert meta["metadata"]["author"] == "Atticus Li"
ui = yaml.safe_load((SKILL / "agents/openai.yaml").read_text())
assert "$plan-first-ab-test" in ui["interface"]["default_prompt"]
assert ui.get("policy", {}).get("allow_implicit_invocation", True) is True
for file in ROOT.rglob("*.md"):
    if "__pycache__" in file.parts:
        continue
    content = file.read_text()
    assert "[TODO:" not in content, file
    for link in re.findall(r"\]\(([^)]+)\)", content):
        if re.match(r"(?:https?://|mailto:|#)", link):
            continue
        destination = file.parent / link.split("#", 1)[0]
        assert destination.exists(), (file.relative_to(ROOT), link)
assert (SKILL / "scripts/plan_binary_test.py").is_file()
assert not list(ROOT.rglob(".env")), "An environment file must not enter the release"
print("One portable skill: metadata, UI invocation, license and relative links valid.")
