# gratik DESIGN-SYSTEM — PGFplots 좌표·함수 스타일 시트

> 짝 문서: `research/DESIGN-SYSTEM.md` (tkz-euclide / gf2 기하 도형용).
> 본 문서는 gratik 전용. 두 문서는 5 프리셋(`exam / textbook / workbook / academy / modern`) 명명·의미를 공유한다.

## 1. 프리셋 마스터 테이블

수치는 Phase 1 측정(`research/measurements.csv` M01-M07, M11) + Phase 1 pgfplots 노트(`research/06_graphs-coords/F1-F4`) + 현 gratik SKILL.md를 정합한 값.

| 프리셋 | axis_line | tick_line | curve_line | guide_line | grid | tick_label | axis_label | point_label | graph_label | color | accent_hex |
|---|---:|---:|---:|---:|---|---|---|---|---|---:|---|
| **exam** | 0.55pt | 0.35pt | 0.55pt | 0.40pt | none | `\scriptsize` | `\small` | `\small` | `\small` | 1 (흑백) | — |
| **textbook** | 0.40pt | none | 0.50pt | 0.30pt dashed | **none** | 값노드만 `\footnotesize` | `\footnotesize` italic | `\footnotesize` | `\footnotesize` | 흑백+`gratikEmph` | `#FF6B35`(곡선 한정) |
| **workbook** | 0.60pt | 0.35pt | 0.60pt | 0.40pt | optional, `gray!20 densely dotted` | `\footnotesize` | `\footnotesize` | `\footnotesize` | `\footnotesize` | 1–2 | `#1E6FB8` |
| **academy** | 0.50pt | 0.30pt | 0.50pt | 0.35pt | none | `\scriptsize` | `\scriptsize` | `\scriptsize` | `\scriptsize` | 1 | — |
| **modern** | 0.80pt | 0.50pt | 0.85pt | 0.60pt | `gray!25 densely dotted, very thin` | `\footnotesize` | `\small` | `\normalsize` | `\normalsize` | 4 | `#2563EB` |

미지정 시: **중학(중1–중3)·에듀넷·검정교과서 자료 = `textbook` 기본**, 수능/평가원 = `exam`. `exam` 수치(0.55/0.35/0.55pt 등)는 KICE 실측 정합으로 **동결**. `textbook`은 2026-05 에듀넷 중3 정합으로 재정의: 축이 곡선보다 가늘고(0.40<0.50), 격자·눈금 없음, 양끝 화살표만, 수치는 값 노드+점선 L-가이드, 곡선은 짧은 호, 강조 채움 `gratikEmph`(orange!35). 명명·의미는 `research/DESIGN-SYSTEM.md`의 5 프리셋과 일치.

## 2. 하위 호환

기존 gratik SKILL.md의 3 프리셋 매핑:

| 기존 | 신 명명 | 이유 |
|---|---|---|
| `exam` | `exam` | 동일 |
| `textbook` | `textbook` | 동일 |
| `worksheet` | `workbook` | DESIGN-SYSTEM 명명에 일치. workbook 별칭으로 worksheet 허용. |

`academy`, `modern`은 신규.

## 3. axis 옵션 코드 매핑

`exam` 기본 프리셋:

```latex
\begin{axis}[
  axis lines=middle,
  axis line style={-stealth, line width=0.55pt},
  tick style={line width=0.35pt, black},
  tick label style={font=\scriptsize},
  label style={font=\small},
  xlabel={$x$}, ylabel={$y$},
  xlabel style={below right},
  ylabel style={above left},
  clip=false
]
```

