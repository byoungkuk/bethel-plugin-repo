# Patch: lecture-plan → lecture-blueprint 연결

## 변경 지점 1 — 파이프라인 위치 블록 (SKILL.md 15행)

### 교체 전

```
lecture-plan [관문 1] → lecture-research [관문 2] → lecture-slides [관문 3] → lecture-infographic [관문 4]
```

### 교체 후

```
lecture-plan [관문 1] → lecture-research [관문 2] → lecture-blueprint [관문 BP] → lecture-slides [관문 3] → lecture-review
```

## 변경 지점 2 — YAML 프론트매터 예시 (Phase 4. 최종 출력 섹션)

### 교체 전

```yaml
gate_1_passed: true
gate_1_score: {N}/12
gate_1_checked_at: {YYYY-MM-DD}
created: {YYYY-MM-DD}
tags: [lecture, plan, LP]
```

### 교체 후

```yaml
gate_1_passed: true
gate_1_score: {N}/12
gate_1_checked_at: {YYYY-MM-DD}
next_skill: lecture-blueprint
created: {YYYY-MM-DD}
tags: [lecture, plan, LP]
```

## 변경 지점 3 — 연계 스킬 블록 (SKILL.md 230행 부근)

### 교체 전

```
## 연계 스킬

- **입력**: (없음 — 파이프라인 1단계)
- **출력 연계**: lecture-research (YAML의 target_profile 블록을 그대로 전달)
```

### 교체 후

```
## 연계 스킬

- **입력**: (없음 — 파이프라인 1단계)
- **출력 연계(필수)**: lecture-research (YAML의 target_profile 블록을 그대로 전달)
- **출력 연계(반일 이상 강의)**: lecture-blueprint (꼭지 단위를 슬라이드 단위로 분해)
  - 슬라이드 15장 이상 예상 시 lecture-research 이후 lecture-blueprint 실행 권장
  - YAML에 `next_skill: lecture-blueprint` 자동 기록
```
