---
name: suno-music-workflow
description: >
  Suno AI(V5) 음악 생성을 위한 전문 프롬프트·가사 설계 워크플로우.
  5단계 프로세스: 콘셉트 설계 → 스타일 프롬프트 구성 → 가사 작성 → 변형 생성 → 반복·리믹스 가이드.
  사용자가 음악 콘셉트(주제, 분위기, 용도)를 입력하면 Suno Custom Mode에 바로 붙여넣을 수 있는
  스타일 프롬프트 + 구조화된 가사(메타태그 포함)를 생성한다.
  장르 크로스오버, 보컬 스타일 지정, 에너지 다이나믹 설계까지 포괄한다.
  트리거: Suno, 수노, AI 음악, AI 노래, AI 작곡, 음악 만들기, 노래 만들기, 작곡,
  BGM 만들기, 배경음악, 징글, 음악 프롬프트, 노래 프롬프트, 가사 작성, 가사 쓰기,
  스타일 프롬프트, 음악 생성, AI 뮤직, Suno 프롬프트, 수노 프롬프트,
  Suno 가사, 수노 가사, Suno 스타일, 커버곡, 리믹스, 음악 AI,
  노래 가사, 작사, AI 작사, Suno V5, 음악 워크플로우.
  일반 글쓰기는 writing-workflow를 사용한다.
  나노바나나 이미지 프롬프트는 nanobanana-infographic-prompt 스킬을 사용한다.
  책 집필은 book-writing-workflow를 사용한다.
---

# Suno 음악 생성 워크플로우 (Suno Music Workflow)

Suno AI V5 Custom Mode에 최적화된 **스타일 프롬프트 + 구조화 가사**를 생성하는 5단계 프로세스.
사용자가 음악 콘셉트를 입력하면, Suno에 바로 붙여넣을 수 있는 완성된 프롬프트 세트를 제공한다.

## 보조 파일 안내

이 스킬은 워크플로우 흐름을 제공하며, 상세 레퍼런스는 보조 파일에서 참조한다.

| 보조 파일 | 내용 | 참조 시점 |
|----------|------|----------|
| `references/genre-style-guide.md` | 장르별 스타일 태그 사전, 크로스오버 공식, 시대별 키워드 | Step 2 스타일 프롬프트 구성 시 |
| `references/metatags-reference.md` | 구조 태그, 보컬 전달 태그, 에너지 태그, 태그 스태킹 규칙 | Step 3 가사 작성 시 |
| `references/prompt-patterns.md` | 스타일 프롬프트 공식, 용도별 패턴, 한국어 가사 팁 | Step 2, Step 3 |
| `references/vocal-instrument-tags.md` | 보컬 스타일·악기·프로덕션 태그 레퍼런스 | Step 2 스타일 구성 시 |
| `references/korean-pronunciation.md` | 한국어 받침별 발음 위험도, 음절 매핑, 호흡 구두점, 한영 혼용 전략 | Step 3 한국어 가사 작성 시 |
| `references/sample-prompts.md` | 장르별 완성 프롬프트+가사 예시 | 모든 단계에서 참고 |

**읽기 규칙:** 각 Step 진입 시 해당 보조 파일을 읽는다. 이미 같은 대화에서 읽은 파일은 다시 읽지 않는다.

---

## Suno 기본 구조 이해

Suno Custom Mode는 **2개 입력 필드**로 구성된다.

| 필드 | 역할 | 입력 형식 |
|------|------|----------|
| **Style Prompt** | 장르·분위기·악기·보컬·프로덕션 등 음악의 전체 사운드 정의 | 쉼표로 구분된 태그 나열 (대괄호 없음) |
| **Custom Lyrics** | 가사 + 구조 메타태그로 곡의 흐름·구조 제어 | 가사 텍스트 + [Verse], [Chorus] 등 대괄호 태그 |

**핵심 원칙:**
- Style Prompt = 사운드 설계 (장르, 무드, 악기, 보컬 톤, 프로덕션 품질)
- Custom Lyrics = 구조 설계 (메타태그) + 가사 텍스트
- Style Prompt에는 대괄호 태그를 넣지 않는다
- Custom Lyrics의 메타태그는 반드시 대괄호 `[ ]`로 감싼다
- Style Prompt는 4~8개 태그가 최적. 너무 적으면 AI 자유도 과다, 너무 많으면 충돌 발생

### 소괄호 금지 규칙 (중요)

**Custom Lyrics 필드에 소괄호 `( )`를 사용하지 않는다.**

