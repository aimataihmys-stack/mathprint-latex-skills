#!/usr/bin/env python3
"""Verify this skill handoff; does not execute TeX or install dependencies."""
from __future__ import annotations
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main() -> int:
    checks: list[dict] = []
    def check(name: str, ok: bool) -> None:
        checks.append({"name": name, "passed": bool(ok)})
    try:
        manifest = json.loads((HERE / "source-manifest.json").read_text(encoding="utf-8"))
        check("manifest-v1", manifest.get("schemaVersion") == 1)
        for item in manifest["files"]:
            rel = Path(item["path"])
            target = ROOT / rel
            valid = not rel.is_absolute() and ".." not in rel.parts and ROOT in target.resolve().parents
            check(f"path:{rel}", valid and target.is_file() and not target.is_symlink())
            if not valid or not target.is_file():
                continue
            data = target.read_bytes()
            check(f"sha256:{rel}", hashlib.sha256(data).hexdigest() == item["publishedSha256"])
            check(f"size:{rel}", len(data) == item["bytes"])
            if target.suffix == ".py":
                ast.parse(data.decode("utf-8"), filename=str(rel))
                check(f"python-syntax:{rel}", True)
        required = [
            ROOT / "MATHPRINT_START_HERE.md", ROOT / ".claude/skills/mathprint-2d/SKILL.md",
            HERE / "DECISIONS.md", HERE / "ERRATA_AND_LIMITS.md",
            HERE / "examples/geometry.tex", HERE / "examples/graph.tex", HERE / "smoke-render.py",
        ]
        for path in required:
            check(f"required:{path.relative_to(ROOT)}", path.is_file())
        router = (ROOT / ".claude/skills/mathprint-2d/SKILL.md").read_text(encoding="utf-8")
        check("explicit-G4-exclusion", "G4" in router and "제외" in router)
        all_paths = {ROOT / item["path"] for item in manifest["files"]} | set(required)
        forbidden = {".otf", ".ttf", ".woff", ".woff2", ".key", ".pem", ".p12"}
        secret = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{25,}|\bgithub_pat_[A-Za-z0-9_]{40,}|\bAIza[A-Za-z0-9_-]{30,}")
        for path in sorted(all_paths):
            check(f"no-font-or-key:{path.relative_to(ROOT)}", path.suffix.lower() not in forbidden)
            if path.is_file():
                check(f"known-secret-patterns:{path.relative_to(ROOT)}", not secret.search(path.read_text(encoding="utf-8")))
        check("renderer-copies-match", (ROOT / "scripts/render-tex.py").read_bytes() == (ROOT / ".claude/skills/gf2/render-tex.py").read_bytes() == (ROOT / ".claude/skills/gratik/scripts/render-tex.py").read_bytes())
    except (OSError, ValueError, KeyError, SyntaxError) as exc:
        checks.append({"name": "exception", "passed": False, "type": type(exc).__name__, "message": str(exc)})
    result = {"kind": "skill-package-verification", "passed": all(c["passed"] for c in checks), "checks": checks, "limitations": "No browser, application, arbitrary-TeX security, visual quality or complete secret audit is claimed."}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
