---
name: gratik
description: Generate accurate TikZ/PGFplots coordinate planes and function graphs for Korean middle-school, high-school, textbook, EBS, and Suneung-style math materials. Use for coordinate axes, grids, ticks, plotted functions, points, guide lines, shaded regions, asymptotes, open/closed endpoints, and graph labels; prefer gf2/tkz-euclide instead for pure Euclidean geometry without coordinate axes.
---

# Gratik

## Core Rule

Use `pgfplots` for nearly all coordinate-plane and function-graph work. Use pure TikZ only for very simple middle-school axes with points/segments and no plotted function.

Always preserve mathematical accuracy before aesthetics:

1. Specify `xmin`, `xmax`, `ymin`, `ymax`, `xtick`, and `ytick`.
2. Use `(axis cs:x,y)` for every `\node`, `\draw`, and manual point inside `axis`.
3. Use `axis equal image` when one x-unit must equal one y-unit visually.
4. Use `mark=none`, explicit `domain`, and `samples=201` for function plots unless the graph is a straight line or data plot.
5. By default, draw each function over the maximum visible part of the coordinate plane. Use `domain=xmin:xmax` when the graph stays inside `ymin:ymax`; otherwise restrict only to the largest interval that remains inside the visible coordinate rectangle.
6. Keep label clearance around the plot edges. If `\mathrm{O}`, `x`, `y`, or point labels sit near an axis boundary, increase the relevant `xmin/xmax/ymin/ymax` margin and set `clip=false`.
7. Text must never obscure the graph. Labels may explain points, curves, axes, regions, and guide lines, but they must not cover or mask any visible graph stroke, marker, tick, arrowhead, or guide segment.
8. Treat non-overlap as a global contract: points, curves, guide lines, axes, tick labels, and text labels must not visually collide. Solve this by placement first; leader arrows are a last resort.
9. Draw in this order: shaded regions, grid/axes, guide lines, main curves, points, labels.
10. **Deliverable contract**: every invocation must produce *three* artifacts — the `.tex` source, the compiled `.pdf`, and a rendered `.png` preview. After writing the TeX, run `python3 .claude/skills/gratik/scripts/render-tex.py <file>.tex` and show the resulting PNG to the user via the Read tool. See §6 below.

Read `references/ingested-pgfplots-kias.md` when you need the PDF-derived source notes. Read `references/templates.md` when you need complete reusable TeX templates. Read `docs/superpowers/specs/gratik-design-system.md` for the full 5-preset master table (all values measured against KICE/EBS PDFs, `research/measurements.csv` rows M01-M07 and M11).

## Workflow

### 1. Classify The Figure

- **Suneung/high-school function graph**: pgfplots, centered axes, minimal or no grid, sparse ticks, black or one accent color.
- **Middle-school coordinate plane**: pgfplots with `axis equal image`, integer ticks, optional light dotted grid.
- **Textbook/EBS graph**: pgfplots with light dotted grid and at most one accent color.
- **Simple axes only**: pure TikZ is acceptable if there is no function, data table, shaded region, or axis scaling issue.

### 2. Choose The Style

Five preset names align with `research/DESIGN-SYSTEM.md` and `docs/superpowers/specs/gratik-design-system.md`.

**Default selection by target** (중요):
- 중학교(중1–중3) · 에듀넷/KERIS · 검정교과서 자료, 또는 수준 미지정 중학 요청 → **`textbook`** (중학 기본)
- 수능 · 평가원 · 모의평가 · 고등 → **`exam`**
- 명시된 프리셋이 있으면 그것을 우선.

`exam` 프리셋 수치(축 0.55 / 틱 0.35 / 곡선 0.55pt, no grid, `\scriptsize`, black)는 KICE/EBS 실측 정합으로 **동결(변경 금지)**. `worksheet` is a deprecated alias for `workbook`.

