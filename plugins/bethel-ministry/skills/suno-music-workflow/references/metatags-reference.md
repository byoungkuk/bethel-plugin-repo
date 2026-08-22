# 메타태그 레퍼런스 (Metatags Reference)

Suno Custom Lyrics 필드에 입력하는 대괄호 `[ ]` 메타태그 레퍼런스.
메타태그는 **가사 필드에서만 사용**하며, 각 태그는 **별도 줄**에 배치한다.

**중요: Custom Lyrics 필드에 소괄호 `( )`를 사용하지 않는다. Suno가 소괄호 안 텍스트를 가사로 인식해서 부를 수 있다. 모든 지시는 대괄호 `[ ]` 태그로만 한다.**

---

## 목차

1. 구조 태그 (Structure Tags)
2. 에너지·다이나믹 태그 (Energy & Dynamic Tags)
3. 보컬 전달 태그 (Vocal Delivery Tags)
4. 악기·사운드 태그 (Instrument Tags)
5. 특수 태그 (Special Tags)
6. 태그 스태킹 규칙 (한 줄에 여러 태그)
7. 태그 배치 규칙
8. 장르별 구조 템플릿

---

## 1. 구조 태그 (Structure Tags)

곡의 섹션을 정의하는 핵심 태그. 별도 줄에 배치하고, 바로 아래에 해당 섹션 가사를 작성한다.

### 필수 태그

| 태그 | 기능 | 설명 |
|------|------|------|
| `[Intro]` | 도입부 | 곡의 시작. 짧은 인스트루멘탈 또는 분위기 설정 |
| `[Verse]` / `[Verse 1]` / `[Verse 2]` | 절 | 스토리·메시지 전개. 번호로 구분 가능 |
| `[Pre-Chorus]` | 프리코러스 | 코러스로의 전환부. 에너지 빌드업 |
| `[Chorus]` | 후렴 | 곡의 핵심 훅. 가장 기억에 남는 부분 |
| `[Bridge]` | 브릿지 | 반복을 깨는 전환부. 새로운 멜로디·감정 |
| `[Outro]` | 아웃트로 | 곡의 마무리. 페이드아웃 또는 마지막 리졸브 |

### 보조 태그

| 태그 | 기능 | 설명 |
|------|------|------|
| `[Instrumental Break]` | 간주 | 보컬 없는 악기 연주 구간 |
| `[Interlude]` | 간주/연결부 | 섹션 사이 짧은 악기 구간 |
| `[Hook]` | 훅 | 짧고 반복되는 캐치 프레이즈 |
| `[Refrain]` | 리프레인 | 반복되는 짧은 구절 |
| `[Final Chorus]` | 마지막 코러스 | 곡의 클라이맥스. 가장 에너지 높은 코러스 |
| `[Break]` | 브레이크 | 갑작스러운 정지 또는 패턴 중단 |
| `[Drop]` | 드롭 | EDM 장르에서 에너지 폭발 지점 |
| `[Build]` / `[Build-Up]` | 빌드업 | 에너지가 점진적으로 올라가는 구간 |
| `[Breakdown]` | 브레이크다운 | 에너지를 낮추고 요소를 줄이는 구간 |
| `[Guitar Solo]` | 기타 솔로 | 기타 솔로 구간 |
| `[Piano Solo]` | 피아노 솔로 | 피아노 솔로 구간 |
| `[End]` | 끝 | 곡 종료 신호 |

---

## 2. 에너지·다이나믹 태그 (Energy & Dynamic Tags)

섹션의 에너지 레벨과 다이나믹을 제어한다. 구조 태그와 같은 줄에 나란히 배치.

| 태그 | 효과 |
|------|------|
| `[Energy: Low]` | 조용하고 차분한 에너지 |
| `[Energy: Medium]` | 중간 에너지 |
| `[Energy: High]` | 높은 에너지, 풀 사운드 |
| `[Mood: Calm]` | 차분한 분위기 |
| `[Mood: Intense]` | 강렬한 분위기 |
| `[Mood: Melancholic]` | 우울한 분위기 |
| `[Mood: Joyful]` | 밝고 즐거운 분위기 |

### 에너지 변화 조합 예시

```
[Verse 1] [Energy: Low]
가사 내용

[Pre-Chorus] [Build-Up]
가사 내용

[Chorus] [Energy: High]
가사 내용

[Bridge] [Breakdown]
가사 내용

[Final Chorus] [Energy: High]
가사 내용
```

---

## 3. 보컬 전달 태그 (Vocal Delivery Tags)

보컬의 전달 방식을 지시한다. 구조 태그와 같은 줄에 나란히 배치.

| 태그 | 효과 |
|------|------|
| `[Whispered]` | 속삭이는 보컬 |
| `[Spoken Word]` | 말하듯 전달 |
| `[Belted]` | 힘차게 내지르는 보컬 |
| `[Falsetto]` | 가성 |
| `[Raspy]` | 허스키한 보컬 |
| `[Harmonized]` | 하모니 보컬 |
| `[Ad-lib]` | 애드리브 |
| `[Call and Response]` | 콜앤리스폰스 |
| `[Chanting]` | 챈팅 |
| `[Humming]` | 허밍 |
| `[Rap]` | 랩 전달 |
| `[Singing]` | 노래 전달 (기본값) |

### 보컬 태그 사용 예시

