# Gratik Templates

## Label Placement Contract

Every template assumes that text must not obscure the graph. Labels have no opaque background by default; use `fill=white` only after the label has already been placed in a clear area and the fill will not cover a visible graph element. If a label would cover a curve, point, axis, tick, arrowhead, dashed guide, or shaded boundary, move it, enlarge the axis limits, shorten it, or place it outside the data rectangle with `clip=false`. Use `leaderArrow` only when a clear label would otherwise have an ambiguous target.

Function plots should fill the visible coordinate plane by default. Match `domain` to the axis `xmin:xmax` when the graph stays inside `ymin:ymax`; otherwise use the largest interval that remains inside the coordinate rectangle. Do not crop a graph just to keep it near points or labels. Add `% gratik-domain-restricted: reason` next to intentional problem/domain restrictions.

## Middle-School Unit Coordinate Plane

```latex
\documentclass[border=12pt]{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}

\begin{document}
\begin{tikzpicture}[
  pointLabel/.style={font=\small, inner sep=1pt},
  graphLabel/.style={font=\small, inner sep=1pt},
  axisLabel/.style={font=\small, inner sep=1pt},
  leaderArrow/.style={->, >=stealth, line width=0.35pt, shorten >=1pt}
]
\begin{axis}[
  axis lines=middle,
  axis line style={-stealth, line width=0.7pt},
  xlabel={$x$}, ylabel={$y$},
  xlabel style={below right},
  ylabel style={above left},
  xmin=-4.5, xmax=4.5,
  ymin=-4.5, ymax=4.5,
  xtick={-4,-3,-2,-1,1,2,3,4},
  ytick={-4,-3,-2,-1,1,2,3,4},
  tick style={line width=0.4pt, black},
  tick label style={font=\scriptsize},
  xmajorgrids=true,
  ymajorgrids=true,
  grid style={very thin, gray!30, densely dotted},
  width=7cm,
  height=7cm,
  axis equal image,
  clip=false
]
  \node[axisLabel, anchor=north east, xshift=-2pt, yshift=-2pt]
    at (axis cs:0,0) {$\mathrm{O}$};
  \addplot[only marks, mark=*, mark size=1.5pt] coordinates {(2,3) (-3,1)};
  \node[pointLabel, anchor=south west, xshift=3pt, yshift=3pt]
    at (axis cs:2,3) {$\mathrm{A}(2,3)$};
  \node[pointLabel, anchor=south east, xshift=-3pt, yshift=3pt]
    at (axis cs:-3,1) {$\mathrm{B}(-3,1)$};
\end{axis}
\end{tikzpicture}
\end{document}
```

## Suneung-Style Function Graph

```latex
\documentclass[border=12pt]{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}

\begin{document}
\begin{tikzpicture}[
  pointLabel/.style={font=\small, inner sep=1pt},
  graphLabel/.style={font=\small, inner sep=1pt},
  axisLabel/.style={font=\small, inner sep=1pt},
  leaderArrow/.style={->, >=stealth, line width=0.35pt, shorten >=1pt}
]
\begin{axis}[
  axis lines=middle,
  axis line style={-stealth, line width=0.55pt},
  xlabel={$x$}, ylabel={$y$},
  xlabel style={below right},
  ylabel style={above left},
  xmin=-1, xmax=5,
  ymin=-1.4, ymax=6,
  xtick={1,2,3,4},
  ytick={1,2,3,4,5},
  tick style={line width=0.35pt, black},
  tick label style={font=\scriptsize},
  width=7.5cm,
  height=6cm,
  clip=false
]
  \node[axisLabel, anchor=north east, xshift=-2pt, yshift=-2pt]
    at (axis cs:0,0) {$\mathrm{O}$};
  \addplot[mark=none, domain=-1:5, samples=201, smooth, line width=0.7pt]
    {0.5*(x-2)^2+1};
  \node[graphLabel, anchor=west, xshift=4pt] at (axis cs:3.35,2.3) {$y=f(x)$};
  \draw[densely dashed, gray, line width=0.4pt]
    (axis cs:2,0) -- (axis cs:2,1);
  \addplot[only marks, mark=*, mark size=1.4pt] coordinates {(2,1)};
\end{axis}
\end{tikzpicture}
\end{document}
```

