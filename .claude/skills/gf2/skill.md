---
name: gf2
description: 기하 문제를 분석하여 tkz-euclide 기반의 정확한 기하 도형 LaTeX 코드를 생성합니다. 프리셋 스타일(수능/교과서/문제집/학원/현대), 8방위 라벨 배치, 치수선 결정 트리, 시각 검증 루프를 포함합니다.
argument-hint: "<기하 문제 설명 또는 도형 요구사항>"
---

# 기하 도형 생성 (tkz-euclide)

## 목적

기하 문제가 주어졌을 때, tkz-euclide 패키지를 사용하여 정확한 기하 도형을 그리는 LaTeX 코드를 생성합니다:

1. **문제 분석** — 기하 요소(점, 선, 원, 삼각형, 다각형 등) 식별
2. **좌표 설계** — 조건에 맞는 정확한 좌표/구성 계획
3. **코드 생성** — tkz-euclide 매크로를 사용한 완전한 LaTeX 코드 출력
4. **레이블링** — 점, 선분, 각도에 적절한 라벨 배치
5. **마킹** — 등변, 직각, 각도 등 수학적 표기 추가
6. **렌더링** — `render-tex.py` 로 `.tex` → `.pdf` → `.png` 산출하고 사용자에게 PNG 시각 표시 (§산출물 참조)

**산출물 컨트랙트**: 매 호출은 `.tex` 소스 + `.pdf` 컴파일본 + `.png` 미리보기 세 개를 모두 만들어 사용자에게 제공해야 합니다. TeX만 주고 끝내지 않습니다.

## 실행 시점

- 기하 문제의 도형을 그려야 할 때
- 수학 시험/교재용 기하 그림이 필요할 때
- 유클리드 기하 작도를 시각화할 때
- 삼각형, 원, 다각형 등의 정밀한 도형이 필요할 때

## tkz-euclide 핵심 레퍼런스

### 문서 기본 구조

```latex
\documentclass[border=15pt]{standalone}
\usepackage{tkz-euclide}
\begin{document}
\begin{tikzpicture}[scale=1]
  % 1. 점 정의 (Setting)
  % 2. 계산 (Calculating)
  % 3. 그리기 (Drawing)
  % 4. 마킹 (Marking)
  % 5. 라벨링 (Labelling)
\end{tikzpicture}
\end{document}
```

### 1. 점 정의 (Setting)

#### 기본 점 정의
```latex
\tkzDefPoint(x,y){Name}              % 데카르트 좌표
\tkzDefPoint(angle:distance){Name}   % 극좌표
\tkzDefPoints{x1/y1/A, x2/y2/B, x3/y3/C}  % 여러 점 동시 정의
```

#### 상대 점 정의
```latex
\tkzDefShiftPoint[A](angle:distance){B}  % A 기준 상대 위치
```

### 2. 특수점 계산 (Calculating)

#### 중점
```latex
\tkzDefMidPoint(A,B) \tkzGetPoint{M}
```

#### 삼각형 중심점
```latex
\tkzDefTriangleCenter[ortho](A,B,C)    \tkzGetPoint{H}   % 수심 (orthocenter)
\tkzDefTriangleCenter[centroid](A,B,C)  \tkzGetPoint{G}   % 무게중심
\tkzDefTriangleCenter[circum](A,B,C)    \tkzGetPoint{O}   % 외심 (circumcenter)
\tkzDefTriangleCenter[in](A,B,C)        \tkzGetPoint{I}   % 내심 (incenter)
\tkzDefTriangleCenter[euler](A,B,C)     \tkzGetPoint{E}   % 오일러 중심
\tkzDefTriangleCenter[symmedian](A,B,C) \tkzGetPoint{K}   % 시메디안점
\tkzDefTriangleCenter[spieker](A,B,C)   \tkzGetPoint{Sp}  % 스피커 중심
\tkzDefTriangleCenter[gergonne](A,B,C)  \tkzGetPoint{Ge}  % 제르곤 점
\tkzDefTriangleCenter[nagel](A,B,C)     \tkzGetPoint{Na}  % 나겔 점
\tkzDefTriangleCenter[feuerbach](A,B,C) \tkzGetPoint{Fe}  % 포이어바흐 점
```

#### 특수 삼각형 정의
```latex
\tkzDefTriangle[equilateral](A,B)  \tkzGetPoint{C}   % 정삼각형
\tkzDefTriangle[two angles=50 and 70](A,B) \tkzGetPoint{C}  % 두 각 지정
\tkzDefTriangle[pythagore](A,B)    \tkzGetPoint{C}   % 3:4:5 직각삼각형
\tkzDefTriangle[school](A,B)       \tkzGetPoint{C}   % 30-60-90 삼각형
\tkzDefTriangle[golden](A,B)       \tkzGetPoint{C}   % 황금삼각형
\tkzDefTriangle[isosceles right](A,B) \tkzGetPoint{C} % 이등변직각삼각형
\tkzDefTriangle[gold](A,B)         \tkzGetPoint{C}   % gold 삼각형
\tkzDefTriangle[euclid](A,B)       \tkzGetPoint{C}   % 유클리드 삼각형
```

#### 특수 관련 삼각형
```latex
\tkzDefSpcTriangle[orthic,name=H](A,B,C){a,b,c}     % 수심삼각형 (Ha,Hb,Hc)
\tkzDefSpcTriangle[medial,name=M](A,B,C){a,b,c}      % 중점삼각형
\tkzDefSpcTriangle[incentral,name=I](A,B,C){a,b,c}    % 내심삼각형
\tkzDefSpcTriangle[excentral,name=E](A,B,C){a,b,c}    % 방심삼각형
\tkzDefSpcTriangle[intouch,name=T](A,B,C){a,b,c}      % 내접삼각형 (접선삼각형)
\tkzDefSpcTriangle[extouch,name=X](A,B,C){a,b,c}      % 방접삼각형
\tkzDefSpcTriangle[feuerbach,name=F](A,B,C){a,b,c}    % 포이어바흐 삼각형
\tkzDefSpcTriangle[tangential,name=T](A,B,C){a,b,c}   % 접선삼각형
\tkzDefSpcTriangle[euler,name=E](A,B,C){a,b,c}        % 오일러삼각형
\tkzDefSpcTriangle[symmedial,name=S](A,B,C){a,b,c}    % 시메디안삼각형
```

#### 다각형 정의
```latex
\tkzDefSquare(A,B)       \tkzGetPoints{C}{D}    % 정사각형 (AB가 한 변)
\tkzDefRectangle(A,C)    \tkzGetPoints{B}{D}    % 직사각형 (대각선)
\tkzDefParallelogram(A,B,C) \tkzGetPoint{D}     % 평행사변형
\tkzDefRegularPolygon[center,sides=5](O,A)      % 정다각형 (중심+꼭짓점)
\tkzDefRegularPolygon[side,sides=6](A,B)        % 정다각형 (한 변)
```

#### 황금비
```latex
\tkzDefGoldenRatio(A,C) \tkzGetPoint{B}   % AB/BC = 황금비
```

#### 무게중심좌표
```latex
\tkzDefBarycentricPoint(A=1,B=1,C=1) \tkzGetPoint{G}  % 무게중심
\tkzDefBarycentricPoint(A=1,B=2) \tkzGetPoint{G}       % 내분점
```

#### 조화분할
```latex
\tkzDefHarmonic[ext](A,B,C) \tkzGetPoint{D}   % 외부 조화점
\tkzDefHarmonic[int](A,B,D) \tkzGetPoint{C}   % 내부 조화점
\tkzDefHarmonic[both](A,B,{1/2}) \tkzGetPoints{C}{D}  % 양쪽
```

### 3. 변환 (Transformations)

```latex
\tkzDefPointBy[translation=from A to B](C)     \tkzGetPoint{C'}  % 평행이동
\tkzDefPointBy[reflection=over A--B](C)         \tkzGetPoint{C'}  % 대칭이동 (선)
\tkzDefPointBy[symmetry=center O](A)            \tkzGetPoint{A'}  % 점대칭
\tkzDefPointBy[rotation=center O angle 60](A)   \tkzGetPoint{A'}  % 회전
\tkzDefPointBy[homothety=center O ratio 2](A)   \tkzGetPoint{A'}  % 닮음변환
\tkzDefPointBy[projection=onto A--B](C)         \tkzGetPoint{H}   % 정사영
\tkzDefPointBy[inversion=center O through A](B) \tkzGetPoint{B'}  % 반전
```

#### 여러 점 동시 변환
```latex
\tkzDefPointsBy[translation=from A to B](C,D,E){C',D',E'}
\tkzDefPointsBy[reflection=over A--B](C,D){C',D'}
\tkzDefPointsBy[symmetry=center O](A,B){A',B'}
```

### 4. 벡터 기반 점 정의

```latex
\tkzDefPointWith[orthogonal](A,B)          \tkzGetPoint{C}  % AB에 수직, 같은 길이
\tkzDefPointWith[orthogonal,K=2](A,B)      \tkzGetPoint{C}  % AB에 수직, 2배 길이
\tkzDefPointWith[orthogonal normed](A,B)   \tkzGetPoint{C}  % AB에 수직, 단위 길이
\tkzDefPointWith[linear,K=0.5](A,B)        \tkzGetPoint{C}  % AB 위 0.5 비율
\tkzDefPointWith[linear normed,K=3](A,B)   \tkzGetPoint{C}  % AB 방향 3cm
\tkzDefPointWith[colinear=at C](A,B)       \tkzGetPoint{D}  % AB 벡터를 C에서
```

### 5. 직선 정의

```latex
\tkzDefLine[mediator](A,B)                 \tkzGetPoints{I}{J}  % 수직이등분선
\tkzDefLine[bisector](A,B,C)               \tkzGetPoint{x}      % 각의 이등분선
\tkzDefLine[bisector out](A,B,C)           \tkzGetPoint{x}      % 외각 이등분선
\tkzDefLine[parallel=through P](A,B)       \tkzGetPoint{x}      % P를 지나는 평행선
\tkzDefLine[perpendicular=through P](A,B)  \tkzGetPoint{x}      % P를 지나는 수선
\tkzDefLine[orthogonal=through P](A,B)     \tkzGetPoint{x}      % 수직선 (= perpendicular)
\tkzDefLine[altitude](A,B,C)               \tkzGetPoint{x}      % 꼭짓점 A에서의 수선의 발
\tkzDefLine[euler](A,B,C)                  \tkzGetPoint{x}      % 오일러 직선
\tkzDefLine[tangent at=P](O)               \tkzGetPoint{x}      % 원 위의 점에서 접선
\tkzDefLine[tangent from=P](O,A)           \tkzGetPoints{x}{y}  % 외부 점에서 접선
```

### 6. 원 정의

```latex
\tkzDefCircle[through](O,A)                  % 중심 O, 점 A를 지남
\tkzDefCircle[R](O,3)            \tkzGetPoint{o}  % 중심 O, 반지름 3cm
\tkzDefCircle[diameter](A,B)     \tkzGetPoint{O}  % 지름 AB
\tkzDefCircle[circum](A,B,C)     \tkzGetPoints{O}{r}  % 외접원
\tkzDefCircle[in](A,B,C)         \tkzGetPoints{I}{r}   % 내접원
\tkzDefCircle[ex](A,B,C)         \tkzGetPoints{E}{r}   % 방접원 (A 맞은편)
\tkzDefCircle[euler](A,B,C)      \tkzGetPoints{E}{r}   % 오일러 원 (구점원)
\tkzDefCircle[apollonius,K=2](A,B) \tkzGetPoints{O}{r}  % 아폴로니우스 원
\tkzDefCircle[orthogonal from=P](O,A) \tkzGetFirstPoint{T}  % 직교원
\tkzDefCircle[orthogonal through=P and Q](O,A)              % 직교원 (두 점)
\tkzDefCircle[spieker](A,B,C)    \tkzGetPoints{S}{r}  % 스피커 원
```

### 7. 교점 (Intersections)

#### 두 직선의 교점
```latex
\tkzInterLL(A,B)(C,D)   \tkzGetPoint{I}      % 직선 AB와 CD의 교점
```

#### 직선과 원의 교점
```latex
\tkzInterLC(A,B)(O,C)   \tkzGetPoints{I}{J}  % 직선 AB와 원(O,C)
\tkzInterLC[R](A,B)(O,3) \tkzGetPoints{I}{J} % 직선 AB와 원(O,r=3)
\tkzInterLC[near](A,B)(O,C)   \tkzGetPoints{I}{J}  % near: I가 A에 가까운 점
\tkzInterLC[common=P](A,B)(O,C) \tkzGetFirstPoint{Q} % 공통점 P 제외
\tkzInterLC[with nodes](A,B)(O,C,D) \tkzGetPoints{I}{J} % CD가 반지름
```

#### 두 원의 교점
```latex
\tkzInterCC(O,A)(O',B)  \tkzGetPoints{I}{J}  % 두 원의 교점
\tkzInterCC[R](O,r)(O',r') \tkzGetPoints{I}{J}  % 반지름 직접 지정
\tkzInterCC[with nodes](O,A,B)(O',C,D) \tkzGetPoints{I}{J}  % AB, CD가 반지름
\tkzInterCC[common=P](O,A)(O',B) \tkzGetFirstPoint{Q}  % 공통점 P 제외
```

#### 교점 존재 테스트
```latex
\tkzTestInterLC(A,B)(O,C)   % \iftkzFlagLC 로 테스트
\tkzTestInterCC(O,A)(O',B)  % \iftkzFlagCC 로 테스트
```

### 8. 선 위/원 위의 점

```latex
\tkzDefPointOnLine[pos=0.5](A,B) \tkzGetPoint{M}  % 선분 위 중점 (pos: 0=A, 1=B)
\tkzDefPointOnCircle[through=center O angle 30 point A] \tkzGetPoint{P}  % 원 위의 점
\tkzDefPointOnCircle[R=center O angle 45 radius 3]      \tkzGetPoint{P}  % 원 위의 점 (R)
```

### 9. 각도 계산

```latex
\tkzFindAngle(A,O,B)    \tkzGetAngle{ang}   % 각 AOB (반시계 방향, 0~360)
\tkzFindSlopeAngle(A,B) \tkzGetAngle{slope}  % AB의 수평 기울기 (-180~180)
```

### 10. 그리기 (Drawing)

#### 점
```latex
\tkzDrawPoint[color=red,size=6](A)
\tkzDrawPoints(A,B,C)
\tkzDrawPoints[fill=gray,opacity=.5](A,B,C)
```

#### 선분, 직선, 반직선
```latex
\tkzDrawSegment[color=red](A,B)
\tkzDrawSegments(A,B C,D E,F)                    % 여러 선분
\tkzDrawSegment[dim={$c$,-10pt,}](A,B)           % 치수선 (dim)
\tkzDrawLine[add=0.2 and 0.2](A,B)               % 양쪽 20% 연장
\tkzDrawLine[add=0 and 0](A,B)                   % 선분과 동일
\tkzDrawLine[add=0 and 1](A,B)                   % 반직선 (A에서 B 방향)
\tkzDrawLines[add=.5 and .5](A,B C,D)            % 여러 직선
```

#### 다각형
```latex
\tkzDrawPolygon(A,B,C)                            % 삼각형
\tkzDrawPolygon[fill=blue!10](A,B,C,D)            % 채움 포함
\tkzDrawPolygon(A,...,E)                           % A,B,C,D,E 축약
\tkzDrawPolySeg(A,B,C,D)                          % 열린 꺾은선
```

#### 원
```latex
\tkzDrawCircle(O,A)                               % 중심 O, 점 A 지남
\tkzDrawCircle[R](O,3)                            % 중심 O, 반지름 3 (주의: \tkzDefCircle[R] 먼저)
\tkzDrawCircles(A,B C,D)                          % 여러 원
\tkzDrawSemiCircle(O,A)                           % 반원 (반시계)
\tkzDrawSemiCircles(O1,A O2,B)                    % 여러 반원
```

#### 호 (Arc)
```latex
\tkzDrawArc(O,A)(B)                               % 중심 O, A에서 B까지 (반시계)
\tkzDrawArc[R](O,2)(30,120)                       % 반지름 2, 30도에서 120도
\tkzDrawArc[delta=10](O,A)(B)                     % delta로 약간 확장
\tkzDrawArc[angles](O,A)(0,120)                   % A에서 시작하여 각도로
```

#### 부채꼴 (Sector)
```latex
\tkzDrawSector(O,A)(B)                            % 중심 O, A에서 B 방향까지
\tkzDrawSector[rotate](O,A)(60)                   % A에서 60도 회전
\tkzDrawSector[R](O,2)(30,90)                     % 반지름, 각도 범위
```

### 11. 채우기 (Filling)