Suno는 소괄호 안의 텍스트를 가사로 인식해서 그대로 부르는 경우가 발생한다. 악기 지시·분위기 설명 등을 소괄호로 넣으면 보컬이 "piano solo, emotional" 같은 지시어를 노래해버린다.

| 잘못된 방식 | 올바른 방식 |
|------------|-----------|
| `[Intro] (gentle piano, no drums)` | `[Intro] [Instrument: Piano]` 또는 Style Prompt에 포함 |
| `[Chorus] (full band, powerful)` | `[Chorus] [Energy: High]` |
| `[Bridge] (strip to vocals only)` | `[Bridge] [Breakdown]` |
| `[Outro] (fade out slowly)` | `[Outro] [Fade Out]` |

악기·프로덕션 관련 지시는 **Style Prompt에 포함**하거나, **대괄호 메타태그**로 변환한다.

### 태그 스태킹 규칙 (한 줄에 여러 태그)

대괄호 태그는 **같은 줄에 나란히 배치**할 수 있다. 쉼표로 합치지 않는다.

```
[Chorus] [Energy: High]          ← O 올바름 (2개 나란히)
[Final Chorus] [Energy: High]    ← O 올바름 (2개 나란히)
[Bridge] [Breakdown]             ← O 올바름 (2개 나란히)
[Chorus, Energy: High]           ← X 잘못됨 (쉼표로 합치면 안 됨)
```

**한 줄 태그 수 제한: 3개 이하**

| 태그 수 | 판정 | 예시 |
|---------|------|------|
| 2개 | 최적 | `[Chorus] [Energy: High]` |
| 3개 | 허용 | `[Bridge] [Breakdown] [Energy: Low]` |
| 4개 이상 | 금지 | `[Chorus] [Energy: High] [Belted] [Harmonized]` ← 충돌 위험 |

---

## 전체 흐름

```
Step 1: 콘셉트 설계 → Step 2: 스타일 프롬프트 구성 → Step 3: 가사 작성 → Step 4: 변형 생성 → Step 5: 반복·리믹스 가이드
```

사용자의 상태에 따라 적절한 단계부터 시작한다.
- 아이디어만 있음 → Step 1부터
- 장르·분위기 확정 → Step 2부터
- 가사 초안 있음 → Step 3부터 (구조 태그 삽입)
- 기존 곡 리믹스/변형 → Step 4부터

### Step 간 전환 규칙

각 Step 완료 후, 다음 Step으로 넘어가기 전에 사용자 확인을 받는다.

| 전환 | 확인 방식 |
|------|----------|
| Step 1 → 2 | 콘셉트 브리프 요약 제시 → 확정 여부 확인 |
| Step 2 → 3 | 스타일 프롬프트 제시 → 수정 여부 확인 |
| Step 3 → 4 | 완성된 가사 제시 → 방향 수정 확인 |
| Step 4 → 5 | 변형 세트 제시 → 추가 변형 여부 확인 |

"한 번에 해줘" 또는 "바로 만들어줘" 요청 시 확인 없이 연속 진행한다.

---

## Step 1: 콘셉트 설계 (Concept Design)

### 수집 항목

| 항목 | 질문 | 기본값 |
|------|------|--------|
| **용도** | 풀곡 / BGM / 징글 / 커버 / 데모 | 풀곡 |
| **장르** | 메인 장르 + 서브장르 (선택) | — |
| **분위기/무드** | 감정·에너지 키워드 | — |
| **보컬** | 남성/여성/듀엣/무보컬(instrumental) | — |
| **언어** | 한국어/영어/기타 | 한국어 |
| **길이** | 2분/4분/8분(최대) | 4분 |
| **참고 아티스트/곡** | 사운드 방향 참고 (직접 입력 불가, 스타일로 변환) | — |
| **주제/메시지** | 가사의 핵심 주제 | — |

### 참고 아티스트 변환 규칙

Suno는 아티스트명 직접 입력을 허용하지 않는다. 참고 아티스트가 있으면 해당 아티스트의 음악적 특징을 스타일 태그로 변환한다.

예시:
- "방탄소년단 느낌" → K-pop, dynamic, layered synths, powerful male vocals, anthemic chorus, hip-hop beats
- "아이유 느낌" → K-pop ballad, warm female vocals, acoustic guitar, gentle piano, intimate, storytelling
- "Billie Eilish 느낌" → dark pop, whispery vocals, heavy bass, minimal production, atmospheric, moody

