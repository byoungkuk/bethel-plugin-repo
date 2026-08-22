---
name: daily-lectionary-devotion
description: "교회력 성서정과(Revised Common Lectionary) 기반 매일 아침 묵상 노트를 자동 생성하고 옵시디언 볼트에 저장하는 스킬. 사용자가 \"오늘 묵상 만들어줘\", \"매일 성서정과 묵상\", \"오늘 성서정과 본문 묵상\", \"아침 묵상 노트\", \"성서정과 묵상 작성\", \"오늘 본문 묵상해줘\", \"묵상 파일 만들어줘\", \"RCL 묵상\", \"02 매일묵상 폴더에 저장\" 등을 언급하면 반드시 이 스킬을 사용할 것. 매일 아침 성서정과 본문을 자동으로 가져오고, 짧은 신학적·인문학적 묵상 포인트를 생성하여 옵시디언 마크다운 노트로 저장한다."
---

# Daily Lectionary Devotion (매일 성서정과 묵상)

군선교사 김병국 목사의 매일 아침 묵상 워크플로우.
교회력 성서정과(RCL) 본문을 조회하고, 신학적·인문학적 묵상 포인트를 작성한 뒤 옵시디언 볼트에 저장한다.

---

## ⚙️ 설정 (CONFIG)

```
VAULT_PATH: /Users/bk-mini/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault_BK
DEVOTION_FOLDER: 30.source/31.daily-lectionary-devotion
FULL_DEVOTION_PATH: /Users/bk-mini/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault_BK/30.source/31.daily-lectionary-devotion
```

> **첫 실행 전 확인**: 사용자에게 옵시디언 볼트의 실제 절대 경로를 확인하고,
> 위 `VAULT_PATH`를 정확하게 설정한 후 진행할 것.

---

## 📋 워크플로우 단계

### Phase 0 — 날짜 및 교회력 정보 확인

```python
# 오늘 날짜 및 교회력 주차 파악
import datetime
today = datetime.date.today()
date_str = today.strftime("%Y-%m-%d")        # 파일명용: 2025-04-29
date_kr  = today.strftime("%Y년 %m월 %d일")  # 노트 헤더용
weekday_kr = ["월","화","수","목","금","토","일"][today.weekday()]
```

### Phase 1 — 오늘의 성서정과 본문 가져오기

**핵심 소스: dailylectio.net** (확인된 URL 패턴)

**Step 1**: 캘린더 페이지에서 오늘 날짜의 슬러그(slug)를 가져온다.
```
web_fetch: https://www.dailylectio.net/calendar?date={YYYY-MM-DD}
```
→ 캘린더 HTML에서 오늘 날짜 셀의 링크 추출 (예: `/2026-04-29/reflecting-on-the-fourth-sunday-of-easter`)

**Step 2**: 해당 슬러그로 본문 페이지 접근
```
web_fetch: https://www.dailylectio.net/{YYYY-MM-DD}/{slug}?calendar={YYYY-MM-DD}
```
→ 본문 전체(시편, 구약, NT/복음서) 추출

**백업 소스 (Step 1~2 실패 시)**:
- `web_search` 쿼리: `dailylectio.net {YYYY-MM-DD} Easter lectionary readings`
- `web_search` 쿼리: `"Revised Common Lectionary" daily readings {YYYY-MM-DD}`

**수집 본문 구성**:

| 구분 | 주일(일요일) | 평일 |
|------|------------|------|
| 구약 | ✅ OT | ✅ OT |
| 시편 | ✅ Psalm | ✅ Psalm |
| 서신서 | ✅ Epistle | 없을 수 있음 |
| 복음서 | ✅ Gospel | ✅ NT (복음서 또는 서신서) |

> **참고**: 평일 RCL은 Psalm + OT + NT 3본문 구조가 일반적.
> 주일(Sunday)은 4본문 구조.
> **주일인 경우**: 교회력 주간 이름(예: "부활절 4주일")과 연도(A/B/C)를 함께 파악한다.

### Phase 2 — 본문 내용 분석 (간략)

각 본문에 대해 다음 항목을 간단히 파악한다:

| 항목 | 내용 |
|------|------|
| 핵심 단어/표현 | 본문에서 눈에 띄는 단어 1~2개 |
| 본문의 배경 | 한 줄 요약 |
| 오늘의 색조 | 위로 / 도전 / 경이 / 회개 / 소망 중 선택 |

4개 본문 사이의 **공통 주제어(테마)** 1개를 추출한다.

### Phase 3 — 묵상 포인트 작성

아래 구조로 묵상 내용을 작성한다. 각 항목은 **짧은 단문**으로, 스피치하듯 읽히게 쓴다.