```
[Verse 1] [Whispered]
아무도 모르게 다가온 너
밤하늘 별처럼 조용히

[Chorus] [Belted] [Energy: High]
소리쳐 불러본다 네 이름
```

---

## 4. 악기·사운드 태그 (Instrument Tags)

섹션별로 악기를 지정할 때 사용한다. 전체 곡의 악기 구성은 Style Prompt에서 설정하고, 섹션별 변화가 필요할 때만 사용한다.

| 태그 | 효과 |
|------|------|
| `[Instrument: Piano]` | 피아노 중심 |
| `[Instrument: Acoustic Guitar]` | 어쿠스틱 기타 중심 |
| `[Instrument: Keys, Drums]` | 건반 + 드럼 |
| `[Instrument: Strings]` | 현악기 중심 |

---

## 5. 특수 태그 (Special Tags — V5)

Suno V5에서 추가·개선된 태그.

| 태그 | 효과 |
|------|------|
| `[Tempo: Slow]` / `[Tempo: Fast]` | 템포 지시 |
| `[Big Finish]` | 곡 끝에 클라이맥스 연출 |
| `[Fade Out]` | 페이드아웃 종료 |

---

## 6. 태그 스태킹 규칙 (한 줄에 여러 태그)

### 기본 규칙

대괄호 태그는 **같은 줄에 나란히 배치**한다. 쉼표로 합치지 않는다.

```
[Chorus] [Energy: High]          ← O 올바름
[Chorus, Energy: High]           ← X 잘못됨
```

### 태그 수 제한

| 태그 수 | 판정 | 예시 |
|---------|------|------|
| 2개 | 최적 | `[Chorus] [Energy: High]` |
| 3개 | 허용 | `[Bridge] [Breakdown] [Energy: Low]` |
| 4개 이상 | 금지 | 충돌 위험, 2~3개로 줄여야 함 |

### 조합 우선순위

태그를 3개 이하로 줄여야 할 때, 아래 우선순위로 선택한다.

1. **구조 태그** (필수): [Verse], [Chorus], [Bridge] 등
2. **에너지/다이나믹 태그** (권장): [Energy: High], [Build-Up], [Breakdown]
3. **보컬 전달 태그** (선택): [Belted], [Whispered], [Rap]

보컬 전달과 악기 태그를 동시에 넣어야 하면, 하나는 Style Prompt로 이동한다.

---

## 7. 태그 배치 규칙

### 필수 규칙

1. **별도 줄**: 모든 메타태그는 가사와 분리해 별도 줄에 배치
2. **대괄호 필수**: `[Verse]` O / `Verse:` X (괄호 없으면 가사로 불림)
3. **소괄호 금지**: `( )` 안의 텍스트는 가사로 불릴 수 있음
4. **일관성**: 같은 기능에 같은 태그 사용 (`[Build]`와 `[Build-Up]` 혼용 금지)
5. **과부하 금지**: 한 섹션에 태그 3개 이하

### 권장 규칙

1. **섹션당 가사 2~6줄**: 너무 많으면 Suno가 구조를 무시
2. **코러스 반복**: 같은 가사를 정확히 반복해야 일관된 멜로디
3. **빈 줄 활용**: 섹션 사이에 빈 줄로 시각적 구분

### 배치 순서

```
[구조 태그] [에너지 태그]
가사 첫 줄
가사 둘째 줄

```

---

## 8. 장르별 구조 템플릿

### 팝/K-Pop (4분)

```
[Intro]
[Verse 1] [Energy: Low]
[Pre-Chorus] [Build-Up]
[Chorus] [Energy: High]
[Verse 2] [Energy: Medium]
[Pre-Chorus] [Build-Up]
[Chorus] [Energy: High]
[Bridge] [Breakdown]
[Final Chorus] [Energy: High]
[Outro] [Fade Out]
```

### EDM/댄스 (4분)

```
[Intro] [Energy: Low]
[Build]
[Drop] [Energy: High]
[Breakdown] [Energy: Low]
[Build]
[Drop] [Energy: High]
[Outro] [Fade Out]
```

### 힙합/랩 (3~4분)

```
[Intro]
[Verse 1] [Rap]
[Chorus] [Energy: High]
[Verse 2] [Rap]
[Chorus] [Energy: High]
[Bridge] [Breakdown]
[Final Chorus] [Energy: High]
[Outro]
```

### 발라드 (4~5분)

```
[Intro] [Energy: Low]
[Verse 1] [Energy: Low]
[Verse 2] [Energy: Low]
[Chorus] [Energy: Medium]
[Verse 3]
[Chorus] [Energy: High]
[Bridge] [Breakdown]
[Final Chorus] [Energy: High] [Belted]
[Outro] [Fade Out]
```

### 로파이/칠 (3분)

```
[Intro] [Energy: Low]
[Verse 1] [Energy: Low]
[Chorus] [Energy: Medium]
[Instrumental Break]
[Verse 2]
[Chorus]
[Outro] [Fade Out]
```

### 시네마틱/Instrumental (3~5분)

```
[Intro] [Energy: Low]
[Verse] [Energy: Medium]
[Build]
[Chorus] [Energy: High]
[Breakdown] [Energy: Low]
[Build]
[Final Chorus] [Energy: High]
[Outro] [Fade Out]
```

### 징글/쇼트 (30초~1분)

```
[Intro]
[Chorus]
[Outro]
```