### 산출물

콘셉트 브리프를 요약 정리해 사용자에게 제시. 확인 후 Step 2로.

---

## Step 2: 스타일 프롬프트 구성 (Style Prompt Design)

> **이 단계 진입 시** `references/genre-style-guide.md`, `references/vocal-instrument-tags.md`, `references/prompt-patterns.md`를 읽는다.

### 스타일 프롬프트 구성 공식

```
[장르 + 시대/서브장르], [무드/감정], [핵심 악기 1~2개], [보컬 스타일], [프로덕션 품질]
```

### 구성 규칙

1. **태그 수**: 4~8개 (최적 6개)
2. **순서**: 장르 → 무드 → 악기 → 보컬 → 프로덕션 순으로 배치
3. **충돌 방지**: 상반되는 태그 조합 금지 (calm + aggressive, minimal + orchestral)
4. **구체성**: "pop"보다 "synth-pop, 80s retro" 처럼 구체적으로
5. **길이**: 120자 이내 권장 (Suno Style Prompt 필드 제한 고려)
6. **Instrumental 표기**: 보컬 없는 곡은 반드시 "instrumental" 태그 포함
7. **악기·프로덕션 지시**: Custom Lyrics에서 소괄호로 넣지 말고 Style Prompt에 포함

### 한국어 곡 추가 태그

한국어 가사 곡에는 다음 태그를 상황에 맞게 Style Prompt에 추가한다:
- 공통: `clear Korean pronunciation`
- K-Pop: `K-pop, Korean vocals`
- 발라드: `Korean ballad, emotional Korean vocals`
- 힙합: `Korean hip-hop, Korean rap`

### 산출물

완성된 Style Prompt를 코드블록으로 제시. 확인 후 Step 3로.

---

## Step 3: 가사 작성 (Lyrics Writing)

> **이 단계 진입 시** `references/metatags-reference.md`를 읽는다. 한국어 가사 작성 시 `references/korean-pronunciation.md`도 읽는다.

### 가사 작성 프로세스

1. **곡 구조 설계** — 메타태그로 섹션 배치
2. **에너지 아크 설계** — 섹션별 에너지 흐름 계획
3. **가사 텍스트 작성** — 각 섹션별 가사
4. **대괄호 태그로 다이나믹 제어** — 에너지·보컬·악기 태그 삽입

### 가사 작성 규칙

1. **짧은 줄**: 한 줄에 7~12음절 (한국어 기준). 너무 길면 보컬이 뭉개짐
2. **단순한 어휘**: 일상적 단어 우선. 복잡한 한자어·전문용어 지양
3. **반복 활용**: 코러스는 같은 훅 라인 반복. 기억에 남는 짧은 구절
4. **운율 고려**: 같은 모음·종성 반복으로 리듬감 형성
5. **감정 전달**: 추상적 감정보다 구체적 상황·행동 묘사
6. **영어 혼용**: 한국어 곡에서 영어 훅은 효과적 (Suno가 잘 처리)
7. **소괄호 사용 금지**: 모든 지시는 대괄호 `[ ]` 태그로

### 한국어 발음 최적화

한국어 가사 작성 시 반드시 `references/korean-pronunciation.md`를 참조한다.

핵심 규칙 요약:
- **Style Prompt에 `clear Korean pronunciation` 태그 추가**
- **겹받침 음절 회피**: 삶→살아감, 넓은→큰, 없다→없어
- **줄당 5~12음절 유지**: 13음절 이상은 2줄로 분리
- **같은 섹션 내 줄별 음절 차이 ±2 이내**
- **쉼표(,)로 호흡 삽입**: 긴 구절 중간에 호흡점 표시
- **한영 혼용은 줄 단위 전환**: 한 줄 안에서 한영 섞지 않기

### 다이나믹 제어 방법

악기·에너지·보컬 변화는 모두 대괄호 메타태그로 지시한다.

```
[Verse 1] [Energy: Low]
나의 하루는 너로 시작해
커피 향처럼 번지는 네 목소리

[Pre-Chorus] [Build-Up]
점점 빨라지는 심장 소리

[Chorus] [Energy: High]
너와 함께라면 두렵지 않아
이 길의 끝까지 함께 걸어갈래
```

### Instrumental 구간 표기

보컬 없는 구간에는 가사를 비우고 대괄호 태그만 사용한다.

```
[Instrumental Break]

[Outro] [Fade Out]
```

### 산출물