#### 3-1. 오늘의 한 줄 테마 (Leitmotif)
- 4개 본문을 아우르는 핵심 문장 1개
- 신학적 개념을 인문학·일상 언어로 표현
- 예: "두려움이 문을 닫는다. 그러나 사랑은 벽을 통과한다."

#### 3-2. 본문별 묵상 포인트 (각 2~4문장)
각 본문마다 짧은 묵상 단락 1개. 형식:
```
**[본문 약어] 핵심 구절 또는 단어**
→ 2~4문장 묵상 (인문학적·신학적 통찰 포함)
```

#### 3-3. 오늘의 질문 (Anchor Question)
- 하루를 살아가며 붙들고 갈 질문 1개
- 군인(20대 초반 남성) 맥락에 연결될 수 있으면 더 좋음
- 예: "오늘 나는 누구에게 '평화가 있기를' 말할 수 있을까?"

#### 3-4. 오늘의 기도 (3~5문장)
- 구어체, 직접적인 언어
- 감사 → 고백 → 간구의 흐름
- 군인 삶의 맥락(훈련, 관계, 사명) 자연스럽게 녹여내기

### Phase 4 — 옵시디언 노트 생성 및 저장

#### 4-1. 파일명 생성
```
형식: YYYY-MM-DD-요일.md
예시: 2026-04-29-수.md
      2026-04-27-일.md
      2026-05-03-일.md
```

#### 4-2. 노트 템플릿

```markdown
---
date: {{date_str}}
tags:
  - 묵상
  - 성서정과
  - {{교회력_주차}}
  - {{본문_테마_태그}}
lectionary_year: {{A/B/C}}
---

# {{date_kr}} ({{weekday}}) — {{교회력_주차}}

> **오늘의 테마**: {{오늘의_한줄_테마}}

---

## 📖 오늘의 성서정과 본문

| 구분 | 본문 |
|------|------|
| 구약 | {{OT_ref}} |
| 시편 | {{Psalm_ref}} |
| 서신서 | {{Epistle_ref}} |
| 복음서 | {{Gospel_ref}} |

---

## 🔍 묵상 포인트

{{본문별_묵상_포인트}}

---

## ❓ 오늘의 질문

> {{오늘의_앵커_질문}}

---

## 🙏 오늘의 기도

{{오늘의_기도}}

---

## 📝 메모

(직접 추가할 공간)

```

#### 4-3. 파일 저장
```bash
# 저장 경로: {VAULT_PATH}/{DEVOTION_FOLDER}/{파일명}
# bash_tool로 파일 생성
TARGET_DIR="{VAULT_PATH}/31.daily-lectionary-devotion"
mkdir -p "$TARGET_DIR"
cat > "$TARGET_DIR/{파일명}" << 'EOF'
{노트_내용}
EOF
```

> **경로 오류 시**: 사용자에게 실제 볼트 경로를 다시 확인하고 CONFIG를 업데이트한다.

### Phase 5 — 결과 확인 및 출력

저장 완료 후 다음을 출력한다:
1. ✅ 저장 경로 (`02 매일묵상/파일명.md`)
2. 📋 오늘의 한 줄 테마
3. 📖 본문 목록
4. 💡 묵상 포인트 미리보기 (첫 번째 포인트만)

---

## 🗂️ 파일 구조 예시

```
Vault_BK/
└── 30.source/
    └──31.daily-lectionary-devotion/
         ├── 2026-04-26-일.md
         ├── 2026-04-27-월.md
         ├── 2026-04-28-화.md
         ├── 2026-04-29-수.md
        └── ...
```

---

## ✍️ 묵상 문체 원칙

- **짧은 단문** 위주. 만연체 금지.
- **인문학적·시적** 표현 환영 (나태주, 박노해 시인의 문체 참조 가능)
- 기독교 전문용어는 **일상 언어로 풀어서** 설명
- 20대 초반 군인이 **공감할 수 있는 구체적 삶의 언어** 사용
- 개인 구원뿐 아니라 **공동체적·사회적 차원**도 자연스럽게 담아냄

---

## 🔁 반복 실행 (매일 자동화 고려)

이 스킬은 매일 한 번 실행을 전제로 한다.
같은 날 중복 실행 시, 기존 파일이 있으면 덮어쓰기 전에 확인한다:
```bash
if [ -f "$TARGET_PATH" ]; then
  echo "⚠️ 오늘 묵상 파일이 이미 존재합니다. 덮어쓸까요?"
fi
```

---

## ⚠️ 주의사항

- 성서정과 본문이 온라인에서 조회되지 않으면, 가장 최근에 알려진 주차 정보와 사용자 확인 후 진행
- 묵상 내용은 정통 개신교 신학(칼 바르트, 본회퍼 전통) 안에서 작성
- 이단 교단(구원파, 신천지 등)의 해석 방식 철저히 배제