| Preset | Use | Axis | Tick | Curve | Guide | Grid | Tick label | Curve color |
|---|---|---:|---:|---:|---:|---|---|---|
| `exam` | 수능/평가원/모의평가 | `0.55pt` | `0.35pt` | `0.55pt` | `0.40pt` | none | `\scriptsize` | black |
| `textbook` | **중학 교과서/에듀넷·EBS (중학 기본)** | `0.40pt` | **none** | `0.50pt` | `0.30pt dashed gray!70` | **none** | 값 노드만 `\footnotesize` | black (강조 `black!65`) |
| `workbook` | 문제집(쎈·마플·블랙라벨) | `0.60pt` | `0.35pt` | `0.60pt` | `0.40pt` | optional `gray!20 densely dotted` | `\footnotesize` | black |
| `academy` | 학원 자체제작 프린트 | `0.50pt` | `0.30pt` | `0.50pt` | `0.35pt` | none | `\scriptsize` | black |
| `modern` | IB·디지털 교재 | `0.80pt` | `0.50pt` | `0.85pt` | `0.60pt` | `gray!25 densely dotted` | `\footnotesize` | black + accent |

> **★ `textbook` 프리셋 = 에듀넷 중3 교과서 정합** (2026-05 분석). 핵심 차이: 축이 곡선보다 **가늘다**(0.40 < 0.50pt); **격자·눈금 둘 다 없음**; 양(+)끝에만 화살표; 수치는 균일 눈금자 대신 **문제 관련점에만 값 노드 + 점선 L-가이드**; 곡선은 **짧은 호**(전폭 아님). 선 굵기는 시작값이며 §6 렌더-비교로 보정(레퍼런스 도형이 저해상도 래스터라 벡터 측정 불가). 자세한 축 블록은 §3, 수식 라벨은 §4.5 참조.

`accent` color is preset-bound: textbook `#FF6B35`(선택적 곡선 색 한정 — fill로 사용 금지), workbook `#1E6FB8`, modern `#2563EB`. 강조 **채움**은 `gratikEmph`(orange!35, §5) 사용. See gratik-design-system.md §6.

Origin: `\mathrm{O}`. Axes: italic `$x$`, `$y$`. Named points: upright roman, e.g. `$\mathrm{P}$`.

### 3. Build The Axis

Canonical pgfplots preamble:

```latex
\documentclass[border=10pt]{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepgfplotslibrary{fillbetween} % only when shading between paths
\usetikzlibrary{arrows.meta}     % textbook 축의 -{Stealth[...]} 단일 화살촉에 필요
```

Canonical axis options:

```latex
\begin{axis}[
  axis lines=middle,
  axis line style={-stealth, line width=0.6pt},
  xlabel={$x$}, ylabel={$y$},
  xlabel style={below right},
  ylabel style={above left},
  xmin=-4.5, xmax=4.5,
  ymin=-4.5, ymax=4.5,
  xtick={-4,-3,...,4},
  ytick={-4,-3,...,4},
  tick style={line width=0.4pt, black},
  tick label style={font=\scriptsize},
  width=7cm,
  height=7cm,
  axis equal image,
  clip=false
]
```

**`textbook` axis block (에듀넷 중3 정합 — 격자·눈금 없음, 양끝 화살표만, italic x/y, O 우하)**:

```latex
\begin{axis}[
  width=4.5cm, height=4.5cm,                 % 근정사각, 콤팩트
  axis lines=middle,
  axis line style={black, line width=0.4pt, -{Stealth[length=2.2mm,width=1.6mm]}}, % 양(+)끝만 화살표
  xtick=\empty, ytick=\empty,                % ★ 눈금 없음 + 격자 없음
  enlarge x limits=0.15, enlarge y limits=0.15,  % 곡선 밖 ~15% 여백
  clip=false,
  xlabel={$x$}, ylabel={$y$},
  xlabel style={anchor=north, font=\itshape},  % x = x화살표 우하
  ylabel style={anchor=east,  font=\itshape},  % y = y화살표 좌상
]
  \node[anchor=north west, font=\footnotesize] at (axis cs:0,0) {$\mathrm{O}$}; % O 우하, 숫자 0 억제
  \addplot[black, mark=none, line width=0.5pt, samples=120, domain=-3:3] {x^2-9}; % 곡선이 축보다 굵음
% 이후: 짧은-호 \addplot(§4), 문제 관련점 값 노드 + 점선 L-가이드(§4), gratikEmph 채움(§5)
```

`pgfplots`의 `axis lines=middle`는 양(+)끝에만 화살표를 그린다 — 음(−)끝에 역방향 화살표를 추가하지 말 것. 단순 bare-axis 도형은 raw TikZ도 허용.

Rules:

