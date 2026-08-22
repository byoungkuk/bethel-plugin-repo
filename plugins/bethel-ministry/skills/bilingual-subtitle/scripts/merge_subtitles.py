#!/usr/bin/env python3
"""
merge_subtitles.py
------------------
두 가지 모드로 한영 병기 SRT를 생성한다.

모드 1 (--ko + --en-dict):
  한글 SRT + 영어 문장 목록(JSON)을 받아 한영 병기 SRT 생성
  영어 목록은 SRT entry 번호(1-based) → 영어 문자열 매핑 dict

모드 2 (--ko + --en-srt):
  한글 SRT + 영어 SRT 두 파일을 타임코드 기준으로 정렬·병합

사용법:
  python3 merge_subtitles.py --ko ko.srt --en-dict en.json --out bilingual.srt
  python3 merge_subtitles.py --ko ko.srt --en-srt en.srt  --out bilingual.srt
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from typing import Optional


# ─── SRT 파싱 ────────────────────────────────────────────────────────────────

@dataclass
class Entry:
    idx: int
    start: str
    end: str
    lines: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(self.lines).strip()

    def start_ms(self) -> int:
        return _ts_to_ms(self.start)

    def end_ms(self) -> int:
        return _ts_to_ms(self.end)


def _ts_to_ms(ts: str) -> int:
    """'HH:MM:SS,mmm' → milliseconds"""
    ts = ts.replace(",", ".")
    h, m, rest = ts.split(":")
    s, ms = rest.split(".")
    return int(h) * 3_600_000 + int(m) * 60_000 + int(s) * 1_000 + int(ms)


def parse_srt(path: str) -> list[Entry]:
    with open(path, encoding="utf-8-sig") as f:
        raw = f.read()
    blocks = re.split(r"\n\n+", raw.strip())
    entries = []
    for block in blocks:
        lines = block.strip().splitlines()
        if len(lines) < 2:
            continue
        try:
            idx = int(lines[0].strip())
        except ValueError:
            continue
        m = re.match(r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})", lines[1])
        if not m:
            continue
        start, end = m.group(1).replace(".", ","), m.group(2).replace(".", ",")
        entries.append(Entry(idx=idx, start=start, end=end, lines=lines[2:]))
    return entries


def write_srt(entries: list[Entry], path: str):
    parts = []
    for i, e in enumerate(entries, 1):
        if e.text:
            parts.append(f"{i}\n{e.start} --> {e.end}\n{e.text}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(parts) + "\n")
    print(f"✅ 저장 완료: {path}  ({len(parts)}개 항목)")


# ─── 모드 1: dict 병합 ────────────────────────────────────────────────────────

def merge_with_dict(ko_entries: list[Entry], en_dict: dict[int, str]) -> list[Entry]:
    result = []
    for e in ko_entries:
        ko_text = e.text
        en_text = en_dict.get(e.idx, "")
        combined = f"{ko_text}\n{en_text}" if en_text else ko_text
        result.append(Entry(idx=e.idx, start=e.start, end=e.end, lines=combined.splitlines()))
    return result


# ─── 모드 2: SRT 두 파일 병합 (타임코드 정렬) ────────────────────────────────

def _overlap_ms(a_start, a_end, b_start, b_end) -> int:
    return max(0, min(a_end, b_end) - max(a_start, b_start))


def merge_two_srts(ko_entries: list[Entry], en_entries: list[Entry]) -> list[Entry]:
    """
    한글 SRT의 각 entry에 가장 많이 겹치는 영어 entry를 찾아 병기한다.
    완전 일치가 없으면 시작시간 기준 가장 가까운 항목을 사용한다.
    """
    result = []
    for ko in ko_entries:
        ks, ke = ko.start_ms(), ko.end_ms()
        # 최대 겹침 찾기
        best_en: Optional[Entry] = None
        best_overlap = -1
        for en in en_entries:
            es, ee = en.start_ms(), en.end_ms()
            ov = _overlap_ms(ks, ke, es, ee)
            if ov > best_overlap:
                best_overlap = ov
                best_en = en
        # 겹침 없으면 시작시간 가장 가까운 항목
        if best_overlap == 0 and en_entries:
            best_en = min(en_entries, key=lambda e: abs(e.start_ms() - ks))

        ko_text = ko.text
        en_text = best_en.text if best_en else ""
        combined = f"{ko_text}\n{en_text}" if en_text else ko_text
        result.append(Entry(idx=ko.idx, start=ko.start, end=ko.end, lines=combined.splitlines()))
    return result


# ─── 메인 ────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="한영 병기 SRT 생성기")
    ap.add_argument("--ko",      required=True, help="한글 SRT 파일 경로")
    ap.add_argument("--en-dict", help="영어 매핑 JSON (dict: {entry_idx: english_text})")
    ap.add_argument("--en-srt",  help="영어 SRT 파일 경로")
    ap.add_argument("--out",     required=True, help="출력 SRT 파일 경로")
    args = ap.parse_args()

    ko = parse_srt(args.ko)
    print(f"한글 SRT 로드: {len(ko)}개 항목")

    if args.en_dict:
        with open(args.en_dict, encoding="utf-8") as f:
            raw = json.load(f)
        en_dict = {int(k): v for k, v in raw.items()}
        result = merge_with_dict(ko, en_dict)
        print(f"영어 dict 매핑: {len(en_dict)}개")
    elif args.en_srt:
        en = parse_srt(args.en_srt)
        print(f"영어 SRT 로드: {len(en)}개 항목")
        result = merge_two_srts(ko, en)
    else:
        print("❌ --en-dict 또는 --en-srt 중 하나를 제공해야 합니다.")
        sys.exit(1)

    write_srt(result, args.out)


if __name__ == "__main__":
    main()
