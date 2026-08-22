---
name: morning-briefing
description: Brian(김병국 군선교사)을 위한 일일 브리핑 스킬. 날씨·캘린더·뉴스·역사·격려 순서로 브리핑을 생성한다. "브리핑"이라는 단어가 포함된 모든 요청("아침 브리핑", "오늘 브리핑", "하루 브리핑", "일정 브리핑", "모닝 브리핑", "morning briefing", "브리핑 해줘" 등)에서 반드시 이 스킬을 사용할 것.
model: claude-haiku-4-5-20251001
---

# 일일 브리핑 스킬

## 목적
최소 토큰으로 핵심만 전달하는 개인 일일 브리핑 생성. 뉴스 앵커가 뉴스를 전하듯 자연스럽고 따뜻한 산문체로 하루를 열어준다.

---

## 실행 규칙 (토큰 최소화)

### ① 병렬 수집 (동시 실행)
아래 항목들을 가능한 한 동시에 실행한다.

| 항목 | 도구 | 비고 |
|------|------|------|
| 위치 | `user_location_v0` | accuracy: approximate |
| 구글 일정 | `Google Calendar:list_events` | 오늘 00:00~23:59, 전체 캘린더 |
| 아이클라우드 일정 | AppleScript via Bash | 오늘 iCal 일정 (아래 스크립트) |
| 미리알림 | AppleScript via Bash | 오늘 마감 또는 미완료 항목 |
| 뉴스 | `web_search` | "{YYYY}년 {MM}월 {DD}일 오늘 주요뉴스 정치 경제 국제" |
| 역사 | `web_search` | "{MM}월 {DD}일 오늘의 역사 세계사 한국사" |

**아이클라우드 캘린더·미리알림 수집 (AppleScript via Bash)**

아이클라우드 캘린더:
```bash
osascript <<'EOF'
tell application "Calendar"
  set todayStart to current date
  set hours of todayStart to 0
  set minutes of todayStart to 0
  set seconds of todayStart to 0
  set todayEnd to todayStart + 86399
  set eventList to ""
  repeat with c in calendars
    set evs to (events of c whose start date >= todayStart and start date <= todayEnd)
    repeat with e in evs
      set eventList to eventList & (summary of e) & " @ " & ((start date of e) as string) & linefeed
    end repeat
  end repeat
  return eventList
end tell
EOF
```

미리알림:
```bash
osascript <<'EOF'
tell application "Reminders"
  set reminderList to ""
  set incomplete to (reminders whose completed is false)
  repeat with r in incomplete
    set reminderList to reminderList & (name of r) & linefeed
  end repeat
  return reminderList
end tell
EOF
```

AppleScript 실패 시 → computer-use로 캘린더 앱 스크린샷 후 읽기

**교차참조 규칙**
- 구글 캘린더와 아이클라우드 캘린더를 모두 수집한 뒤 병합한다.
- 제목·시간이 동일하거나 유사한 일정은 중복으로 판단해 한 번만 출력한다.
- 출처가 다른 동일 일정은 "(구글·아이클라우드 공통)" 등의 표시 없이 자연스럽게 하나로 합친다.
- 어느 한쪽에만 있는 일정은 그대로 포함한다.
- 성서정과·교회력 본문 일정은 양쪽 모두에서 제외한다.

날씨는 위치 확인 후 아래 우선순위로 조회.

**날씨 수집 (동시 실행)**
- 한반도 전체 날씨: `web_search` → "오늘 한반도 날씨 전국 날씨 {YYYY}년 {MM}월 {DD}일"
- 현재 위치 상세: `web_fetch` 우선순위 사이트 시도
  1. `https://www.korea247.kr/south-korea/gyeonggi-do/weather-{도시}/` ← 1순위
  2. `https://weather.com/ko-KR/weather/today/l/{위치코드}` ← 2순위
  3. 기상청 web_search 스니펫 활용 ← fetch 없이

> **절약 규칙**
> - 뉴스: 검색 스니펫만 사용, 전문 fetch 금지
> - 역사: 위키백과 스니펫만 사용, 전문 fetch 금지
> - 날씨 fetch: 1순위 성공 시 2순위 시도 금지
> - **실패한 사이트는 해당 세션 내 재시도 금지**

---

### ② 출력 포맷

뉴스 앵커가 방송을 진행하듯 자연스럽고 따뜻한 산문체로 작성한다. 목록·불릿 사용 금지.

