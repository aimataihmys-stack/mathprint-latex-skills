# Ingested Source Notes: PGFplots Slides + KIAS TikZ Lecture

Use this file as the compact substitute for the unavailable `/ingest` skill. It records the actionable rules extracted from:

- `[local-source-not-bundled]/PGFplots(slides).pdf`
- `[local-source-not-bundled]/lecture2-KIAS.pdf`

## PGFplots Slides

- Use `\usepackage{pgfplots}` with `\begin{tikzpicture}` and `\begin{axis}[...]`.
- Coordinate-plane graphs should use centered axes: `axis x line=center`, `axis y line=center`, or the equivalent `axis lines=middle`.
- Set `xmin`, `xmax`, `ymin`, and `ymax` explicitly. Do not rely on automatic ranges for educational diagrams.
- Control ticks explicitly with `xtick={...}` and `ytick={...}`.
- Use `xlabel={$x$}`, `ylabel={$y$}`, then place them with `xlabel style={below right}`, `ylabel style={above left}`.
- For precise label placement, use `x label style={at={(axis cs:...)}}` and `y label style={at={(axis cs:...)}}`.
- Function plots should usually include `mark=none`, explicit `domain`, and enough samples, such as `samples=201`.
- Use `\addplot[dashed] coordinates {(x1,y1) (x2,y2)};` for guide segments when convenient.
- Place points and labels with `\node[...] at (axis cs:x,y) {...};`.
- Closed points: `\node[circle,fill,inner sep=1pt] at (axis cs:x,y) {};`.
- Open points: `\node[circle,draw=black,fill=white,inner sep=1pt] at (axis cs:x,y) {};`.
- For complex numeric data, prefer external tables or precomputed values over heavy TeX-side computation.

## KIAS TikZ Lecture

- TikZ is command- and coordinate-driven; every command must end with `;`.
- Use `>=stealth` or `-stealth` for clean textbook-style arrows.
- Do not mix ordinary TikZ coordinates with PGFplots coordinates inside `axis`; use `(axis cs:x,y)`.
- Use `+` for relative helper branches and `++` for continuing paths in pure TikZ.
- Use `name path` and `fill between` for bounded regions.
- Draw region fills before curves and labels.
- General layer order: background/shading, axes/grid/guides, main graphs, points, labels.
- Use light fills (`gray!25`, `gray!30`) and dashed guide lines for exam-style readability.

## Local Research To Respect

- `research/06_graphs-coords/F1-axes.md`: axis labels, origin `O`, arrowheads, line widths.
- `research/06_graphs-coords/F2-ticks-grid.md`: tick density and dotted gray grid style.
- `research/06_graphs-coords/F3-curves.md`: samples, `smooth`, labels near flat parts.
- `research/06_graphs-coords/F4-regions-asymptotes.md`: `fillbetween`, asymptotes, open/closed endpoints.
- `research/DESIGN-SYSTEM.md`: Korean exam/textbook line weights, typography, and color restraint.
