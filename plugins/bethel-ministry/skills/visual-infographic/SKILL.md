---
name: visual-infographic
description: 클로드 자체 HTML+CSS 인포그래픽 생성 워크플로우 v2. 5가지 고정 레이아웃(중앙 타이틀·2분할 비교·카드 6단·타임라인·방사형)으로 매거진급 정적 인포그래픽을 HTML 아티팩트로 생성한다. 1200px 고정 폭, 흰 배경, Google Fonts Noto Sans KR, 컬러 키 7종을 CSS 변수로 정의해 --primary 교체만으로 컬러 전환. 카드 6단은 2×3 그리드 + 일러스트 배경 원. 매거진 헤더·영문 부제·장식 라인·그라데이션·그림자·이모지·@media 반응형 금지. Generator↔Evaluator 분리로 자동 수정. 트리거: HTML 인포그래픽, 웹 인포그래픽, 카드 인포그래픽, 비교 인포그래픽, 타임라인 인포그래픽, 방사형 인포그래픽, 매거진 인포그래픽, 인포그래픽 HTML, 정적 인포그래픽, 6단 카드, 카드 레이아웃, 2분할 비교, 인포그래픽 페이지, 시각 정리, 요약 인포그래픽. SVG 개념 도식은 visual-diagram, 나노바나나 이미지 프롬프트는 lecture-infographic-image, 블로그 썸네일은 image-thumbnail, 책 삽화는 book-illustration을 사용한다.
---

# visual-infographic v2

## 컬러 키 7종 (CSS 변수)
```css
/* blue */   :root{--primary:#2563EB;--accent:#F59E0B;--text:#333;--line:#E5E5E5;--bg:#FFFFFF}
/* green */  :root{--primary:#059669;--accent:#DC2626; ...}
/* purple */ :root{--primary:#7C3AED;--accent:#F59E0B; ...}
/* orange */ :root{--primary:#EA580C;--accent:#2563EB; ...}
/* teal */   :root{--primary:#0D9488;--accent:#DC2626; ...}
/* rose */   :root{--primary:#E11D48;--accent:#2563EB; ...}
/* slate */  :root{--primary:#475569;--accent:#EA580C; ...}
```
컬러 전환은 `--primary`·`--accent` 값만 교체.

## 5단계 워크플로우

### Phase 1. 입력 정리
1. 메인 타이틀 1줄
2. 핵심 메시지 3~6개 (제목 ≤20자, 본문 ≤60자)
3. 레이아웃 5종 중 1개
4. 컬러 키 7종 중 1개

### Phase 2. 레이아웃 (5종)
| 레이아웃 | 슬롯 | 템플릿 |
|---|---|---|
| 중앙 타이틀 | 1+3 | center-title.html |
| 2분할 비교 | 2×3 | compare-2col.html |
| 카드 6단 | 6 | cards-6.html |
| 타임라인 | 5~7 | timeline.html |
| 방사형 | 1+4~6 | radial.html |

### Phase 3. HTML Generator
- 컨테이너 `width:1200px` 고정 (`@media` 금지)
- Google Fonts Noto Sans KR 400/700/900 임포트
- 타이포: 메인 48/900, 서브 24/700, 카드 제목 20/700, 본문 16/400, line-height 1.6
- 카드: padding 32px, border-radius 16px, gap 24px
- 일러스트 배경 원: SVG `<circle>`, opacity 0.15, 카드 우상단 배치

### Phase 4. Evaluator 자동 수정
| 문제 | 조치 |
|---|---|
| 제목 >20자 | 말줄임 또는 2줄 분할 |
| 본문 >60자 | 2줄 분할, 초과분 다음 슬롯 |
| 금지 요소 검출 | 제거 (매거진 헤더·영문 부제·장식 라인·이모지·그라데이션·그림자·@media) |
| 컬러 규칙 위반 | --primary/--accent로 강제 교체 |
| Noto Sans KR 누락 | head에 링크 주입 |

### Phase 5. 출력
1. 단일 .html (인라인 CSS)
2. 아티팩트 렌더 → 스크린샷 1200×n 캡처

## Harness 규칙
1. Generator↔Evaluator 분리
2. 레이아웃 5종 외 금지
3. 슬롯당 제목 ≤20자·본문 ≤60자
4. 컬러 2+1 규칙 (CSS 변수 3개만 사용)
5. 금지 요소 엄수
6. 1200px 고정, 반응형 금지
