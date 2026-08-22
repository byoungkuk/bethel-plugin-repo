---
name: visual-chart
description: 클로드 자체 데이터 차트 생성 워크플로우 v2. 5가지 고정 차트 유형(세로 막대·가로 막대·선 그래프·도넛·영역 그래프)으로 수치 데이터를 시각화한다. Recharts 기반 React 아티팩트(인터랙션 지원)와 정적 SVG 두 가지 출력 모드 지원. 1200px 고정 폭, 흰 배경, Noto Sans KR, 컬러 키 7종(blue·green·purple·orange·teal·rose·slate) 중 선택, 컬러 2+1 규칙, 다계열은 주조색 opacity 파생(1.0/0.75/0.5/0.25), 데이터 포인트 최대 12개, 라벨 최대 15자, 천 단위 콤마 포맷, Y축 0 시작 강제(선 그래프 제외), Y축 단위 필수. Generator↔Evaluator 분리로 축 범위·라벨 겹침·컬러 일관성 자동 검증·수정. 강의 설문 결과, 블로그 방문자 추이, 채널별 콘텐츠 비중, 매출·수강생 추이 시각화에 사용한다. 트리거: 차트, 그래프, 막대그래프, 가로막대그래프, 선그래프, 꺾은선그래프, 도넛차트, 파이차트, 영역그래프, 누적그래프, 데이터 시각화, 수치 시각화, 통계 시각화, 차트 만들기, 그래프 만들기, 순위 차트, 추이 그래프, 비율 차트, 비교 차트, 설문 결과 시각화, 방문자 추이, 매출 추이, 블로그 통계 시각화. 개념도는 visual-diagram, 카드·타임라인은 visual-infographic, 비교표는 visual-table, 나노바나나 이미지는 lecture-infographic-image를 사용한다.
---

# visual-chart v2

## 컬러 키 7종 + 다계열 파생
| 키 | --primary | --accent | --grid | --text |
|---|---|---|---|---|
| blue | #2563EB | #F59E0B | #E5E5E5 | #333333 |
| green | #059669 | #DC2626 | 〃 | 〃 |
| purple | #7C3AED | #F59E0B | 〃 | 〃 |
| orange | #EA580C | #2563EB | 〃 | 〃 |
| teal | #0D9488 | #DC2626 | 〃 | 〃 |
| rose | #E11D48 | #2563EB | 〃 | 〃 |
| slate | #475569 | #EA580C | 〃 | 〃 |

**다계열 파생색 규칙 (최대 4계열)**
- 계열1: `--primary` (opacity 1.0)
- 계열2: `--primary` opacity 0.75
- 계열3: `--primary` opacity 0.5
- 계열4: `--accent` (강조 계열)

## 차트 유형 5종
| 유형 | 데이터 최소~최대 | 주의 |
|---|---|---|
| 세로 막대 | 3~10 | 10 초과 시 가로 막대로 전환 |
| 가로 막대 | 3~12 | 긴 라벨·순위에 유리 |
| 선 그래프 | 5~24 | Y축 0 강제 예외 (실제 범위 사용 가능) |
| 도넛 | 2~6 | 6 초과 시 "기타" 그룹화, 외부 라인 라벨 |
| 영역 | 5~24 | 2~3계열 권장 |

## 출력 모드
- **A. React 아티팩트** (기본): Recharts 기반, 인터랙션·툴팁 지원
- **B. 정적 SVG**: 블로그·책·슬라이드 삽입용

신호어: "SVG로", "정적으로", "블로그용", "스크린샷용", "Obsidian 삽입" → 모드 B

## 5단계 워크플로우

### Phase 1. 입력 정리
유형 / 데이터 / 제목·부제 / Y축 단위 / 컬러 키 / 출력 모드

### Phase 2. 데이터 검증
- [ ] 포인트 ≤ 12
- [ ] 라벨 ≤ 15자
- [ ] 단위 통일
- [ ] 결측·음수 처리

### Phase 3. Generator

**모드 A 기본 스켈레톤 (세로 막대)**
```jsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LabelList } from 'recharts';

const COLORS = { primary:'#EA580C', accent:'#2563EB', text:'#333', grid:'#E5E5E5' };
const fmt = (v) => v.toLocaleString();

export default function Chart() {
  const data = [{name:'항목A', value:120}, {name:'항목B', value:85}];
  return (
    <div style={{width:1200, background:'#FFFFFF', padding:'64px 48px', fontFamily:'Noto Sans KR, sans-serif'}}>
      <h1 style={{fontSize:36, fontWeight:900, color:COLORS.primary, margin:0}}>제목</h1>
      <p style={{fontSize:16, color:COLORS.text, margin:'8px 0 32px'}}>부제</p>
      <div style={{width:'100%', height:480}}>
        <ResponsiveContainer>
          <BarChart data={data} margin={{top:30, right:40, bottom:40, left:40}}>
            <CartesianGrid stroke={COLORS.grid} strokeDasharray="3 3" vertical={false}/>
            <XAxis dataKey="name" tick={{fill:COLORS.text, fontSize:14}} axisLine={{stroke:COLORS.grid}}/>
            <YAxis tick={{fill:COLORS.text, fontSize:14}} tickFormatter={fmt} axisLine={{stroke:COLORS.grid}} unit=" 명"/>
            <Tooltip formatter={fmt}/>
            <Bar dataKey="value" fill={COLORS.primary} radius={[8,8,0,0]}>
              <LabelList dataKey="value" position="top" formatter={fmt} style={{fill:COLORS.text, fontSize:13, fontWeight:700}}/>
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
```

**모드 B 정적 SVG 축 계산 공식**
- 캔버스: 1200×675, 플롯 영역 x=120~1120 (폭 1000), y=160~580 (높이 420)
- Y축 스케일: `yPixel = 580 - (value / maxValue) * 420`
- 막대 폭: `barWidth = (1000 / dataCount) * 0.6`, gap = 0.4
- X축 중심: `xCenter = 120 + (1000 / dataCount) * (i + 0.5)`
- Y축 눈금: 0 / 1/4 / 1/2 / 3/4 / max (5단계)
- 데이터 레이블: 막대 상단 y-8 위치, font 13/700

**도넛 라벨 규칙**
- 외부 라인 라벨 (곡선 → 직선 → 텍스트)
- 텍스트 앵커: 우측(x>center) `start`, 좌측 `end`
- 슬라이스 <5% 시 "기타" 그룹화

### Phase 4. Evaluator 자동 수정
| 문제 | 조치 |
|---|---|
| 포인트 >12 | 상위 10 + 기타 |
| 라벨 겹침 | 15자 말줄임 또는 45도 회전 |
| Y축 0 아님 | 막대·영역·도넛 강제 0 (선 그래프만 예외) |
| 단위 누락 | 제목·Y축에 단위 주입 |
| 콤마 누락 | tickFormatter·LabelList에 toLocaleString 주입 |
| 다계열 >4 | 계열1~3 + 기타 합산 |
| 도넛 라벨 겹침 | 외부 라인 라벨로 전환 |
| 컬러 규칙 위반 | 주조색·opacity 파생·보조색 외 제거 |

### Phase 5. 출력
- 모드 A: .jsx + 아티팩트 렌더
- 모드 B: .svg + 코드 블록

## Harness 규칙
1. Generator↔Evaluator 분리
2. 유형 5종 외 금지
3. 포인트 ≤12, 라벨 ≤15자
4. Y축 0 강제(선 그래프 예외), 단위 필수
5. 천 단위 콤마 통일
6. 다계열은 주조색 opacity 파생 + 보조색
7. 그라데이션·그림자·3D·이모지·@media 금지
