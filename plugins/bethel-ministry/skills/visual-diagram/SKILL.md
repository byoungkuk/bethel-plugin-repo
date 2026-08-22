---
name: visual-diagram
description: 클로드 자체 SVG 다이어그램 생성 워크플로우 v2. 6가지 고정 레이아웃(수평 플로우·수직 파이프라인·중앙 방사형·2×N 매트릭스·타임라인·계층 트리)으로 개념도·플로우차트·구조도·관계도·파이프라인·마인드맵을 SVG 코드로 생성한다. 1200×675 캔버스, 흰 배경, Noto Sans KR, 컬러 키 7종 중 선택, 컬러 2+1 규칙, 노드 최대 8개, 노드당 최대 20자 가드레일. 각 레이아웃별 3·4·5노드 좌표 프리셋 포함. Generator↔Evaluator 분리로 텍스트 겹침·여백·화살표 방향·컬러 대비 자동 검증·수정. 결과물은 SVG 코드와 .svg 파일로 출력. 트리거: 개념도, 플로우차트, 구조도, 관계도, 파이프라인 도식, 마인드맵, 워크플로우 도식, SVG 다이어그램, SVG 시각화, 다이어그램 만들기, 도식화, 개념 시각화, 프로세스 도식, 계층 구조도, 타임라인 도식, 비교 도식, 매트릭스 도식, 방사형 도식, 허브 도식, 흐름도. 매거진급 HTML 인포그래픽은 visual-infographic, 나노바나나 이미지 프롬프트는 lecture-infographic-image, 블로그 썸네일은 image-thumbnail, 책 삽화는 book-illustration을 사용한다.
---

# visual-diagram v2

## 컬러 키 7종 (HEX 고정)
| 키 | 주조색 | 보조색 | 공통 |
|---|---|---|---|
| blue | #2563EB | #F59E0B | text #333 / line #E5E5E5 / bg #FFFFFF |
| green | #059669 | #DC2626 | 〃 |
| purple | #7C3AED | #F59E0B | 〃 |
| orange | #EA580C | #2563EB | 〃 |
| teal | #0D9488 | #DC2626 | 〃 |
| rose | #E11D48 | #2563EB | 〃 |
| slate | #475569 | #EA580C | 〃 |

## 5단계 워크플로우

### Phase 1. 입력 정리
1. 유형 (개념도/플로우/구조/관계/파이프라인/마인드맵)
2. 노드 리스트 (최대 8개, 각 ≤20자)
3. 관계 방식 (순서·포함·대비·순환)
4. 컬러 키 (7종 중 1개)

### Phase 2. 레이아웃 선택 (6종 × 노드 수 프리셋)
| 레이아웃 | 노드 수별 템플릿 |
|---|---|
| 수평 플로우 | horizontal-flow-3/4/5.svg |
| 수직 파이프라인 | vertical-pipeline-3/4/5.svg |
| 중앙 방사형 | radial-4/6/8.svg |
| 2×N 매트릭스 | matrix-4/6/8.svg |
| 타임라인 | timeline-4/5/6.svg |
| 계층 트리 | hierarchy-3level.svg |

### Phase 3. SVG Generator
- viewBox `0 0 1200 675`, 배경 `#FFFFFF`
- 폰트 `Noto Sans KR, sans-serif`
- 노드 220×100, rx=12, 여백 40px 이상
- 연결선 stroke-width=2, marker arrow
- 제목 18px/700, 본문 14px/400
- 주조색·보조색·회색 외 금지

### Phase 4. Evaluator 자동 수정 규칙
| 문제 | 자동 조치 |
|---|---|
| 텍스트 >20자 | 2줄 분할 또는 노드 폭 +40px |
| 노드 겹침 | gap 40px 확보까지 재배치 |
| 화살표 방향 불일치 | 가장 많은 방향으로 통일 |
| 금지 컬러 검출 | 주조색으로 교체 |
| font-family 누락 | 루트에 주입 |

### Phase 5. 출력
1. SVG 코드 블록 (```svg```)
2. .svg 파일 저장·다운로드
3. 수정 요청 시 Phase 3 재실행

## Harness 규칙
1. Generator↔Evaluator 분리
2. 레이아웃 6종 외 금지
3. 노드 ≤8, 텍스트 ≤20자
4. 컬러 2+1 규칙
5. 그라데이션·그림자·3D·@media 금지