## Shaded Region Between Curves

```latex
\documentclass[border=12pt]{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepgfplotslibrary{fillbetween}

\begin{document}
\begin{tikzpicture}[
  pointLabel/.style={font=\small, inner sep=1pt},
  graphLabel/.style={font=\small, inner sep=1pt},
  axisLabel/.style={font=\small, inner sep=1pt},
  leaderArrow/.style={->, >=stealth, line width=0.35pt, shorten >=1pt}
]
\begin{axis}[
  axis lines=middle,
  axis line style={-stealth, line width=0.6pt},
  xlabel={$x$}, ylabel={$y$},
  xlabel style={below right},
  ylabel style={above left},
  xmin=-0.5, xmax=3.5,
  ymin=-0.9, ymax=5,
  xtick={1,2,3},
  ytick={1,2,3,4},
  tick label style={font=\scriptsize},
  width=7cm,
  height=6cm,
  clip=false
]
  \node[axisLabel, anchor=north east, xshift=-2pt, yshift=-2pt]
    at (axis cs:0,0) {$\mathrm{O}$};
  \addplot[mark=none, domain=-0.5:3.5, samples=201, smooth, line width=0.7pt, name path=f]
    {x^2};
  \addplot[mark=none, domain=-0.5:3.5, samples=2, line width=0.7pt, name path=g]
    {2*x};
  \addplot[fill=gray!25, draw=none]
    fill between[of=f and g, soft clip={domain=0:2}];
  \node[graphLabel, anchor=south east, xshift=-4pt, yshift=3pt] at (axis cs:2.05,4.95) {$y=x^2$};
  \node[graphLabel, anchor=north west, xshift=4pt, yshift=-3pt] at (axis cs:2.55,4.55) {$y=2x$};
\end{axis}
\end{tikzpicture}
\end{document}
```

## Last-Resort Leader Arrow Pattern

Use this only when moving the label to a clear empty area makes the target ambiguous. Prefer moving the label, increasing axis margins, or shortening the label first. Draw the arrow before the label and start it from an explicit empty coordinate, not from a text-node anchor. Prefer a gentle curved route with `to[out=..., in=...]`; use a straight segment only when it is visibly clear.

```latex
\draw[leaderArrow]
  (axis cs:3.15,3.0) to[out=230,in=45] (axis cs:3.05,2.05);
\node[graphLabel, anchor=south west]
  at (axis cs:3.3,3.1) {$y=x-1$};
```

> 곡선 수식 라벨에는 leader를 쓰지 않는다(§4.5) — 아래 textbook 템플릿처럼 근접성으로만 연결.

---

## Textbook (에듀넷 중3) Templates

격자·눈금 없음, 양(+)끝 화살표만, italic x/y tip, O 우하, 수치는 값 노드 + 점선 L-가이드, 곡선은 짧은 호. 검증 완료(render-vs-reference + verify-gratik PASS).

### T1. 이차함수 — 단일 read-off (수식 라벨 없음)

```latex
\documentclass[border=10pt]{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usetikzlibrary{arrows.meta}
\begin{document}
\begin{tikzpicture}
\begin{axis}[
  width=5cm, height=4.5cm,
  axis lines=middle,
  axis line style={black, line width=0.4pt, -{Stealth[length=2.2mm,width=1.6mm]}},
  xtick=\empty, ytick=\empty,
  xmin=-3.6, xmax=3.6, ymin=-1.1, ymax=3.2,
  enlarge x limits=0.05, enlarge y limits=0.05, clip=false,
  xlabel={$x$}, ylabel={$y$},
  xlabel style={anchor=north, font=\itshape},
  ylabel style={anchor=east,  font=\itshape},
]
  \node[anchor=north west, font=\footnotesize] at (axis cs:0,0) {$\mathrm{O}$};
  % gratik-domain-textbook-arc: vertex 0 +/- (marked-x 2 + 1.2)
  \addplot[black, mark=none, line width=0.5pt, samples=120, domain=-3.2:3.2] {0.25*x^2};
  \addplot[only marks, mark=*, mark size=1.3pt, black] coordinates {(2,1)};
  \node[anchor=south west, xshift=2pt, yshift=2pt, font=\footnotesize] at (axis cs:2,1) {$\mathrm{P}$};
  \draw[densely dashed, line width=0.3pt, gray!70]
    (axis cs:2,0) -- (axis cs:2,1) -- (axis cs:0,1);
  \node[anchor=north, font=\footnotesize] at (axis cs:2,0) {$2$};
  \node[anchor=east,  font=\footnotesize] at (axis cs:0,1) {$1$};
\end{axis}
\end{tikzpicture}
\end{document}
```

