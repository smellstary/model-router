"""废弃副本不得再被运行时代码导入；武学状态机不再充当安全层。"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMPORT_RE = re.compile(r"^\s*(?:import|from)\s+oriental_agent\b", re.M)


def test_deprecated_module_is_marked_and_not_imported():
    header = (ROOT / "oriental_agent.py").read_text(encoding="utf-8")[:400]
    assert "DEPRECATED" in header
    assert "core/agent.py" in header

    offenders = []
    for path in ROOT.rglob("*.py"):
        if any(part in {".venv", "venv", "__pycache__", "uploads"} for part in path.parts):
            continue
        if path.name == "oriental_agent.py":
            continue
        text = path.read_text(encoding="utf-8")
        if IMPORT_RE.search(text):
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == []


def test_martial_state_machine_is_not_the_security_boundary():
    import security.martial_defense as shim
    import narrative.martial_state_machine as play

    assert shim.TaijiDefense is play.TaijiDefense
    assert "不是安全边界" in shim.__doc__
    assert "叙事状态机" in play.__doc__
    assert "integration" in play.__doc__
