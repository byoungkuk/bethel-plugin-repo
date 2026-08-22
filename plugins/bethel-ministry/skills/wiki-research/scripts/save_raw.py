#!/usr/bin/env python3
"""
save_raw.py — wiki-research Phase 1 원문 저장 헬퍼.

원문 본문을 받아 `raw/` 폴더에 `raw_<title>.md`로 저장한다. 결정적 작업(파일명
NFC 정규화, 같은 source URL 중복 점검, frontmatter 일관성, 파일명 충돌 회피)을
코드로 처리해, 매 실행이 같은 동작을 보장한다. 본문 텍스트는 모델이 web_fetch로
가져와 stdin 또는 --body-file로 넘긴다(이 스크립트는 네트워크 접근을 하지 않는다).

사용:
  python save_raw.py --raw-dir "<vault>/50 LLM 위키/raw" \
    --source "https://..." --title "원본제목" \
    --grade C --context "수집 이유 + 연결 위키 주제" \
    [--published 2026-05-20] --body-file body.txt
  # 또는 본문을 stdin으로:
  cat body.txt | python save_raw.py ... (--body-file 생략)

출력(stdout): 결과 JSON {status, path|reason}
  status: saved | duplicate | error
종료 코드: 0 saved, 3 duplicate, 1 error
"""
import argparse
import datetime
import json
import re
import sys
import unicodedata
from pathlib import Path


def kst_today() -> str:
    # KST = UTC+9
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return (now_utc + datetime.timedelta(hours=9)).strftime("%Y-%m-%d")


def yaml_quote(value: str) -> str:
    """콜론·따옴표가 들어와도 frontmatter가 깨지지 않게 큰따옴표 인용."""
    return json.dumps(value, ensure_ascii=False)


def safe_title(title: str) -> str:
    # 파일명 안전화: 경로 구분자·제어문자 제거, 공백 정리. 한글은 유지.
    t = re.sub(r"[\\/:*?\"<>|\n\r\t]", " ", title).strip()
    t = re.sub(r"\s+", " ", t)
    return t[:80] if t else "untitled"


def find_duplicate(raw_dir: Path, source: str):
    """raw/ 안에서 frontmatter source가 동일한 파일을 찾는다.

    본문 오탐을 막기 위해 첫 frontmatter 블록(--- ... ---) 안에서만 검색한다.
    """
    if not raw_dir.exists():
        return None
    target = source.strip().rstrip("/")
    for f in raw_dir.glob("*.md"):
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        fm = re.match(r"\A---\n(.*?)\n---", text, flags=re.DOTALL)
        scope = fm.group(1) if fm else text
        m = re.search(r"^source:\s*(.+)$", scope, flags=re.MULTILINE)
        if m and m.group(1).strip().strip("\"'").rstrip("/") == target:
            return f
    return None


def unique_path(raw_dir: Path, title: str) -> Path:
    """충돌 시 날짜, 그다음 _2·_3… 순번을 붙여 덮어쓰기를 방지한다."""
    base = safe_title(title)
    candidates = [f"raw_{base}.md", f"raw_{base}_{kst_today()}.md"]
    n = 2
    while True:
        for name in candidates:
            path = raw_dir / unicodedata.normalize("NFC", name)
            if not path.exists():
                return path
        candidates = [f"raw_{base}_{kst_today()}_{n}.md"]
        n += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", required=True, help="raw 폴더 경로 (예: '<vault>/50 LLM 위키/raw')")
    ap.add_argument("--source", required=True, help="원문 URL")
    ap.add_argument("--title", required=True, help="원본 제목(파일명에 사용)")
    ap.add_argument("--grade", required=True, choices=["A", "B", "C"], help="출처 등급")
    ap.add_argument("--context", required=True, help="수집 이유 + 연결할 위키 주제")
    ap.add_argument("--published", default="", help="원문 작성일(있으면)")
    ap.add_argument("--body-file", default="", help="본문 파일 경로(없으면 stdin)")
    args = ap.parse_args()

    try:
        raw_dir = Path(args.raw_dir)
        raw_dir.mkdir(parents=True, exist_ok=True)

        # 중복 점검 (같은 source URL)
        dup = find_duplicate(raw_dir, args.source)
        if dup is not None:
            print(json.dumps({"status": "duplicate", "reason": f"같은 source 존재: {dup.name}"}, ensure_ascii=False))
            sys.exit(3)

        # 본문 로드
        if args.body_file:
            body_path = Path(args.body_file)
            if not body_path.exists():
                print(json.dumps({"status": "error", "reason": f"본문 파일 없음: {args.body_file}"}, ensure_ascii=False))
                sys.exit(1)
            body = body_path.read_text(encoding="utf-8")
        else:
            body = sys.stdin.read()
        body = body.strip()
        if not body:
            print(json.dumps({"status": "error", "reason": "본문이 비어 있음"}, ensure_ascii=False))
            sys.exit(1)

        # 파일명: NFC 정규화(맥 자소 분리 방지) + 충돌 회피(덮어쓰기 금지)
        path = unique_path(raw_dir, args.title)

        fm_lines = [
            "---",
            "raw_type: collect",
            f"source: {yaml_quote(args.source)}",
            f"captured: {kst_today()}",
        ]
        if args.published:
            fm_lines.append(f"published: {yaml_quote(args.published)}")
        fm_lines += [
            f"grade: {args.grade}",
            f"context: {yaml_quote(args.context)}",
            "---",
            "",
        ]
        path.write_text("\n".join(fm_lines) + body + "\n", encoding="utf-8")
        print(json.dumps({"status": "saved", "path": str(path)}, ensure_ascii=False))
        sys.exit(0)
    except SystemExit:
        raise
    except Exception as e:
        print(json.dumps({"status": "error", "reason": f"{type(e).__name__}: {e}"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
