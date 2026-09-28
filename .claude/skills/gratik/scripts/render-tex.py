#!/usr/bin/env python3
"""Compile a .tex source to PDF and render to PNG in one step.

Use as the final step of any gratik/gf2 skill invocation so the user
receives TeX (source) + PDF (compiled) + PNG (preview) instead of just TeX.

Usage:
    python3 scripts/render-tex.py path/to/figure.tex
    python3 scripts/render-tex.py figure.tex --dpi 300 --engine xelatex

Outputs (next to the .tex source):
    figure.pdf
    figure.png            (single-page)
    figure-p1.png ... -pN.png  (multi-page)

Dependencies: TeX Live (pdflatex/xelatex/lualatex on PATH), pymupdf.
The script keeps intermediate .aux/.log/.fls files so latex error logs
remain available for debugging; clean them with `latexmk -c` if needed.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def compile_tex(tex: Path, engine: str) -> tuple[bool, str]:
    if shutil.which(engine) is None:
        return False, f"{engine} not on PATH"
    cmd = [engine, "-interaction=nonstopmode", "-halt-on-error", tex.name]
    proc = subprocess.run(cmd, cwd=tex.parent, capture_output=True, text=True)
    if proc.returncode != 0:
        # Tail of stdout typically holds the error context
        tail = "\n".join(proc.stdout.splitlines()[-25:])
        return False, tail
    pdf = tex.with_suffix(".pdf")
    if not pdf.exists():
        return False, "compile succeeded but no .pdf produced"
    return True, ""


def render_png(pdf: Path, dpi: int) -> list[Path]:
    import fitz

    doc = fitz.open(pdf)
    outputs: list[Path] = []
    if len(doc) == 1:
        png = pdf.with_suffix(".png")
        doc[0].get_pixmap(dpi=dpi).save(png)
        outputs.append(png)
    else:
        for i, page in enumerate(doc):
            png = pdf.parent / f"{pdf.stem}-p{i+1}.png"
            page.get_pixmap(dpi=dpi).save(png)
            outputs.append(png)
    return outputs


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="TeX → PDF → PNG one-shot renderer")
    parser.add_argument("tex", type=Path, help=".tex file to compile and render")
    parser.add_argument("--dpi", type=int, default=200, help="PNG resolution (default 200)")
    parser.add_argument(
        "--engine",
        default="pdflatex",
        choices=["pdflatex", "xelatex", "lualatex"],
        help="LaTeX engine (default pdflatex; use xelatex for Korean fonts via kotex)",
    )
    parser.add_argument("--quiet", action="store_true", help="suppress success messages")
    args = parser.parse_args(argv[1:])

    if not args.tex.is_file():
        print(f"error: not a file: {args.tex}", file=sys.stderr)
        return 2
    if args.tex.suffix != ".tex":
        print(f"error: not a .tex file: {args.tex}", file=sys.stderr)
        return 2

    ok, err = compile_tex(args.tex, args.engine)
    if not ok:
        print(f"COMPILE FAILED ({args.engine}):", file=sys.stderr)
        print(err, file=sys.stderr)
        return 1

    pdf = args.tex.with_suffix(".pdf")
    pngs = render_png(pdf, args.dpi)
    if not args.quiet:
        print(f"TeX:  {args.tex}")
        print(f"PDF:  {pdf}")
        for p in pngs:
            print(f"PNG:  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
