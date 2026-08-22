---
name: bilingual-subtitle
description: >
  영어 MP4 영상과 한글 SRT 자막을 받아 영상에 자막을 나눔스퀘어 폰트로 burn-in하는 스킬.
  두 가지 모드를 지원한다:
  (1) 한글 자막만 — 한글 SRT를 그대로 영상에 합성.
  (2) 한영 병기 — 한글 아래 영어를 함께 표시.
  사용자가 "자막 달아줘", "자막 입혀줘", "자막 합성", "SRT 넣어줘", "영상에 자막",
  "한영 병기", "bilingual subtitle", "한글 자막만", "자막 burn-in" 등을 언급하거나
  MP4 + SRT 파일을 함께 제공할 때 반드시 이 스킬을 사용할 것.
  모드가 명확하지 않으면 물어보고 시작한다.
---

# bilingual-subtitle 스킬

MP4 영상에 한글 SRT 자막을 나눔스퀘어 폰트로 직접 새겨 넣는다.  
요청에 따라 **한글만** 또는 **한영 병기** 두 가지 모드로 동작한다.

---

## STEP 0 — 모드 결정

자막 작업을 시작하기 전에 **어떤 모드**로 진행할지 결정한다.

**자동 감지 규칙:**

| 사용자 발언 | 모드 |
|------------|------|
| "한영 병기", "한영 자막", "영어도 같이", "bilingual" | → **한영 병기 모드** |
| "한글만", "한글 자막만", "영어 필요 없어" | → **한글 전용 모드** |
| 모드 언급 없이 "자막 달아줘" 등 | → **사용자에게 질문** |

모드가 명확하지 않으면 AskUserQuestion 도구로 물어본다:

> "자막을 어떻게 넣을까요?  
> 1. 한글 자막만  
> 2. 한글 + 영어 병기 (한영 자막)"

모드가 결정되면 해당 섹션으로 이동한다.

---

## STEP 1 — 공통 파일 준비

어떤 모드든 먼저 파일을 공백 없는 경로로 복사한다.

```bash
cp "<원본_mp4>" /tmp/bs_input.mp4
cp "<원본_srt>" /tmp/bs_ko.srt
```

파일명에서 영상 제목을 추출해 출력 파일명을 정한다.  
예: `"You Raise Me Up.mp4"` → 출력명 = `"YouRaiseMeUp_자막.mp4"` (또는 `_한영자막.mp4`)

---

## MODE A — 한글 전용 자막

### A-1. 나눔스퀘어 폰트 준비

```bash
bash <skill_dir>/scripts/setup_font.sh /tmp/nanum-fonts
```

### A-2. ffmpeg burn-in

```bash
FONT_DIR="/tmp/nanum-fonts"
ffmpeg -y -i /tmp/bs_input.mp4 \
  -filter_complex \
    "[0:v]subtitles=/tmp/bs_ko.srt:\
force_style='FontName=NanumSquare,FontSize=14,\
PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,\
Outline=1,Shadow=1,Alignment=2,MarginV=25':\
fontsdir=${FONT_DIR}[v]" \
  -map "[v]" -map 0:1 \
  -c:v libx264 -preset fast -crf 18 \
  -c:a copy \
  /tmp/bs_output.mp4 \
  2>&1 | grep -E "Lsize=|Error|error" | tail -5
```

> **FontSize 기준 (한글 전용):**
> - FHD 1920×1080: 기본 14
> - HD 1280×720: 기본 11
> - 4K 3840×2160: 기본 22

### A-3. 저장 및 전달 → [STEP 3으로 이동]

---

## MODE B — 한영 병기 자막

### B-1. 영어 텍스트 확보

**영어 SRT가 함께 제공된 경우** → `/tmp/bs_en.srt`로 복사하고 B-2로 이동.

**영어 SRT가 없는 경우**, 다음 순서로 영어 텍스트를 확보한다.

