---
name: bible-study-worksheet
description: "벧엘교회(1사단 58포병대대) 주일 성경공부 교안(학습자용 + 교사용 PDF 쌍)을 생성하는 스킬. 사용자가 \"교안 작성해줘\", \"성경공부 자료 만들어줘\", \"학습자용/교사용 교안\", \"이번 주 성경공부\", \"성서정과 교안\", \"BS 파일 만들어줘\" 등을 언급할 때 반드시 이 스킬을 사용할 것. 성경 본문(성서정과 복음서)이 제공되면 즉시 이 스킬을 적용하여 PDF 2종을 생성한다."
---

# 벧엘교회 성경공부 교안 생성 스킬

## 1. 개요
성서정과 복음서 본문을 바탕으로 매주 성경공부 교안 PDF 2종을 생성한다.
- 학습자용: A4 1페이지 완전 충전, 최소 잉크 인쇄
- 교사용: A4 2페이지, 텍스트 중심 심플 레이아웃

---

## 2. 반드시 지켜야 할 규칙

| 항목 | 규칙 |
|------|------|
| 교안 날짜 | 성서정과 날짜 -1주 (성경공부는 성서정과 한 주 전 주일에 실시) |
| 학습자용 | A4 1페이지: 2열 성경비교(개역개정/새한글) + 귀납적 질문 + 답변 여백 |
| 교사용 | A4 2페이지: 성경번역 비교표 없음 / 텍스트 위주 역사배경 + 질문해설 |
| 폰트 | 서버: NanumBarunGothic / 요청 폰트: Apple SD 산돌고딕 Neo |
| 파일명 | BS{YYYYMMDD}_{성경약어}{장}_{절기}_{학습자용|교사용}.pdf |

---

## 3. 색상 팔레트 (초저잉크 프린트 기준)

HEADER_BG = #EFF3FA  (헤더/섹션바 - 매우 연한 파랑회색)
SEC_BAR   = #F2F5FB  (섹션 바 - 더 옅게)
MEMO_BG   = #FDFAF0  (교사 메모 박스)
BORDER    = #BBCCDD  (테두리)
MEMO_BDR  = #CCAA44  (메모 박스 테두리)
TEXT_MAIN = #111111  (본문 텍스트)
TEXT_DARK = #1C2B4A  (제목/강조)

잉크 절약 3원칙:
1. 헤더/섹션 바: 연배경 + 진한 글자. 흰 글자+짙은 배경 절대 금지
2. 성경 본문 비교표: 헤더 행만 HEADER_BG, 본문 행은 배경색 없음(순백)
3. 교사 메모 박스: 아주 연한 황색 + 황금색 테두리만

---

## 4. 학습자용 레이아웃

### 4-1. 헤더 1행
[ 벧 엘 교 회  성경공부 ]   [ YYYY. M. D.  |  성경책 장:절  (절기명) ]
배경: HEADER_BG, 텍스트: TEXT_DARK 볼드

### 4-2. 성경 본문 비교표
- 열: [절번호 | 개역개정판 | 새한글성경]
- 헤더 행 배경: HEADER_BG
- 본문 행: 배경 없음(순백) — 교대 음영 사용 안 함
- 전 절 수록, 폰트 7~7.5pt

### 4-3. 말씀 나눔 질문 (4개, 단문만)
1. 본문이해 - 모르는 단어/개념
2. 관찰 - 본문에서 직접 답 찾기
3. 해석 - 핵심 개념 의미 도출
4. 적용 - 개인 고백/삶 연결

### 4-3-1 학습자용 본문표 규칙: 성경 본문이 불연속으로 제시되면(예: 31–33절, 44–52절), 건너뛴 경계 지점에 높이 약 2.6mm의 빈 행(3열 병합·흰 배경)을 넣어 구간을 구분한다.

### 4-3-2 학습자용 질문 규칙: 각 질문은 항목명(Q1. 본문이해/관찰/해석/적용)을 굵은 글씨 한 줄로 두고, 실제 질문 문장은 줄바꿈하여 그 아랫줄에 배치해 항목명과 질문이 확실히 구분되게 한다.

### 4-4. A4 1페이지 완전 충전 알고리즘 (필수 구현)

반드시 2-패스(two-pass) 방식으로 구현한다.

