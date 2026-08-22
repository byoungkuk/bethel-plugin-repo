---
name: visual-table
description: 클로드 자체 구조화 비교표 생성 워크플로우 v2. 4가지 고정 표 유형(단순 비교표·체크리스트 매트릭스·2×2 우선순위 매트릭스·단계별 체크포인트 표)으로 텍스트 밀도 높은 비교·분류·체크리스트를 HTML+CSS 아티팩트로 생성한다. 마크다운 표보다 디자인 완성도 높고 카드 인포그래픽보다 텍스트 밀도 높다. 1200px 고정, 흰 배경, Noto Sans KR, 컬러 키 7종 공유, 행 기본 ≤10(컴팩트 모드 11~15행), 열 ≤6, 셀 ≤40자, 헤더 ≤15자, 강조 셀 최대 2개. ✓/✗/△는 이모지 금지, CSS 원형 span으로 처리. 2×2 매트릭스는 grid 4분면 + X/Y축 라벨 + 사분면 투명도 차등. 트리거: 비교표, 비교 표, 기능 비교, 기능 매트릭스, 체크리스트 매트릭스, 2x2 매트릭스, 우선순위 매트릭스, 중요도 매트릭스, 도구 비교표, 플랜 비교표, 요금제 비교, 스킬 비교표, 단계별 체크포인트, 체크리스트 표, 구조화 표, HTML 표, 매거진 표. 개념도는 visual-diagram, 카드·타임라인은 visual-infographic, 수치 차트는 visual-chart를 사용한다.
---

# visual-table v2

## 컬러 키 7종 공유
blue/green/purple/orange/teal/rose/slate (HEX는 visual-chart SKILL.md 참조)  
추가: `--even: #F9FAFB` (짝수 행), `--check-no: #CBD5E1` (미지원 회색)

## 표 유형 4종

| 유형 | 구조 | 행·열 |
|---|---|---|
| A. 단순 비교표 | 세로 항목 × 가로 속성 | ≤10 × ≤6 |
| B. 체크리스트 매트릭스 | ✓/✗/△ 원형 셀 | ≤10 × ≤6 |
| C. 2×2 우선순위 매트릭스 | grid 4분면 | 사분면당 ≤4항목 |
| D. 단계별 체크포인트 표 | 단계(25%) + 항목(75%) | 단계 ≤8 |

## 공통 CSS 베이스
```css
:root{--primary:#7C3AED;--accent:#F59E0B;--text:#333;--line:#E5E5E5;--bg:#FFFFFF;--even:#F9FAFB;--check-no:#CBD5E1}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);font-family:'Noto Sans KR',sans-serif;color:var(--text);word-break:keep-all}
.container{width:1200px;margin:0 auto;padding:64px 48px}
h1{font-size:42px;font-weight:900;color:var(--primary);margin:0 0 12px}
h2{font-size:18px;font-weight:400;margin:0 0 40px}
```

## 유형별 규격

### A. 단순 비교표
```css
table{width:100%;border-collapse:collapse;font-size:15px}
thead th{background:var(--primary);color:#FFF;padding:18px;text-align:left;font-weight:700;font-size:16px}
thead th:first-child{border-top-left-radius:10px}
thead th:last-child{border-top-right-radius:10px}
tbody td{padding:16px 18px;border-bottom:1px solid var(--line);line-height:1.6}
tbody tr:nth-child(even){background:var(--even)}
tbody td:first-child{font-weight:700;color:var(--primary)}
.highlight{background:rgba(245,158,11,0.15);color:var(--accent);font-weight:700}
/* 컴팩트 모드 (행 11~15) */
.compact tbody td{padding:12px 16px;font-size:13px}
```
강조 셀 최대 2개.

### B. 체크리스트 ✓/✗/△
```css
.check{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;font-size:14px;font-weight:700}
.check-yes{background:var(--primary);color:#FFF}
.check-no{background:var(--check-no);color:#FFF}
.check-partial{background:var(--accent);color:#FFF}
```
HTML: `<span class="check check-yes">✓</span>` (문자는 ✓/✗/△, 이모지 아님)

### C. 2×2 매트릭스
```css
.matrix{display:grid;grid-template-columns:80px 1fr 1fr;grid-template-rows:40px 1fr 1fr;gap:12px;height:720px}
.y-label{grid-column:1;grid-row:2/4;writing-mode:vertical-rl;transform:rotate(180deg);text-align:center;font-weight:700;color:var(--primary);display:flex;align-items:center;justify-content:center}
.x-label{grid-column:2/4;grid-row:1;text-align:center;font-weight:700;color:var(--primary)}
.quad{padding:28px;border-radius:14px;border:1px solid var(--line)}
.q1{background:rgba(124,58,237,0.15)} /* 중요·긴급 진함 */
.q2{background:rgba(124,58,237,0.10)}
.q3{background:rgba(124,58,237,0.06)}
.q4{background:rgba(124,58,237,0.03)} /* 비중요·비긴급 연함 */
.quad h3{font-size:18px;font-weight:700;color:var(--primary);margin:0 0 14px}
.quad ul{margin:0;padding-left:18px;font-size:14px;line-height:1.7}
```
사분면당 항목 ≤4.

### D. 단계별 체크포인트
```css
.step-table{display:grid;grid-template-columns:25% 75%;gap:0;border-top:2px solid var(--primary)}
.step-name{padding:24px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:16px}
.step-num{width:44px;height:44px;border-radius:50%;background:var(--primary);color:#FFF;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;flex-shrink:0}
.step-name h3{font-size:17px;font-weight:700;color:var(--primary);margin:0}
.step-items{padding:24px;border-bottom:1px solid var(--line);background:var(--even)}
.step-items ul{margin:0;padding-left:20px;font-size:14px;line-height:1.8}
```

## Evaluator 자동 수정
| 문제 | 조치 |
|---|---|
| 행 >10 | 11~15면 compact 모드, 16+ 분할 권장 |
| 열 >6 | 덜 중요한 열 제거 제안 |
| 셀 >40자 | 줄바꿈 또는 말줄임 |
| 헤더 >15자 | 말줄임 |
| 강조 >2 | 상위 2개만 유지 |
| 2×2 사분면 항목 >4 | 상위 4 + 기타 |
| 이모지 검출 | CSS span으로 교체 |
| @media 검출 | 제거 |

## Harness 규칙
1. Generator↔Evaluator 분리
2. 유형 4종 외 금지
3. 행 ≤10(compact ≤15), 열 ≤6, 셀 ≤40자, 헤더 ≤15자
4. 강조 셀 ≤2
5. ✓/✗/△는 CSS span
6. 1200px 고정, @media 금지
