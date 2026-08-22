# 프로젝트 설정 가이드 (Project Setup Guide)

이 파일은 `book-writing-pro` 스킬의 산출물 체계, 프로젝트 폴더 구조, 파일 운영 규칙, 장르별 가이드를 포함한다.

---

## 산출물 총괄

모든 산출물은 `.docx` 형식. 문서 생성 전 반드시 `/mnt/skills/public/docx/SKILL.md`를 읽고 따른다.

| 단계 | 산출물 | 파일명 |
|------|--------|--------|
| Phase 1: 기획 | 책 기획서 | `01-book-plan.docx` |
| Phase 1: 기획 | 작가 관점 선언 | `book-perspective-{프로젝트명}.md` |
| Phase 2: 목차설계 | 상세 목차 | `02-table-of-contents.docx` |
| Phase 2: 목차설계 | 경험·사례 뱅크 | `experience-bank-{프로젝트명}.md` |
| Phase 3: 집필 | 챕터별 초안 | `chapter-XX-draft.docx` |
| Phase 4: 경험주입 | 경험 삽입 챕터 | `chapter-XX-enriched.docx` |
| Phase 4: 경험주입 | 삽입 로그 | `04-experience-log.md` |
| Phase 5: 통합점검 | 통합 점검 리포트 | `05-integration-report.docx` |
| Phase 5: 통합점검 | 통합 원고 | `05-manuscript-full.docx` |
| Phase 6: 퇴고 | 퇴고 원고 | `06-manuscript-edited.docx` |
| Phase 6: 퇴고 | 편집 리포트 | `06-editing-report.docx` |
| Phase 7: 최종편집 | 최종 완성본 | `07-manuscript-final.docx` |

---

## 프로젝트별 스킬 폴더 구조

새 책 프로젝트마다 다음 구조로 스킬 폴더를 구성한다:

```
book-writing-pro/
├── SKILL.md                              ← 공통 워크플로우
├── book-perspective-template.md          ← 관점 선언 작성 가이드
├── experience-bank-template.md           ← 경험 뱅크 작성 가이드
├── editing-checklist.md                  ← 퇴고 3Pass 체크리스트
├── project-setup-guide.md               ← 이 파일 (산출물·폴더·장르 가이드)
├── hongstyle2.md                          ← 문체 가이드 (공통)
├── writing-principles.md                 ← 글쓰기 원칙 (공통)
└── [프로젝트별 파일]
    ├── book-perspective-{프로젝트명}.md   ← 이 책의 관점 선언
    ├── experience-bank-{프로젝트명}.md    ← 이 책의 경험 뱅크
    ├── chapter-template-{프로젝트명}.md   ← 이 책의 챕터 템플릿 (선택)
    ├── glossary-{프로젝트명}.md           ← 이 책의 용어 사전 (선택)
    └── anti-patterns-{프로젝트명}.md      ← 이 책의 구체적 금지 패턴 (선택)
```

프로젝트별 파일이 없으면 SKILL.md의 기본 규칙을 따른다. 프로젝트별 파일이 있으면 해당 파일이 우선한다.

---

## glossary 분리 기준

book-perspective의 "반복 키워드·개념 정의" 항목과 별도 `glossary-{프로젝트명}.md`의 역할을 구분한다.

| 조건 | 관리 위치 |
|------|----------|
| 핵심 용어 5개 이하 | book-perspective 안에 포함 (별도 파일 불필요) |
| 핵심 용어 6개 이상, 또는 용어 간 관계도 필요 | `glossary-{프로젝트명}.md` 별도 분리 |

별도 파일로 분리한 경우, book-perspective의 glossary 항목에는 "glossary 파일 참조"로만 표기하고 내용을 중복 기재하지 않는다.

---

## anti-patterns 역할 구분

book-perspective의 "쓰지 않을 것"과 별도 `anti-patterns-{프로젝트명}.md`는 역할이 다르다.

| 파일 | 역할 | 예시 |
|------|------|------|
| book-perspective "쓰지 않을 것" | 방향성: 이 책의 범위·논조·배제할 접근법 | "도구별 기능 비교표를 넣지 않는다" |
| anti-patterns 파일 | 구체적 금지 패턴: 문장·표현·구조 수준의 금지 목록 | "~하면 됩니다" 패턴, 리스트 나열 후 해설 없는 구성 |

anti-patterns 파일이 없으면 `writing-principles.md`의 금지어 규칙 + book-perspective의 "쓰지 않을 것"만으로 운영한다. 프로젝트 고유의 금지 패턴이 5개 이상 누적되면 별도 파일로 분리한다.

---

## 파일 참조 우선순위

챕터 작성 시 Claude가 참조하는 파일 우선순위:

| 우선순위 | 파일 | 참조 시점 |
|---------|------|----------|
| 1 (필수) | SKILL.md | 매 작업 시 |
| 2 (필수) | hongstyle2.md | 매 작업 시 |
| 3 (필수) | book-perspective-{프로젝트명}.md | 매 챕터 작성 전 |
| 4 (필수) | experience-bank-{프로젝트명}.md | 매 챕터 작성 전 (Phase 3~4) |
| 5 (해당 시) | chapter-template-{프로젝트명}.md | 챕터 구조 확인 필요 시 |
| 6 (해당 시) | glossary / anti-patterns | 용어 확인·금지 패턴 점검 시 |
| 7 (해당 시) | writing-principles.md | 금지어·분량 규칙 재확인 시 |

우선순위 1~4 외의 파일은 **필요 시에만** 참조한다. 모든 파일을 매번 읽지 않는다.

---

## 장르별 구조 가이드

장르에 따라 챕터 구성과 분량을 조정한다.

| 장르 | 챕터 수 | 챕터당 분량 | 총 분량 |
|------|---------|------------|---------|
| 실용서/가이드북 | 10~15 | 3,000~6,000자 | 40,000~70,000자 |
| 자기계발 | 10~15 | 2,500~4,000자 | 30,000~50,000자 |
| 논픽션 | 10~15 | 3,000~6,000자 | 40,000~70,000자 |
| 에세이/회고록 | 12~20 | 3,000~5,000자 | 50,000~80,000자 |
| 소설 (일반) | 15~25 | 3,000~5,000자 | 60,000~90,000자 |

### 장르별 경험·사례 비율 가이드

| 장르 | 권장 경험 비율 | 주요 경험 유형 |
|------|---------------|---------------|
| 실용서/가이드북 | 본문의 20~30% | 비교사례, 실패담 중심 |
| 경험서 | 본문의 40~50% | 직접경험, 전환점 중심 |
| 자기계발 | 본문의 30~40% | 전환점, 관찰사례 중심 |
| 논픽션 | 본문의 15~25% | 관찰사례, 비교사례 중심 |
| 에세이/회고록 | 본문의 50~60% | 직접경험, 전환점 중심 |