```latex
\tkzFillPolygon[color=blue!20](A,B,C)            % 다각형 채움
\tkzFillCircle[color=red!10](O,A)                 % 원 채움
\tkzFillSector[fill=purple!20](O,A)(B)            % 부채꼴 채움
\tkzFillAngle[size=1,fill=gray!20](A,O,B)         % 각도 영역 채움
\tkzFillAngles[fill=red!20,opacity=.2](A,B,C D,E,F)  % 여러 각도
```

### 12. 마킹 (Marking)

#### 선분 마크
```latex
\tkzMarkSegment[mark=|](A,B)                      % 단일 틱
\tkzMarkSegment[mark=||](A,B)                     % 이중 틱
\tkzMarkSegment[mark=|||](A,B)                    % 삼중 틱
\tkzMarkSegment[mark=s|](A,B)                     % 슬래시 틱
\tkzMarkSegment[mark=s||](A,B)                    % 이중 슬래시
\tkzMarkSegments[mark=|](A,B C,D)                 % 여러 선분 (같은 마크)
\tkzMarkSegments[mark=s||](A,B B,C C,A)           % 정삼각형 표시
```

#### 각도 마크
```latex
\tkzMarkAngle[size=1](A,O,B)                      % 각도 호 (반시계: A→O→B)
\tkzMarkAngle[size=1,mark=|](A,O,B)               % 틱 마크 포함
\tkzMarkAngle[size=1,mark=||](A,O,B)              % 이중 틱
\tkzMarkAngles[mark=|](A,B,C D,E,F)               % 여러 각도
\tkzMarkRightAngle(A,B,C)                          % 직각 표시 (B가 꼭짓점)
\tkzMarkRightAngle[size=.4,fill=gray!20](A,B,C)   % 크기, 채움
\tkzMarkRightAngles(A,B,C D,E,F)                   % 여러 직각
```

### 13. 라벨링 (Labelling)

#### 점 라벨
```latex
\tkzLabelPoint[above](A){$\mathrm{A}$}
\tkzLabelPoint[below left](B){$\mathrm{B}$}
\tkzLabelPoints(A,B,C)                             % 기본 위치 (아래)
\tkzLabelPoints[above](C,D)
\tkzAutoLabelPoints[center=G](A,B,C)              % 중심 기준 자동 배치
```

위치 옵션: `above`, `below`, `left`, `right`, `above left`, `above right`, `below left`, `below right`

#### 선분 라벨
```latex
\tkzLabelSegment(A,B){$c$}
\tkzLabelSegment[swap](A,B){$c$}                  % 반대쪽
\tkzLabelSegment[above,sloped](A,B){$c$}          % 선분 따라
\tkzLabelSegments[swap](A,B){$c$}
```

#### 각도 라벨
```latex
\tkzLabelAngle[pos=1.5](A,O,B){$\alpha$}
\tkzLabelAngles[pos=1.5](A,B,C D,E,F){$\alpha$}
```

#### 원 라벨
```latex
\tkzLabelCircle[above=12pt](O,A)(180){$\mathcal{C}$}  % (center,point)(angle){label}
```

#### 직선 라벨
```latex
\tkzLabelLine[pos=1.25,right](A,B){$(d)$}
```

### 14. 보조 도구 (Complements)

#### 컴퍼스 자국
```latex
\tkzCompass(A,B)                                   % 컴퍼스 호
\tkzCompass[length=1](A,B)                         % 길이 제한
\tkzCompass[delta=10](A,B)                         % 확장
\tkzCompasss(A,B C,D)                              % 여러 개
```

#### 작도 표시
```latex
\tkzShowLine[mediator](A,B)                        % 수직이등분선 작도 표시
\tkzShowLine[bisector](A,B,C)                      % 이등분선 작도 표시
\tkzShowLine[parallel=through P](A,B)              % 평행선 작도 표시
\tkzShowLine[perpendicular=through P](A,B)         % 수선 작도 표시
```

#### 길이 계산
```latex
\tkzCalcLength(A,B) \tkzGetLength{len}             % 길이를 cm로 저장
\tkzDuplicateSegment(A,B)(C,D) \tkzGetPoint{E}     % 선분 복제: CE = AB
```

#### 좌표 추출
```latex
\tkzGetPointCoord(A){a}    % \ax, \ay 로 접근
```

#### 내적, 거듭제곱
```latex
\tkzDotProduct(A,B,C)      % 벡터 BA·BC 내적
\tkzPowerCircle(A)(O,B)    % 점 A의 원(O,B)에 대한 거듭제곱
```

### 15. 스타일 설정

```latex
\tkzSetUpPoint[size=4,color=blue]                  % 점 스타일
\tkzSetUpLine[line width=1pt,color=gray]           % 선 스타일
\tkzSetUpArc[line width=1pt,color=gray]            % 호 스타일
\tkzSetUpCompass[color=gray,line width=.4pt]       % 컴퍼스 스타일
\tkzSetUpLabel[font=\small]                        % 라벨 스타일
\tkzSetUpStyle[postaction=decorate,...]{name}       % 커스텀 스타일
```

### 16. 클리핑과 바운딩 박스

```latex
\tkzInit[xmin=-2,xmax=8,ymin=-1,ymax=6]           % 좌표 범위 설정
\tkzClip                                            % 범위 밖 잘라내기
\tkzClip[space=1]                                   % 여유 공간 추가
\tkzClipPolygon(A,B,C)                              % 다각형 내부만
\tkzClipPolygon[out](A,B,C)                         % 다각형 외부만
\tkzClipCircle(O,A)                                 % 원 내부만
\tkzClipCircle[out](O,A)                            % 원 외부만
\tkzShowBB                                          % 바운딩 박스 표시
```

### 17. 상수

```latex
\tkzPhi      = 1.618034   % 황금비
\tkzInvPhi   = 0.618034   % 황금비 역수
\tkzSqrTwo   = 1.414213   % √2
\tkzSqrThree = 1.7320508  % √3
\tkzSqrFive  = 2.2360679  % √5
\tkzPi       = 3.1415926  % π
```

### 18. 화살표 (Arrows)

```latex
% 선분 끝에 화살표
\tkzDrawSegment[>=stealth,->,line width=1pt](A,B)
\tkzDrawSegment[>=stealth,<->,line width=1pt](A,B)

% 중점에 화살표 (데코레이션)
\tkzSetUpStyle[postaction=decorate,
  decoration={markings,
  mark=at position .5 with {\arrow[thick]{>}}}]{myarrow}
\tkzDrawSegments[myarrow=stealth](A,B)
```

---

## Workflow

### Step 1: 문제 분석

주어진 기하 문제를 분석하여 다음을 식별합니다:

- **기본 도형**: 삼각형, 사각형, 원, 다각형 등
- **특수 조건**: 정삼각형, 이등변삼각형, 직각, 평행, 수직 등
- **필요한 점**: 꼭짓점, 중심, 교점, 특수점(수심, 내심, 외심 등)
- **보조선**: 수선, 이등분선, 중선, 접선 등
- **마킹 요구**: 등변 표시, 직각 표시, 각도 표시 등
- **길이/각도 조건**: 주어진 수치

### Step 2: 좌표 설계

도형의 정확한 좌표를 설계합니다:

1. **기준점 배치** — 가장 단순한 위치에 기준점을 놓습니다 (보통 원점이나 x축 위)
2. **조건 기반 구성** — tkz-euclide의 매크로를 활용하여 조건에 맞는 점을 계산합니다
3. **스케일 결정** — 도형이 적절한 크기가 되도록 scale 조정

**좌표 설계 원칙:**

**다각형 배치 규칙: 왼쪽 상단(A)부터 시계 방향 (CW)**
- 모든 다각형은 **A를 왼쪽 상단**에 놓고, **시계 방향**으로 꼭짓점을 배치 (한국 평가지 표준 검증: 92/95 ≈ 97% 일치)
- 삼각형: A(꼭대기/좌상), B(좌하), C(우하) — 둘레 따라 시계 방향
  ```
      A                  A
     / \                /|
    /   \              / |
   B─────C            B──C
  예: A(2,4), B(0,0), C(5,0)
  ```
- 사각형: A(좌상) → B(좌하) → C(우하) → D(우상)  — 둘레 따라 CW (y축 위쪽인 표준 좌표계 기준)
  ```
  A ─────── D        예: A(0,4), B(0,0), C(6,0), D(6,4)
  │         │        평행사변형: A(0,3), B(0,0), C(6,0), D(8,3)
  │         │        사다리꼴 (AD<BC): A(2,3), B(0,0), C(7,0), D(5,3)
  B ─────── C
  ```
- **마름모 다이아몬드 변형** (한국 평가지 마름모의 64%): A(상정점), B(좌), C(하정점), D(우) — 회전된 정사각형. 둘레 CW.
  ```
        A
       / \
      /   \         예: A(0,3), B(-3,0), C(0,-3), D(3,0)
     B     D
      \   /
       \ /
        C
  ```
- 오각형 이상: A(좌상)부터 시계 방향으로 B, C, D, E, ...

**기타 원칙:**
- 원: 중심을 원점 또는 적절한 위치에 배치
- 대칭 도형: 대칭축을 좌표축에 맞춤
- 복잡한 조건: tkz-euclide 매크로로 자동 계산 (교점, 변환 등)

### Step 2.5: 각도 방향 판단

`\tkzMarkAngle(A,O,B)`는 꼭짓점 O에서 **OA → OB 반시계 방향**으로 호를 그립니다.

**내각 판단 규칙:**
1. 꼭짓점 O에서 OA, OB의 대략적 방향을 파악
2. OA에서 OB로 **반시계 회전이 180° 미만** → 내각 ✓
3. 180° 초과 → 외각이므로 순서를 뒤집어 `(B,O,A)` 사용

**삼각형 ABC 표준 배치** (B 왼쪽 아래, C 오른쪽 아래, A 위):
| 각도 | 코드 | 이유 |
|------|------|------|
| ∠A (꼭대기) | `(B,A,C)` | B→C 반시계 = 아래쪽 내각 |
| ∠B (왼쪽 아래) | `(A,B,C)` | A→C 반시계 = 오른쪽 내각 |
| ∠C (오른쪽 아래) | `(A,C,B)` | A→B 반시계 = 왼쪽 내각 |

**빠른 확인법:**
- 삼각형 내부를 향해 호가 그려지면 정답
- `\tkzFillAngle`로 채워서 시각적으로 확인 가능 (디버깅 전용 — 최종 출력에서 제거)
- 잘못된 순서 = 360°−θ (외각)이 그려짐

### Step 3: 코드 생성

다음 순서로 LaTeX 코드를 작성합니다:

1. **Setting** — `\tkzDefPoint`, `\tkzDefPoints`로 고정점 정의
2. **Calculating** — 교점, 중점, 특수점 등 계산
3. **Drawing** — 선분, 다각형, 원, 호 그리기
4. **Filling** — 필요한 영역 채우기 (음영)
5. **Marking** — 등변, 직각, 각도 마킹
6. **Labelling** — 점, 선분, 각도 라벨 배치

**코드 작성 규칙:**
- 항상 `\documentclass[border=15pt]{standalone}` + `\usepackage{tkz-euclide}` 사용 (`border=15pt`로 사방 여백 확보)
- 주석으로 각 단계를 구분
- 보조선은 `dashed` 또는 `new` 스타일
- 한글 라벨이 필요하면 `\usepackage{kotex}` 추가
- 수식 라벨은 `$...$`로 감싸기
- **각도 기호**: `$40^\circ$` 형식 사용 (`\degree` 사용 금지)
- **점 크기**: `\tkzDrawPoints[size=0]` 사용. **단, 다음은 visible (size=2pt)**: 외심 O, 내심 I, 무게중심 G, 사각형 대각선 교점 O, 일반적으로 "강조 대상 중심점" (Agent 1 검증)
- **라벨 표기**: 대문자(점 이름)는 `$\mathrm{A}$` (upright). 소문자 변수 `$x$`, 선 `$\ell, m, n$`, 변 길이 `$a, b, c$` 모두 italic (Agent 5 검증)
- **닮음 대응점**: `$\mathrm{A}'$` (prime, upright)
- **마크 절제 원칙** (Agent 2 검증): "정사각형 ABCD" 같이 도형 이름이 본문에 명시되면 직각·등변 마크 생략. 보조 조건일 때만 마킹.
- **답 영역 음영**: `\tkzFillPolygon[color=gray!15]` (또는 `gray!20`) — 한국 평가지 표준. accent 컬러(파랑·빨강 등) 금지. 기하 사각형 단원 합성 도형의 ~90% 가 답 영역 음영을 사용 (Agents 2, 4)

**스타일 프리셋 선택:** 아래 `## 스타일 프리셋` 섹션의 표를 참조하여 적용합니다. 미지정 시 대상별 분기 — 중학(에듀넷·검정교과서) → **textbook**, 수능·평가원·고등 → **exam**.

**라벨 배치 전략:**
- `\tkzAutoLabelPoints[center=G](A,B,C)` — 도형 중심 기준 자동 배치 (겹침 방지에 효과적)
- 점이 밀집된 영역: `font=\small` 또는 `pos` 조정으로 간격 확보
- 보조점은 라벨 크기를 줄이거나 생략 가능
- 선분 위 라벨: `sloped` 옵션으로 선분 방향에 맞춤

**8방위 정점 라벨 배치 규칙:**
정점 P의 라벨은 인접 변들의 외각 이등분선 방향(= 도형 바깥쪽)에 배치합니다:

| 방위각 θ | 앵커 | 예시 |
|----------|------|------|
| 0° ± 22.5° (E) | `right` | 오른쪽 꼭짓점 |
| 45° ± 22.5° (NE) | `above right` | 우상단 |
| 90° ± 22.5° (N) | `above` | 꼭대기 |
| 135° ± 22.5° (NW) | `above left` | 좌상단 |
| ±180° (W) | `left` | 왼쪽 |
| -135° ± 22.5° (SW) | `below left` | 좌하단 |
| -90° ± 22.5° (S) | `below` | 하단 |
| -45° ± 22.5° (SE) | `below right` | 우하단 |

**충돌 우선순위**: 정점 라벨 (고정) > 변 길이 라벨 (pos 조정) > 각 라벨 (pos 축소)

**각도 라벨 pos 규칙** (한국 평가지 검증, Agent 7: 호 size 절대 0.3-0.45 / 라벨 외측 1.3-1.5):
| 각 크기 θ | `\tkzMarkAngle[size=…]` | `\tkzLabelAngle[pos=…]` |
|----------|-------------------------|-------------------------|
| θ ≥ 90° | 0.40-0.45 | 1.3-1.5 |
| 60°-90° | 0.35-0.40 | 1.4-1.6 |
| 30°-60° | 0.30-0.35 | 1.5-1.8 |
| 15°-30° | 0.30 | 1.5-1.8 (호 위 직접) |
| θ < 15° | 외부 전용 | leader line |

> **★ 한국 평가지 정책** (Agent 7 검증):
> - 호 크기는 **절대 고정** (변 길이 비례 X). 변 16cm 큰 도형에서도 호 ≈0.3cm.
> - 호 두께는 본 변과 동일 (`line width=0.4pt` 권장).
> - 라벨 형식 100% `숫자°` (∠B/α/`\circ` 0건).
> - 같은 각 표시 = **같은 반지름 호 두 번**. 슬래시(`|`, `||`) 마크 0건. 변=슬래시, 각=호만.
> - **`\tkzMarkAngle[fill=...]` 사용 금지** — 한국 평가지의 채움색은 면적 강조(`\tkzFillPolygon`) 전용.
> - 직각 마크는 **빈 작은 사각형** (filled/dot 형태 0건), `\tkzMarkRightAngle[size=0.2]` (이전 0.3 → 0.2 갱신, Agents 1·3·7 합의).
> - **★ textbook(에듀넷)**: 직각 사각형 size **0.2–0.25** 허용(약간 큼). **계산형 도형(삼각비/원 각 구하기)은 등각 이중 호 미사용** — 단일 호 + 값만. 등각 이중 호는 합동/등변 논증 도형에서만.

**변 길이 라벨 수평 유지 원칙**: 숫자+단위 라벨은 기울어진 변에서도 `sloped` 사용 금지 (수평 유지). 변수 기호(`a`, `c`)만 `sloped` 허용.

### Step 4: 출력

**전체 컴파일 가능한 코드를 출력합니다:**

```latex
\documentclass[border=15pt]{standalone}
\usepackage{tkz-euclide}
% \usepackage{kotex}  % 한글 라벨 필요 시

\begin{document}
\begin{tikzpicture}[scale=1]
  % === 점 정의 ===
  ...
  % === 계산 ===
  ...
  % === 그리기 ===
  ...
  % === 마킹 ===
  ...
  % === 라벨링 ===
  ...
\end{tikzpicture}
\end{document}
```

