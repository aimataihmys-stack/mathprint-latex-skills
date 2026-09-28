#!/usr/bin/env python3
"""
gf2 라벨-도형 겹침 자동 검증.

사용법:
    python verify-overlap.py <fig.tex> [--dpi 200] [--ring-px 6]
                                       [--dark-threshold 80] [--overlap-threshold 0.04]
                                       [--no-compile] [--report PATH]

동작:
    1) <fig.tex> 를 pdflatex 로 컴파일 (이미 PDF가 있으면 --no-compile 로 스킵)
    2) pdftotext -bbox 로 단어 bbox(좌상단 기준 pt) 추출
    3) pdftoppm 으로 PNG 렌더 (DPI 지정)
    4) 각 라벨 bbox 외곽 ring 영역의 검은 픽셀 비율 측정
       - ring 비율 < 0.005    → ok
       - 0.005 ≤ 비율 < 임계  → near (라벨 가까이 변이 있음)
       - 비율 ≥ 임계          → overlap (변/요소가 라벨을 가림)

산출:
    <fig>-overlap.json — 라벨별 등급/비율 보고서
    표준 출력: 요약 + overlap/near 항목 리스트
    종료 코드:
        0 = 모든 라벨 안전 (overlap 없음)
        1 = 일부 라벨 overlap
        2 = 컴파일/도구 실패
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Tuple

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow 필요. `pip install Pillow`", file=sys.stderr)
    sys.exit(2)


# 라벨 타입 분류 정규식
_RE_POINT = re.compile(r"^[A-Z](_\d+|_\{[^}]+\})?$")           # A, B, P_1, P_{12}
_RE_DIM = re.compile(r"^[\d.,/+\-*\\\s\^={}()$\\\,a-z]+$")     # 4, 10, 4cm, x+y, \sqrt{2}
_RE_VAR = re.compile(r"^[a-zα-ωθφψ]$|^x$|^y$|^z$")             # x, y, a, θ


def classify_label(text: str) -> str:
    """라벨을 point / dim / other 로 분류.
    - point: 단일 대문자(±첨자) — 정점 이름 (변과 가까움이 정상)
    - dim:   숫자·식·단위 — 길이 치수 (도형과 떨어져야 함, 엄격 검사)
    - other: 기타 변수·각도 — 중간 검사
    """
    s = text.strip().lstrip("$").rstrip("$").strip()
    # \mathrm{A} 형태 정규화
    m = re.match(r"\\mathrm\{([^}]+)\}", s)
    if m:
        s = m.group(1)
    if _RE_POINT.match(s):
        return "point"
    if any(c.isdigit() for c in s) or "cm" in s or "mathrm" in s:
        return "dim"
    if _RE_VAR.match(s):
        return "other"
    return "other"


def compile_tex(tex_path: Path) -> Path:
    cwd = tex_path.parent
    proc = subprocess.run(
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
        cwd=cwd, capture_output=True, text=True
    )
    pdf = tex_path.with_suffix(".pdf")
    if proc.returncode != 0 or not pdf.exists():
        tail = (proc.stdout or "")[-2000:]
        raise RuntimeError(f"pdflatex 실패\n{tail}")
    return pdf


def _win_to_wsl_path(p: str) -> str:
    """C:\\Users\\... 또는 /c/Users/... → /mnt/c/Users/..."""
    p = p.replace("\\", "/")
    if len(p) >= 2 and p[1] == ":":
        return f"/mnt/{p[0].lower()}/{p[3:]}"
    if p.startswith("/") and len(p) >= 3 and p[2] == "/" and p[1].isalpha():
        return f"/mnt/{p[1].lower()}/{p[3:]}"
    return p


def _pdftotext_supports_bbox() -> bool:
    """현재 pdftotext가 -bbox 옵션을 지원하는지 (-h 출력에서 확인)."""
    try:
        proc = subprocess.run(["pdftotext", "-h"], capture_output=True, text=True, timeout=10)
        return "-bbox" in (proc.stdout + proc.stderr)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _run_pdftotext_bbox(pdf_path: Path) -> str:
    """pdftotext -bbox 실행. 로컬이 -bbox 미지원이면 wsl.exe로 폴백."""
    if _pdftotext_supports_bbox():
        proc = subprocess.run(
            ["pdftotext", "-bbox", str(pdf_path), "-"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        if proc.returncode != 0:
            raise RuntimeError(f"pdftotext 실패\n{proc.stderr}")
        return proc.stdout
    # Fallback: WSL의 poppler pdftotext 사용
    wsl_pdf = _win_to_wsl_path(str(pdf_path))
    proc = subprocess.run(
        ["wsl.exe", "-e", "pdftotext", "-bbox", wsl_pdf, "-"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(
            "pdftotext -bbox 실패. 로컬 pdftotext가 xpdf 계열이고 WSL 폴백도 실패함.\n"
            f"stderr: {proc.stderr}"
        )
    return proc.stdout


def extract_bboxes(pdf_path: Path) -> Tuple[list, float, float]:
    """pdftotext -bbox 로 단어 bbox 리스트 + 페이지 크기(pt) 추출.

    pdftotext -bbox 는 origin=top-left, y가 아래로 증가.
    poppler pdftotext만 -bbox 옵션 지원. xpdf 계열은 WSL 폴백 사용.
    """
    text = _run_pdftotext_bbox(pdf_path)
    bboxes = []
    for m in re.finditer(
        r'<word\s+xMin="([-\d.]+)"\s+yMin="([-\d.]+)"\s+xMax="([-\d.]+)"\s+yMax="([-\d.]+)"\s*>([^<]*)</word>',
        text, re.IGNORECASE
    ):
        x0, y0, x1, y1, content = m.groups()
        bboxes.append({
            "text": content.strip(),
            "bbox_pt": [float(x0), float(y0), float(x1), float(y1)],
        })
    page_w = page_h = 0.0
    pm = re.search(r'<page\s+width="([\d.]+)"\s+height="([\d.]+)"', text, re.IGNORECASE)
    if pm:
        page_w, page_h = float(pm.group(1)), float(pm.group(2))
    return bboxes, page_w, page_h


def render_png(pdf_path: Path, dpi: int, suffix: str = "-overlap") -> Path:
    """pdftoppm 로 1쪽 PDF → PNG. <stem><suffix>.png 반환."""
    out_base = pdf_path.with_suffix("")
    out_arg = str(out_base.parent / f"{out_base.name}{suffix}")
    proc = subprocess.run(
        ["pdftoppm", "-png", "-r", str(dpi), "-singlefile", str(pdf_path), out_arg],
        capture_output=True, text=True
    )
    if proc.returncode != 0:
        raise RuntimeError(f"pdftoppm 실패\n{proc.stderr}")
    png = Path(out_arg + ".png")
    if not png.exists():
        raise RuntimeError(f"PNG 생성 실패: {png}")
    return png


def analyze_overlap(
    png_path: Path,
    bboxes: list,
    dpi: int,
    ring_px: int,
    dark_threshold: int,
    dim_overlap_threshold: float,
    point_overlap_threshold: float,
    near_threshold: float = 0.005,
) -> list:
    """라벨 bbox 외곽 ring 영역의 검은 픽셀 비율 측정 + 라벨 타입별 임계.

    - point 라벨(A, B, P_1): 변/점에 가까움이 정상 → 임계 0.20
    - dim 라벨(4, 10, 4cm): 도형과 떨어져야 함 → 임계 0.04
    - other 라벨(x, θ): 중간 임계 0.10

    PNG 좌표 = PIL 좌표 (top-left origin). pdftotext bbox 도 top-left.
    비율 = (ring 검은 픽셀 수) / (ring 전체 픽셀 수).
    """
    img = Image.open(png_path).convert("L")
    W, H = img.size
    px_per_pt = dpi / 72.0
    px_data = img.load()

    type_thresholds = {
        "dim": dim_overlap_threshold,
        "point": point_overlap_threshold,
        "other": (dim_overlap_threshold + point_overlap_threshold) / 2,
    }

    results = []
    for b in bboxes:
        x0p, y0p, x1p, y1p = b["bbox_pt"]
        ix0 = int(round(x0p * px_per_pt))
        iy0 = int(round(y0p * px_per_pt))
        ix1 = int(round(x1p * px_per_pt))
        iy1 = int(round(y1p * px_per_pt))
        if ix1 <= ix0 or iy1 <= iy0:
            continue
        rx0 = max(0, ix0 - ring_px)
        ry0 = max(0, iy0 - ring_px)
        rx1 = min(W, ix1 + ring_px)
        ry1 = min(H, iy1 + ring_px)
        ring_total = 0
        ring_dark = 0
        for y in range(ry0, ry1):
            for x in range(rx0, rx1):
                if ix0 <= x < ix1 and iy0 <= y < iy1:
                    continue
                ring_total += 1
                if px_data[x, y] < dark_threshold:
                    ring_dark += 1
        if ring_total == 0:
            continue
        ratio = ring_dark / ring_total
        label_type = classify_label(b["text"])
        threshold = type_thresholds[label_type]
        if ratio < near_threshold:
            severity = "ok"
        elif ratio < threshold:
            severity = "near"
        else:
            severity = "overlap"
        results.append({
            "text": b["text"],
            "type": label_type,
            "bbox_pt": b["bbox_pt"],
            "bbox_px": [ix0, iy0, ix1, iy1],
            "ring_px": ring_px,
            "ring_dark_ratio": round(ratio, 4),
            "threshold": threshold,
            "severity": severity,
        })
    return results


# ============================================================================
# § F: 마크-점 충돌 검출 (.tex 정적 분석)
# ============================================================================
# 지원하는 점 정의 매크로:
#   \tkzDefPoint(x,y){name}
#   \tkzDefPoint[options](x,y){name}
#   \tkzDefPoints{x1/y1/A, x2/y2/B, ...}
#   \tkzDefMidPoint(P,Q) \tkzGetPoint{name}    (P, Q 좌표 알려진 경우만)
# 지원하는 마크 매크로:
#   \tkzMarkSegment[options](P,Q)
#   \tkzMarkSegments[options](P1,Q1 P2,Q2 ...)


_RE_DEFPOINT = re.compile(
    r"\\tkzDefPoint\s*(?:\[[^\]]*\])?\s*\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*\)\s*\{\s*([A-Za-z_][\w]*)\s*\}"
)
_RE_DEFPOINTS = re.compile(
    r"\\tkzDefPoints\s*\{\s*([^}]+)\s*\}"
)
_RE_MIDPOINT = re.compile(
    r"\\tkzDefMidPoint\s*\(\s*([A-Za-z_][\w]*)\s*,\s*([A-Za-z_][\w]*)\s*\)\s*\\tkzGetPoint\s*\{\s*([A-Za-z_][\w]*)\s*\}"
)
_RE_MARKSEG = re.compile(
    r"\\tkzMarkSegment\s*(?:\[([^\]]*)\])?\s*\(\s*([A-Za-z_][\w]*)\s*,\s*([A-Za-z_][\w]*)\s*\)"
)
_RE_MARKSEGS = re.compile(
    r"\\tkzMarkSegments\s*(?:\[([^\]]*)\])?\s*\(\s*([^)]+)\s*\)"
)
_RE_POS_OPT = re.compile(r"pos\s*=\s*([\d.]+)")


def parse_tex_geometry(tex_path: Path) -> Tuple[dict, list]:
    """tex 파일에서 점 좌표 dict 와 마크 호출 리스트를 추출.

    반환:
        points: {name: (x, y)}  — 알려진 좌표만
        marks:  [{P, Q, pos, options, line}]
    """
    text = tex_path.read_text(encoding="utf-8", errors="replace")
    # 주석 제거 (단순: % 부터 줄 끝, 단 \% 는 보존)
    no_comments = re.sub(r"(?<!\\)%[^\n]*", "", text)

    points: dict = {}

    # 1차: \tkzDefPoint(x,y){name}
    for m in _RE_DEFPOINT.finditer(no_comments):
        x, y, name = m.group(1), m.group(2), m.group(3)
        try:
            points[name] = (float(x), float(y))
        except ValueError:
            pass

    # 2차: \tkzDefPoints{x1/y1/A, x2/y2/B, ...}
    for m in _RE_DEFPOINTS.finditer(no_comments):
        body = m.group(1)
        for entry in body.split(","):
            entry = entry.strip()
            parts = entry.split("/")
            if len(parts) == 3:
                try:
                    x = float(parts[0].strip())
                    y = float(parts[1].strip())
                    name = parts[2].strip()
                    points[name] = (x, y)
                except ValueError:
                    pass

    # 3차: \tkzDefMidPoint(P,Q) \tkzGetPoint{name}  (반복 적용 — 의존성 해결)
    for _ in range(8):
        progressed = False
        for m in _RE_MIDPOINT.finditer(no_comments):
            p, q, name = m.group(1), m.group(2), m.group(3)
            if name in points:
                continue
            if p in points and q in points:
                px, py = points[p]
                qx, qy = points[q]
                points[name] = ((px + qx) / 2, (py + qy) / 2)
                progressed = True
        if not progressed:
            break

    # 마크 추출
    marks = []
    for m in _RE_MARKSEG.finditer(no_comments):
        opts = (m.group(1) or "").strip()
        p, q = m.group(2), m.group(3)
        pos_m = _RE_POS_OPT.search(opts)
        pos = float(pos_m.group(1)) if pos_m else 0.5
        marks.append({"P": p, "Q": q, "pos": pos, "options": opts})

    # \tkzMarkSegments[opt](A,B C,D E,F)
    for m in _RE_MARKSEGS.finditer(no_comments):
        opts = (m.group(1) or "").strip()
        body = m.group(2)
        pos_m = _RE_POS_OPT.search(opts)
        pos = float(pos_m.group(1)) if pos_m else 0.5
        # 공백 구분 페어
        for pair in re.finditer(r"([A-Za-z_]\w*)\s*,\s*([A-Za-z_]\w*)", body):
            marks.append({"P": pair.group(1), "Q": pair.group(2), "pos": pos, "options": opts})

    return points, marks


def analyze_mark_collisions(
    points: dict,
    marks: list,
    pos_dead_zone: float = 0.10,
) -> list:
    """각 마크에 대해, 변 (P,Q) 위에 있는 다른 점들과의 pos 거리 검사.

    반환: [{mark, P, Q, pos, conflicting_points: [(name, point_pos, distance)], ...}]
    """
    results = []
    for mk in marks:
        P, Q = mk["P"], mk["Q"]
        if P not in points or Q not in points:
            results.append({
                "mark": f"\\tkzMarkSegment[pos={mk['pos']}]({P},{Q})",
                "P": P, "Q": Q, "pos": mk["pos"],
                "options": mk["options"],
                "status": "unknown_endpoints",
                "conflicting_points": [],
            })
            continue
        px, py = points[P]
        qx, qy = points[Q]
        vx, vy = qx - px, qy - py
        L2 = vx * vx + vy * vy
        if L2 == 0:
            continue
        L = L2 ** 0.5
        # 마크 좌표 (시각용, 보고서에 포함)
        mx = px + mk["pos"] * vx
        my = py + mk["pos"] * vy

        conflicts = []
        for name, (xx, yy) in points.items():
            if name == P or name == Q:
                continue
            # name 이 변 (P,Q) 위에 있는가? (pos 가 [0, 1] 범위 + 수직 거리 < ε·L)
            wx, wy = xx - px, yy - py
            t = (wx * vx + wy * vy) / L2
            if t < -0.05 or t > 1.05:
                continue
            # 수직 거리
            perp_x = wx - t * vx
            perp_y = wy - t * vy
            perp_dist = (perp_x * perp_x + perp_y * perp_y) ** 0.5
            if perp_dist > 0.05 * L:   # 변에서 5% 이상 떨어졌으면 변 위 아님
                continue
            # 이 점은 변 위에 있다. 마크 pos 와의 pos 거리 검사
            pos_dist = abs(t - mk["pos"])
            if pos_dist < pos_dead_zone:
                conflicts.append({
                    "point": name,
                    "point_pos": round(t, 3),
                    "pos_distance": round(pos_dist, 3),
                    "linear_distance_cm": round(pos_dist * L, 3),
                })

        results.append({
            "mark": f"\\tkzMarkSegment[pos={mk['pos']}]({P},{Q})",
            "P": P, "Q": Q, "pos": mk["pos"],
            "options": mk["options"],
            "edge_length_cm": round(L, 3),
            "mark_xy": [round(mx, 3), round(my, 3)],
            "status": "collision" if conflicts else "ok",
            "conflicting_points": conflicts,
        })
    return results


def suggest_mark_pos_fix(
    mark_result: dict,
    points: dict,
) -> str:
    """충돌하는 마크에 대해 § F.3 lookup 기반 pos 권장값 반환.

    가용 영역 (0.10, 0.90) − dead zones[obstacle_pos ± 0.10] 에서 0.5 가까운 값.
    """
    P, Q = mark_result["P"], mark_result["Q"]
    if P not in points or Q not in points:
        return "(좌표 미상 — § F.3 lookup 표 참조)"
    px, py = points[P]
    qx, qy = points[Q]
    vx, vy = qx - px, qy - py
    L2 = vx * vx + vy * vy
    if L2 == 0:
        return "(영변)"
    # 변 위 obstacle pos
    obstacles = []
    for name, (xx, yy) in points.items():
        if name == P or name == Q:
            continue
        wx, wy = xx - px, yy - py
        t = (wx * vx + wy * vy) / L2
        if 0.05 < t < 0.95:
            perp = ((wx - t * vx) ** 2 + (wy - t * vy) ** 2) ** 0.5
            if perp <= 0.05 * L2 ** 0.5:
                obstacles.append(t)
    obstacles.sort()
    # 가용 영역 sub-segments
    intervals = [(0.10, 0.90)]
    for o in obstacles:
        new_intervals = []
        for (a, b) in intervals:
            lo = o - 0.10
            hi = o + 0.10
            if hi <= a or lo >= b:
                new_intervals.append((a, b))
            else:
                if a < lo:
                    new_intervals.append((a, lo))
                if hi < b:
                    new_intervals.append((hi, b))
        intervals = new_intervals
    if not intervals:
        return "(가용 영역 없음 — § F.5 참조: dim 라벨 외측 호 격하 또는 마크 종류 축소)"
    # 0.5 가까운 sub-segment 의 중점
    best = min(intervals, key=lambda iv: abs((iv[0] + iv[1]) / 2 - 0.5))
    candidate = round((best[0] + best[1]) / 2, 2)
    return f"pos={candidate} (가용 영역 {[(round(a, 2), round(b, 2)) for a, b in intervals]})"


def main() -> int:
    ap = argparse.ArgumentParser(description="gf2 라벨-도형 겹침 자동 검증")
    ap.add_argument("tex", help="입력 .tex 파일 경로")
    ap.add_argument("--dpi", type=int, default=200, help="PNG 렌더링 해상도(기본 200)")
    ap.add_argument("--ring-px", type=int, default=6, help="라벨 외곽 ring 픽셀 두께(기본 6)")
    ap.add_argument("--dark-threshold", type=int, default=80,
                    help="0-255, 이 값 미만이면 검은 픽셀로 판정(기본 80)")
    ap.add_argument("--dim-threshold", type=float, default=0.025,
                    help="dim(치수) 라벨 ring 검은 픽셀 비율 임계(기본 0.025 = 2.5%%)")
    ap.add_argument("--point-threshold", type=float, default=0.20,
                    help="point(정점) 라벨 ring 검은 픽셀 비율 임계(기본 0.20 = 20%%)")
    ap.add_argument("--report", help="JSON 보고서 출력 경로(기본: <fig>-overlap.json)")
    ap.add_argument("--no-compile", action="store_true",
                    help="이미 PDF가 있으면 컴파일 스킵")
    ap.add_argument("--no-mark-check", action="store_true",
                    help="§ F 마크-점 충돌 정적 분석 스킵")
    ap.add_argument("--mark-pos-dead-zone", type=float, default=0.10,
                    help="마크 pos 와 점 pos 의 충돌 임계 (기본 0.10)")
    args = ap.parse_args()

    tex_path = Path(args.tex).resolve()
    if not tex_path.exists():
        print(f"ERROR: {tex_path} not found", file=sys.stderr)
        return 2

    pdf_path = tex_path.with_suffix(".pdf")
    if not args.no_compile or not pdf_path.exists():
        try:
            pdf_path = compile_tex(tex_path)
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            return 2

    try:
        bboxes, page_w, page_h = extract_bboxes(pdf_path)
        png_path = render_png(pdf_path, args.dpi)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        return 2

    results = analyze_overlap(
        png_path, bboxes, args.dpi, args.ring_px,
        args.dark_threshold, args.dim_threshold, args.point_threshold,
    )

    # dim 라벨의 overlap만 critical (실패 신호). point overlap은 정보용.
    overlaps_dim = [r for r in results if r["severity"] == "overlap" and r["type"] == "dim"]
    overlaps_other = [r for r in results if r["severity"] == "overlap" and r["type"] != "dim"]
    nears = [r for r in results if r["severity"] == "near"]

    # § F: 마크-점 충돌 정적 분석
    mark_collisions = []
    mark_results = []
    points_dict: dict = {}
    if not args.no_mark_check:
        try:
            points_dict, marks = parse_tex_geometry(tex_path)
            mark_results = analyze_mark_collisions(points_dict, marks, args.mark_pos_dead_zone)
            for mr in mark_results:
                if mr["status"] == "collision":
                    mr["suggested_fix"] = suggest_mark_pos_fix(mr, points_dict)
                    mark_collisions.append(mr)
        except (OSError, UnicodeDecodeError) as e:
            print(f"WARN: 마크 분석 실패: {e}", file=sys.stderr)

    report = {
        "tex": str(tex_path),
        "pdf": str(pdf_path),
        "png": str(png_path),
        "page_pt": [page_w, page_h],
        "dpi": args.dpi,
        "ring_px": args.ring_px,
        "dark_threshold": args.dark_threshold,
        "dim_threshold": args.dim_threshold,
        "point_threshold": args.point_threshold,
        "mark_pos_dead_zone": args.mark_pos_dead_zone,
        "labels_total": len(results),
        "dim_overlaps_count": len(overlaps_dim),
        "other_overlaps_count": len(overlaps_other),
        "nears_count": len(nears),
        "marks_total": len(mark_results),
        "mark_collisions_count": len(mark_collisions),
        "labels": results,
        "marks": mark_results,
        "known_points": list(points_dict.keys()) if points_dict else [],
    }
    report_path = Path(args.report) if args.report else tex_path.with_name(tex_path.stem + "-overlap.json")
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    # ASCII-only output for terminals with cp949
    print(f"PNG: {png_path}")
    print(f"REPORT: {report_path}")
    print(
        f"labels={len(results)} | dim_overlaps={len(overlaps_dim)} | "
        f"other_overlaps={len(overlaps_other)} | nears={len(nears)} | "
        f"marks={len(mark_results)} | mark_collisions={len(mark_collisions)}"
    )
    for r in overlaps_dim + overlaps_other + nears:
        print(f"  [{r['severity']:>7}/{r['type']:>5}] '{r['text']}' ring={r['ring_dark_ratio']:.4f} (thr={r['threshold']:.2f})")
    for mc in mark_collisions:
        cps = ", ".join(f"{c['point']}@{c['point_pos']:.2f}(dist={c['linear_distance_cm']}cm)" for c in mc["conflicting_points"])
        print(f"  [MARK    ] {mc['mark']} L={mc['edge_length_cm']}cm | conflicts: {cps}")
        print(f"            -> 권장: {mc['suggested_fix']}")

    failed = bool(overlaps_dim or mark_collisions)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
