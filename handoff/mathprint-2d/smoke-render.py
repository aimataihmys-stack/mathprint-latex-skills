#!/usr/bin/env python3
"""Compile only the two bundled, reviewed examples. Not an untrusted-TeX sandbox."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trusted-examples", action="store_true", help="Explicitly authorize compiling the fixed bundled examples.")
    args = parser.parse_args()
    if not args.trusted_examples:
        parser.error("Read the examples first, then pass --trusted-examples. No arbitrary input path is accepted.")
    engine = shutil.which("pdflatex")
    if not engine:
        print(json.dumps({"passed": False, "status": "blocked_missing_pdflatex", "compiled": 0}))
        return 2
    here = Path(__file__).resolve().parent
    results = []
    with tempfile.TemporaryDirectory(prefix="mathprint-skills-smoke-") as temp:
        work = Path(temp)
        for name in ("geometry", "graph"):
            shutil.copyfile(here / "examples" / f"{name}.tex", work / f"{name}.tex")
            try:
                process = subprocess.run([engine, "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error", f"{name}.tex"], cwd=work, capture_output=True, text=True, errors="replace", timeout=45)
                pdf = work / f"{name}.pdf"
                ok = process.returncode == 0 and pdf.is_file() and pdf.read_bytes().startswith(b"%PDF-")
                record = {"example": name, "passed": ok, "returncode": process.returncode, "pdfBytes": pdf.stat().st_size if pdf.is_file() else 0}
                if not ok:
                    record["logTail"] = process.stdout[-1800:]
                results.append(record)
            except subprocess.TimeoutExpired:
                results.append({"example": name, "passed": False, "status": "timeout"})
    passed = all(r["passed"] for r in results)
    print(json.dumps({"kind": "trusted-example-compilation", "passed": passed, "results": results, "limitations": "No persistent output, no font redistribution, no visual or browser acceptance, no arbitrary TeX sandbox claim."}, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