### Step 5: 검증 체크리스트 (한국 평가지 표준 정합)

코드 생성 후 다음을 확인합니다:

1. **조건 일치**: 문제의 모든 조건(등변, 각도, 평행, 수직 등)이 도형에 반영되었는가?
2. **점 위치**: 각 점이 올바른 선분/원 위에 있는가? (`\tkzInterLC`, `\tkzInterCC` 결과 확인)
3. **다각형 명명 방향**: A 좌상부터 **시계방향(CW)** B → C → D 순인가? (사각형) / A 꼭대기, B 좌하, C 우하 (삼각형)
4. **마킹 완전성**: 등변(`mark=|` 또는 `||`, **변에 perpendicular tick — slash 금지**), 직각(`\tkzMarkRightAngle[size=0.2]`), 각도 표시가 빠짐없는가?
5. **마크 절제**: "정사각형 ABCD" 등 도형 이름이 본문에 있으면 직각·등변 마크 생략 (한국 평가지 표준)
6. **틱 개수 제한**: 한 도형에 등변 마크는 최대 2 종류(`|`, `||`). `|||` 회피 (Agent 6 검증).
7. **각도 방향**: `\tkzMarkAngle`이 내각을 표시하는가? (Step 2.5 규칙 적용)
8. **각도 호 size**: 0.4 (이전 0.7 → 0.4 갱신, 변 길이 비례 X — 절대 고정)
9. **각도 라벨 위치**: 호 외측 (pos 1.3-1.5)
10. **각도 채움 금지**: `\tkzMarkAngle[fill=...]` 사용 금지. 채움은 `\tkzFillPolygon` 면적 강조 전용.
11. **같은 각 표기**: 같은 반지름 호 두 번. 슬래시 마크 금지 (변=슬래시, 각=호만).
12. **평행 마크**: 닮음·평행선 비례 도형에서는 화살표 마크 생략 (텍스트 조건 의존). 사각형 외곽 평행 변에서만 단일 `>` 사용.
13. **명명 평행선**: ℓ ∥ m ∥ n 은 화살표 X, 선 끝 텍스트 라벨만.
14. **길이 라벨**: exam·workbook=**인라인 디폴트** (`\tkzLabelSegment`); **textbook=변/현은 점선 치수 호(`\dimarc`) 디폴트**, 내부 선분은 인라인 (modern도 점선 호 허용). ROLE: 실제 윤곽 변은 길이표시용 dashed 금지.
15. **라벨 회전**: 회전된 변에서도 라벨 텍스트는 수평 (`sloped` 사용 금지).
16. **라벨 겹침**: 라벨이 선분이나 다른 라벨과 겹치지 않는가? (`verify-overlap.py` 자동 검증)
17. **구하는 값 표시**: 구하는 각도/길이에 `$x$`로 라벨 표시 (채움/강조색 금지)
18. **각도 기호**: `$40^\circ$` 형식 사용 확인 (`\degree` 미사용)
19. **점 크기**: `\tkzDrawPoints[size=0]` 일반 점, 중심점(O, I, G, 대각선 교점)은 `size=2pt` visible
20. **라벨 표기**: 대문자 점 `$\mathrm{A}$`, 변수 `$x$`, 선 `$\ell$`, 변 길이 `$a$` 일관
21. **선 스타일**: 보조선은 solid 디폴트. dashed 는 가려진 변·연장선 한정.
22. **음영색**: exam=`gray!15`/`gray!20` (accent 금지, **불변**); **textbook=`emphPeach`/`emphCream`/`emphTan` 또는 `gray!22`, 답 부분영역 한정** (fill-only, 한 tint, fill 먼저 → 검은 선 위에).

---

## 스타일 프리셋

사용자가 스타일을 명시하면 아래 프리셋을 자동 적용합니다. **미지정 시 대상별 분기**: 중학(중1–중3)·에듀넷/KERIS·검정교과서 자료 → **textbook**; 수능·평가원·고등 단원평가 → **exam**. 명시된 프리셋이 있으면 그것을 우선.

| 프리셋 | line_pt | aux_pattern | label_font | point_style | color | dim_default | use_case |
|--------|---------|-------------|------------|-------------|-------|-------------|----------|
| **exam** (고등/평가지 기본) | 0.4 (균일) | `dashed` 단일 (한정 용도) | `\small` | size=0 (중심점만 size=2) | 흑백 + `gray!15` fill 옵션 | **인라인** | 수능·평가원·고등 단원평가 (한국 평가지 표준) |
| **textbook** (중학 기본) | 0.5 외곽 / 0.33 점선(~0.65x) | `dashed`, `dash pattern=on 3pt off 2.2pt` | `\small` | size=0 (중심점 size=2) | 흑백 + 따뜻한 fill(emphPeach/emphCream/emphTan) 또는 gray!22 (답 부분영역 한정) | **변/현=점선 치수 호** + 내부선분 인라인 | 에듀넷 중1–중3·검정교과서 (중학 기본) |
| workbook | 0.45 | `dashed` 단일 | `\footnotesize` | size=0 | 흑백 + 회색 fill | **인라인** | 쎈·마플·블랙라벨 |
| academy | 0.4 | `dashed` 단일 | `\scriptsize` | size=0 | 흑백 | 인라인 | 학원 자체제작 프린트 |
| modern | 0.6 | dashed/dotted/dash-dot 분기 가능 | `\normalsize` | size=2 | 4색 + 따뜻한 fill 가능 | 외측 점선 호 (§B-D) | IB·디지털 교재 |

> **★ 굵기 정책 (프리셋 분기)**:
> - `exam`(한국 평가지 인쇄, Agent 9): 주선/보조선 굵기 차이가 **시각적으로 식별 불가** → 균일 thin(0.4pt), 의미 구분은 **패턴(solid/dashed)** 으로만. **불변**.
> - `textbook`(에듀넷 중3 교과서, 2026-05 레퍼런스 실측): solid 외곽 0.5pt vs 점선 0.33pt(**~0.65x**)로 **명확히 가늘게**. 인쇄-평가지 대 교과서 도판의 **매체 차이**.

**프리셋 적용 코드 — exam (불변):**
```latex
\tkzSetUpLine[line width=0.4pt,color=black]
\tkzSetUpLabel[font=\small]
\tkzSetUpPoint[size=0]
% 중심점(외심·내심·G·교점 O) 만 visible:
% \tkzDrawPoint[size=2pt](O)
```

**프리셋 적용 코드 — textbook (에듀넷 중3 표준):**
```latex
\tkzSetUpLine[line width=0.5pt,color=black]      % 외곽 변/현/원 = solid 0.5pt
\tkzSetUpLabel[font=\small]
\tkzSetUpPoint[size=0]                            % 중심점 O/I/G/대각선 O 만 size=2pt
% --- 점선(보조/치수) 스타일: 외곽선의 ~0.65배, 듬성한 패턴 ---
\tikzset{dimdash/.style={dashed, line width=0.33pt, dash pattern=on 3pt off 2.2pt}}
\tikzset{auxdash/.style={dashed, line width=0.33pt, dash pattern=on 3pt off 2.2pt}}
% --- 따뜻한 강조 fill 팔레트 (에듀넷 픽셀 실측) ---
\definecolor{emphPeach}{RGB}{248,163,135}  % 강조 살몬 ~orange!75, fill opacity=0.45
\definecolor{emphCream}{RGB}{255,244,215}  % 3D 본체 워시 ~orange!15 (opacity 불필요)
\definecolor{emphTan}{RGB}{235,207,143}    % 중간 탄/부채꼴 ~orange!50
\definecolor{emphGray}{RGB}{197,199,199}   % 중립 대안 ~black!22
\definecolor{emphLilac}{RGB}{197,165,209}  % 겹침/교집합 ~violet!30
% --- 치수 호 매크로: \dimarc{P}{Q}{bend}{label} (양수 bend=좌측, 음수=우측 부풀림) ---
\newcommand{\dimarc}[4]{\draw[dimdash] (#1) to[bend left=#3]
  node[midway,fill=white,inner sep=1pt,font=\small]{#4} (#2);}
```

사용자가 "수능 스타일"이라 하면 exam, "EBS·교과서·중학 스타일"이면 textbook, "현대적·컬러"이면 modern 프리셋을 적용합니다. 따뜻한 fill·`\dimarc`는 **textbook(+modern) 전용** — exam은 0.4pt·인라인·gray!15로 **불변**.

---

## 점 라벨 타이포그래피 정책

**기본값 (모든 프리셋)**: 점 이름은 **upright** `$\mathrm{A}$` — ISO 80000-2 권고 준수.
**한국 평가지 검증 결과** (Agent 5, 13/13 전수 일치): Computer Modern Roman upright 가 표준 — **변경 불요**.

| 요소 | 표기 | LaTeX | 비고 |
|------|------|-------|------|
| 대문자 점 (A, B, C, …) | upright | `$\mathrm{A}$` | 한국 평가지 100% 일치 |
| **닮음 대응점 prime** | upright + prime | `$\mathrm{A}'$` | 닮음 단원 표준 (Agent 5) |
| 소문자 변수 (x, y) | italic | `$x$`, `$y$` | 미지수 |
| **선 (l, m, n)** | italic | `$\ell$`, `$m$`, `$n$` | 평행선 명명 (Agent 5) |
| **변 길이 (a, b, c)** | italic | `$a$`, `$b$`, `$c$` | 변 길이 미지수 (Agent 5) |
| 함수 이름 | upright (자동) | `$\sin$`, `$\cos$` | |
| 단위 | upright. exam=타이트/좁게, **textbook=thin space** | exam `$4\mathrm{cm}$` / textbook `$4\,\mathrm{cm}$` | 에듀넷 중3 교과서는 thin space `N\,cm` 표준; 삼각비 직각삼각형 도형은 bare 숫자(단위 생략) 허용 (Agent 5 / 2026-05 레퍼런스) |
| 각도 기호 | `^\circ` | `$60^\circ$` | `\degree` 금지 |
| 기하 합동 | `\cong` | `$\triangle\mathrm{ABC} \cong \triangle\mathrm{DEF}$` | |
| 기하 닮음 | `\sim` 또는 `\backsim` | `$\triangle\mathrm{ABC} \sim \triangle\mathrm{DEF}$` | |
| 닮음비 (콜론) | `\rat{m}{n}` 매크로 | `$2\!:\!3$` | thin negative space (Agent 3) |
| 수론 합동 | `\equiv` | `$a \equiv b \pmod{n}$` | 기하에서 사용 금지 |

**italic 선택 프리셋** (사용자가 "italic 수능 스타일" 명시 시만):
preamble에 다음 토글 추가:
```latex
% 기본: upright
\newcommand{\ptlab}[3][]{\tkzLabelPoint[#1](#2){$\mathrm{#3}$}}
% italic 전환 (주석 해제):
% \renewcommand{\ptlab}[3][]{\tkzLabelPoint[#1](#2){$#3$}}
```

> `\ptlab`은 preamble 유틸리티입니다. skill.md 본문 예시는 `\tkzLabelPoint`를 직접 사용합니다.

---

## 따뜻한 강조 fill (textbook 전용 — 에듀넷 중3 정합)

에듀넷 중3 교과서 도형은 답 영역을 **따뜻한 탄/피치색**으로 강조한다(픽셀 실측). `exam`은 `gray!15`/`gray!20` + "accent 컬러 금지" **불변**; 따뜻한 fill은 **textbook(+modern) 전용**.

**명명색** (textbook preamble의 `\definecolor` 5개):

| 색 | RGB | 근사 | 용도 | opacity |
|----|-----|------|------|---------|
| `emphPeach` | 248,163,135 | orange!75 | 답 부분영역 강조(살몬) | 0.45 |
| `emphCream` | 255,244,215 | orange!15 | 3D 입체 본체 워시 | 1.0 (자체 옅음) |
| `emphTan` | 235,207,143 | orange!50 | 부채꼴·중간 강조 | 0.5 |
| `emphGray` | 197,199,199 | black!22 | 중립 대안(평범한 넓이) | 1.0 |
| `emphLilac` | 197,165,209 | violet!30 | 겹침/교집합 전용 | 0.4 |

**사용 규칙**:

1. **기본 = 채움 없음** (레퍼런스 >95% 무채움 흑백). 채움은 강조가 필요할 때만.
2. **답 부분영역만** 채운다(전체 외곽 X). 예외: 3D 입체는 `emphCream` 옅은 전체 워시 허용.
3. **한 도형에 한 tint만** — `emphPeach`(강조) **또는** `emphCream`(본체) **또는** `gray!22`(중립). gray와 peach 혼용 금지. `emphLilac`은 겹침 전용.
4. **FILL-ONLY**: 경계선은 항상 `draw=black`. 색 외곽선 금지.
5. **그리기 순서**: fill 최하층 → 검은 변 → 점선 호 → 마크 → 라벨 (tint 위로 선·라벨이 비쳐야 함).

```latex
% 답 부분영역만 강조 (fill 먼저, 검은 선/라벨은 위에)
\fill[emphPeach, fill opacity=0.45] (O) -- (A) -- (B) -- cycle;  % 답영역(예: △OAB)
\tkzDrawCircle(O,P)
\tkzDrawSegments(O,A O,B)
\tkzMarkRightAngle[size=0.22](A,O,B)
% 중립/겹침 대안:
% \fill[emphGray] <부채꼴 path>;          % 평범한 넓이
% \fill[emphLilac, fill opacity=0.40] <겹침 path>;  % 두 도형 교집합
```

---

## 핵심 구성 관용구

### 관용구 1: 선분 위의 점 (조건부 교점)
"변 AB 위의 점 D에서 CD = k" → 직선 AB와 원(C, k)의 교점
```latex
% B가 이미 원 위에 있으면 common=B로 제외
\tkzInterLC[common=B](A,B)(C,B) \tkzGetFirstPoint{D}

% B가 원 위에 없으면 near로 원하는 점 선택
\tkzInterLC[near](A,B)(C,B) \tkzGetPoints{D}{D'}
```

### 관용구 2: 원과 직선의 교점 (중심이 직선 위)
직선이 원의 중심을 지나면 지름의 양 끝점이 교점:
```latex
% CE = BC, E는 AC 위 (C가 원의 중심이자 직선 위)
\tkzInterLC[near](A,C)(C,B) \tkzGetPoints{E}{E'}
% E: A에 가까운 점 (선분 AC 위), E': C 너머 반대쪽
```

### 관용구 3: 수선의 발
```latex
\tkzDefPointBy[projection=onto B--C](A) \tkzGetPoint{H}
\tkzMarkRightAngle(A,H,B)
```

### 관용구 4: 내분점/외분점
```latex
% A에서 AB의 2/5 지점
\tkzDefBarycentricPoint(A=3,B=2) \tkzGetPoint{P}  % AP:PB = 2:3
% 또는
\tkzDefPointOnLine[pos=0.4](A,B) \tkzGetPoint{P}   % pos: 0=A, 1=B
```

### 관용구 5: 등변 조건으로 점 구성
"CD = BC" 같은 조건 → 원과 직선의 교점으로 변환:
```latex
% CD = BC, D는 AB 위 → 원(C, BC) ∩ 직선(AB)
\tkzInterLC[common=B](A,B)(C,B) \tkzGetFirstPoint{D}
```

---

## 한국 수학 시험 패턴

### 패턴 1: 이등변삼각형 + 조건부 점 (등변 조건)

**유형:** AB=AC인 이등변삼각형에서 변 위의 점이 등변 조건을 만족

```latex
\begin{tikzpicture}
  % 이등변삼각형 ABC (∠B = ∠C = 70°, ∠A = 40°)
  \tkzDefPoints{0/0/B, 5/0/C}
  \tkzDefTriangle[two angles=70 and 70](B,C) \tkzGetPoint{A}
  % D: AB 위, CD = BC
  \tkzInterLC[common=B](A,B)(C,B) \tkzGetFirstPoint{D}
  % E: AC 위, CE = BC
  \tkzInterLC[near](A,C)(C,B) \tkzGetPoints{E}{E'}
  % 그리기
  \tkzDrawPolygon(A,B,C)
  \tkzDrawSegments(C,D D,E)
  \tkzMarkSegments[mark=||](B,C C,D C,E)
  \tkzMarkAngle[size=0.4](B,A,C)
  \tkzLabelAngle[pos=1.4](B,A,C){$40^\circ$}
  \tkzMarkAngle[size=0.4](D,E,C)
  \tkzLabelAngle[pos=1.5](D,E,C){$x$}
  \tkzDrawPoints[size=0](A,B,C,D,E)
  \tkzLabelPoint[above](A){$\mathrm{A}$}
  \tkzLabelPoint[below left](B){$\mathrm{B}$}
  \tkzLabelPoint[below right](C){$\mathrm{C}$}
  \tkzLabelPoint[left](D){$\mathrm{D}$}
  \tkzLabelPoint[right](E){$\mathrm{E}$}
\end{tikzpicture}
```