- Hide the numeric 0 when showing `\mathrm{O}` as the origin label.
- **원점 O 앵커**: `textbook` 기본은 **우하**(`anchor=north west` → O가 원점 우하에 위치), 숫자 0 항상 억제. 원점 **우하 사분면이 곡선·점·음영으로 점유**되면 좌하(`anchor=north east`)로 flip(렌더 확인). `exam`에서 O가 `below left`일 때는 x축 아래 ≥10% y-범위 확보(8–12%, 기본 10%; 예: `ymax=13`이면 `ymin<=-1.3`).
- `standalone` border does not fix labels clipped by the `axis` rectangle. Add both enough data-space margin and `clip=false` for boundary labels.
- **축 라벨 x/y**: bare italic 단일 문자. `textbook`은 `xlabel style={anchor=north, font=\itshape}`(x화살표 우하), `ylabel style={anchor=east, font=\itshape}`(y화살표 좌상). 한국어 'x축'/'y축'·회전 축제목·괄호 금지. `exam`은 `below right`/`above left` 사용.
- **눈금 정책 (프리셋 분기)**: `exam`/`workbook`은 4–8개 라벨 눈금 유지. **`textbook`은 균일 눈금자 없음**(`xtick=\empty, ytick=\empty`) — 수치는 문제 관련점에만 값 노드 + 점선 L-가이드로(§4).
- **격자 정책**: `textbook`은 **격자 없음**(레퍼런스 0/14). 격자가 필요한 `modern`만 `grid style={very thin, gray!30, densely dotted}` 사용.

### 3.5. Enforce The No-Overlap Contract

Non-obscuration principle:

- A label with `fill=white` must never be used to hide a curve, point, axis, tick, arrowhead, dashed guide, or shaded-boundary line.
- If text visually covers a graph element, the figure is invalid even when the text is readable.
- If there is no safe empty area inside the current axis rectangle, first enlarge the axis limits or move the label outside the data rectangle with `clip=false`.
- Prefer short labels (`$l$`, `$m$`, `$y=f(x)$`) inside the graph and put long equations in empty margins or outside crowded graph regions.
- The only acceptable contact between text and graph is a deliberate thin leader arrow that does not cover the target.

Before writing labels, build a collision inventory:

- **Hard objects**: axes, curves, guide lines, plotted points, arrowheads, tick labels.
- **Text objects**: origin, axis labels, point labels, graph labels, region labels.
- **Reserved zones**: point radius + 3pt, line/curve corridor + 4pt, text box + 2pt, page boundary + 6pt.

Placement priority:

1. Place important point labels first. Do not put text directly on a plotted point.
2. Expand `xmin/xmax/ymin/ymax` by 10% when boundary labels or graph labels need breathing room (range 8-15%; 10% as default).
3. Move labels into empty regions using outward anchors and explicit shifts. Prefer 4-8pt clearance for point labels and 6-12pt clearance for graph labels.
4. Put graph labels in low-curvature/low-slope empty regions, never directly on top of the curve.
5. Keep labels off dashed guide lines; labels should sit on the outside of the guide rectangle or beyond the marked point.
6. If a full equation label is too large, first move it farther out or use a shorter label such as `$l$`, `$m$`, `$y=f(x)$`, or place the full equation in a separate legend-like row outside the crowded area.
7. Check rendered output mentally or visually: no text box may sit on a curve corridor, point, axis, tick, arrowhead, dashed guide, or shaded boundary.
8. Use a leader arrow only when the label is collision-free but the referenced point/curve/line would otherwise be ambiguous.
9. Use semantic label styles without an opaque background by default:

```latex
\begin{tikzpicture}[
  pointLabel/.style={font=\small, inner sep=1pt},
  graphLabel/.style={font=\small, inner sep=1pt},
  axisLabel/.style={font=\small, inner sep=1pt},
  leaderArrow/.style={->, >=stealth, line width=0.35pt, shorten >=1pt}
]
```

Do not rely on `fill=white` to make a label readable. Move labels first; add a white background only when the label already sits in empty space and the background will not cover any black graph stroke, point marker, axis, tick, arrowhead, guide line, or shaded boundary. A label that hides a graph element is invalid even if the hidden part is small.

Default point-label anchors:

