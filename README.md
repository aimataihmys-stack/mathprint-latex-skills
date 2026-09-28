# MathPrint LaTeX Skills

한국 수학 문제집용 **2D 도형·함수 그래프** 저작을 위한 로컬 gf2·gratik 스킬 인계본입니다. G4·3D·Blockly는 적용 범위에서 제외합니다.

**먼저 [MATHPRINT_START_HERE.md](MATHPRINT_START_HERE.md)를 읽으세요.** 이어서 `.claude/skills/mathprint-2d/SKILL.md`가 제품 범위·원문 보존·조판·검증 기준을 안내합니다.

이 저장소는 앱 자체나 완성된 빌드가 아닙니다. 기하·그래프 스킬과 필요한 보조 스크립트, 자체 예제, 적용 결정만 담은 배포본입니다. 현재 빌드 코드의 진행 상태는 실행자의 별도 앱 저장소에서 확인해야 합니다.

```bash
python3 handoff/mathprint-2d/verify-package.py
python3 handoff/mathprint-2d/smoke-render.py --trusted-examples
```

첫 명령은 Python 표준 라이브러리만 사용합니다. 두 번째 명령은 **동봉된 신뢰 예제 두 개만** pdflatex로 컴파일합니다. TeX 의존성이 없으면 중단하며 자동 설치하지 않습니다. 기존 렌더러는 불신 입력용 샌드박스가 아닙니다.

## 원본과 검증

원본: `hotdeli88-pixel/geo`의 로컬 gf2·gratik 최신 스냅샷. 선별 파일의 SHA-256은 `handoff/mathprint-2d/source-manifest.json`에 기록했습니다. 원본 저장소·기본 브랜치·로컬 작업·글로벌 설정은 변경하지 않았습니다. 이 배포본은 원본의 Git 이력이나 연구 코퍼스를 포함하지 않습니다.

로컬 패키지 검사와 자체 기하/그래프 예제 컴파일은 실행했습니다. **별도 Claude 웹 세션의 정확한 세 요구사항은 읽지 못했으므로, `DECISIONS.md`의 세 항목은 이 대화에서 확인한 요구에 대한 적용 결정입니다.** 세션 실행자는 실제 원문과 대조해야 합니다. Claude가 이미 이 파일을 읽거나 작업을 시작했다고 주장하지 않습니다.

폰트 파일·교재 PDF·학생 데이터·비밀값·글로벌 설정을 추가하지 않았습니다. 원본 문서 안의 3D 확장 설명은 보관된 자료이며, 이 제품의 구현 지시가 아닙니다. 원문에서 참조하는 전체 연구 디렉터리와 로컬 문서는 이 최소 배포본에 포함되지 않을 수 있습니다. 필수 읽기 경로는 START_HERE에 있는 파일들입니다.