```python
class MeasureDoc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if hasattr(self, 'frame') and self.frame:
            self._last_y = self.frame._y

def build_student_pdf(...):
    # 1차 패스: 최소 여백으로 콘텐츠 높이 측정
    story_probe = build_story(q_gap=8*mm, apply_pad_bottom=8*mm)
    buf = BytesIO()
    doc_probe = MeasureDoc(buf, pagesize=A4,
                           leftMargin=LM, rightMargin=RM,
                           topMargin=TM, bottomMargin=BM)
    doc_probe._last_y = BM
    doc_probe.build(story_probe)

    # 남은 공간 계산 및 분배
    remaining = doc_probe._last_y - BM

    # 30%는 질문 간격, 70%는 고백 박스 하단에 분배
    extra_per_q  = max(0, remaining * 0.30 / len(questions))
    extra_apply  = max(0, remaining * 0.70)
    final_q_gap     = 8*mm + extra_per_q
    final_apply_bot = 8*mm + extra_apply

    # 2차 패스: 최종 PDF 생성
    story_final = build_story(q_gap=final_q_gap,
                              apply_pad_bottom=final_apply_bot)
    doc_final = SimpleDocTemplate(output_path, pagesize=A4, ...)
    doc_final.build(story_final)
```

### 4-5. 푸터
한 주간 이 말씀을 묵상하며 하나님의 음성에 귀 기울이시기 바랍니다. 건강한 한 주간 보내세요.

---

## 5. 교사용 레이아웃

### 5-1. 구성 (2페이지, 번역 비교표 없음)
1페이지: 헤더 / 역사적 배경(bullet) / Q1 해설+메모 / Q2 해설+메모
2페이지: 헤더(반복) / Q3 해설+메모 / Q4 해설+메모 / 적용질문지침 / 푸터

### 5-2. 섹션 바
배경: SEC_BAR (#F2F5FB), 텍스트: TEXT_DARK 볼드

### 5-3. 교사 메모 박스
배경: MEMO_BG, 테두리: MEMO_BDR 0.6pt, 레이블: ✎  교사 적용

### 5-4. 역사적 배경 필수 항목
- 시대적 배경 (연도, 정치·종교 상황)
- 핵심 어휘 원어(헬라어/히브리어) 설명
- 인용 구약 예언 / 전후 문맥
- 등장인물의 기대·오해·반응 포인트

---

## 6. 성경 비교표 코드 패턴 (본문 행 배경 없음)

```python
def make_bible_table(verses, W):
    col_w = [7*mm, (W-7*mm)*0.50, (W-7*mm)*0.50]
    sT = S('t','NG',7,leading=10.5)
    data = [[헤더행]]
    for num, rev, new in verses:
        data.append([절번호, 개역개정, 새한글])

    rstyles = [
        ('BACKGROUND', (0,0),(-1,0), HEADER_BG),  # 헤더 행만 배경
        # 본문 행 BACKGROUND 없음 (순백)
        ('GRID', (0,0),(-1,-1), 0.3, BORDER),
        ('VALIGN', (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 2),
        ('BOTTOMPADDING', (0,0),(-1,-1), 2),
        ('LEFTPADDING',   (0,0),(-1,-1), 2.5),
        ('RIGHTPADDING',  (0,0),(-1,-1), 2.5),
        ('ALIGN', (0,0),(0,-1), 'CENTER'),
    ]
    tbl = Table(data, colWidths=col_w)
    tbl.setStyle(TableStyle(rstyles))
    return tbl
```

---

## 7. 파일명 규칙
BS{YYYYMMDD}_{성경약어}{장}_{절기약어}_{학습자용|교사용}.pdf
성서정과 날짜에서 7일을 빼서 교안 날짜를 계산한다.

---

## 8. 작업 순서 체크리스트
- [ ] 1. 성서정과 날짜, 절기, 복음서 범위 확인
- [ ] 2. 교안 날짜 = 성서정과 날짜 − 7일
- [ ] 3. 개역개정 / 새한글 전 절 텍스트 준비
- [ ] 4. 귀납적 질문 4개 설계 (본문이해→관찰→해석→적용)
- [ ] 5. 역사적 배경 / 질문별 해설 / 교사 적용 포인트 작성
- [ ] 6. 학습자용: 2-패스 알고리즘으로 A4 완전 충전 PDF 생성
- [ ] 7. 교사용: 2페이지 텍스트 심플 PDF 생성
- [ ] 8. /mnt/user-data/outputs/ 복사 후 present_files 호출

---

## 9. 품질 체크

| 항목 | 기준 |
|------|------|
| 학습자용 분량 | A4 정확히 1페이지 (2-패스로 자동 충전) |
| 교사용 분량 | A4 2페이지 (PageBreak 정확 분리) |
| 성경 본문 행 | 배경색 없음(순백) 확인 |
| 헤더/섹션 배경 | #EFF3FA / #F2F5FB 이하 확인 |
| 날짜 | 성서정과 날짜 −1주 확인 |
| 질문 형식 | 단문, 설명 없이 질문만 |
| 고백 박스 | 페이지 하단까지 여백 충분히 확보 |