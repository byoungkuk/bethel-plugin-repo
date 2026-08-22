# lecture-blueprint 연계 패치 (3종)

lecture-blueprint 스킬을 정상 작동시키려면 기존 3개 스킬의 SKILL.md에 아래 변경 사항을 반영해야 한다. 각 스킬별 패치 파일에 교체 지점과 교체 텍스트를 명시했다.

## 적용 순서

1. 각 패치 파일의 "교체 전(Before)" 블록을 본인 터미널의 해당 SKILL.md에서 찾는다
2. 해당 블록을 "교체 후(After)" 블록으로 교체한다
3. 저장 후 스킬 재로드 (Cowork 설정에서 Skills → Reload)

## 파일 위치

| 대상 스킬 | SKILL.md 경로 |
|-----------|----------------|
| lecture-plan | `~/.claude/skills/lecture-plan/SKILL.md` |
| lecture-slides | `~/.claude/skills/lecture-slides/SKILL.md` |
| lecture-review | `~/.claude/skills/lecture-review/SKILL.md` |

## 패치 파일

- `patch-lecture-plan.md` — YAML에 `next_skill` 추가, 파이프라인 위치 갱신
- `patch-lecture-slides.md` — Phase 0 파이프라인 스캔 + BP 자동 탐색 + palette_key 자동 적용 + fast-track 우선순위 조정
- `patch-lecture-review.md` — 점검 축 0.5 (블루프린트 반영률) 추가
- `lecture-slides-SKILL-COMPLETE.md` — **완전판**: 패치를 모두 반영한 lecture-slides SKILL.md 전체 교체본 (수동 패치 대신 백업 후 덮어쓰기 가능)

## 설치 방법 2가지

### 방법 A: 완전판 덮어쓰기 (권장, 간단)

```bash
# 1. 기존 파일 백업
cp ~/.claude/skills/lecture-slides/SKILL.md ~/.claude/skills/lecture-slides/SKILL.md.bak

# 2. 완전판으로 교체
cp "lecture-slides-SKILL-COMPLETE.md" ~/.claude/skills/lecture-slides/SKILL.md
```

lecture-plan, lecture-review는 patch-*.md 파일대로 수동 적용.

### 방법 B: 수동 패치 (세밀한 변경 확인)

각 patch-*.md 파일의 교체 전/후 블록을 터미널에서 하나씩 수정.

## 주의

- 3개 중 **patch-lecture-slides는 반드시** 적용해야 lecture-blueprint가 파이프라인에서 호출된다
- patch-lecture-plan, patch-lecture-review는 권장 사항 (적용하지 않아도 lecture-blueprint 단독 사용은 가능)
