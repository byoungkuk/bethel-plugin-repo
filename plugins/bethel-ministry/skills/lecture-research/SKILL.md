---
name: lecture-research
description: 강의 기획안 기반 리서치 워크플로우 v2.1. lecture-plan v2의 기획안(target_profile 포함)을 입력받아, 목차 꼭지별로 리서치 질문을 생성하고 web_search·web_fetch로 자료를 수집한 뒤, 슬롯형 템플릿(도입 훅·핵심 개념·대표 사례[A/B/C 등급]·실습 소재·수준별 포인트·슬라이드 키워드·구술용 메모)에 채워 RL_ 접두어 노트로 저장한다. 관문 2(슬라이드 진입 검증)를 포함한다. 파이프라인 2단계. 트리거: 강의 리서치, 강의용 리서치, 강의 자료 조사, 강의 기획안 리서치, 교안 리서치, 슬라이드용 리서치, 커리큘럼 리서치, 강의 목차별 리서치, 강의 사례 조사, 강의 실습 소재 조사, RL 노트, RL_ 노트 생성, 강의 준비 리서치, 타깃 맞춤 사례, 강의 사례 등급. 일반 주제 리서치는 research-topic, 책쓰기 챕터 리서치는 book-research, 강의 기획안 작성은 lecture-plan, 슬라이드 제작은 lecture-slides를 사용한다.
---

# lecture-research v2.1

강의 기획안을 입력받아, 목차 꼭지별로 타깃에 적합한 강의 재료를 리서치·정리하는 스킬. 파이프라인 2단계.

v2.1 변경: Phase B 평가를 **관문 2**로 명시 승격, `gate_2_passed` 플래그 추가, lecture-plan v2의 `target_profile` YAML 블록 자동 수신, 실패 시 대응 경로 강화.

## 파이프라인 위치

lecture-plan [관문 1] → **lecture-research [관문 2]** → lecture-slides [관문 3] → lecture-infographic [관문 4]

## 입력

### 필수
- **강의 기획안**: lecture-plan v2 산출물(LP_*.md) 또는 직접 작성
  - `gate_1_passed: true` 플래그 있으면 Phase 1.5 생략

### 선택
- 추가 키워드, 기존 RL_ 노트(보강), 리서치 깊이(기본 3~5 / 딥 5~10)

## 프로세스

### Phase 1. 기획안 확인
- 강의 제목·대상·시간·목차·학습 목표 추출
- **lecture-plan v2 YAML에서 gate_1_passed, target_profile 로드**
- gate_1_passed가 true면 Phase 1.5 건너뛰고 Phase 2로

### Phase 1.5. 타깃 프로파일 추출 (lecture-plan v2 미사용 시)
- 직무/업종, 사전지식, 관심 맥락, 이탈 요인, 반응 요인 5항목
- 확인 불가 시 "일반 직장인" 기본값 + 노트 명시

### Phase 2. 꼭지별 리서치 질문 생성
- 꼭지당 2~4개, **타깃 프로파일 변수 강제 주입**
- 개념/사례/실습/수준별 4종

### Phase 3. 웹 리서치 실행
- 최근성(1년, AI는 6개월 가점), 원본 소스, 타깃 직무 일치, 숫자·결과 명시 우선

### Phase 4. 슬롯 채우기

꼭지별 템플릿:
- 도입 훅
- 핵심 개념 (1~2줄)
- 대표 사례 3개 (각 A/B/C 등급 태그 필수, 결과 수치 명시)
- 실습 소재 (소요·난이도·준비물)
- 수준별 설명 (초/중/고)
- 슬라이드 이미지 키워드 3~5개
- 구술용 메모 (3~5분 분량)

**등급 정의**
- A: 타깃 직무 동일 + 최근 1년 + 결과 수치
- B: 유사 직무 + 최근 2년 + 과정 설명
- C: 개념 예시용 보조

### Phase 4.5. 리서치 실패 경로
A·B 2개 미만 꼭지: 검색어 재구성 → 인접 확장 → 대체 설계(수강생 사례 수집 세션)

### Phase 5. Phase A 꼭지별 평가 (8개 중 7개 통과)
- [ ] 7개 슬롯 완성
- [ ] A/B/C 등급 태그 부여
- [ ] A·B 사례 2개 이상
- [ ] 타깃 직무 동일 맥락 사례 1개 이상
- [ ] 결과 수치 명시
- [ ] 실습 시간 내 실행 가능
- [ ] 도입 훅 반응 가능
- [ ] 구술 메모 3~5분 분량

### Phase 6. 관문 2: 슬라이드 진입 검증 (8/8 모두 충족)

- [ ] 모든 꼭지가 7개 슬롯 완성
- [ ] 모든 꼭지 A·B 사례 2개 이상
- [ ] 전체 A·B 사례 비율 70% 이상
- [ ] 실습 시간 내 실행 가능
- [ ] 구술 메모 꼭지당 3~5분
- [ ] 이미지 키워드 꼭지당 3~5개
- [ ] target_profile YAML 블록 채움
- [ ] 출처 1줄 형식

**AI 흔적 점검**: 과장형 형용사·모호한 부사·추측 표현 제거

**실패 시 대응**
- 1~6 실패: 해당 꼭지만 Phase 4·4.5 재실행
- 7~8 실패: YAML·출처 형식 수정
- 2회 연속 전체 실패: 기획안 재검토 + Phase 1 회귀

### Phase 7. 노트 저장
파일명: `RL_{강의명}_{YYYYMMDD}.md`

YAML 프론트매터:
\`\`\`yaml
---
title: {강의명} 리서치 노트
type: lecture-research
lecture_title: {강의 제목}
lecture_duration_minutes: {시간}
target_profile:
  job: {직무/업종}
  prior_knowledge: {사전지식}
  motivation: {관심 맥락}
  avoid: {이탈 요인}
  react: {반응 요인}
gate_1_passed: true
gate_2_passed: true
gate_2_score: 8/8
gate_2_checked_at: {YYYY-MM-DD}
ab_case_ratio: {N}%
created: {YYYY-MM-DD}
tags: [lecture, research, RL]
---
\`\`\`

## 출력
- `RL_{강의명}_{YYYYMMDD}.md`
- 8시간 이상은 꼭지별 분할 옵션

## 연계 스킬
- **입력**: lecture-plan v2 (LP_*.md, gate_1_passed, target_profile)
- **출력**: lecture-slides (슬롯 + YAML 플래그 전달)

## Harness 블록

| 항목 | 값 |
|---|---|
| 원문 보존 레벨 | L2 균형형 |
| 생성-평가 분리 | 슬롯 채움 → Phase A → 관문 2 → 재생성 |
| 분량 가드레일 | 꼭지당 600~1,000자 / 전체 4,000~10,000자 |
| 재생성 트리거 | A·B 2개 미만 / Phase A 7/8 미만 / 관문 2 8/8 미만 |

### 원문 보존 원칙
- 직접 인용 금지 기본. 강의 전달용 재구성
- 예외: 숫자·고유명사·공식 발표 문구는 원문 + 출처
- 구술 메모는 말로 전달할 형태 (글말 금지)

## 실행 원칙
- lecture-plan v2 입력 시 gate_1_passed 확인 후 진행
- 기획안 없이 실행 시 lecture-plan 먼저 안내
- 슬롯은 강의 바로 쓸 수 있는 형태로 (원문 요약 금지)
- 사례는 A·B 2개 이상이 통과 기준
- **관문 2 통과 전 lecture-slides 진입 금지**
- 금지어 규칙 적용