| Point position | First candidate | Fallbacks |
|---|---|---|
| Right branch / right side | `anchor=south east, xshift=-3pt, yshift=3pt` | `anchor=east, xshift=-4pt`; move to a clearer empty region |
| Left branch / left side | `anchor=east, xshift=-4pt` | `anchor=south east, xshift=-3pt, yshift=3pt`; move to a clearer empty region |
| Top boundary | `anchor=south, yshift=4pt` only if top margin exists | move inside with `anchor=north` |
| Near origin | move away from both axes | suppress if redundant |

**`textbook` 명명점 규칙 (에듀넷 정합)**: 점 이름은 upright 대문자(`$\mathrm{A}$`), 점이 빈 공간일 때만 작은 점(`mark=*, mark size=1.3pt`). 라벨은 **도형 바깥(outward) 코너 방향**으로 앵커:

| 점 위치 | 앵커(라벨이 바깥쪽으로) |
|---|---|
| 좌상 | `anchor=south east` |
| 우상 | `anchor=south west` |
| 좌하 | `anchor=north east` |
| 우하 | `anchor=north west` |
| 고립/측면 | `anchor=east` 또는 `west` |

오프셋 3–4pt(`xshift`/`yshift`). **★ 명명점에 (a,b) 좌표쌍을 붙이지 말 것** — 좌표값은 §4의 축 위 값 노드 + 점선 L-가이드로 분해한다(`$\mathrm{A}(2,3)$` 형식은 `textbook`에서 금지, `exam`에서만 허용).

Leader-arrow rules, only after placement fails:

- Use at most one or two leader arrows in a typical exam figure. If more are needed, redesign label placement, enlarge the axis margin, or simplify labels.
- Keep the arrow short and thin: `leaderArrow/.style={->, >=stealth, line width=0.35pt, shorten >=1pt}`.
- The arrow must point to the referenced object but should stop just before it. Do not cover the point marker or sit along the curve.
- Prefer a gentle curved arrow, especially around labels and crowded intersections: `to[out=..., in=...]` is usually clearer than a straight `--` segment.
- Avoid crossing axes, curves, dashed guide lines, tick labels, or other text. If an arrow crosses another object, bend it away or move the label instead.
- Do not start arrows from text-node anchors such as `label.south west` or `label.north east`; that commonly causes the arrow stroke to touch or overlap glyphs.
- Draw the arrow before the label node, from an explicit nearby empty coordinate that is outside the text box.
- Do not use leader arrows to excuse poor placement. If the text overlaps any graph element, the figure is still invalid.

Preferred leader-arrow pattern:

```latex
\draw[leaderArrow]
  (axis cs:3.15,3.0) to[out=230,in=45] (axis cs:3.05,2.05);
\node[graphLabel, anchor=south west]
  at (axis cs:3.3,3.1) {$y=x-1$};
```

### 4. Plot Functions And Points

Domain coverage rule:

- If the axis uses `xmin=a, xmax=b`, the default plot domain is `domain=a:b`.
- If `domain=a:b` would draw outside `ymin:ymax` while `clip=false`, adjust the domain only to the boundary intersections so the visible graph is still maximal inside the coordinate plane.
- Do not trim the graph merely to keep it near a marked point or label. Move labels or enlarge the axis instead.
- Restrict a domain only for a stated interval, an endpoint/open-circle graph, a piecewise definition, a discontinuity/asymptote, or a true function domain such as square roots/logarithms.
- When a restricted domain is intentional, add a nearby comment: `% gratik-domain-restricted: reason`.
- For discontinuous functions, split the graph into multiple `\addplot` commands, each covering the largest valid visible interval.

**★ `textbook` 도메인 규칙 (위 전폭 기본을 덮어씀)**: 포물선/곡선을 축 전폭이 아니라 **꼭짓점 ± (최외곽 표시 절편까지 거리 + ~0.4 패딩) 짧은 호**로 그린다. 끝은 **free end**(화살표 없음, 끝점 마커 없음). 그 다음 축을 타이트하게 크롭(곡선 밖 ~10–20% / ~0.5–1 단위). `exam`/고등은 전폭 기본 유지.

```latex
% 꼭짓점 x=-2, 절편 x=-5,1 -> 호 도메인 -5.4:1.4 (free ends)
% gratik-domain-textbook-arc: vertex +/- (intercept dist + 0.4)
\addplot[black, mark=none, line width=0.5pt, samples=120, domain=-5.4:1.4] {(x+2)^2-9};
```