1. 한글 SRT를 파싱해 entry 수·타임코드를 파악한다.
2. 파일명·영상 제목으로 곡명/콘텐츠를 식별한다.
3. WebSearch로 영어 원문 검색: `"<제목> lyrics"` 또는 `"<제목> transcript"`.
4. 검색 결과를 SRT entry 번호(1-based) → 영어 문장 dict로 매핑한다.

   ```python
   en_dict = {
       1: "When I am down and, oh, my soul so weary,",
       2: "When troubles come and my heart burdened be;",
       # ... (크레딧/빈 entry는 생략)
   }
   ```
   매핑 시: 한 entry가 여러 줄이면 해당 구간 전체를 커버하는 영어 1문장으로.  
   한 줄 50자 이내를 권장한다.

5. dict를 JSON으로 저장:
   ```python
   import json
   with open("/tmp/bs_en_dict.json", "w", encoding="utf-8") as f:
       json.dump(en_dict, f, ensure_ascii=False, indent=2)
   ```

### B-2. 한영 병기 SRT 생성

```bash
# 영어 SRT가 있을 때
python3 <skill_dir>/scripts/merge_subtitles.py \
  --ko /tmp/bs_ko.srt --en-srt /tmp/bs_en.srt \
  --out /tmp/bs_bilingual.srt

# 영어 dict를 만든 경우
python3 <skill_dir>/scripts/merge_subtitles.py \
  --ko /tmp/bs_ko.srt --en-dict /tmp/bs_en_dict.json \
  --out /tmp/bs_bilingual.srt
```

생성 후 처음 3~4 entry를 확인해 형식 검증: 한글 줄 아래 영어 줄이 있어야 한다.

### B-3. 나눔스퀘어 폰트 준비

```bash
bash <skill_dir>/scripts/setup_font.sh /tmp/nanum-fonts
```

### B-4. ffmpeg burn-in

```bash
FONT_DIR="/tmp/nanum-fonts"
ffmpeg -y -i /tmp/bs_input.mp4 \
  -filter_complex \
    "[0:v]subtitles=/tmp/bs_bilingual.srt:\
force_style='FontName=NanumSquare,FontSize=14,\
PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,\
Outline=1,Shadow=1,Alignment=2,MarginV=25':\
fontsdir=${FONT_DIR}[v]" \
  -map "[v]" -map 0:1 \
  -c:v libx264 -preset fast -crf 18 \
  -c:a copy \
  /tmp/bs_output.mp4 \
  2>&1 | grep -E "Lsize=|Error|error" | tail -5
```

> **FontSize 기준 (한영 병기 — 두 줄이므로 작게):**
> - FHD 1920×1080: 기본 14
> - HD 1280×720: 기본 11
> - 4K 3840×2160: 기본 22

---

## STEP 3 — 결과물 저장 및 전달

```bash
mkdir -p /sessions/.../mnt/outputs/
cp /tmp/bs_output.mp4 "/sessions/.../mnt/outputs/<제목>_자막.mp4"
```

`computer://` 링크로 파일을 전달하고, 다음 정보를 간략히 요약한다:

- 해상도, 재생시간, 파일 크기
- 사용 폰트 및 크기
- 자막 모드 (한글 전용 / 한영 병기)
- 자막 항목 수

---

## 오디오 스트림 확인

`-map 0:1`이 실패하면 먼저 스트림 인덱스를 확인한다:

```bash
ffprobe -v quiet -show_streams /tmp/bs_input.mp4 2>&1 | grep "codec_type=audio"
```

출력된 스트림 번호로 `-map 0:<N>` 수정.

---

## 오류 대응

| 오류 | 원인 | 해결 |
|------|------|------|
| `Glyph not found` | 폰트명 불일치 | `FontName=NanumSquare` 확인 |
| `-map 0:1` 실패 | 오디오 스트림 번호 다름 | ffprobe로 확인 후 수정 |
| SRT 경로 공백 오류 | 파일명 공백 | `/tmp/bs_ko.srt`로 복사 후 사용 |
| 폰트 다운로드 실패 | 네트워크 차단 | 사용자에게 NanumSquare.ttf 직접 요청 |
| 영어 가사 검색 실패 | 네트워크/저작권 | 사용자에게 영어 SRT 또는 가사 텍스트 요청 |

---

## 스크립트 경로

```
<skill_dir>/scripts/merge_subtitles.py   — 한영 병기 SRT 생성
<skill_dir>/scripts/setup_font.sh        — 나눔스퀘어 폰트 설치
```

`<skill_dir>`는 이 SKILL.md 파일이 위치한 디렉토리 경로다.