### 패턴 2: 삼각형의 오심 (외심/내심/수심)

```latex
\begin{tikzpicture}
  \tkzDefPoints{0/0/B, 6/0/C, 1.5/4.5/A}
  % 외심 + 외접원
  \tkzDefTriangleCenter[circum](A,B,C) \tkzGetPoint{O}
  \tkzDefCircle[circum](A,B,C) \tkzGetPoints{O}{o}
  % 수선의 발 (수직이등분선 표시용)
  \tkzDefMidPoint(B,C) \tkzGetPoint{Ma}
  \tkzDefMidPoint(A,C) \tkzGetPoint{Mb}
  \tkzDrawPolygon(A,B,C)
  \tkzDrawCircle[thin,gray](O,o)
  \tkzDrawSegments[dashed](O,Ma O,Mb)
  \tkzMarkRightAngle[size=0.2](O,Ma,B)
  \tkzMarkRightAngle[size=0.2](O,Mb,A)
  \tkzDrawPoints[size=0](A,B,C,O)
  \tkzAutoLabelPoints[center=O](A,B,C)
  \tkzLabelPoint[above right](O){$\mathrm{O}$}
\end{tikzpicture}
```

### 패턴 3: 원에 내접하는 사각형 + 접선

```latex
\begin{tikzpicture}
  \tkzDefPoint(0,0){O}
  \tkzDefPoint(3,0){A}
  % 원 위의 4점
  \tkzDefPointOnCircle[through=center O angle 40 point A]  \tkzGetPoint{B}
  \tkzDefPointOnCircle[through=center O angle 130 point A] \tkzGetPoint{C}
  \tkzDefPointOnCircle[through=center O angle 210 point A] \tkzGetPoint{D}
  % 접선 (A에서)
  \tkzDefLine[tangent at=A](O) \tkzGetPoint{t}
  \tkzDrawCircle(O,A)
  \tkzDrawPolygon(A,B,C,D)
  \tkzDrawLine[add=0.3 and 0.3,dashed](A,t)
  \tkzMarkRightAngle[size=0.2](t,A,O)
  \tkzDrawPoints[size=0](A,B,C,D,O)
  \tkzLabelPoint[right](A){$\mathrm{A}$}
  \tkzLabelPoint[above right](B){$\mathrm{B}$}
  \tkzLabelPoint[above left](C){$\mathrm{C}$}
  \tkzLabelPoint[left](D){$\mathrm{D}$}
  \tkzLabelPoint[below](O){$\mathrm{O}$}
\end{tikzpicture}
```

### 패턴 4: 평행선 + 동위각/엇각 + 삼각형

```latex
\begin{tikzpicture}
  \tkzDefPoints{0/0/A, 7/0/B, 1/3/C, 8/3/D}
  \tkzDefPoints{2.5/-0.5/E, 5/4/F}
  \tkzInterLL(E,F)(A,B) \tkzGetPoint{P}
  \tkzInterLL(E,F)(C,D) \tkzGetPoint{Q}
  \tkzDrawLines[add=.2 and .2](A,B C,D)
  \tkzDrawLine[add=.3 and .3](P,Q)
  % 동위각 표시 (같은 색)
  \tkzFillAngle[size=0.7,fill=blue!20](B,P,Q)
  \tkzFillAngle[size=0.7,fill=blue!20](D,Q,F)
  \tkzLabelAngle[pos=1.0](B,P,Q){$\alpha$}
  \tkzLabelAngle[pos=1.0](D,Q,F){$\alpha$}
  % 엇각 표시 (다른 색)
  \tkzFillAngle[size=0.6,fill=red!20](Q,P,A)
  \tkzFillAngle[size=0.6,fill=red!20](F,Q,C)
  \tkzDrawPoints[size=0](P,Q)
  \tkzLabelPoint[below](P){$\mathrm{P}$}
  \tkzLabelPoint[above left](Q){$\mathrm{Q}$}
  % 평행 표시
  \tkzLabelLine[pos=0.1,above](A,B){$\ell$}
  \tkzLabelLine[pos=0.1,above](C,D){$m$}
\end{tikzpicture}
```

### 패턴 5: 원과 접선 + 할선 (방멱)

```latex
\begin{tikzpicture}
  \tkzDefPoints{0/0/O, 3/0/A, 6.5/1.5/P}
  \tkzDefLine[tangent from=P](O,A) \tkzGetPoints{T1}{T2}
  % 할선: P를 지나는 직선과 원의 두 교점
  \tkzDefPoint(1.5,2.5){Q}
  \tkzInterLC[near](P,Q)(O,A) \tkzGetPoints{X}{Y}
  \tkzDrawCircle(O,A)
  \tkzDrawSegments(P,T1 P,Y)
  \tkzDrawSegment[dashed](O,T1)
  \tkzMarkRightAngle[size=0.2](P,T1,O)
  \tkzDrawPoints[size=0](O,P,T1,X,Y)
  \tkzLabelPoint[below](O){$\mathrm{O}$}
  \tkzLabelPoint[right](P){$\mathrm{P}$}
  \tkzLabelPoint[above left](T1){$\mathrm{T}$}
  \tkzLabelPoint[above left](X){$\mathrm{A}$}
  \tkzLabelPoint[left](Y){$\mathrm{B}$}
  % PA·PB = PT² 표시
  \tkzLabelSegment[above,sloped,pos=0.6](P,T1){$PT$}
\end{tikzpicture}
```

### 패턴 6: 닮음 삼각형 (평행선에 의한)

> **★ 한국 평가지 검증 (Agents 3, 6)**: 평행 화살표 마크 `>` / `>>` 는 **닮음·평행선 비례 도형에서 거의 0건 사용**.
> 평행 조건은 본문 텍스트("DE∥BC")로 전달하고, 도형에는 변 길이 라벨만 표기하는 것이 한국 표준이다.
> 평행 화살표 마크는 *사다리꼴·평행사변형 외곽 변* 에서만 사용하는 보수적 패턴.

```latex
\begin{tikzpicture}
  \tkzDefPoints{0/0/B, 6/0/C, 2/5/A}
  % DE // BC (D는 AB 위, E는 AC 위) — 본문에서 "DE∥BC" 명시
  \tkzDefPointOnLine[pos=0.4](A,B) \tkzGetPoint{D}
  \tkzDefPointOnLine[pos=0.4](A,C) \tkzGetPoint{E}
  \tkzDrawPolygon(A,B,C)
  \tkzDrawSegment(D,E)
  % ★ 평행 화살표 마크 생략 — 한국 평가지 표준
  % (선택) modern 프리셋 또는 명시적 강조 시:
  % \tkzMarkSegment[mark=>](D,E)
  % \tkzMarkSegment[mark=>](B,C)
  % 닮음비 라벨 — 인라인
  \tkzLabelSegment[left](A,D){$m$}
  \tkzLabelSegment[left](D,B){$n$}
  \tkzDrawPoints[size=0](A,B,C,D,E)
  \tkzLabelPoint[above](A){$\mathrm{A}$}
  \tkzLabelPoint[below left](B){$\mathrm{B}$}
  \tkzLabelPoint[below right](C){$\mathrm{C}$}
  \tkzLabelPoint[left](D){$\mathrm{D}$}
  \tkzLabelPoint[right](E){$\mathrm{E}$}
\end{tikzpicture}
```

### 패턴 7: 사각형 대각선 4분할 + 교점 O (사각형 단원 시그니처)

**유형**: 사각형 ABCD 의 두 대각선이 점 O 에서 교차, 4개 삼각형 중 하나(또는 두 개)에 옅은 회색 fill 로 답 영역 강조.

**한국 평가지 빈도** (Agents 2, 10): 사각형 단원의 ~59%, 교점 라벨은 94% `O`.

```latex
\begin{tikzpicture}
  % 평행사변형 ABCD (CW from A 좌상)
  \tkzDefPoints{0/4/A, 0/0/B, 7/0/C, 7/4/D}
  % 대각선 교점
  \tkzInterLL(A,C)(B,D) \tkzGetPoint{O}
  % 답 영역 fill (예: △OBC)
  \tkzFillPolygon[color=gray!20](O,B,C)
  % 외곽 + 대각선
  \tkzDrawPolygon[thick](A,B,C,D)
  \tkzDrawSegments[thick](A,C B,D)
  % 점·라벨
  \tkzDrawPoints[size=0](A,B,C,D)
  \tkzDrawPoint[size=2pt](O)               % 중심점 visible
  \tkzLabelPoint[above left](A){$\mathrm{A}$}
  \tkzLabelPoint[below left](B){$\mathrm{B}$}
  \tkzLabelPoint[below right](C){$\mathrm{C}$}
  \tkzLabelPoint[above right](D){$\mathrm{D}$}
  \tkzLabelPoint[above right=1pt](O){$\mathrm{O}$}
\end{tikzpicture}
```

### 패턴 8: 직각삼각형 + 빗변 위 수선의 발 D (닮음 3분할)

**유형**: △ABC, ∠A=90°, AD⊥BC. 한 직각삼각형 안에 △ABD ∽ △CBA ∽ △ACD 동시 포함.

**한국 평가지 빈도** (Agents 3, 4): 닮음 단원 5+ 회, 후반 12+ 회 — **가장 빈출 닮음 패턴**.

```latex
\begin{tikzpicture}
  % B 좌하, C 우하, A 위 (∠A=90°)
  \tkzDefPoints{0/0/B, 7/0/C}
  \tkzDefTriangle[pythagore](B,C) \tkzGetPoint{A}    % 3:4:5 (또는 임의 직각)
  % 빗변 위 수선의 발
  \tkzDefPointBy[projection=onto B--C](A) \tkzGetPoint{D}
  % 그리기
  \tkzDrawPolygon[thick](A,B,C)
  \tkzDrawSegment[thick](A,D)
  \tkzMarkRightAngle[size=0.2](B,A,C)         % ∠A 직각
  \tkzMarkRightAngle[size=0.2](A,D,B)         % AD⊥BC
  % 길이 라벨 (인라인)
  \tkzLabelSegment[left](A,B){$c$}
  \tkzLabelSegment[right](A,C){$b$}
  \tkzLabelSegment[below](B,D){$x$}
  \tkzLabelSegment[below](D,C){$y$}
  \tkzLabelSegment[right=1pt](A,D){$h$}
  % 점·라벨
  \tkzDrawPoints[size=0](A,B,C,D)
  \tkzLabelPoint[above](A){$\mathrm{A}$}
  \tkzLabelPoint[below left](B){$\mathrm{B}$}
  \tkzLabelPoint[below right](C){$\mathrm{C}$}
  \tkzLabelPoint[below](D){$\mathrm{D}$}
\end{tikzpicture}
```

### 패턴 9: 변 위 정사각형 (피타고라스 풍차)

**유형**: 직각삼각형 세 변에 외측으로 정사각형, 면적 라벨(`a²`, `b²`, `c²`).

**한국 평가지 빈도** (Agents 4, 10): 피타고라스 단원 8+ 회 — 단원 시그니처.

```latex
\begin{tikzpicture}[scale=0.6]
  \tkzDefPoints{0/0/B, 4/0/C}
  \tkzDefTriangle[pythagore](B,C) \tkzGetPoint{A}
  % 외측 정사각형 (\tkzDefSquare 매크로 — 두 점에서 외측 자동)
  \tkzDefSquare(B,C) \tkzGetPoints{S1}{S2}    % BC 변의 정사각형 (아래)
  \tkzDefSquare(C,A) \tkzGetPoints{T1}{T2}    % CA 변의 정사각형 (오른쪽)
  \tkzDefSquare(A,B) \tkzGetPoints{U1}{U2}    % AB 변의 정사각형 (왼쪽)
  % 그리기
  \tkzDrawPolygon[thick](A,B,C)
  \tkzDrawPolygon[thick, fill=gray!10](B,C,S1,S2)
  \tkzDrawPolygon[thick, fill=gray!10](C,A,T1,T2)
  \tkzDrawPolygon[thick, fill=gray!10](A,B,U1,U2)
  \tkzMarkRightAngle[size=0.2](B,A,C)
  % 면적 라벨 (정사각형 중심에)
  \node at ($(B)!0.5!(S1)$) {$a^2$};
  \node at ($(C)!0.5!(T1)$) {$b^2$};
  \node at ($(A)!0.5!(U1)$) {$c^2$};
  \tkzDrawPoints[size=0](A,B,C)
  \tkzLabelPoint[above](A){$\mathrm{A}$}
  \tkzLabelPoint[below left](B){$\mathrm{B}$}
  \tkzLabelPoint[below right](C){$\mathrm{C}$}
\end{tikzpicture}
```

### 패턴 10: 평행선 횡단 닮음 (Thales)

**유형**: ℓ ∥ m (또는 ℓ ∥ m ∥ n) 사이를 가로지르는 두 직선이 만든 닮음 삼각형.

**한국 평가지 빈도** (Agents 3, 10): 닮음 단원 4+ 회, 별개 패턴.

```latex
\begin{tikzpicture}
  % 두 평행선 ℓ (위), m (아래)
  \tkzDefPoints{-0.5/3/L1, 7.5/3/L2}    % ℓ 양 끝
  \tkzDefPoints{-0.5/0/M1, 7.5/0/M2}    % m 양 끝
  % 횡단 두 직선 (한 점 P 에서 출발, ℓ·m 위 점 A·B / C·D 만남)
  \tkzDefPoints{3/4/P}
  \tkzDefPoints{1/3/A, 5/3/C, 0/0/B, 6/0/D}     % 직접 좌표 (간단 버전)
  % 평행선
  \tkzDrawSegments[thick](L1,L2 M1,M2)
  % 횡단선
  \tkzDrawSegment[thick](A,B)
  \tkzDrawSegment[thick](C,D)
  % 평행선 라벨 (텍스트만, 화살표 X)
  \node[right, font=\small] at (L2) {$\ell$};
  \node[right, font=\small] at (M2) {$m$};
  % 인라인 길이 라벨
  \tkzLabelSegment[left](A,B){$5$}
  \tkzLabelSegment[right](C,D){$x$}
  \tkzDrawPoints[size=0](A,B,C,D)
  \tkzLabelPoint[above](A){$\mathrm{A}$}
  \tkzLabelPoint[below](B){$\mathrm{B}$}
  \tkzLabelPoint[above](C){$\mathrm{C}$}
  \tkzLabelPoint[below](D){$\mathrm{D}$}
\end{tikzpicture}
```

### 패턴 11: 포함형 합동·닮음 (한 도형 안에 작은 닮은 도형)

**유형**: 큰 △ABC 또는 큰 사각형 안에 한 변·한 꼭짓점을 공유하는 작은 닮은 도형 △ADE.

**한국 평가지 빈도** (Agents 1, 3, 4, 10): 합동·닮음 메인 idiom. 두 도형 좌우 분리는 닮음 단원에서 *때로* 등장(9건), 그 외는 포함형이 압도적.

```latex
\begin{tikzpicture}
  % 큰 △ABC
  \tkzDefPoints{0/0/B, 7/0/C, 1.5/5/A}
  % 작은 닮은 △ADE (DE ∥ BC, A 공유)
  \tkzDefPointOnLine[pos=0.4](A,B) \tkzGetPoint{D}
  \tkzDefPointOnLine[pos=0.4](A,C) \tkzGetPoint{E}
  % 작은 닮은 도형 fill 강조 (옅은 회색 또는 노랑)
  \tkzFillPolygon[color=gray!15](A,D,E)
  % 외곽 + 내부 분할
  \tkzDrawPolygon[thick](A,B,C)
  \tkzDrawSegment[thick](D,E)
  % 인라인 길이 라벨
  \tkzLabelSegment[left](A,D){$3$}
  \tkzLabelSegment[left](D,B){$5$}
  \tkzLabelSegment[right](A,E){$4$}
  \tkzLabelSegment[right](E,C){$x$}
  \tkzDrawPoints[size=0](A,B,C,D,E)
  \tkzLabelPoint[above](A){$\mathrm{A}$}
  \tkzLabelPoint[below left](B){$\mathrm{B}$}
  \tkzLabelPoint[below right](C){$\mathrm{C}$}
  \tkzLabelPoint[left](D){$\mathrm{D}$}
  \tkzLabelPoint[right](E){$\mathrm{E}$}
\end{tikzpicture}
```