**★ `textbook` 수치 표기 — 값 노드 + 점선 L-가이드 (눈금자 대체)**: 균일 눈금 없이, 문제 관련점(절편·꼭짓점·주어진 점)에만 bare 숫자(음수는 en-dash `−`). x값=축 **아래**, y값=축 **오른쪽**(점유 시 반대측). 좌표를 읽는 점은 양 축으로 **점선 L-가이드**(densely dashed, 0.3pt, gray!70 — 축 0.4·곡선 0.5보다 가늘게)를 내리고 발치에 값 노드.

```latex
% 꼭짓점 (-1,5) 좌표 읽기: 양 축으로 L-가이드 + 값 노드
\draw[densely dashed, line width=0.3pt, gray!70]
  (axis cs:-1,0) -- (axis cs:-1,5) -- (axis cs:0,5);
\node[anchor=north, font=\footnotesize] at (axis cs:-1,0) {$-1$}; % x값 = 축 아래
\node[anchor=west,  font=\footnotesize] at (axis cs:0,5)  {$5$};  % y값 = 축 오른쪽
```

Function graph:

```latex
\addplot[mark=none, domain=-4.5:4.5, samples=201, smooth, line width=0.7pt]
  {x^2};
```

Straight line:

```latex
\addplot[mark=none, domain=-4.5:4.5, samples=2, line width=0.65pt]
  {-2*x+5};
```

Point and label (`exam` — 좌표쌍 허용):

```latex
\addplot[only marks, mark=*, mark size=1.5pt] coordinates {(2,4)};
\node[pointLabel, anchor=south west, xshift=3pt, yshift=3pt]
  at (axis cs:2,4) {$\mathrm{P}(2,4)$};
```

Point and label (`textbook` — **문자만**, 좌표는 축으로 분해, mark 1.3pt):

```latex
\addplot[only marks, mark=*, mark size=1.3pt, black] coordinates {(2,4)};
\node[anchor=south west, font=\footnotesize] at (axis cs:2,4) {$\mathrm{P}$}; % (2,4) 붙이지 않음
% 좌표가 필요하면 위 §4 L-가이드 + 값 노드(2, 4)로 표기
```

Open and closed endpoints:

```latex
\node[circle,draw=black,fill=white,inner sep=1pt] at (axis cs:1,3) {};
\node[circle,fill=black,inner sep=1.2pt] at (axis cs:2,1) {};
```

Guide line:

```latex
\draw[densely dashed, gray, line width=0.4pt]
  (axis cs:2,0) -- (axis cs:2,4);
```

### 4.5. Equation Label Policy (그래프 수식 라벨 — 에듀넷 정합)

레퍼런스 실측: 포물선 도형의 ~2/3은 수식 라벨이 **없다**. 수식은 곡선이 2개 이상이거나 영역 음영이 있을 때 **구분 목적**으로만 곡선 옆에 띄운다.

1. **기본 = 라벨 없음**: 단일 곡선에서 꼭짓점·절편·표시점을 *읽는* 도형은 수식을 그래프에 적지 않는다. 곡선은 비워두고 표시점/절편 값으로만 식별 — 수식은 문제 본문에만.
2. **구분용으로만 라벨**: 곡선이 2개 이상이거나 곡선 사이를 음영할 때만 수식을 적고, 그때는 **모든 곡선에 각각** 하나씩.
3. **외측 여백·볼록측 배치**: 관련 가지의 **볼록(바깥)측 빈 공간**에 0.3–0.6 축단위 띄운다. 위로 볼록(아래로 열린 cup) 포물선 → 위쪽에 `anchor=west`(텍스트가 오른쪽 빈 공간으로). 아래로 볼록 → 아래쪽. **cup 내부 금지**(음영·짝 곡선 자리). y축에서 ≥~0.4단위, 화살촉에서 ≥반 단위 클리어. **축을 가로지르지 않는다.**
4. **획 위 금지**: 라벨이 곡선 stroke 위에 얹히면 안 됨(빈 공간에만).
5. **리더선 없음**: 수식↔곡선은 **근접성**으로만 연결한다(레퍼런스 리더 0건). 리더 화살표는 §3.5의 *점* 참조 모호 해소 전용 — 곡선 수식에는 쓰지 않는다.
6. **쌍곡선/음영**: 두 곡선 라벨은 **반대 극단**(하나 위, 하나 아래)에 두어 충돌 방지. 곡선을 색 구분하면(예: red 위로-열림, `green!55!black` 아래로-열림) 각 수식을 자기 색 곡선 옆에.
7. **폰트**: 축 변수 글자·값 숫자와 **같은 크기**(textbook=`\footnotesize`) math-italic, 분수는 `\dfrac` 디스플레이.

