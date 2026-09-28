# MathPrint 2D — 로컬 LaTeX 스킬 인계

2026-09-28 · 기하 `gf2` + 함수 그래프 `gratik`

이 전용 저장소는 로컬에 있던 최신 스킬과 필요한 보조 스크립트를 클라우드 코드 세션에서 **직접 읽을 수 있게 전달하는 자료**입니다. 완성된 MathPrint 앱이나 배포 결과를 뜻하지 않습니다. 원본 `hotdeli88-pixel/geo`와 로컬 원본은 수정하지 않았습니다. 해당 원격의 현재 연결에 쓰기 권한이 없어, 사용자의 다른 게시 가능 계정에 선별 파일만 올린 독립 배포 저장소입니다.

## 먼저 읽을 파일

1. `.claude/skills/mathprint-2d/SKILL.md` — 이번 제품에 적용할 범위·우선순위
2. `handoff/mathprint-2d/DECISIONS.md` — 위임받은 범위에서 정한 구현 결정과 미확인 항목
3. `.claude/skills/gf2/skill.md` — 기하 작도·라벨·치수·선 스타일 원본
4. `.claude/skills/gratik/SKILL.md` — 함수·좌표축·그래프 원본
5. `handoff/mathprint-2d/ERRATA_AND_LIMITS.md` — 원본의 충돌·한계와 제품 적용 기준
6. `docs/superpowers/specs/gratik-design-system.md`, `.claude/skills/gratik/references/templates.md`

`gf2/skill.md`는 원본처럼 소문자 파일명입니다. 대소문자를 구별하는 클라우드에서도 위 경로를 그대로 읽으세요. 자동 탐색용 진입점은 대문자 `SKILL.md`를 가진 `mathprint-2d`입니다. 실제 자동 탐색 여부는 해당 클라이언트에서 확인해야 하며, 직접 파일을 읽는 방식은 자동 탐색에 의존하지 않습니다.

## 적용할 제품 범위

한국 수학 문제집에 넣을 **2D 도형·함수 그래프·정적 일러스트의 제작·편집·출력**에 집중합니다. G4, Blockly, 3D·전개도·단면·숨은선 자동 계산은 제외합니다. 원본 스킬에 남아 있는 3D 확장 설명은 보관용 참고이며 이 제품의 구현 지시가 아닙니다.

첫 세로 기능은 다음입니다.

> 지원되는 gf2 원문 가져오기 → 선택한 보조선만 점선으로 변경 → 점 이름/한글·수식 라벨 수정 → 폭 60mm로 실제 조판 → 저장·재열기 → 원문 차이 검증

이 인계만으로 기존 개발판의 모든 기능이나 테스트 통과를 주장하지 마세요. 현재 작업 저장소의 코드·테스트·중단 기록을 먼저 확인해야 합니다.

## 파일만 읽고 사용하기

별도 디렉터리에 이 저장소를 clone하거나, GitHub의 해당 파일을 직접 읽으면 됩니다. 기존 작업 저장소의 브랜치를 전환하거나 `reset`, `clean`, 강제 checkout하지 마세요.

```bash
git clone --single-branch --branch main \
  https://github.com/aimataihmys-stack/mathprint-latex-skills.git geo-mathprint-skills
cd geo-mathprint-skills
python3 handoff/mathprint-2d/verify-package.py
```

기존 폴더가 있으면 덮어쓰지 말고 다른 새 디렉터리를 선택합니다. 재현 가능한 인계를 위해 전달받은 커밋 SHA와 `git rev-parse HEAD`를 비교하세요. 이 스킬을 읽기 위해 글로벌 스킬·하네스·계정 설정을 설치하거나 수정할 필요는 없습니다. 이 용도에서는 기존 `MAC_INSTALL.md`의 글로벌 설정 변경 절차를 실행하지 마세요.

## 렌더러와 안전 경계

로컬의 공용 `scripts/render-tex.py`를 포함했고, 원본 스킬의 두 렌더러 링크 위치도 **일반 파일**로 복사해 깨진 심볼릭 링크를 없앴습니다. 이 기존 렌더러는 임의 TeX를 실행하므로 신뢰한 로컬 예제에만 사용합니다. 공개 업로드 API에 연결하지 마세요.

신뢰한 두 예제만 컴파일하는 보조 검증은 다음과 같습니다.

```bash
python3 handoff/mathprint-2d/smoke-render.py --trusted-examples
```

기본 패키지 검증은 Python 표준 라이브러리만 사용합니다. 예제 조판에는 PATH에 `pdflatex`와 TeX 패키지 `standalone`, `tkz-euclide`, `pgfplots`가 필요합니다. 패키지가 없으면 설치 완료로 표시하지 않고 중단합니다. 이 명령은 자동 설치하지 않습니다. 한글은 별도 LuaLaTeX/한글 패키지·폰트 검수가 필요하며, 한글 조판 전체를 이 두 예제로 검증했다고 주장하지 않습니다.

폰트 파일, 인증정보, 개인 설정, 수집한 교재 PDF·이미지 코퍼스, 학생 데이터는 이번 커밋에 추가하지 않습니다. `handoff/mathprint-2d/source-manifest.json`은 선별한 로컬 원본과 게시 사본의 SHA-256을 기록합니다.