> **닮음비 매크로** (Agent 3 추천):
> ```latex
> \newcommand{\rat}[2]{$#1\!:\!#2$}    % 콜론 양옆 thin negative space
> ```
> 사용: `\rat{2}{3}` → `2:3` (한국 평가지 표준 형식).

---

## 길이 표시 (Dimension Annotation)

> **★ 정책 (프리셋 분기 — 2026-05 에듀넷 중3 레퍼런스로 재정합)**:
>
> **ROLE 규칙** (에듀넷 레퍼런스 18/18 무반례): **SOLID = 도형의 실제 윤곽**(원·다각형 변·현·접선·빗변). **DASHED = 보조 overlay 전용** — (a) 길이를 매단 바깥쪽 치수 호, (b) 중심에서 나온 반지름/아포템·현에 내린 수선, (c) 연장선/가이드. **실제 윤곽 변은 길이 표시를 위해 절대 dashed로 그리지 않는다** — 점선은 측정/보조 overlay 전용. 이 한 원칙이 아래 Method 2·3을 묶는다.
>
> **외곽 변/현 길이 표기 디폴트 (프리셋 분기)** — *직전 라운드 codex 자문(인쇄 문제집·평가원 기준)과 에듀넷 중3 교과서 레퍼런스를 화해시킨 결론*:
> - **textbook (에듀넷 중3 교과서)**: **변/현 = 바깥쪽 얕은 점선 치수 호**(`\dimarc`, Method 2). 에듀넷 중3 도판의 **지배적 표기**(레퍼런스 ≥9/18 페이지, 미래엔·신사고·교학사·천재·금성·동아 — 무반례). 값은 호 중앙 `fill=white`로 점선을 끊는다.
> - **exam (수능/평가원), workbook (쎈/마플/블랙라벨/EBS 수능특강)**: **변 옆 직접 인라인**(Method 1). codex 자문대로 인쇄 문제집·평가원 정통 표기는 인라인 — **불변**.
> - 내부 선분(수선·중선·대각선)은 모든 프리셋에서 인라인 또는 Method 3.
>
> > 과거 메모: Agent 12의 "외측 점선 호 11/16"은 *에듀넷 중3 도판의 실제 표준*이었고(당시 "자동생성 흔적"으로 잘못 기각됨), codex 자문은 *쎈/마플/평가원 문맥*에서 옳다. 둘은 **프리셋(매체) 차이**이지 모순이 아니다.
>
> **Method 3 의미 분기**:
>   - 도형의 본질적 구성선(마름모/정사각형/평행사변형 대각선, 사각형 분할선) = **solid**
>   - 풀이용 보조선(작도 보조, 연장선, 숨은 변) = **dashed**
>   - 수선·높이: 주어진 높이(넓이 핵심) = thin solid + 직각 / 추가 보조선 = dashed. **단 textbook에서 원 중심 반지름·아포템·현에 내린 수선은 dashed(`auxdash`)** + 수선의 발 직각 (에듀넷 정합, 아래 Method 3 carve-out).
>
> **점선 패턴**: exam=`dash pattern=on 2pt off 1.5pt`; **textbook=`dash pattern=on 3pt off 2.2pt`(더 듬성)**.
>
> **굵기 위계**: exam=균일 thin(0.4pt, 패턴으로만 구분); **textbook=외곽 0.5pt solid / 점선(치수·보조) 0.33pt(~0.65x)** — 점선이 외곽보다 명확히 가늘게.
>
> **fill=white 라벨**: textbook 치수 호의 값은 호 중앙 `fill=white inner sep=1pt`로 점선을 끊는다(레퍼런스 표준). 그 외 인라인 라벨은 선 옆 분리 배치.

### Method 1 — 인라인 라벨 (변 옆 직접)

```latex
\tkzLabelSegment[above](A,B){$5\,\mathrm{cm}$}      % 외곽 변, 위쪽 외측
\tkzLabelSegment[below](B,C){$8\,\mathrm{cm}$}      % 외곽 변, 아래쪽 외측
\tkzLabelSegment[right](D,C){$6\,\mathrm{cm}$}      % 외곽 변, 오른쪽 외측
\tkzLabelSegment[left](A,D){$h$}                     % 변수 라벨 (italic 자동)
```

**Method 1b** (★ 변 위 중앙 + fill=white 변 끊기) — 사선 변·내부 선분에 안정적, codex+자체 검증:
```latex
\path (A) -- (G) node[midway, fill=white, inner sep=3pt] {$6$};
\path (B) -- (G) node[pos=0.45, fill=white, inner sep=3pt] {$8$};
```

**Method 1c** (수평/수직 변 외측 명시 offset):
```latex
\path (B) -- (C) node[midway, below=5pt, fill=white, inner sep=1pt] {$9\,\mathrm{cm}$};
```

### Method 2 — 외측 점선 치수 호 (★ textbook 변/현 길이 디폴트 / exam·workbook은 인라인)

> **프리셋 분기**:
> - **textbook (에듀넷 중3)**: 변·현 길이의 **표준** — 같은 두 끝점을 잇는 **바깥쪽(무게중심 반대쪽) 얕은 점선 호**, 값은 호 중앙 `fill=white inner sep=1pt`. bow는 **얕게**(현 길이의 8–15%, `bend 12–18`) — 통통한 렌즈가 아니라 가는 측정 곡선으로 읽혀야 함.
> - **exam·workbook**: 외측 점선 호 **사용 안 함** — 변 옆 직접 인라인(Method 1). (codex 자문: 인쇄 문제집·평가원 정통 표기는 인라인.)
>
> **ROLE 재확인**: 점선 호는 solid 외곽 변 *위에 겹쳐지는 측정 overlay*다. 외곽 변 자체는 항상 solid로 따로 그린다 — 점선 호가 변을 대체하지 않는다.

```latex
% textbook 기본: \dimarc{P}{Q}{bend}{값}  (양수 bend=좌측 부풀림; 밑변 등 아래로는 to[bend right] 변형)
\dimarc{A}{C}{14}{$13\,\mathrm{cm}$}                 % 빗변: 위로 얕게
\draw[dimdash] (B) to[bend right=14]
  node[midway,fill=white,inner sep=1pt,font=\small]{$5\,\mathrm{cm}$} (C);  % 우측 변: 오른쪽으로
```

**exam·workbook은 인라인 (불변)**:
```latex
\tkzLabelSegment[above](A,D){$9\,\mathrm{cm}$}
\tkzLabelSegment[left](A,B){$6\,\mathrm{cm}$}
```

**bend 방향 결정** (외측 = 도형 무게중심 G 의 반대쪽, 사각형 ABCD CW from A 좌상):
| 변 | 표준 draw 순서 | 외측 | bend |
|----|---------------|------|------|
| AD (위 변) | A → D (좌→우) | 위 (북) | `bend left=N` |
| BC (아래 변) | B → C (좌→우) | 아래 (남) | `bend right=N` |
| AB (왼쪽 변) | A → B (위→아래) | 왼쪽 (서) | `bend right=N` |
| DC (오른쪽 변) | D → C (위→아래) | 오른쪽 (동) | `bend left=N` |
| 사선 변 | (예 사다리꼴 AB 좌측) | 외측 | dot product 룰 (§ 외측 방향 결정 참조) |

**bend 값** (변 길이 L cm 기준): L≤2.5→35 / L≤4→30 / L≤6→22 / L≤9→18 / L≤13→14 / L>13→10

> **★ textbook 얕은 bow**: 위 표는 라벨 sagitta 확보용 깊은 bow(짧은 변에서 큼). **textbook(에듀넷)은 얕게** — 현 길이의 8–15%, 즉 `bend 12–18`로 클램프(긴 변일수록 12에 가깝게). 값은 `fill=white` 노드가 호를 끊으므로 깊은 sagitta 불필요. exam·modern은 위 표대로.

### ★ Method 3 — 내부 보조선 + 라벨 (의미 분기 필수)

**핵심 원칙** (codex 자문): 점선은 *보조 정보*라는 강한 의미. 도형의 본질적 구성선을 dashed 로 그리면 "작도 보조"·"숨은 선"·"나중에 그은 선"으로 오해됨.

**의미 분기**:
| 선분 종류 | 권장 스타일 | 굵기 |
|----------|------------|------|
| 도형 변 (외곽) | **solid** | 0.45-0.5pt |
| **마름모/평행사변형/사각형 대각선** (도형 본질) | **thin solid** | 0.35-0.4pt |
| 사각형 4분할 대각선 + 교점 O | thin solid | 0.4pt |
| 삼각형 중선·중점 연결 | thin solid | 0.4pt |
| 각의 이등분선 (도형의 일부로 그림) | thin solid | 0.4pt |
| **주어진 높이 (넓이 계산 핵심)** | thin solid + 직각 표시 | 0.4pt |
| 풀이용 추가 보조선 (작도) | **dashed** | 0.3-0.35pt |
| 변의 연장선 (점선 화살표) | dashed | 0.3pt |
| 가려진 변·뒤쪽 변 | dashed | 0.35pt |
| 점선 평행 보조선 (대각선의 평행이동 등) | dashed | 0.3pt |

> **★ textbook carve-out (에듀넷 원 도형)**: 위 "도형 본질=solid"는 유지하되, **원 중심에서 나온 반지름/아포템, 현에 내린 수선(수선의 발)은 textbook에서 `auxdash` 점선** + 수선의 발 직각 사각형 + 길이는 점선 옆 인라인. 원·현·접선·외곽 변은 항상 solid. (exam은 이런 구성선을 thin solid로 둬도 됨 — 매체 차이.)
>
> ```latex
> % textbook: 반지름/수선 = dashed, 현·원=solid, 수선의 발에 직각
> \coordinate (O) at (0,0); \draw[line width=0.5pt] (O) circle (2.2);  % 원=solid
> \coordinate (C) at (-1.95,-1); \coordinate (D) at (1.95,-1);
> \draw[line width=0.5pt] (C)--(D);                                     % 현=solid
> \coordinate (N) at (0,-1); \coordinate (A) at (-2.2,0);
> \draw[auxdash] (O)--node[above,inner sep=1.5pt,font=\small]{$4\,\mathrm{cm}$}(A); % 반지름=dashed
> \draw[auxdash] (O)--node[right,inner sep=1.5pt,font=\small]{$2\,\mathrm{cm}$}(N); % 수선=dashed
> \tkzMarkRightAngle[size=0.2](D,N,O)                                   % 수선의 발 직각
> \tkzDrawPoint[size=2pt](O) \tkzLabelPoint[above right](O){$\mathrm{O}$}
> ```

```latex
% 케이스 A: 마름모 대각선 — solid (도형 본질)
\tkzDefPoints{0/3/A, -4/0/B, 0/-3/C, 4/0/D}    % 다이아몬드 배치
\tkzInterLL(A,C)(B,D) \tkzGetPoint{O}
\tkzDrawPolygon[thick](A,B,C,D)
\tkzDrawSegments[thin](A,C B,D)                 % ★ 대각선 = thin solid (NOT dashed)
\tkzLabelSegment[right=2pt](B,O){$8\,\mathrm{cm}$}    % 반대각선 BO 인라인
\tkzLabelSegment[left=2pt](A,O){$6\,\mathrm{cm}$}     % 반대각선 AO 인라인

% 케이스 B: 직각삼각형 빗변 위 주어진 높이 (넓이 핵심) — thin solid
\tkzDefPoints{0/0/B, 5/0/C, 1.8/2.4/A}
\tkzDefPointBy[projection=onto B--C](A) \tkzGetPoint{H}
\tkzDrawPolygon[thick](A,B,C)
\tkzDrawSegment[thin](A,H)                       % ★ thin solid (문제의 높이로 주어짐)
\tkzMarkRightAngle[size=0.2](A,H,B)
\tkzMarkRightAngle[size=0.2](B,A,C)
\tkzLabelSegment[right=2pt](A,H){$h$}

% 케이스 C: 풀이용 추가 보조선 (예: 평행사변형 안에서 추가 작도)
\tkzDrawSegment[dashed, line width=0.3pt,
                dash pattern=on 2pt off 1.5pt](P,Q)
% 라벨은 점선 옆 (선 위 얹지 않음)
\tkzLabelSegment[right=3pt](P,Q){$x$}
```

### Method 4 (★ 신규) — 짧은 점선 패턴 (한국 문제집 표준)

```latex
% Preamble:
\tikzset{auxline/.style={dashed, line width=0.3pt,
                         dash pattern=on 2pt off 1.5pt}}
% 사용:
\tkzDrawSegment[auxline](A,H)         % 풀이 보조선
```

| 패턴 | TikZ 코드 | 인상 |
|------|----------|------|
| 너무 듬성 (피하기) | `dashed` (TikZ 기본 ~3pt-3pt) | 자동 생성 티남 |
| ★ 권장 표준 | `dash pattern=on 2pt off 1.5pt` | 한국 문제집 톤 |
| 더 촘촘 | `dash pattern=on 1.5pt off 1.5pt` | 작은 도형용 |
| 점선 (도트) | `dotted` | **거의 미사용** (한국 평가지) |

### 결정 트리 (어느 Method 를 쓸 것인가)

```
입력: 변 (P, Q), 도형 컨텍스트

1. P-Q 가 도형 외곽 변인가?
   ├── 예 → 단계 2
   └── 아니오 (내부 선분: 수선·중선·대각선) → 단계 3

2. 외곽 변 → Method 선택:
   ├── 단순 변 (충돌·강조 없음) → Method 1 (인라인)
   ├── 변 옆에 다른 라벨/점이 있어 인라인 충돌 → Method 1c (above=5pt offset) 또는 Method 2 (외측 점선 호)
   ├── 사각형 단원·닮음 단원의 둘러싼 도형 (변 길이 강조) → Method 2 권장
   └── 사선 변에서 인라인이 변에 가까움 → Method 1b (fill=white inner sep=3pt)

3. 내부 선분 → Method 선택:
   ├── 수선의 발(높이)·중선·내분 보조선 → Method 3 (보조선 자체 dashed + 라벨)
   ├── 도형 안 분할선 (대각선 등) — 답 영역 강조와 함께 → Method 1b 또는 Method 3
   └── 정수 분할 (변 위 두 점) → Method 1 (각 세그먼트 인라인 2개)

특수: 짧은 변 (L<2cm) + 긴 라벨 → Leader (D9)
특수: 호/반경 치수 → Pattern D10 (호 외측)
```

### verify-overlap.py 통과 임계 (실측)

| 패턴 | 안전 ring ratio | 메모 |
|------|---------------|------|
| Method 1 inline (`above`) | < 0.02 | 디폴트 안전 |
| Method 1b inline (fill=white inner sep=3pt) | < 0.025 | 변 끊기, 사선 안전 |
| Method 1c offset (`above=5pt + inner sep=1pt`) | < 0.025 | 수평/수직 안전 |
| Method 2 외측 점선 호 (`bend N + fill=white`) | < 0.02 | bend 표 따르면 안전 |
| Method 3 점선 위 라벨 (`fill=white`) | < 0.02 | inner sep=2pt 권장 |

**라벨 텍스트 수평 원칙** (한국 평가지 표준): `sloped` 사용 금지 — 변 회전 따라 텍스트 회전하면 평가지 양식과 어긋남. 변 법선 offset 필요하면 `fill=white inner sep=3pt` 변 끊기 또는 Method 2 외측 호 사용.

### ★ 외측 방향 결정 (deterministic, 6단계)

변 (P,Q)와 도형 무게중심 G가 주어졌을 때:

```text
1. 중점 M = midpoint(P,Q)
2. 변 단위 벡터 u = (Q-P)/|Q-P|
3. 좌측 법선 n_L = rotate(u, +90°)         (u의 왼손 쪽)
4. dot = (M - G) · n_L
5. dot > 0 → 외측 = 좌측 법선 방향
   dot < 0 → 외측 = 우측 법선 방향
   dot ≈ 0 → 변이 G를 통과 (드뭄). 두 후보 중 도형 외곽선과 더 멀리 떨어진 쪽 선택.
6. TikZ 매핑:
   외측 = u 의 좌측  → \draw (P) to[bend left=N] ... (Q);
   외측 = u 의 우측  → \draw (P) to[bend right=N] ... (Q);
```

**암기 단축 표** (사각형 ABCD: A 좌상, B 좌하, C 우하, D 우상, 반시계):

| 변 | 표준 draw 순서 | 외측 | 결과 |
|----|---------------|------|------|
| AD (위 변) | A → D (좌→우, 동쪽) | 위 (북) | `bend left=N` |
| BC (아래 변) | B → C (좌→우, 동쪽) | 아래 (남) | `bend right=N` |
| AB (왼쪽 변) | A → B (위→아래, 남쪽) | 왼쪽 (서) | `bend right=N` |
| DC (오른쪽 변) | D → C (위→아래, 남쪽) | 오른쪽 (동) | `bend left=N` |
| 사선 변 (예: 사다리꼴 좌변 AB) | A → B (남서 방향) | 좌(외측) | `bend right=N` |