### T2. 이차함수 — 다중 곡선 + 수식 라벨 (곡선 tip 외측, 리더 없음)

```latex
\documentclass[border=10pt]{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usetikzlibrary{arrows.meta}
\begin{document}
\begin{tikzpicture}
\begin{axis}[
  width=5cm, height=5cm,
  axis lines=middle,
  axis line style={black, line width=0.4pt, -{Stealth[length=2.2mm,width=1.6mm]}},
  xtick=\empty, ytick=\empty,
  xmin=-3.2, xmax=3.2, ymin=-3.4, ymax=3.4,
  enlarge x limits=0.05, enlarge y limits=0.05, clip=false,
  xlabel={$x$}, ylabel={$y$},
  xlabel style={anchor=north, font=\itshape},
  ylabel style={anchor=east,  font=\itshape},
]
  \node[anchor=north west, font=\footnotesize] at (axis cs:0,0) {$\mathrm{O}$};
  \addplot[black, mark=none, line width=0.5pt, samples=120, domain=-1.78:1.78] {x^2};
  \addplot[black, mark=none, line width=0.5pt, samples=120, domain=-1.78:1.78] {-x^2};
  \node[anchor=west, font=\footnotesize] at (axis cs:0.95,2.7)  {$y=x^{2}$};
  \node[anchor=west, font=\footnotesize] at (axis cs:0.95,-2.7) {$y=-x^{2}$};
\end{axis}
\end{tikzpicture}
\end{document}
```

### T3. 통계 — 데이터 박스 (기본) / 도수분포다각형 (유일한 차트)

중3 통계는 기본이 데이터/표. 차트는 도수분포다각형에만 — 이 축 규칙(격자 ON, 굵은 L축, 화살표 없음, 단위 괄호)은 위 함수 그래프 축과 **다르다**.

```latex
% (a) 데이터 박스
\documentclass[border=8pt]{standalone}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}
  \node[draw=black, line width=0.6pt, rounded corners=4pt, fill=white, inner sep=10pt]
    {$8,\ 6,\ 3,\ 10,\ a,\ 2,\ 5,\ 4$};
\end{tikzpicture}
\end{document}
```

```latex
% (b) 도수분포다각형 — 한글 라벨((명)/(점)) 포함 → render-tex.py --engine xelatex 로 컴파일
\documentclass[border=10pt]{standalone}
\usepackage{kotex}                               % 한글 단위 라벨
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\begin{document}
\begin{tikzpicture}
\begin{axis}[
  width=7cm, height=5cm,
  axis lines=left,
  axis line style={black, line width=1pt, -},    % 굵은 L축, 화살표 없음(-)
  xmajorgrids=true, ymajorgrids=true,
  grid style={gray!35, line width=0.4pt},        % 연회색 정사각 격자
  xmin=0, xmax=6, ymin=0, ymax=10,
  xtick={1,2,3,4,5}, ytick={2,4,6,8,10},
  xticklabels={1,2,3,4,{5(점)}},                  % 마지막 눈금에 단위(중괄호로 보호)
  tick label style={font=\footnotesize},
  ylabel={(명)}, ylabel style={rotate=-90, font=\footnotesize},
]
  \addplot[black, line width=1.3pt, mark=*, mark size=1.5pt]
    coordinates {(1,2)(2,5)(3,9)(4,6)(5,3)};
\end{axis}
\end{tikzpicture}
\end{document}
```
