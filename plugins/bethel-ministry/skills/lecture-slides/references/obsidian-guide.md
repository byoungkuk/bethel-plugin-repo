# 강의 파이프라인 옵시디언 통합 가이드

강의 준비 파이프라인(research-topic → lecture-plan → lecture-slides)의 .md 산출물에 적용하는 옵시디언 통합 규칙.

---

## 1. 폴더 구조

```
강의명/
├── _MOC.md              ← 강의 전체 인덱스 (자동 생성)
├── 리서치/              ← RL_*.md
├── 기획/                ← 강의명_기획안.md
├── 슬라이드/            ← 구조.md, pptx, 이미지리스트.md
├── 이미지/              ← 인포그래픽 프롬프트 + 생성 이미지
└── 발표/                ← 스크립트, 핸드아웃
```

폴더명: 강의 제목 사용, 한글 허용, 30자 이내, 특수문자 제외.
첫 산출물 저장 시 폴더 생성.

## 2. YAML 프론트매터 표준

모든 .md 산출물에 공통 필드를 포함. 스킬 고유 필드는 각 스킬 기존 규칙 유지.

```yaml
---
title: "문서 제목"
date: YYYY-MM-DD
tags: [lecture-pipeline, 강의명태그, 스킬별태그]
type: research | plan | slide-structure | image-list | image-prompt | script | handout
lecture: "강의 제목"
stage: "Stage 0~4"
status: draft | done
# + 스킬 고유 필드 (research_depth, research_mode 등)
---
```

| 스킬 | type | stage |
|------|------|-------|
| research-topic | `research` | `Stage 0` |
| lecture-plan | `plan` | `Stage 1` |
| lecture-slides 구조 | `slide-structure` | `Stage 2` |
| lecture-slides 이미지 리스트 | `image-list` | `Stage 2` |
| image-infographic | `image-prompt` | `Stage 3` |
| 발표 노트/핸드아웃 | `script` / `handout` | `Stage 4` |

태그: `lecture-pipeline`(고정) + 강의명(공백 없이) + 스킬태그(research/plan/slides 등).

## 3. 백링크 규칙

YAML 바로 아래, 본문 전에 연결 블록을 삽입한다.

```markdown
> **연결**: [[이전 단계 파일명]] → 이 문서 → [[다음 단계 파일명]]
```

| 산출물 | 이전 링크 | 다음 링크 |
|--------|----------|----------|
| RL_*.md | (없음) | [[강의명_기획안]] |
| 기획안 | [[RL_주제명]] (없으면 생략) | [[강의명_슬라이드구조]] |
| 슬라이드 구조 | [[강의명_기획안]] | [[강의명_이미지리스트]] |
| 이미지 리스트 | [[강의명_슬라이드구조]] | image-infographic |

파일명 패턴: `RL_주제명`, `강의명_기획안`, `강의명_슬라이드구조`, `강의명_이미지리스트`.

## 4. MOC 자동 생성

첫 산출물 저장 시 `_MOC.md`를 생성. 이후 산출물 추가 시 갱신.

```markdown
---
title: "강의명 - 준비 현황"
date: YYYY-MM-DD
tags: [lecture-pipeline, MOC, 강의명태그]
type: moc
lecture: "강의 제목"
---

# 강의명 — 준비 현황

| Stage | 산출물 | 상태 | 링크 |
|-------|--------|------|------|
| 0. 리서치 | RL_주제명.md | done/- | [[RL_주제명]] |
| 1. 기획 | 강의명_기획안.md | done/- | [[강의명_기획안]] |
| 2. 슬라이드 구조 | 강의명_슬라이드구조.md | done/- | [[강의명_슬라이드구조]] |
| 2. pptx | 04-slides.pptx | done/- | (파일) |
| 2. 이미지 리스트 | 강의명_이미지리스트.md | done/- | [[강의명_이미지리스트]] |
| 3. 이미지 | (image-infographic) | done/- | - |
| 4. 발표 | (선택) | done/- | - |

**메타**: 총 시간 / 대상 / 슬라이드 N장 / 이미지 필요 N장
```

"MOC 안 만들어도 돼" 명시 시 생략.

## 5. 적용 순서

산출물 저장 시: ① 폴더 확인·생성 → ② YAML 작성 → ③ 백링크 삽입 → ④ 파일 저장 → ⑤ MOC 갱신

## 6. 적용 판별

**기본 적용**: .md 산출물에 YAML 프론트매터 + 백링크 항상 포함.
**파일 저장 요청 시 추가**: 폴더 구조 생성 + MOC 생성·갱신.
**생략**: "프론트매터 빼줘", "백링크 안 해도 돼" 명시 시.