> **유도 원리**: `bend right`는 진행 방향의 **오른손 쪽**으로 호가 부풀어 오른다.
> 진행 방향이 남쪽(↓)이면 오른손 쪽 = **서쪽(왼쪽)** 이므로 외측이 왼쪽일 때 `bend right` 사용.
> 의심스러우면 § A 의 알고리즘 6단계로 확인하거나 **순서 뒤집기 + bend 부호 반전**이 동치임을 활용한다:
> `(P) to[bend right=N] (Q)` ≡ `(Q) to[bend left=N] (P)`.

### 방법 1: `\tkzLabelSegment` (인라인 라벨) — 단순 표기
```latex
\tkzLabelSegment[above](A,B){$4$}
\tkzLabelSegment[below,pos=.3](A,B){$a$}
\tkzLabelSegment[fill=white,inner sep=2pt](A,B){$4$}  % 선 위 겹칠 때
```

### 방법 2: 점선 호 치수선 (dashed arc) — ★ textbook(에듀넷 교과서) 변/현 길이 디폴트

> **프리셋 스코프**: 이 점선 호 치수선은 **textbook(+modern) 전용** 외곽 변/현 길이 표기다. **exam·workbook은 인라인(방법 1)** — 위 "## 길이 표시" 정책 분기와 동일. textbook은 `\dimarc` 매크로(프리셋 preamble)로 호출하고 bow는 얕게(`bend 12–18`).

꼭짓점 사이를 직접 **점선 곡선 호**로 연결하는 간결한 치수선. 라벨은 호의 **정중앙에 배치**되어 `fill=white`로 호를 자연스럽게 끊습니다.

```
  A ─────────── B
   ╲             ╱
    ╲  ┌─────┐  ╱
     ╰─┤ 4cm ├─╯   ← 라벨이 호 위에 (fill=white로 호를 끊음)
        └─────┘
```

**기본 구문:**
```latex
\draw[dashed] (A) to[bend right=30]
  node[midway, fill=white, inner sep=2pt, font=\small] {$4\,\mathrm{cm}$} (B);
```

> **핵심**: `below`/`right` 등 방향 지정 **없이** `midway`만 사용 → 라벨이 호 경로 정중앙에 위치.
> `fill=white`가 호 선을 끊어 라벨 가독성을 확보합니다.

**`bend right` 방향 판단법:**
`bend right`는 **진행 방향의 오른손 쪽**으로 휩니다:

| 출발→도착 | 진행 방향 | bend right 결과 | bend left 결과 |
|-----------|----------|----------------|----------------|
| 좌→우 (동쪽) | → | 아래쪽 ↓ | 위쪽 ↑ |
| 우→좌 (서쪽) | ← | 위쪽 ↑ | 아래쪽 ↓ |
| 위→아래 (남쪽) | ↓ | 왼쪽 ← | 오른쪽 → |
| 아래→위 (북쪽) | ↑ | 오른쪽 → | 왼쪽 ← |

> **팁**: 원하는 방향이 안 나오면 출발/도착 순서를 뒤집으면 됩니다.
> `\draw[dashed] (A) to[bend left=30] ... (B);` = `\draw[dashed] (B) to[bend right=30] ... (A);`

**수평선 아래 (BC = 8cm):**
```latex
% B(좌) → C(우), bend right = 아래쪽
\draw[dashed] (B) to[bend right=30]
  node[midway, fill=white, inner sep=2pt, font=\small] {$8\,\mathrm{cm}$} (C);
```

**수직선 오른쪽 (AC = 6cm):**
```latex
% C(아래) → A(위), bend right = 오른쪽
\draw[dashed] (C) to[bend right=30]
  node[midway, fill=white, inner sep=2pt, font=\small] {$6\,\mathrm{cm}$} (A);
```

**대각선 (OC = 5cm):**
```latex
% O → C 방향의 오른쪽으로 호
\draw[dashed] (O) to[bend right=20]
  node[midway, fill=white, inner sep=2pt, font=\small] {$5\,\mathrm{cm}$} (C);
```

**조절 파라미터:**
| 파라미터 | 역할 | 기본값 | 프리셋별 |
|----------|------|--------|---------|
| `bend right=22` | 호의 곡률 (클수록 휨) | 22 (변 5cm 기준) | L≤1.5→45, L≤2.5→35, L≤4→30, L≤6→22, L≤9→18, L≤13→14, L>13→10 |
| `font=\small` | 라벨 폰트 크기 | `\small` (exam) | textbook=`\small`, workbook=`\footnotesize`, academy=`\scriptsize`, modern=`\normalsize` |
| `fill=white` | 호를 끊는 배경 (**필수**) | 항상 사용 | — |
| `inner sep=2pt` | 배경 패딩 | 2pt | — |

### ★ bend 자동 결정 (sagitta ≥ 라벨높이 보장)

라벨 글자 높이를 약 0.20cm로 잡으면, **sagitta s ≥ 0.40cm** 가 안전. 공식: `s = L · tan(b/4) / 2`.

| 변 길이 L (cm) | 권장 bend (°) | 결과 sagitta (cm) | 라벨 안전 여유 |
|---------------|--------------|------------------|----------------|
| L ≤ 1.5       | 45           | 0.31             | 좁음 — `\scriptsize` |
| 1.5 < L ≤ 2.5 | 35           | 0.39             | 표준 (`\footnotesize`) |
| 2.5 < L ≤ 4   | 30           | 0.54             | 안전 |
| 4 < L ≤ 6     | 22           | 0.59             | ★ 표준 (`\small`) |
| 6 < L ≤ 9     | 18           | 0.71             | 안전 |
| 9 < L ≤ 13    | 14           | 0.81             | 안전 |
| L > 13        | 10           | 0.86             | 안전 (긴 변, 호 부드러움) |

> **불변식**: 모든 행에서 sagitta ≥ 0.30 cm — 라벨이 변과 닿지 않는다.
> 단위 포함 긴 라벨(`$10\,\mathrm{cm}$`)은 한 단계 bend 증가 권장.

### ★ 인접 외곽 변 — 공통 꼭짓점 분리 규칙

두 외곽 변 (P,V)와 (V,Q) 가 꼭짓점 V를 공유하고 같은 외측 영역에 라벨이 들어갈 때:

1. **두 호가 V에서 만나면 시각적으로 끊어 보이도록**:
   - 첫째 변의 호: `(P) to[bend ... = N1] ... (V)`  → V에서 끝
   - 둘째 변의 호: `(V) to[bend ... = N2] ... (Q)`  → V에서 시작
   - 두 호가 V 부근에서 분리되도록 N1, N2를 ±2° 다르게 두면 안전.

2. **두 호가 평행처럼 보이는 위험**(예: 변 길이가 비슷하고 외측이 같은 영역):
   - 한쪽을 Method 2, 다른 쪽을 Pattern D7(stack 1-layer)로 변형 → offset 0.5cm 확보.
   - 또는 라벨 위치를 `pos=0.4` / `pos=0.6` 으로 약간 옮겨 시각 분리.

3. **레퍼런스 이미지 사례** (사다리꼴 좌하 B에서 AB="6", EB="3"):
   ```latex
   % 변 AB (전체 좌측 변)와 변 EB (AB의 하단 절반)이 둘 다 좌측(서) 외측 라벨
   % A→B 진행은 남쪽 방향 → 외측(서) = 진행 오른손 쪽 → bend right
   \draw[dashed, thin] (A) to[bend right=22]
     node[midway, fill=white, inner sep=2pt, font=\small] {$6$} (B);   % AB 호
   \draw[dashed, thin] (E) to[bend right=30]
     node[midway, fill=white, inner sep=2pt, font=\footnotesize] {$3$} (B);  % EB 호 (더 짧은 변, bend 큼)
   % 두 호가 B에서 만나지만 bend 차이(22 vs 30)와 길이 차이로 자연 분리됨
   ```

### ★ 라벨 사전 충돌 체크 (코드 생성 전)

각 외곽 변 길이 라벨에 대해 LaTeX 코드를 emit 하기 **전에** 다음을 점검:

| 체크 | 위반 시 처치 |
|------|-------------|
| 1. 호의 외측 영역에 다른 도형 변/점이 있는가? | `bend` 한 단계 증가 (호를 더 부풀려 우회) |
| 2. 변의 양 끝점에 점 라벨(`A`, `B`)이 같은 외측 방향으로 배치되어 있는가? | 호 시작점을 0.05 단위 안쪽으로 이동: `to[bend ...] (P) ... (Q)` 대신 `($(P)!0.05!(Q)$)`에서 시작 |
| 3. 라벨 길이(C 글자)가 sagitta 폭의 80% 초과인가? | bend 한 단계 증가 또는 `font` 한 단계 축소 |
| 4. 같은 외측에 ≥ 2 호가 있고 호끼리 교차할 가능성이 있는가? | 한쪽을 Pattern D7(stack)로 변형 — offset 0.5cm 추가 |
| 5. 호의 외측 영역이 standalone border 밖인가? | `\documentclass[border=20pt]{standalone}` 으로 border 확장 |

> 위반이 없으면 § A 의 단일 권장 템플릿을 그대로 emit.

### ★ § F. 마크-점 충돌 회피 (Mark-Point Avoidance)

**문제**: 평행 마크(`>`, `>>`)와 등변 마크(`|`, `||`, `|||`)는 `\tkzMarkSegment` 가 기본 `pos=0.5`(변 중점)에 그린다.
변 위에 다른 점이 있거나(예: 사다리꼴 EF의 중점 G), dim 라벨이 같은 변에 있거나, 두 종류의 마크가
한 변에 동시에 필요할 때 **마크가 점/라벨/다른 마크와 시각적으로 겹친다**.

**핵심 통찰**: 마크의 정확한 `pos`는 **의미를 바꾸지 않는다**(같은 마크의 다른 변과 같은 종류임이 의미).
따라서 `pos`를 자유롭게 분산해 충돌을 0으로 만들 수 있다. dim 라벨도 § A 외측 호로 격하하면 변 위는 마크만 점유.

#### F.1 충돌 케이스 7종

| # | 충돌 | 자주 발생하는 상황 |
|---|------|------------------|
| C1 | 마크 vs **변 위 다른 점** | 사다리꼴 EF에 중점 G가 있고 평행 마크가 pos=0.5 |
| C2 | 마크 vs **변에 부착된 dim 라벨** | 둘 다 pos=0.5 → 라벨 위에 마크가 얹힘 |
| C3 | **같은 변에 두 종류 마크** (등변+평행) | 두 마크 모두 pos=0.5 |
| C4 | dim 라벨 vs **정점 라벨** | 매우 짧은 변(L<2cm)에서 라벨이 정점 이름과 충돌 |
| C5 | 한 변에 **두 dim 라벨** (드뭄) | 분할된 두 구간의 길이를 함께 표기 |
| C6 | 마크 multiplicity 분산 | `\|\|\|` 의 3개 stroke 간격이 너무 좁아 점/라벨과 겹침 |
| C7 | **인접 변 마크끼리** 꼭짓점 부근 충돌 | 짧은 변 두 개가 만나는 곳에서 두 마크가 가까움 |

#### F.2 결정적 회피 알고리즘 (모든 마크 부착 변에 적용)

```text
입력:
  변 (P,Q), 길이 L (cm)
  변 위 점 R = {(name, pos_i)}            # \tkzInterLC, \tkzDefMidPoint 등으로 만들어진 점들
  필요 마크 K = {등변? 평행? 수직?}        # 종류 수, 0~3
  has_dim_inline = (dim 라벨이 외측 호 아니라 변 위에 있는가)

Step 1. 가용 영역 계산
  obstacles = [pos_i for R] + ([0.5] if has_dim_inline else [])
  dead_zones = ⋃ [p − δ, p + δ]   where δ = max(0.10, 0.30/L)
  available = (0.10, 0.90) − dead_zones    # 양 끝 [0,0.10] 및 [0.90,1] 정점 라벨 회피

Step 2. 가용 영역의 sub-segment 리스트화
  segments = available 의 연결 구간들 (예: [(0.10, 0.35), (0.55, 0.78)])
  segments 를 길이 내림차순 정렬

Step 3. 마크 K개를 segments 에 할당
  if |K| == 0:    종료
  if |K| == 1:    가장 긴 segment 의 중점에 배치
  if |K| == 2:    가장 긴 segment 둘에 각각 중점 (둘 다 같은 segment면 그 segment 의 1/3, 2/3 지점)
  if |K| >= 3:    가장 긴 segment 를 K등분, 분할점에 배치

Step 4. 마크 size 결정 (변 길이 비례)
  L >= 4cm  → size=4pt (기본)
  2 <= L < 4 → size=3pt
  L < 2     → size=2pt + 가능하면 마크 종류 1개로 축소

Step 5. 만약 segments 가 모두 너무 짧다 (<0.10):
  - has_dim_inline이면 → § A 외측 호로 격하해 변 위 자유 확보, Step 1 재실행
  - 그래도 부족하면 → 마크 종류 1개만 유지 (등변 우선, 평행은 같은 그룹의 다른 변에서 표기)
```

#### F.3 자주 쓰는 lookup 표 (사람이 직접 보고 쓰는 결정표)

| 케이스 | 변 위 obstacle | 등변 마크 pos | 평행 마크 pos | dim 처리 | 비고 |
|--------|--------------|--------------|--------------|---------|------|
| 깨끗한 외곽 변 | 없음 | 0.5 | 0.5 (다른 변과 동일) | 외측 호 | 기본 |
| **EF (중점 G)** | G@0.5 | **0.3** (G 왼쪽) | **0.7** (G 오른쪽) | 외측 호 | C1 회피 — 본 파트의 핵심 |
| 분할점 R@0.4 | R@0.4 | 0.7 | — | 외측 호 | R 회피 |
| 두 점 1/3, 2/3 | R₁@0.33, R₂@0.67 | 0.5 | — | 외측 호 | 사이 빈공간 |
| 짧은 변 L<2cm | 없음 | 0.5, size=2pt | — | 외측 호 + small font | 마크 축소 |
| 평행 그룹 변 | 없음 | — | 0.5 (그룹 내 동일) | 외측 호 | 그룹 일관성 |
| 등변 + 평행 동시 | 없음 | 0.35 | 0.65 | 외측 호 | C3 분산 |
| 인접 짧은 변 | (양 꼭짓점) | 0.55 (먼 쪽) | 0.55 (먼 쪽) | 외측 호 | C7 — 양쪽 변이 꼭짓점에서 멀어지는 방향 |

> **불변식**: 어떤 케이스도 dim 라벨을 외측 호(§A)로 격하하면 변 위는 마크만 자유롭게 분산 가능.
> 외측 호 사용을 거부할 의미적 이유가 없다면 항상 § A 적용.

#### F.4 워크드 예시 — 사다리꼴 EF의 중점 G (C1 + C3)

문제 상황: 사다리꼴 ABCD, EF는 중점선(AB 중점 E, DC 중점 F), G는 EF의 중점.
EF에 평행 마크(AD/BC와 같은 그룹)와 등변 마크(EG=GF)를 모두 표시하고 dim 라벨 "x"도 필요.

> **중요**: tkz-euclide의 `\tkzMarkSegment[mark=…]` 는 **등변 마크(`|`, `||`, `|||`, `s|`)** 전용이다.
> **평행 마크(화살표 `>`, `>>`)** 는 TikZ `decorations.markings` 라이브러리로 그린다.