`textbook` 차이 (에듀넷 중3 정합 — 격자·눈금 없음, 양끝 화살표만, italic x/y, O 우하):
```latex
width=4.5cm, height=4.5cm,
axis line style={black, line width=0.40pt, -{Stealth[length=2.2mm,width=1.6mm]}}, % 양(+)끝만
xtick=\empty, ytick=\empty,                  % ★ 격자·눈금 둘 다 없음
enlarge x limits=0.15, enlarge y limits=0.15,
xlabel style={anchor=north, font=\itshape},  % x = x화살표 우하
ylabel style={anchor=east,  font=\itshape},  % y = y화살표 좌상
% O 노드: \node[anchor=north west, font=\footnotesize] at (axis cs:0,0) {$\mathrm{O}$};  (우하, 0 억제)
% 수치: 값 노드 + 점선 L-가이드 (densely dashed, 0.30pt, gray!70)
```

`workbook` 차이: line 0.60pt, tick 0.35pt, grid는 사용자 선택(기본 off).
`academy` 차이: line 0.50pt, tick 0.30pt, tick label `\scriptsize`, 화살촉 생략 가능.
`modern` 차이: line 0.80pt, accent 색 적용, point size=2, 색상 4종.

## 4. 함수 곡선과 점·보조선

| 항목 | exam | textbook | workbook | academy | modern |
|---|---|---|---|---|---|
| `\addplot` line width | 0.55pt | 0.50pt (강조 `black!65` 0.6pt) | 0.60pt | 0.50pt | 0.85pt |
| samples (곡선) | 201 | 201 | 201 | 201 | 201 |
| samples (직선) | 2 | 2 | 2 | 2 | 2 |
| 점 mark size | 1.5pt | 1.5pt | 1.5pt | 1.2pt | 2.0pt |
| 점선 보조선 | `densely dashed, gray, 0.40pt` | 동일 | 동일 | `densely dashed, gray, 0.35pt` | `densely dashed, gray!60, 0.60pt` |
| 열린 원 | `circle, draw=black, fill=white, inner sep=1pt` | 동일 | 동일 | 동일 | 동일 |
| 닫힌 원 | `circle, fill=black, inner sep=1.2pt` | 동일 | 동일 | 동일 | 동일 |

## 5. 라벨 클리어런스 (실측 기반)

DESIGN-SYSTEM.md §라벨 배치 8방위 규칙과 동일. gratik 추가 규칙:

| 라벨 종류 | 최소 클리어런스 | xshift/yshift 표준 |
|---|---|---|
| 점 라벨 (점에서) | 4pt | `xshift=3pt, yshift=3pt` (NE 기준) |
| graph 라벨 (곡선에서) | 6pt | curvature 낮은 영역 |
| 축 라벨 (`x`, `y`) | 6pt | `below right` / `above left` |
| 원점 `\mathrm{O}` (exam) | 4pt 대각 | `anchor=north east, xshift=-2pt, yshift=-2pt` |
| 원점 `\mathrm{O}` (textbook) | 우하 기본 | `anchor=north west` (우하 점유 시 `north east`로 flip) |
| 경계 라벨 여유 (xmin/xmax/ymin/ymax 확장) | **10%** | 범위: 8–15%, 기본값 채택 |
| `\mathrm{O}` 하방 여백 (ymin) | **10%** of y-range | 범위: 8–12%, 기본값 채택 |

## 6. 색·음영

| 용도 | exam | textbook | workbook | academy | modern |
|---|---|---|---|---|---|
| 일반 영역 음영 | `gray!25` | `gray!20` | `gray!20` | `gray!15` | `accent!20` |
| 적분/구간 강조 | `gray!30` | **`gratikEmph` (orange!35)** | `gray!30` | `gray!25` | `accent!30` |
| 최대 opacity | 0.30 | 0.30 | 0.30 | 0.25 | 0.35 |
| 화살촉 | `-stealth` | `-stealth` | `-stealth` | `->` (간이) | `-stealth` |

## 7. 폰트 패밀리 (gf2와 공유)

DESIGN-SYSTEM.md §타이포그래피 계층의 3 프리셋 폰트 조합을 gratik에도 그대로 적용:

| 프리셋 | 본문/라벨 | 한글 | 수학 | 엔진 |
|---|---|---|---|---|
| exam · workbook · academy | TeX Gyre Termes | Noto Serif CJK KR | TeX Gyre Termes Math | XeLaTeX |
| textbook | Latin Modern | Noto Serif KR | Latin Modern Math | XeLaTeX/LuaLaTeX |
| modern | Inter | Pretendard | STIX Two Math | XeLaTeX |

폰트 미설치 환경: Latin Modern fallback.

## 8. 핸드오프 경계

- 함수 그래프 / 좌표평면 → gratik (본 문서)
- 좌표축 없는 유클리드 기하 → gf2 (`research/DESIGN-SYSTEM.md`)
- 3D 입체 → tikz-3dplot 핸드오프 (`research/F-G-SCOPE-PROPOSAL.md` §G)

## 9. SKILL.md 갱신 가이드

`SKILL.md:37-41`의 스타일 표를 본 문서 §1의 5 프리셋 표로 교체. 단 SKILL.md는 컴팩트 형태(주요 컬럼만)로 유지하고 상세는 본 문서 참조:

```markdown
| 프리셋 | axis | curve | guide | label | grid | 색 |
|---|---:|---:|---:|---|---|---:|
| exam | 0.55pt | 0.55pt | 0.40pt | `\small` | none | 흑백 |
| textbook | 0.40pt | 0.50pt | 0.30pt dashed | `\footnotesize` | none | 흑백+gratikEmph |
| workbook | 0.60pt | 0.60pt | 0.40pt | `\footnotesize` | optional | 흑백 |
| academy | 0.50pt | 0.50pt | 0.35pt | `\scriptsize` | none | 흑백 |
| modern | 0.80pt | 0.85pt | 0.60pt | `\normalsize` | `gray!25 densely dotted` | 4색 |

> 상세 규격: `docs/superpowers/specs/gratik-design-system.md`
```

## 10. 측정 출처

- exam: M01-M04, M11, A26-A29 (`research/measurements.csv`)
  - **A28 suneung-2026-nov-math (40p, 5416 strokes)**: main 0.54pt, aux 0.36pt
  - **A29 suneung-2025-nov-math (20p, 2708 strokes)**: main 0.54pt, aux 0.36pt
  - **A26 moed-2026-jun-math, A27 moed-2026-sep-math**: main 0.54pt, aux 0.36pt
  - 모두 `scripts/measure-style-from-pdf.py` 자동 측정 (mupdf-vector). 수능·모의평가 군의 **main stroke mode 0.54pt**가 절대 다수(suneung 2026: 5416회 / 8000여 stroke 중) — exam preset 0.55pt는 측정과 ±0.01pt 정합.
- textbook: M05-M07 — EBS 수능특강·수능완성. (구) main 0.65-0.75pt, label 10pt.
  - **에듀넷 중3 재정의 (2026-05)**: 도형이 PDF에 **저해상도 래스터 비트맵**으로 임베드되어 벡터 stroke 측정 불가(`measure-style-from-pdf.py`로 잰 0.24/0.48/0.72pt는 평가지 罫線 chrome). 따라서 textbook 선 굵기(축 0.40 / 곡선 0.50pt)는 **시작값**이며 §6 렌더-비교로 보정. 채움색은 픽셀 샘플링값(`gratikEmph` orange!35). 라벨 배치·축 규칙은 레이아웃 관찰이라 저해상도에서도 신뢰도 높음.
- workbook · academy · modern: 현 수치는 기존 gratik SKILL.md + DESIGN-SYSTEM.md 정합치(측정 데이터 추가는 Phase 3에서).

### 검증 결과 (2026-05-14)

회귀 테스트 `test_figures/v2/gratik-quadratic-k-v2.tex` (exam preset 적용)을 컴파일·측정한 결과 main stroke 0.55pt 정확 일치. 기존 v1의 0.75pt drift가 해소됨. histogram도 axis(0.55, 2)+curve(0.55, 200)으로 통합되어 시각적 위계도 균질.