헬퍼 (리더 없는 외측 수식 라벨):

```latex
% \eqlabel{<x>}{<y>}{<anchor>}{<equation>}
\newcommand{\eqlabel}[4]{\node[anchor=#3, font=\footnotesize, inner sep=2pt] at (axis cs:#1,#2){$#4$};}
% 위로-열림, 가지 위 west 앵커:    \eqlabel{1.2}{6}{west}{y=x^{2}}
% 아래로-열림, 가지 아래 west 앵커:  \eqlabel{5.6}{-3.2}{west}{y=-\dfrac{1}{2}(x-5)^{2}}
```

쌍곡선 색 구분 예 (반대 극단):

```latex
\addplot[red, mark=none, line width=0.5pt, domain=-1.6:1.6, samples=120]{3*x^2-2};
\node[anchor=west, font=\footnotesize] at (axis cs:-3.3,7){$y=3x^{2}-2$};                  % 좌상
\addplot[green!55!black, mark=none, line width=0.5pt, domain=2.2:7.8, samples=120]{-0.5*(x-5)^2};
\node[anchor=west, font=\footnotesize] at (axis cs:5.6,-3.2){$y=-\dfrac{1}{2}(x-5)^{2}$};  % 우하
```

### 5. Shade Regions

Use `fillbetween` for regions bounded by curves:

```latex
\addplot[mark=none, domain=0:2, samples=201, name path=f] {x^2};
\addplot[mark=none, domain=0:2, samples=2, draw=none, name path=xaxis] {0};
\addplot[fill=gray!25, draw=none]
  fill between[of=f and xaxis, soft clip={domain=0:1}];
```

Shading defaults by preset (range allowed, default in bold):
- `exam`: **`gray!25`** (range `gray!20`–`gray!30`) — accent fill 금지
- `textbook`: 일반 영역 **`gray!20`**, 강조 영역 **`gratikEmph`(orange!35)** — 에듀넷 따뜻한 탄/피치 채움
- `workbook`: **`gray!20`** (range `gray!15`–`gray!25`)
- `academy`: **`gray!15`** (range `gray!10`–`gray!20`)
- `modern`: **`accent!20`** (range `accent!15`–`accent!30`)

**★ `textbook` 강조 채움 `gratikEmph` (에듀넷 정합)**: preamble/스타일 블록에 명명 스타일 정의 후 fill 먼저, 곡선/경계는 그 위에 검은 선으로 재묘사(경계가 채움에 흐려지지 않게).

```latex
% 스타일: gratikEmph/.style={fill=orange!35, draw=none}
\addplot[gratikEmph] fill between[of=A and B, soft clip={domain=...}]; % 채움 먼저(최하층)
\addplot[black, line width=0.5pt, smooth] ...;                         % 경계/곡선 위에 선명하게
```

색 팔레트(맥락별): 강조=`gratikEmph` orange!35, 중립 영역=`gray!20`, 곡선 사이 대안=`yellow!40`/`blue!15`. `#FF6B35` accent는 **곡선 색**으로만(채움 금지).

Max opacity 0.30 (exam/textbook/workbook), 0.25 (academy), 0.35 (modern). Above limit, the region must contain no labels.

### 6. Render and Validate (TeX → PDF → PNG)

**Every gratik invocation must produce three artifacts: the `.tex` source, the compiled `.pdf`, and a rendered `.png` preview.** Do not stop at TeX — the user expects to see the figure.

One-shot pipeline:

```bash
python3 .claude/skills/gratik/scripts/render-tex.py path/to/figure.tex
```

This compiles via `pdflatex` and renders the PDF to PNG at 200 dpi using pymupdf, producing `figure.pdf` and `figure.png` (or `figure-p{N}.png` for multi-page) next to the source. The script exits non-zero on compile failure and prints the latex log tail.

After rendering, **read the PNG with the Read tool and show it to the user** so they can verify the figure visually before saving or exporting.

Options:

- `--dpi 300` for high-resolution PNG (defaults to 200)
- `--engine xelatex` for Korean labels with `kotex` (defaults to `pdflatex`)
- `--engine lualatex` for complex pgfmath where precision matters

Static checker (run before render to catch rule violations early):

```bash
python3 .claude/skills/gratik/scripts/verify-gratik.py path/to/figure.tex
```

If verify-gratik reports issues, fix the TeX first; then run render-tex. If compile fails, read the latex tail in stderr to diagnose, fix the TeX, and re-run render-tex (it's idempotent).

### 7. Statistics Figures (중 통계 — 에듀넷 정합)

중3 통계는 대부분 **수치/표** 문제다(레퍼런스 8/10 페이지 무그래프). 차트를 함부로 생성하지 말 것.

- **기본 = 데이터/표** (차트 아님):
  - 원자료 나열 → 둥근 사각 **데이터 박스** (`rounded corners=4pt`, 0.6pt 검은 테두리, 흰 배경, 쉼표 구분, 변수는 italic).
  - 도수분포표 → 罫線 그리드 표. 줄기와잎 → 2열(줄기|잎) 표 + key 캡션.
- **좌표 플롯은 도수분포다각형(frequency polygon)에만** — 이 축 규칙은 §3 포물선 축과 **다르다**(혼용 금지):
  - 연회색 **정사각 격자**(`gray!35`, 0.4pt) + **굵은 검은 L축**(`axis lines=left`, 1pt, **화살표 없음**).
  - y축 상단 `(명)`, x축 마지막 눈금에 단위 `(점)`/`(시간)` 부착.
  - 계열별 단색 꺾은선(~1.3pt) + 채운 원 마커, peak 근처 인라인 라벨(박스 범례 없음).
- **히스토그램·막대·상자그림은 중3 수준에서 생성 금지.**

```latex
% 기본: 데이터 박스 (차트 아님)
\node[draw=black, line width=0.6pt, rounded corners=4pt, fill=white, inner sep=10pt]
  {$8,\ 6,\ 3,\ 10,\ a,\ 2,\ 5,\ 4$};
```

자세한 도수분포다각형/표 템플릿은 `references/templates.md` 참조.

## Checklist

- [ ] `pgfplots` and `\pgfplotsset{compat=1.18}` are present.
- [ ] Axis ranges and ticks are explicit.
- [ ] Manual nodes/draws inside `axis` use `axis cs:`.
- [ ] Boundary labels have clearance: enough data-space margin plus `clip=false` when labels are near edges.
- [ ] Point labels use explicit `xshift`/`yshift` and a semantic label style.
- [ ] Text does not sit directly on a point, curve, guide line, axis, tick label, or arrowhead.
- [ ] `fill=white` does not mask a graph stroke; it only protects against grid dots or light shading.
- [ ] Labels that cannot fit safely are moved, shortened, or placed outside the data rectangle before considering arrows.
- [ ] Leader arrows, if any, are rare, short, thin, and do not cross or cover graph elements.
- [ ] Equal-unit coordinate planes use `axis equal image`.
- [ ] Function plots use `mark=none`, explicit `domain`, and enough `samples`.
- [ ] Origin is `\mathrm{O}` and does not duplicate tick label `0`.
- [ ] Grid, if present, is light dotted gray.
- [ ] Labels are outside curves/points and do not cover the graph.

**`textbook` 프리셋 추가 체크 (에듀넷 정합)**:

- [ ] 격자 없음, 균일 눈금 없음(`xtick=\empty, ytick=\empty`) — 수치는 값 노드 + 점선 L-가이드.
- [ ] 축선이 곡선보다 가늘다(축 0.4 < 곡선 0.5pt); 양(+)끝에만 화살표.
- [ ] 원점 O = 우하(`anchor=north west`), 숫자 0 억제.
- [ ] x/y = bare italic, 화살표 tip; 한국어 'x축' 미사용.
- [ ] 명명점은 문자만(좌표쌍 미부착).
- [ ] 수식 라벨: 단일 read-off는 없음; 2곡선↑/음영만 외측 볼록측·리더 없음.
- [ ] 곡선은 짧은 호(꼭짓점±절편+여백), free end.
- [ ] 강조 채움은 `gratikEmph`(orange!35) fill 먼저 → 경계 검은 선 위에.