```latex
% Preamble
\usetikzlibrary{decorations.markings}
\tikzset{parmark/.style 2 args={postaction=decorate,
  decoration={markings, mark=at position #1 with {\arrow{#2}}}}}
% 사용: \draw[parmark={pos}{>}] (P) -- (Q);   % 또는 {>>}, {>>>} 로 그룹 구분

% === 도형 정의 ===
\tkzDefPoints{0/0/B, 10/0/C, 3/4/A, 8/4/D}
\tkzDefMidPoint(A,B) \tkzGetPoint{E}
\tkzDefMidPoint(D,C) \tkzGetPoint{F}
\tkzDefMidPoint(E,F) \tkzGetPoint{G}    % G는 EF의 pos=0.5 = obstacle
\tkzDrawPolygon[thick](A,B,C,D)
\tkzDrawSegment(E,F)

% === § F.3 lookup: EF (중점 G) ===
% 등변 마크 pos=0.3 (G 왼쪽), 평행 화살표 pos=0.7 (G 오른쪽)
\tkzMarkSegment[pos=0.3, mark=|, size=3pt](E,F)      % EG = GF (등변)
\draw[thick, parmark={0.7}{>}] (E) -- (F);            % EF ∥ AD (평행 화살표)

% AD, BC 에 같은 평행 화살표 (그룹 일관성, 점 없음 → pos=0.5 기본)
\draw[thick, parmark={0.5}{>}] (A) -- (D);
\draw[thick, parmark={0.5}{>}] (B) -- (C);

% dim 라벨 "x" 는 § A 외측 호로 (변 위는 마크가 차지하므로 외측 호로 격하)
\draw[dashed, thin] (E) to[bend left=18]
  node[midway, fill=white, inner sep=2pt, font=\small] {$x$} (F);

% === ANTI-PATTERN (피할 것) ===
% \tkzMarkSegment[mark=|](E,F)              % pos=0.5 → G 와 정확히 겹침
% \tkzMarkSegment[mark=>](E,F)              % mark=> 는 정의되지 않음 → 빈 마크
% \tkzLabelSegment[above](E,F){$x$}         % 변 위 라벨 → 두 마크와 모두 겹침
% \draw[parmark={0.5}{>}] (E) -- (F);       % G 와 정확히 겹침
```

> **검증 시 주의**: `verify-overlap.py` 의 마크 검출은 `\tkzMarkSegment` (등변)만 추적한다.
> 평행 화살표(`parmark` 또는 직접 `decoration`)는 정적 분석에 안 잡히므로 사람이 § F.3 lookup 으로 직접 분산 배치해야 한다.

#### F.5 짧은 변의 인접 마크 (C7) 처리

```latex
% 짧은 변 두 개가 꼭짓점 V에서 만남 (예: 정삼각형 한 변 L=1.5cm)
% 두 마크가 V 부근에서 시각적으로 겹치는 위험
% 처치: 두 마크 모두 V에서 먼 쪽 (pos=0.55, V가 P쪽이면)
\tkzMarkSegment[pos=0.55, mark=||, size=2pt](V,P)   % V로부터 멀리
\tkzMarkSegment[pos=0.55, mark=||, size=2pt](V,Q)   % V로부터 멀리
% size=2pt 로 축소하여 짧은 변에 맞게
```

#### F.6 마크 wrapper 매크로 (선택 — 명시적 회피)

매번 lookup 표를 보지 않고 wrapper로 회피 의도를 코드에 남기고 싶다면 preamble 에 다음 헬퍼:

```latex
% 변에 등변 마크 + obstacle 회피 (수동 pos)
\newcommand{\eqmark}[3][0.5]{\tkzMarkSegment[pos=#1, mark=#2, size=3pt](#3)}
% 사용:
\eqmark[0.3]{||}{E,F}        % C1 회피 (G@0.5 obstacle 가정)
\eqmark[0.7]{>>}{E,F}

% 짧은 변 전용 (size 자동 축소)
\newcommand{\eqmarkS}[3][0.55]{\tkzMarkSegment[pos=#1, mark=#2, size=2pt](#3)}
```

#### F.7 자동 검증 (verify-overlap.py)

verify-overlap.py 는 `--check-marks` 옵션으로 마크-점 충돌도 검사한다 (V2 스펙 — F.8 참조).
규칙:
- `.tex` 에서 `\tkzMarkSegment[...](P,Q)` 와 `\tkzDefPoint(x,y){name}`, `\tkzDefMidPoint(P,Q) \tkzGetPoint{name}`,
  `\tkzInterLC(...)\tkzGetPoint{name}` 호출을 정규식으로 추출.
- 마크 좌표 = (1−pos)·P + pos·Q (직선 보간).
- 변 위에 정의된 모든 점에 대해 거리 < 0.20·L 이면 `mark_collision` 으로 보고.
- exit code 1 (overlap 과 동일 처치 트리거).

#### F.8 처치 매핑 (mark_collision → 자동 수정)

`figure-overlap.json` 의 `mark_collisions` 항목마다 우선순위로 처치:

| # | 트리거 | 처치 | 근거 |
|---|-------|------|------|
| 1 | 마크 vs 점 (`mark_collision`) | F.3 lookup으로 pos 변경 (점 회피 zone 밖으로) | F.2 / F.3 |
| 2 | 처치 1 후에도 충돌 (가용 영역 부족) | mark size 축소 (4pt → 3pt → 2pt) | F.4 Step 4 |
| 3 | 처치 2 후에도 부족 | dim 라벨을 § A 외측 호로 격하 | F.2 Step 5 |
| 4 | 그래도 부족 (매우 짧은 변) | 마크 종류 1개만 유지 (등변 우선, 평행은 다른 변에서) | F.5 |



점선 보조선 + 실선 호 + 라벨로 구성된 외부 치수선. 도형 변과 떨어진 위치에 치수를 표시할 때 사용합니다.

```
  A ─────────── B          A ─────────── B
  ╎             ╎          (선분 아래 치수선)
  ╎             ╎
  └─────4──────┘   ← 실선 호 + 라벨
```

**선분 아래 치수선:**
```latex
% 점선 보조선 + 곡선 호 (선분 AB 아래, 거리 0.5cm)
\coordinate (dA) at ($(A)!0.5cm!-90:(B)$);
\coordinate (dB) at ($(B)!0.5cm!90:(A)$);
\draw[dashed, thin] (A) -- (dA);
\draw[dashed, thin] (B) -- (dB);
\draw[thin] (dA) to[bend right=20] node[midway, below, font=\small] {$4$} (dB);
```

**선분 위 치수선:**
```latex
% 점선 보조선 + 곡선 호 (선분 AB 위, 거리 0.5cm)
\coordinate (dA) at ($(A)!0.5cm!90:(B)$);
\coordinate (dB) at ($(B)!0.5cm!-90:(A)$);
\draw[dashed, thin] (A) -- (dA);
\draw[dashed, thin] (B) -- (dB);
\draw[thin] (dA) to[bend left=20] node[midway, above, font=\small] {$4$} (dB);
```

**원리:** `($(A)!0.5cm!-90:(B)$)` = A에서 AB 방향을 -90° 회전한 방향으로 0.5cm 이동 (아래쪽)

**회전 각도 주의 (선분 방향별):**
| 선분 방향 | 외부 방향 (오른쪽/아래) | 첫째 점 회전 | 둘째 점 회전 |
|-----------|----------------------|-------------|-------------|
| 수평 (좌→우) | 아래 | `-90` | `90` |
| 수직 (위→아래) | 오른쪽 | `90` | `-90` |

> **주의**: 수직선에서 `-90`은 "왼쪽(내부)"이 됩니다. 수평선의 관례와 반대이므로 각도를 뒤집어야 합니다.

**조절 파라미터:**
| 파라미터 | 역할 | 기본값 |
|----------|------|--------|
| `0.5cm` | 보조선 길이 (도형과의 거리) | 0.5cm |
| `bend right=20` | 호의 곡률 (클수록 휨) | 20 |
| `font=\small` | 라벨 폰트 크기 | `\small` |

> **주의**: 이 패턴은 `calc` 라이브러리를 사용합니다. `tkz-euclide`가 자동 로드하므로 추가 설정 불필요.

**치수선 방법 선택 기준:**
| 상황 | 방법 | 이유 |
|------|------|------|
| 한국 교과서/시험 스타일 (**기본**) | **방법 2** (점선 호) | 간결, 1줄, 교과서와 동일한 시각적 스타일 |
| 기술도면/설계도 스타일 | 방법 3 (오프셋 보조선) | 도형 변과 명확히 분리된 치수 표기 |
| 도형 내부 선분 (대각선, 중선 등) | 방법 1 (`\tkzLabelSegment`) | 외부 치수선이 다른 요소와 겹침 |
| 각도 | `\tkzLabelAngle` | 호 위에 직접 표기 |

---

## 치수선 결정 트리

입력 튜플 `(P, S, θ, L, C)` → 정확히 하나의 Method/Pattern 출력.
최초 매치에서 확정, 오버라이드 없음.

```
입력: P=위치, S=레이어수, θ=방향, L=변길이(cm), C=라벨문자수

1. P == internal (내부 선분)?
   └── Method 1 (\tkzLabelSegment + fill=white)

2. S ≥ 2 (다중 레이어)?
   ├── S=2 → Pattern D7 (2-layer stack)
   └── S≥3 → Pattern D8 (3+layer stack)

3. C/L ≥ 2 (짧은 변 + 긴 라벨)?
   └── Pattern D9 (Leader 외부 배치)

4. 호/반경 치수?
   └── Pattern D10 (Arc/radial)

5. 외곽 변 (P=edge, S=1)?
   ├── textbook(에듀넷) → Method 2 점선 치수 호 (\dimarc, bend 12–18 얕게, 외측은 § B 알고리즘)
   └── exam·workbook → Method 1 인라인 (\tkzLabelSegment)
```

**bend 값** (변 길이 기준): L≤1.5→45, L≤2.5→35, L≤4→30, L≤6→22, L≤9→18, L≤13→14, L>13→10
**단위**: `$4\,\mathrm{cm}$` (thin space `\,` + upright 단위). 문제에 단위 명시 시 생략 가능(`$4$`).
**고급 패턴 코드 템플릿 (D4-D10):**

| Pattern | 핵심 코드 | 용도 |
|---------|----------|------|
| D4 | `\draw[dashed] (A) to[bend right=30] node[midway,fill=white,inner sep=2pt,font=\footnotesize] {$4$} (B);` | Method 2 짧은 변 변형 |
| D5 | `\coordinate (dA) at ($(A)!0.5cm!90:(B)$); ...` + `\draw[thin] (dA) to[bend left=20] node[midway,left,font=\small] {$h$} (dB);` | 수직 외측 오프셋 |
| D6 | 법선 방향 계산 후 D5와 동일 구조 | 경사 변 외측 오프셋 |
| D7 | D5/D6를 offset 0.5cm, 0.9cm 2단으로 배치 | 2-layer 스택 |
| D8 | D7 + 1.3cm 3단 | 3+layer 스택 |
| D9 | `\draw[-stealth,thin] (A) -- ++(0,-0.5) -- ++(1,0) node[right,font=\small] {$4\,\mathrm{cm}$};` | Leader (짧은 변) |
| D10 | 호 확대: `\tkzDefPointBy[homothety=center O ratio 1.3](A)\tkzGetPoint{A'}` → `\tkzDrawArc[dashed](O,A')(B')` 후 라벨 | Arc/radial |

상세 예제와 컴파일된 PDF는 `research/04_dashed-dimension/catalog/fig-D01~D30.tex` 참조.

---

## 점선 표시 (Dashed Lines)

> **★ 한국 평가지 검증 (Agent 9)**: 실제 평가지에서는 `dashed` 패턴이 **단일** 사용된다.
> `dotted` / `dash dot` / `densely dashed` / `loosely dashed` 사례 0건.
> exam/textbook/workbook 프리셋은 `dashed` 단일 사용을 권장한다.

### 선 스타일 표

| 스타일 | 용도 | 권장 프리셋 |
|--------|------|------|
| `solid` (기본) | 주요 도형 변 + 보조선 (수선·중선·각이등분선 등 — 한국 평가지 ~95% 솔리드 보조선) | exam/textbook/workbook/modern |
| `dashed` | 가려진 변·연장선·치수선 외측 호 (modern) — 한 가지 의미만 사용 | exam/textbook/workbook/modern |
| `densely dashed` | 숨은 변 (3D 또는 뒤쪽) — **평면도형에선 사실상 미사용** | modern only |
| `loosely dashed` | 가벼운 참조선 — **한국 평가지 미사용** | modern only |
| `dotted` | 연장선·보조원 — **한국 평가지 미사용** | modern only |
| `dash dot` | 대칭축 — **한국 평가지 미사용** | modern only |

> **삼각형 단원 검증** (Agent 1): 수선·중선·각이등분선 등 보조선은 거의 100% 실선. dashed 는 외접원 반지름 등 한정 용도에만.

### 용도별 권장 스타일
```latex
% 보조선/구성선
\tkzDrawSegment[dashed](C,H)
\tkzDrawSegment[densely dashed, gray, thin](A,B)

% 연장선
\tkzDrawLine[add=.3 and .3, loosely dashed, gray](A,B)

% 보조 원
\tkzDrawCircle[dotted, thin](O,A)

% 대칭축
\tkzDrawLine[dash dot, blue!50, thin](A,B)

% 커스텀 패턴
\tkzDrawSegment[dash pattern={on 3pt off 2pt on 1pt off 2pt}](A,B)
```

### 의미 기반 점선 패턴 규칙

| 의미 역할 | 패턴 | 굵기 | 사용 |
|----------|------|------|------|
| 확장 보조선 (extension) | `dashed` | `thin` (0.4pt) | 치수선까지 뻗는 선 |
| 치수선 본체 | `dashed` | `thin` | 외곽 치수선 호/선 |
| 숨은 변 (3D 또는 뒤쪽) | `densely dashed` | `thin` | 보이지 않는 모서리 |
| 동치 마킹 (`\|`, `\|\|`) | solid | 0.4pt | 등변 표시 -- dashed 아님 |
| 대칭축 | `dash dot` | `thin` | 대칭 변환 축 |
| 호 길이 치수 | `dashed` | `thin` | 원호/부채꼴 외측 |

동치 마킹 스트로크 길이: mark 기본 `size=0.17` (tikz-euclide 기본 + 수능 A1 관례 5pt).

---

## 겹침 방지 전략

### 전략 1: 그리기 순서 (Layer Order) — 가장 중요

TikZ는 나중에 그린 것이 위에 표시됩니다. **반드시 이 순서를 따를 것:**

```
1. 채우기 (\tkzFillPolygon, \tkzFillAngle)    ← 맨 아래
2. 보조선 (dashed, dotted, gray)
3. 주요 도형 (\tkzDrawPolygon, \tkzDrawCircle)
4. 마킹 (\tkzMarkSegments, \tkzMarkAngle)
5. 점 (\tkzDrawPoints[size=0])
6. 라벨 (\tkzLabelPoint, \tkzLabelSegment)    ← 맨 위
```

### 전략 2: `fill=white` 배경 패딩

라벨이 선분 위를 지날 때 흰색 배경으로 가독성 확보:
```latex
\tkzLabelSegment[fill=white, inner sep=2pt](A,B){$4$}
\tkzLabelAngle[fill=white, inner sep=1pt, pos=1.2](A,O,B){$60^\circ$}
```

### 전략 3: `\tkzAutoLabelPoints` 자동 배치

도형 중심에서 바깥쪽으로 자동 배치:
```latex
\tkzDefTriangleCenter[centroid](A,B,C) \tkzGetPoint{G}
\tkzAutoLabelPoints[center=G, dist=.3](A,B,C)
```
> **한계**: 선분/다른 라벨과의 충돌은 감지 못함. 복잡한 도형은 수동 배치 필요.

### 전략 4: 수동 미세 조정

```latex
% 방향 + 거리
\tkzLabelPoint[above=4pt](A){$\mathrm{A}$}
\tkzLabelPoint[below left=3pt](B){$\mathrm{B}$}

% 선분 위 위치 조절 (pos: 0=시작, 1=끝)
\tkzLabelSegment[above, pos=.3](A,B){$a$}   % 시작점 쪽
\tkzLabelSegment[above, pos=.7](A,B){$b$}   % 끝점 쪽
```

### 전략 5: 치수선 방향 스택 (D7)

같은 변에 여러 치수선이 필요할 때 평행하게 쌓습니다:

```latex
% 1차 치수선 (가장 가까운 변, offset 0.5cm)
\coordinate (d1A) at ($(A)!0.5cm!-90:(B)$);
\coordinate (d1B) at ($(B)!0.5cm!90:(A)$);
% 2차 치수선 (offset 0.9cm = 0.5 + 0.4 간격)
\coordinate (d2A) at ($(A)!0.9cm!-90:(B)$);
\coordinate (d2B) at ($(B)!0.9cm!90:(A)$);
```

**스택 간격**: base=0.5cm, step=0.4cm. 4레이어(1.7cm) 초과 시 라벨 재배치 권장.

### 전략 6: 치수선 방향 우선순위

| 변 방향 | 치수선 배치 | bend 방향 |
|---------|-----------|----------|
| 수평 하변 | 아래쪽 | (좌→우) `bend right` |
| 수평 상변 | 위쪽 | (좌→우) `bend left` |
| 수직 좌변 | 왼쪽 | (아래→위) `bend right` |
| 수직 우변 | 오른쪽 | (위→아래) `bend right` |
| 경사 변 | 외측 법선 방향 | 도형 바깥쪽 |

---

## 예외사항

다음은 **문제가 아닙니다**:

1. **3D 도형** — tkz-euclide는 2D 유클리드 기하 전용입니다. 3D가 필요하면 tikz-3dplot를 사용합니다. → 아래 `고급 확장` 섹션의 G 핸드오프 참조.
2. **함수 그래프** — 함수 플롯은 pgfplots를 사용해야 합니다. 좌표평면·함수 그래프는 `gratik` 스킬을 우선 사용하고, 아래 `고급 확장` 섹션의 F 핸드오프를 보조 참조합니다.
3. **비유클리드 기하** — 쌍곡 기하, 구면 기하 등은 tkz-euclide의 범위 밖입니다.
4. **애니메이션** — 정적 도형만 생성합니다.
5. **정밀도 한계** — pgfmath의 부동소수점 정밀도 제한이 있을 수 있으며, `\fpeval`로 보완할 수 있습니다.

## 고급 확장 (예외사항 보강)

### F · 함수 그래프 (pgfplots 핸드오프)

함수식·좌표평면 도식은 tkz-euclide 범위 밖이므로 pgfplots를 사용합니다.
사용자가 `y=f(x)` 그래프, 좌표축, 격자, 점, 영역 음영을 요청하면 `gratik` 스킬을 우선 사용합니다. 빠른 핸드오프가 필요하면 함수식·정의역·축 스타일을 확인 후:

```latex
\documentclass{standalone}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\begin{document}
\begin{tikzpicture}
  \begin{axis}[
    axis lines=middle, xlabel=$x$, ylabel=$y$,
    axis line style={-stealth, line width=0.6pt},
    xlabel style={below right}, ylabel style={above left},
    xmin=-3, xmax=3, ymin=-1, ymax=4,
    xtick={-2,-1,1,2}, ytick={1,2,3},
  ]
    \node[below left, font=\small] at (axis cs:0,0) {$\mathrm{O}$};
    \addplot[mark=none, domain=-2:2, samples=201, smooth, thick] {x^2};
  \end{axis}
\end{tikzpicture}
\end{document}
```

상세: `.claude/skills/gratik/SKILL.md`, `research/06_graphs-coords/F1-F4`, `research/F-G-SCOPE-PROPOSAL.md`

### G · 3D 입체도형 (tikz-3dplot 핸드오프)

3D 입체는 tikz-3dplot를 사용합니다. 입체 종류·치수·숨은선 처리를 확인 후:

```latex
\documentclass{standalone}
\usepackage{tikz}
\usepackage{tikz-3dplot}
\tdplotsetmaincoords{70}{110}
\begin{document}
\begin{tikzpicture}[tdplot_main_coords, scale=1.5]
  \draw[thick] (0,0,0) -- (1,0,0) -- (1,1,0) -- (0,1,0) -- cycle;
  \draw[thick] (0,0,1) -- (1,0,1) -- (1,1,1) -- (0,1,1) -- cycle;
  \draw[thick] (0,0,0) -- (0,0,1); \draw[thick] (1,0,0) -- (1,0,1);
  \draw[thick] (1,1,0) -- (1,1,1); \draw[dashed,thin] (0,1,0) -- (0,1,1);
\end{tikzpicture}
\end{document}
```

상세: `research/07_solid-3d/G1-G3`, `research/F-G-SCOPE-PROPOSAL.md`

#### G.1 · 3D 라벨 겹침 방지 체크리스트 (시점 종속 규칙)

> **본질**: 3D→2D 투영 시 같은 화면 영역으로 몰리는 요소를 **투영 후 빈 사분면**으로 분산.
> 텍스트 길이를 줄이는 것은 표면적 처치이며, 같은 클러스터에 머무르면 다시 붙는다.

**체크리스트** (모든 3D figure에 적용):

- [ ] **G.1.1** 라벨 배치는 3D 좌표 직관이 아니라 **최종 2D 투영 화면 기준**으로 판단한다.
- [ ] **G.1.2** 축 끝에 점 라벨이 있으면 축을 점보다 **최소 한 라벨 폭 이상 더 연장**한 뒤 축 라벨을 단다.
- [ ] **G.1.3** `above right` 등 anchor 키워드는 의미적 방향이 아니라 **화면상 빈 사분면 선택 도구**로만 사용.
- [ ] **G.1.4** 점 라벨 충돌 시 첫 처치는 텍스트 축약이 아니라 **기준점 분리**(축 연장, 라벨 위치 이동).
- [ ] **G.1.5** 보조 표기(`S`, `C_1`, `C_2`)는 뒤쪽 점선/원호 위에 직접 올리지 말고 **명도 대비 나는 빈 영역**에.
- [ ] **G.1.6** 회색 점선·보조평면 주변 라벨은 단색 `gray` 보다 **진한 색 또는 흰 배경 패딩** 우선:
      `\node[fill=white, inner sep=1pt]`
- [ ] **G.1.7** 교점·중심처럼 시선이 모이는 점 주변에 **축 라벨, 원 이름, 점 이름을 동시에 모으지 않는다**.
- [ ] **G.1.8** `\tdplotsetmaincoords` 를 바꾸면 라벨 anchor 도 **재검토**. 3D 라벨 배치는 시점 종속.

**처치 우선순위** (라벨 충돌 발견 시 순서대로 시도):

| # | 처치 | 적용 시점 |
|---|------|----------|
| 1 | 축 연장으로 **기준점 분리** | 축 끝 라벨이 점 라벨과 인접할 때 (가장 일반화) |
| 2 | anchor 재배치 (빈 사분면 탐색) | 동일 화면 클러스터 잔존 시 |
| 3 | `fill=white, inner sep=1pt` (흰 배경 패딩) | 고밀도 교점 영역 |
| 4 | 색 강화 (`gray` → `black!60`) | 저대비 요소 주변 |
| 5 | 텍스트 축약 (`A(a,0,0)` → `A`) | 마지막 수단 |

**구 표현 관용구** (tikz-3dplot에서 `circle (\R)` 사용 금지 — 좌표계 변환 비대칭):

```latex
% 세 개의 큰 원으로 구를 표현 (equator + 2 meridians)
\draw[gray!50, thin] plot[smooth cycle, samples=72, domain=0:360, variable=\t]
  ({\R*cos(\t)}, {\R*sin(\t)}, 0);                          % 적도
\draw[gray!35, thin, dashed] plot[smooth cycle, samples=72, domain=0:360, variable=\t]
  ({\R*cos(\t)}, 0, {\R*sin(\t)});                          % xz 자오선
\draw[gray!35, thin, dashed] plot[smooth cycle, samples=72, domain=0:360, variable=\t]
  (0, {\R*cos(\t)}, {\R*sin(\t)});                          % yz 자오선
```

**평면 위의 원 관용구** (3D 평면 절단 원):

```latex
% 평면 x = px 위의 원 (반지름 r)
\draw[red, thick] plot[smooth cycle, samples=80, domain=0:360, variable=\t]
  ({\px}, {\r*cos(\t)}, {\r*sin(\t)});

% 평면 y = py 위의 원
\draw[blue, thick] plot[smooth cycle, samples=80, domain=0:360, variable=\t]
  ({\r*cos(\t)}, {\py}, {\r*sin(\t)});
```

**검증 도구의 한계**: `verify-overlap.py` 는 2D dim 라벨 vs 도형선만 검출.
3D 케이스는 별도 도구 필요 (현재 미구현 — 작성 시 G.1 체크리스트로 수동 점검).

상세 사례: [[opsi:Wiki/Entities/gf2]], [[opsi:Wiki/Concepts/3D_라벨_겹침_방지]] (누적 메모리)

## 시각 검증 루프 (Visual Refinement) — 자동 겹침 검출 + 결정적 처치

> **핵심**: 코드를 생성하면 **반드시** 자동 겹침 검출 스크립트를 돌려서 dim(치수) 라벨이 도형과 겹치는지
> 결정적으로 판정한다. 시각 판독은 보조 수단이다. 최대 3회 반복한다.

### 자동 검증 스크립트

`.claude/skills/gf2/verify-overlap.py` — pdflatex 컴파일 + pdftotext bbox 추출 + PNG 픽셀 분석.
라벨을 **point**(정점 이름, 변에 가까움이 정상) / **dim**(치수, 도형과 떨어져야 함) / **other**(변수)로 자동 분류하고
타입별 다른 임계로 판정한다.

```bash
# 기본 사용 (컴파일 → 분석 → JSON 보고서)
python .claude/skills/gf2/verify-overlap.py path/to/figure.tex

# 옵션
python .claude/skills/gf2/verify-overlap.py figure.tex \
  --dpi 200 \                  # PNG 해상도
  --ring-px 6 \                # 라벨 외곽 ring 픽셀 두께
  --dark-threshold 80 \        # 0-255, 미만이면 검은 픽셀
  --dim-threshold 0.025 \      # dim 라벨 ring 검은비율 임계 (2.5%%)
  --point-threshold 0.20 \     # point 라벨 임계 (20%%, 변에 가까운 게 정상이라 느슨)
  --no-compile                 # 이미 PDF가 있으면 컴파일 스킵
```

**종료 코드**:
- `0` = 모든 dim 라벨 안전 (최종 통과)
- `1` = 일부 dim 라벨 overlap (수정 필요 — 아래 처치 매핑 적용)
- `2` = 컴파일/도구 실패

**보고서**: `<figure>-overlap.json` — 라벨별 `text`, `type`, `severity`(ok/near/overlap), `ring_dark_ratio`.

### 검증 절차 (결정적, 최대 3회 반복)

```text
회차 k (k = 1..3):
  1. python verify-overlap.py figure.tex
  2. exit code 분기:
     - 0 → 종료 (성공)
     - 2 → 컴파일 실패. .log 의 `!` 라인 분석 후 .tex 수정. 회차 다시 시도.
     - 1 → 보고서 figure-overlap.json 읽기. 각 dim overlap 라벨에 처치 매핑 적용.
  3. 처치 적용 후 회차 k+1 로 이동.

3회 후에도 dim overlap 잔존 시:
  → Read 도구로 figure-overlap.png 시각 판독.
  → 자동화로 풀리지 않는 케이스(겹친 호, 라벨-라벨 근접 등)는 § E 충돌 체크로 수동 결정.
```

### 처치 매핑 (overlap → 자동 수정 규칙)

`figure-overlap.json` 의 `severity == "overlap"` 인 dim 라벨마다 아래 우선순위로 처치를 시도한다.
한 회차에서 한 라벨에 한 가지 처치만 적용 (다중 처치는 다음 회차).

| # | 트리거 | 처치 (한 단계만) | 근거 섹션 |
|---|-------|-----------------|----------|
| 1 | dim overlap, 호 = 외측 정상 | **bend 한 단계 증가** (§ C 표의 다음 행) — sagitta 확대로 라벨 분리 | § C |
| 2 | 처치 1 후에도 overlap | **font 한 단계 축소** (`\small` → `\footnotesize` → `\scriptsize`) | § E #3 |
| 3 | 처치 2 후에도 overlap | **호 끝점 in-tip**: `($(P)!0.05!(Q)$)` 부터 시작·끝 | § E #2 |
| 4 | 처치 3 후에도 overlap, 인접 변과 충돌 | **Pattern D7 stack 으로 격하** (offset 0.5cm 추가) | § D, § E #4 |
| 5 | 처치 4 후에도 overlap, border 인접 | **standalone border 확장** `border=20pt` | § E #5 |

> **회차당 처치 1개만** 적용. 회차마다 재컴파일 + 재검증. 처치 1→5 순서로 시도하다가 통과하면 종료.

### 시각 체크리스트 (자동 검증으로 잡지 못하는 항목 — 보조)

`verify-overlap.py` 는 **dim 라벨 vs 도형선** 충돌만 결정적으로 잡는다.
다음 항목은 Read 도구로 PNG를 직접 봐서 판정한다 (스크립트가 통과해도 추가 점검).

| 항목 | 판단 기준 (시각) | 수정 방법 |
|------|----------------|----------|
| 라벨-라벨 겹침 | 두 라벨 박스가 ≤ 4pt 거리 | 하위 우선순위 라벨의 pos/anchor 조정 |
| 호 내부 라벨 이탈 | 각도 라벨이 호 바깥 | `\tkzLabelAngle[pos=...]` 값 축소 (1.5→1.2) |
| 치수선 호 교차 | 두 외측 호가 시각상 교차 | § D 인접 외곽 변 처치(bend 차이/스택) |
| 도형 외곽 이탈 | 라벨이 standalone border 밖 | `border=20pt` 확장 |
| 의미적 오류 | 각도 방향·등변 마크 누락 등 | Step 2.5 / Step 5 체크리스트 재적용 |

### 우선순위 (충돌 시)

```
정점 라벨 (위치 고정) > 변 길이 라벨 (pos 조정) > 각 라벨 (pos 축소/외부 전치)
```

### 워크드 예시

```bash
# 1회차 — "8" 라벨이 BC 변 위에 직접 올라감
$ python .claude/skills/gf2/verify-overlap.py fig.tex
labels=4 | dim_overlaps=1 | other_overlaps=0 | nears=3
  [overlap/  dim] '8' ring=0.0392 (thr=0.03)
$ echo $?
1

# 처치 #1: bend 한 단계 증가 (§C: L≤8 → 18 → 22) +
#         외측 점선 호로 감싸기 (\node 직접 삽입 금지)
# .tex 편집:
#   변경 전: \node at ($(B)!0.5!(C)$) {$8$};
#   변경 후: \draw[dashed, thin] (B) to[bend right=22]
#             node[midway, fill=white, inner sep=2pt, font=\small] {$8$} (C);

# 2회차
$ python .claude/skills/gf2/verify-overlap.py fig.tex
labels=4 | dim_overlaps=0 | other_overlaps=0 | nears=1
$ echo $?
0   # 통과
```

> **주의**: 시각 검증은 xelatex + pdftoppm이 WSL에 설치된 환경에서만 동작합니다. 컴파일 환경이 없으면 규칙 기반 배치(B1-B3)만 사용합니다.

## 산출물 (TeX + PDF + PNG)

**모든 gf2 호출은 세 개의 산출물을 만들어야 한다**: `.tex` 소스, 컴파일된 `.pdf`, 렌더링된 `.png` 미리보기. TeX만 주고 끝내면 사용자가 도형을 시각 확인할 수 없다.

한 줄 파이프라인:

```bash
python3 .claude/skills/gf2/render-tex.py path/to/figure.tex
```

내부적으로 `pdflatex`로 컴파일하고 pymupdf로 200dpi PNG를 만든다. 단일 페이지는 `figure.png`, 다페이지는 `figure-p{N}.png` 형식. 컴파일 실패 시 stderr에 latex 로그 tail이 출력되어 디버그 가능.

옵션:

- `--dpi 300` 고해상도
- `--engine xelatex` 한글 라벨(`kotex`)
- `--engine lualatex` 정밀 pgfmath

워크플로우 통합:

1. tkz-euclide 코드 작성 → `figure.tex`
2. `verify-overlap.py figure.tex` 로 정적 라벨 충돌 검사 (선택)
3. `render-tex.py figure.tex` 로 PDF·PNG 생성
4. **Read 도구로 `figure.png` 를 열어 사용자에게 시각 표시** — 시각 검증 루프(§시각 검증 루프)와 결합해 자동 회귀 가능

`verify-overlap.py`가 0(통과)일 때만 render-tex로 진행하지 말 것 — render-tex는 항상 실행해 사용자가 결과를 볼 수 있게 해야 한다. verify는 추가 안전망이지 게이트가 아니다.

## 주의사항

- **각도 기호**: 항상 `$40^\circ$` 형식 사용. `\degree`, `°` 직접 입력 금지.
- **각도 방향**: tkz-euclide에서 각도는 **반시계 방향**이 양수입니다. `\tkzFindAngle(A,O,B)`는 항상 0~360 사이의 값을 반환합니다. (Step 2.5 참조)
- **교점 순서**: `\tkzInterLC`, `\tkzInterCC`의 첫 번째 점(tkzFirstPoint)은 더 작은 각도에 해당합니다. `near` 옵션으로 직선의 첫 번째 점에 가까운 점을 얻을 수 있습니다.
- **common= 활용**: 한 교점이 이미 알려진 점이면 `common=B`로 제외하고 나머지만 취득.
- **원 정의 주의**: `\tkzDrawCircle[R](O,3)` 대신 먼저 `\tkzDefCircle[R](O,3) \tkzGetPoint{o}`한 후 `\tkzDrawCircle(O,o)` 사용을 권장합니다.
- **네임스페이스 충돌**: 점 이름은 대문자 알파벳 사용을 권장합니다. 인덱스가 필요하면 `P_1`, `P_2` 형식을 사용합니다.
- **LuaLaTeX 권장**: v5부터 `\usepackage[lua]{tkz-euclide}`로 더 정밀한 계산이 가능합니다.