완성된 Custom Lyrics를 코드블록으로 제시. Style Prompt와 함께 Suno 입력 세트로 제공. 확인 후 Step 4로.

---

## Step 4: 변형 생성 (Variation Generation)

동일 콘셉트에서 2~3개 변형을 생성한다.

| 변형 유형 | 방법 | 예시 |
|----------|------|------|
| **장르 믹스** | 메인 장르 유지 + 서브장르 교체 | indie folk → indie folk + electronic |
| **에너지 변환** | 같은 가사, 에너지 레벨 변경 | acoustic ballad → upbeat pop version |
| **보컬 변환** | 보컬 스타일·성별 교체 | 남성 보컬 → 여성 보컬 |
| **시대 변환** | 같은 장르의 다른 시대 사운드 | modern pop → 80s synth-pop |
| **용도 변환** | 풀곡 → instrumental BGM | 보컬 제거 + 악기 강화 |

### 변형 규칙

- 한 번에 1개 변수만 변경 (장르 OR 에너지 OR 보컬)
- Style Prompt만 변경하고 가사는 유지하는 것이 가장 안정적
- 가사까지 변경할 경우 구조(메타태그)는 유지

---

## Step 5: 반복·리믹스 가이드 (Iteration & Remix Guide)

### 생성 결과 평가 기준

| 평가 항목 | 체크 포인트 |
|----------|-----------|
| **장르 일치** | Style Prompt의 장르가 실제 사운드에 반영되었는가 |
| **보컬 품질** | 가사가 명확하게 전달되는가, 발음이 자연스러운가 |
| **구조 준수** | 메타태그대로 섹션이 구분되는가 |
| **에너지 아크** | 계획한 에너지 흐름이 구현되었는가 |
| **길이** | 원하는 길이에 근접한가 |
| **전체 완성도** | 곡 전체가 일관되고 마무리가 자연스러운가 |

### 결과별 대응 전략

| 문제 | 대응 방법 |
|------|----------|
| 장르가 다르게 나옴 | Style Prompt에서 장르 태그를 더 구체적으로 |
| 보컬이 뭉개짐 | 가사를 더 짧고 단순하게 수정 |
| 구조가 무시됨 | 메타태그를 별도 줄에 배치, 섹션당 가사 줄 수 줄이기 |
| 에너지가 평탄함 | [Energy: High/Low] 태그 추가 |
| 곡이 너무 짧음 | Extend 기능 사용 또는 가사 섹션 추가 |
| AI가 가사를 무시함 | 가사를 더 단순한 어휘로 교체 (5학년 수준) |

### Suno 후속 기능 활용

| 기능 | 설명 | 활용 시점 |
|------|------|----------|
| **Extend** | 생성된 곡을 이어서 확장 | 2분 곡을 4분으로 늘릴 때 |
| **Remix** | 기존 곡을 다른 장르·스타일로 변환 | 장르 전환 시 |
| **Cover** | 기존 곡에 다른 보컬 페르소나 적용 | 보컬 스타일 변경 시 |
| **Remaster** | 이전 버전 곡을 V5 품질로 업그레이드 | V3/V4 곡 업그레이드 시 |
| **Stem Export** | 보컬·드럼·베이스 등 개별 트랙 분리 | DAW에서 추가 편집 시 |

---

## 출력 포맷

모든 프롬프트는 코드블록으로 감싸서 복사 가능하게 제공한다.

```
=== Suno 프롬프트 세트 ===

[콘셉트]
용도: OOO / 장르: OOO / 분위기: OOO / 보컬: OOO / 언어: OOO

[Style Prompt]
스타일 프롬프트 — Suno Style 필드에 붙여넣기

[Custom Lyrics]
구조화된 가사 — Suno Custom Lyrics 필드에 붙여넣기

[설정 참고]
- Suno 모드: Custom Mode
- 추천 길이: O분
- Instrumental 여부: O
```

사용자가 파일로 요청할 경우 `.md` 또는 `.docx`로 저장한다.

---

## 스킬 간 연계

Suno AI 음악 생성용 프롬프트·가사 설계. 범위 밖:

| 요청 | 대상 스킬 |
|------|----------|
| 일반 글쓰기 | writing-workflow |
| 책 집필 | book-writing-workflow |
| 블로그 글 | blog-writing-workflow |
| 페이스북 글 | facebook-writing-workflow |
| 인포그래픽 이미지 프롬프트 | nanobanana-infographic-prompt |
| 책 표지 이미지 프롬프트 | bookcover-prompt-workflow |