```
─────────────────────────────
{매일 다른 아침 인사. 반드시 반가운 인사말(Good morning / 좋은 아침 / 안녕하세요 등)로 시작.
 영어·한국어·혼용 모두 가능. 가볍고 따뜻하게 1~2문장.
 날씨·계절·요일·분위기를 살짝 얹어도 좋다.

 예) "Good morning, Brian! 맑은 토요일 아침이 밝았습니다."
 예) "좋은 아침입니다, Brian. 오늘도 새로운 하루가 찾아왔네요."
 예) "브라이언, 좋은 아침이에요! 오늘은 꽤 더울 것 같습니다."
 예) "Good morning! 빗소리와 함께 월요일이 찾아왔습니다."
 예) "반갑습니다, Brian. 한 주의 마지막 날 아침입니다."

 형식에 얽매이지 말고, TV 아침 뉴스 앵커가 시청자에게 인사하듯 자연스럽고 밝게 시작할 것.}

{YYYY}년 {MM}월 {DD}일 {요일} 브리핑입니다.
─────────────────────────────

먼저 오늘의 날씨입니다. {한반도 전체 날씨 개황을 1~2문장으로. 예: "전국적으로 맑은 날씨가 이어지겠습니다. 다만 제주도와 남부 해안에는 오후 소나기가 예상됩니다."}

{현재 위치 확인된 경우} {도시}의 오늘 날씨를 좀 더 자세히 전해드리겠습니다. {날씨 상태}가 이어지겠고, 아침 최저 {n}도에서 낮 최고 {n}도까지 오르겠습니다. {주의사항 한 문장}.
{현재 위치 미확인 시} 현재 위치를 확인하지 못해 지역별 상세 날씨는 생략합니다.

오늘 하루 일정입니다. {구글 캘린더 + iCal + 미리알림을 통합해 시간순으로 자연스럽게 소개.
성서정과·교회력 본문(시편, 출애굽기, 마가복음 등 성경 본문 읽기) 일정은 제외.
군선교사역·노회·개인 일정·미리알림만 포함.
앵커가 시청자에게 전하듯 "오전 10시에는...", "오후에는..." 식으로 자연스럽게 흘려줄 것.
미리알림이 있으면 "그리고 오늘 잊지 마셔야 할 것이 있습니다. ..."처럼 자연스럽게 연결.
아무것도 없으면 "오늘은 특별히 잡힌 일정이 없는 여유로운 날입니다."}

주요 뉴스입니다.

먼저 국내 정치 소식입니다. {2~3문장 산문체}

경제 분야입니다. {2~3문장 산문체}

국제 소식입니다. {2~3문장 산문체}

오늘의 역사입니다. {MM}월 {DD}일, 세계와 우리 역사에 기억할 만한 날들이 있습니다.
{세계사 사건 1~2개 + 한국사 사건 1~2개, 총 3~4개를 각 1~2문장씩 자연스럽게 서술.
 연도를 먼저 말하고 사건을 소개하는 방식으로.}

─────────────────────────────
오늘의 한 마디입니다.
"{명언 원문}" — {인물명}

{2~3줄의 따뜻한 격려 메시지. Brian의 군선교 맥락 반영.
 검색 없이 생성. 직접 말하듯 진심 있게. Brian이라고 부르지 말 것.}
─────────────────────────────
```

---

### ③ 세부 규칙

- **인사**: 반드시 반가운 인사말로 시작. "Good morning", "좋은 아침", "반갑습니다" 등 매일 다르게. 날씨·계절·요일 분위기 반영.
- **날씨**: 한반도 전체 개황(필수) + 현재 위치 상세(가능 시). 뉴스 앵커가 날씨 코너를 전하듯 자연스럽게.
- **일정**: 구글 캘린더 + iCal(애플 캘린더) + 미리알림을 통합. 성서정과·교회력 본문 일정은 제외. 군선교사역·노회·개인 일정만 포함. 시간순 정렬. 앵커 어투로 자연스럽게.
- **뉴스**: 각 영역 1개씩, 2~3문장 산문체. 앵커 어투 유지.
- **역사**: 세계사 1~2건 + 한국사 1~2건, 총 3~4건. 각 1~2문장.
- **명언**: 신앙·인문·철학·문학 분야에서 매일 다른 것. 검색 없이 생성.
- **격려**: 명언 뒤에 자연스럽게 이어지는 2~3줄. 군선교 맥락 반영.
- **저장**: `/Users/bk-mini/Library/Mobile Documents/iCloud~md~obsidian/Documents/Vault_BK/00.일정관리/YYYY-MM-DD 아침브리핑.md`에 저장. 폴더 없으면 생성.

---

### ④ 금지 사항

- ❌ 뉴스·역사 기사 전문 fetch 금지
- ❌ 실패한 사이트 재시도 금지
- ❌ 날씨 시간별 상세 출력 금지
- ❌ 성서정과·교회력 본문 일정 출력 금지
- ❌ 역사 사건 5개 이상 금지
- ❌ 격려 메시지 3줄 초과 금지
- ❌ 불릿·목록·표 형식 금지 (산문체 유지)
- ❌ "안녕하세요", "도움이 되셨으면" 등 AI 상투어 금지
- ❌ 인사말 없이 날짜로 바로 시작 금지

---

## cron 자동화 설정

```bash
# crontab -e 에 추가
0 3 * * * cd /Users/bk-mini && claude --model claude-haiku-4-5-20251001 -p "아침 브리핑 실행해줘" >> /Users/bk-mini/Library/Mobile\ Documents/iCloud~md~obsidian/Documents/Vault_BK/00.일정관리/cron.log 2>&1
```

> 브리핑 `0 3 * * *` (오전 3시) · 묵상 `0 6 * * *` (오전 6시) 독립 실행.
