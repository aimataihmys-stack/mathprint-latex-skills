#!/usr/bin/env python3
"""Static checks for Gratik Korean exam-style PGFplots TeX."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Issue:
    severity: str
    line: int
    message: str


@dataclass
class FunctionPlot:
    line: int
    expression: str
    domain_min: float | None
    domain_max: float | None


def line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def axis_blocks(text: str) -> list[tuple[int, str]]:
    blocks: list[tuple[int, str]] = []
    pattern = re.compile(r"\\begin\{axis\}(\[[\s\S]*?\])?([\s\S]*?)\\end\{axis\}")
    for match in pattern.finditer(text):
        blocks.append((line_number(text, match.start()), match.group(0)))
    return blocks


def extract_axis_options(block: str) -> str:
    """Return the balanced ``[...]`` option list after ``\\begin{axis}``, handling
    nested brackets such as ``-{Stealth[length=...]}`` arrow tips so the header is
    not truncated at the first ``]``."""
    start = block.find("[")
    if start == -1:
        return block
    depth = 0
    for i in range(start, len(block)):
        c = block[i]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return block[start + 1 : i]
    return block[start + 1 :]


def addplot_options(command: str) -> str:
    match = re.search(r"\\addplot\s*(?:\+)?\s*\[([\s\S]*?)\]", command)
    return match.group(1) if match else ""


def addplot_commands(block: str, start_line: int) -> list[tuple[int, str]]:
    commands: list[tuple[int, str]] = []
    for match in re.finditer(r"\\addplot\s*(?:\+)?[\s\S]*?;", block):
        commands.append((start_line + block.count("\n", 0, match.start()), match.group(0)))
    return commands


def draw_commands(block: str, start_line: int) -> list[tuple[int, str]]:
    commands: list[tuple[int, str]] = []
    for match in re.finditer(r"\\draw(?:\s*\[[\s\S]*?\])?[\s\S]*?;", block):
        commands.append((start_line + block.count("\n", 0, match.start()), match.group(0)))
    return commands


def node_commands(block: str, start_line: int) -> list[tuple[int, str, float, float, str]]:
    commands: list[tuple[int, str, float, float, str]] = []
    pattern = re.compile(
        r"\\node\s*(?:\[([\s\S]*?)\])?\s*"
        r"(?:\([A-Za-z][A-Za-z0-9_-]*\)\s*)?at\s*"
        r"\(\s*axis cs:\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)"
        r"\s*\{([\s\S]*?)\}\s*;",
    )
    for match in pattern.finditer(block):
        options = match.group(1) or ""
        x = float(match.group(2))
        y = float(match.group(3))
        content = match.group(4).strip()
        commands.append((start_line + block.count("\n", 0, match.start()), options, x, y, content))
    return commands


def is_function_addplot(command: str) -> bool:
    if "\\addplot" not in command:
        return False
    if any(token in command for token in ("coordinates", "table", "only marks", "fill between")):
        return False
    return "{" in command or command.rstrip().endswith(";")


def function_plots(block: str, start_line: int) -> list[FunctionPlot]:
    plots: list[FunctionPlot] = []
    for command_line, command in addplot_commands(block, start_line):
        if not is_function_addplot(command):
            continue

        expression_match = re.search(r"\{([^{}]+)\}\s*;", command)
        if expression_match is None:
            continue

        options = addplot_options(command)
        domain_min: float | None = None
        domain_max: float | None = None
        domain_match = re.search(
            r"domain\s*=\s*(-?\d+(?:\.\d+)?)\s*:\s*(-?\d+(?:\.\d+)?)",
            options,
        )
        if domain_match:
            domain_min = float(domain_match.group(1))
            domain_max = float(domain_match.group(2))

        plots.append(FunctionPlot(command_line, expression_match.group(1).strip(), domain_min, domain_max))
    return plots


def evaluate_simple_expression(expression: str, x: float) -> float | None:
    expression = expression.strip().replace("^", "**")
    if not re.fullmatch(r"[0-9xX+\-*/().\s*]+", expression):
        return None
    try:
        value = eval(expression, {"__builtins__": {}}, {"x": x, "X": x})
    except Exception:
        return None
    return float(value) if isinstance(value, (int, float)) else None


def point_on_function_plot(x: float, y: float, plot: FunctionPlot) -> bool:
    if plot.domain_min is not None and x < min(plot.domain_min, plot.domain_max or plot.domain_min) - 1e-6:
        return False
    if plot.domain_max is not None and x > max(plot.domain_min or plot.domain_max, plot.domain_max) + 1e-6:
        return False

    value = evaluate_simple_expression(plot.expression, x)
    if value is None:
        return False
    return abs(value - y) <= 1e-3


def approximate_visible_x_interval(
    expression: str,
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
) -> tuple[float, float] | None:
    axis_min = min(xmin, xmax)
    axis_max = max(xmin, xmax)
    y_min = min(ymin, ymax)
    y_max = max(ymin, ymax)
    steps = 1200
    visible: list[float] = []
    for index in range(steps + 1):
        x = axis_min + (axis_max - axis_min) * index / steps
        y = evaluate_simple_expression(expression, x)
        if y is None:
            return None
        if y_min - 1e-6 <= y <= y_max + 1e-6:
            visible.append(x)

    if not visible:
        return None
    return min(visible), max(visible)


def marked_coordinates(block: str) -> set[tuple[float, float]]:
    coords: set[tuple[float, float]] = set()
    for _, command in addplot_commands(block, 1):
        if "only marks" not in command:
            continue
        for x, y in re.findall(r"\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)", command):
            coords.add((float(x), float(y)))
    return coords


def draw_segments(block: str) -> list[tuple[float, float, float, float]]:
    segments: list[tuple[float, float, float, float]] = []
    pattern = re.compile(
        r"\\draw[\s\S]*?"
        r"\(\s*axis cs:\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)"
        r"\s*--\s*"
        r"\(\s*axis cs:\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*\)"
        r"[\s\S]*?;",
    )
    for match in pattern.finditer(block):
        segments.append(tuple(float(v) for v in match.groups()))
    return segments


def point_on_segment(x: float, y: float, segment: tuple[float, float, float, float]) -> bool:
    x1, y1, x2, y2 = segment
    dx = x2 - x1
    dy = y2 - y1
    cross = (x - x1) * dy - (y - y1) * dx
    if abs(cross) > 1e-6:
        return False
    return min(x1, x2) - 1e-6 <= x <= max(x1, x2) + 1e-6 and min(y1, y2) - 1e-6 <= y <= max(y1, y2) + 1e-6


def has_explicit_shift(options: str) -> bool:
    return "xshift" in options or "yshift" in options


def has_semantic_label_style(options: str) -> bool:
    return any(token in options for token in ("pointLabel", "graphLabel", "axisLabel", "fill=white"))


def has_direction(options: str) -> bool:
    return any(token in options for token in ("anchor=", "above", "below", "left", "right"))


def is_leader_arrow_draw(command: str) -> bool:
    options = ""
    match = re.search(r"\\draw\s*\[([\s\S]*?)\]", command)
    if match:
        options = match.group(1).replace(" ", "").replace("\n", "")
    return "leaderArrow" in command or "->" in options


def uses_node_anchor_endpoint(command: str) -> bool:
    return re.search(r"\([A-Za-z][A-Za-z0-9_-]*\.[A-Za-z ]+\)", command) is not None


def uses_straight_leader_path(command: str) -> bool:
    if "leaderArrow" not in command:
        return False
    if "--" not in command:
        return False
    return re.search(r"\bto\s*\[", command) is None and ".." not in command


def expression_can_need_restricted_domain(expression: str) -> bool:
    compact = expression.replace(" ", "").lower()
    if any(token in compact for token in ("sqrt", "ln", "log", "tan", "asin", "acos")):
        return True
    return re.search(r"/\(?x", compact) is not None


def has_domain_restriction_note(block: str, command_line: int, start_line: int) -> bool:
    lines = block.splitlines()
    local_line = max(0, command_line - start_line)
    window = lines[max(0, local_line - 2) : min(len(lines), local_line + 3)]
    # textbook 짧은-호 도메인은 의도적 — 두 주석 형식 모두 인정
    return any(
        ("gratik-domain-restricted" in line) or ("gratik-domain-textbook-arc" in line)
        for line in window
    )


def axis_option_float(axis_header: str, key: str) -> float | None:
    match = re.search(rf"\b{key}\s*=\s*(-?\d+(?:\.\d+)?)", axis_header)
    return float(match.group(1)) if match else None


def check_file(path: Path) -> list[Issue]:
    text = path.read_text(encoding="utf-8")
    issues: list[Issue] = []

    if "\\begin{axis}" in text:
        if "\\usepackage{pgfplots}" not in text:
            issues.append(Issue("error", 1, "pgfplots axis is used without \\usepackage{pgfplots}."))
        if "\\pgfplotsset{compat=" not in text:
            issues.append(Issue("warning", 1, "Missing explicit \\pgfplotsset{compat=...}; use compat=1.18."))

    if "\\draw[leaderArrow" in text or "\\draw [leaderArrow" in text:
        if "leaderArrow/.style" not in text:
            issues.append(Issue("warning", 1, "Leader arrows should use a named `leaderArrow/.style` definition."))
        if "shorten >=" not in text:
            issues.append(Issue("warning", 1, "Leader arrows should use `shorten >=1pt` so they do not cover targets."))

    for style_name in ("pointLabel", "graphLabel", "axisLabel"):
        pattern = re.compile(rf"{style_name}/\.style\s*=\s*\{{([^}}]*)\}}")
        for match in pattern.finditer(text):
            if "fill=white" in match.group(1).replace(" ", ""):
                issues.append(
                    Issue(
                        "warning",
                        line_number(text, match.start()),
                        f"`{style_name}` should not include `fill=white` by default; move labels to empty space instead.",
                    )
                )

    blocks = axis_blocks(text)
    if not blocks:
        issues.append(Issue("warning", 1, "No pgfplots axis environment found; pure TikZ is OK only for very simple axes."))
        return issues

    for start_line, block in blocks:
        axis_header = extract_axis_options(block)
        # textbook 프리셋: 격자·눈금 없는 에듀넷 축. 값 노드/수식 라벨은 직접 font 노드를
        # 축·가이드 위에 두는 것이 표준이므로 해당 경고들을 완화한다.
        textbook = (
            "xtick=\\empty" in axis_header.replace(" ", "")
            or "ytick=\\empty" in axis_header.replace(" ", "")
        )
        marks = marked_coordinates(block)
        segments = draw_segments(block)
        plots = function_plots(block, start_line)
        has_center_axes = any(
            token in axis_header
            for token in ("axis lines=middle", "axis x line=center", "axis x line=middle")
        )
        if not has_center_axes:
            issues.append(Issue("warning", start_line, "Coordinate-plane axis should use centered axes."))

        for key in ("xmin", "xmax", "ymin", "ymax", "xtick", "ytick"):
            if re.search(rf"\b{key}\s*=", axis_header) is None:
                issues.append(Issue("warning", start_line, f"Axis option `{key}=...` should be explicit."))

        if "grid" in axis_header:
            if "gray!30" not in axis_header or "densely dotted" not in axis_header:
                issues.append(Issue("warning", start_line, "Grid should usually be `very thin, gray!30, densely dotted`."))

        leader_arrows = [(line, command) for line, command in draw_commands(block, start_line) if is_leader_arrow_draw(command)]
        if len(leader_arrows) > 2:
            issues.append(
                Issue(
                    "warning",
                    leader_arrows[2][0],
                    "Leader arrows should be rare; prefer moving labels, expanding margins, or shortening labels.",
                )
            )
        for leader_line, leader_command in leader_arrows:
            if uses_node_anchor_endpoint(leader_command):
                issues.append(
                    Issue(
                        "warning",
                        leader_line,
                        "Leader arrow uses a text-node anchor; draw from an explicit clear coordinate before the label node.",
                    )
                )
            if uses_straight_leader_path(leader_command):
                issues.append(
                    Issue(
                        "warning",
                        leader_line,
                        "Leader arrow is straight; prefer a gentle curved route such as `to[out=...,in=...]`.",
                    )
                )

        has_origin_label = any(token in block for token in ("\\mathrm{O}", "{$O$}", "{$0$}", "{0}"))
        if not has_origin_label:
            issues.append(Issue("warning", start_line, "Origin label `\\mathrm{O}` or data-graph origin `0` is missing."))
        elif "below left" in block and "axis cs:0,0" in block:
            ymin = axis_option_float(axis_header, "ymin")
            ymax = axis_option_float(axis_header, "ymax")
            if ymin is not None and ymax is not None and ymin < 0 < ymax:
                lower_fraction = abs(ymin) / (ymax - ymin)
                if lower_fraction < 0.08:
                    issues.append(
                        Issue(
                            "warning",
                            start_line,
                            "Origin label has low bottom clearance; lower `ymin` or move the label.",
                        )
                    )
            if "clip=false" not in axis_header:
                issues.append(
                    Issue(
                        "warning",
                        start_line,
                        "Boundary labels such as origin `O` should use `clip=false` to avoid axis clipping.",
                    )
                )

        for command_line, command in addplot_commands(block, start_line):
            if is_function_addplot(command):
                options = addplot_options(command)
                compact_options = options.replace(" ", "").replace("\n", "")
                if "mark=none" not in compact_options and "onlymarks" not in compact_options:
                    issues.append(Issue("warning", command_line, "Function addplot should include `mark=none`."))
                sample_match = re.search(r"samples\s*=\s*(\d+)", options)
                if sample_match is None:
                    issues.append(Issue("warning", command_line, "Function addplot should specify `samples`, usually 201."))
                elif int(sample_match.group(1)) < 100 and "samples=2" not in compact_options:
                    issues.append(Issue("warning", command_line, "Curved function plots should usually use at least 100 samples."))

                xmin = axis_option_float(axis_header, "xmin")
                xmax = axis_option_float(axis_header, "xmax")
                ymin = axis_option_float(axis_header, "ymin")
                ymax = axis_option_float(axis_header, "ymax")
                domain_match = re.search(
                    r"domain\s*=\s*(-?\d+(?:\.\d+)?)\s*:\s*(-?\d+(?:\.\d+)?)",
                    options,
                )
                expression_match = re.search(r"\{([^{}]+)\}\s*;", command)
                if (
                    xmin is not None
                    and xmax is not None
                    and ymin is not None
                    and ymax is not None
                    and domain_match
                    and expression_match
                ):
                    domain_min = float(domain_match.group(1))
                    domain_max = float(domain_match.group(2))
                    axis_min = min(xmin, xmax)
                    axis_max = max(xmin, xmax)
                    plot_min = min(domain_min, domain_max)
                    plot_max = max(domain_min, domain_max)
                    tolerance = max((axis_max - axis_min) * 0.02, 1e-6)
                    has_reason = has_domain_restriction_note(block, command_line, start_line)
                    expression = expression_match.group(1)
                    has_natural_limit = expression_can_need_restricted_domain(expression)
                    visible_interval = None if has_natural_limit else approximate_visible_x_interval(expression, xmin, xmax, ymin, ymax)
                    if visible_interval is None:
                        if plot_min < axis_min - tolerance or plot_max > axis_max + tolerance:
                            issues.append(
                                Issue(
                                    "warning",
                                    command_line,
                                    "Function domain extends outside `xmin:xmax`; keep plots inside the coordinate plane unless explicitly needed.",
                                )
                            )
                        elif (
                            (plot_min > axis_min + tolerance or plot_max < axis_max - tolerance)
                            and not has_reason
                            and not has_natural_limit
                        ):
                            issues.append(
                                Issue(
                                    "warning",
                                    command_line,
                                    "Function domain is narrower than `xmin:xmax`; use the full visible range or add `% gratik-domain-restricted: reason`.",
                                )
                            )
                    else:
                        visible_min, visible_max = visible_interval
                        if plot_min < visible_min - tolerance or plot_max > visible_max + tolerance:
                            issues.append(
                                Issue(
                                    "warning",
                                    command_line,
                                    "Function domain extends beyond the visible coordinate rectangle; restrict to the boundary intersections.",
                                )
                            )
                        elif (plot_min > visible_min + tolerance or plot_max < visible_max - tolerance) and not has_reason:
                            issues.append(
                                Issue(
                                    "warning",
                                    command_line,
                                    "Function domain is narrower than the maximal visible graph interval; extend it or add `% gratik-domain-restricted: reason`.",
                                )
                            )

        origin_tokens = ("$\\mathrm{O}$", "$O$", "$0$", "0")
        for node_line, options, x, y, content in node_commands(block, start_line):
            if not content:
                continue
            is_origin = content in origin_tokens
            if not has_direction(options):
                issues.append(Issue("warning", node_line, "Text node should specify an outward anchor or direction."))
            # textbook: 값 노드/수식 라벨은 직접 font 노드를 표준으로 쓴다 → semantic-style 요구 생략
            if not textbook and not has_semantic_label_style(options):
                issues.append(Issue("warning", node_line, "Text node should use pointLabel/graphLabel/axisLabel."))
            if (x, y) in marks and not has_explicit_shift(options):
                issues.append(Issue("warning", node_line, "Text label sits on a plotted point; move it clear and add explicit xshift/yshift."))
            # textbook 값 노드는 점선 L-가이드 발치/축 위에 의도적으로 배치 → guide/axis 세그먼트 경고 생략
            if not textbook and any(point_on_segment(x, y, segment) for segment in segments) and not has_explicit_shift(options):
                issues.append(Issue("warning", node_line, "Text label sits on a guide/axis segment; move it clear and add explicit xshift/yshift."))
            # 곡선 마스킹 검사: 원점 라벨 O는 곡선이 원점을 지나도 관례상 허용 → 제외
            if not is_origin and any(point_on_function_plot(x, y, plot) for plot in plots) and not has_explicit_shift(options):
                issues.append(
                    Issue(
                        "warning",
                        node_line,
                        "Text label is anchored on a plotted curve/line; move it clear instead of masking the graph.",
                    )
                )
            # textbook 값 노드는 축 위에 두는 것이 표준 → 축-앵커 경고 생략 (exam만 적용)
            if not textbook and not is_origin and (abs(x) <= 1e-9 or abs(y) <= 1e-9):
                if not has_explicit_shift(options):
                    issues.append(Issue("warning", node_line, "Text label is anchored on an axis; move it clear and add explicit shift."))

        for offset, line in enumerate(block.splitlines(), start=start_line):
            stripped = line.strip()
            if not stripped or stripped.startswith("%"):
                continue

            if ("\\node" in stripped or "\\draw" in stripped) and "axis cs:" not in stripped:
                if re.search(r"\(\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?", stripped):
                    issues.append(Issue("error", offset, "Manual node/draw inside axis must use `(axis cs:x,y)`."))

    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("tex_file", type=Path)
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    args = parser.parse_args()

    issues = check_file(args.tex_file)
    if not issues:
        print(f"PASS {args.tex_file}")
        return 0

    for issue in issues:
        print(f"{issue.severity.upper()}:{args.tex_file}:{issue.line}: {issue.message}")

    has_error = any(issue.severity == "error" for issue in issues)
    has_warning = any(issue.severity == "warning" for issue in issues)
    return 1 if has_error or (args.strict and has_warning) else 0


if __name__ == "__main__":
    sys.exit(main())
