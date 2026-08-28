#!/usr/bin/env python3
"""Deterministic Gate 0 checks for Korean sermon move manuscripts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def location(text: str, offset: int) -> dict[str, int]:
    line = text.count("\n", 0, offset) + 1
    last_newline = text.rfind("\n", 0, offset)
    column = offset + 1 if last_newline < 0 else offset - last_newline
    return {"line": line, "column": column}


def analyze(text: str, target_min: int, target_max: int) -> dict[str, object]:
    character_count = len(re.sub(r"\s", "", text))
    blocking_issues: list[dict[str, object]] = []
    warnings: list[dict[str, object]] = []

    if not target_min <= character_count <= target_max:
        blocking_issues.append(
            {
                "type": "character_count",
                "message": (
                    f"자수 {character_count}자 — 목표 "
                    f"{target_min}~{target_max}자 범위 밖"
                ),
            }
        )

    # Ignore leading indentation and trailing spaces; flag only internal runs.
    for match in re.finditer(r"(?<=\S) {2,}(?=\S)", text):
        blocking_issues.append(
            {
                "type": "double_space",
                "message": "이중 공백 발견",
                "text": match.group(0),
                **location(text, match.start()),
            }
        )

    # Candidate detector only. Gate 1 decides whether the construction is truly wrong.
    for match in re.finditer(r"(?:히|리|이|기)어?지(?:다|는|고|며|면|니)", text):
        warnings.append(
            {
                "type": "possible_double_passive",
                "message": "이중피동 의심 — Gate 1에서 문맥 확인",
                "text": match.group(0),
                **location(text, match.start()),
            }
        )

    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.?!])\s+", text)
        if sentence.strip()
    ]
    long_indexes = [
        index + 1
        for index, sentence in enumerate(sentences)
        if len(re.sub(r"\s", "", sentence)) > 60
    ]
    for first, second in zip(long_indexes, long_indexes[1:]):
        if second == first + 1:
            warnings.append(
                {
                    "type": "consecutive_long_sentences",
                    "message": "60자 초과 장문이 연속 2개 이상 — 단문 원칙 점검",
                    "sentence_indexes": [first, second],
                }
            )
            break

    return {
        "character_count_without_whitespace": character_count,
        "target": {"min": target_min, "max": target_max},
        "passed": not blocking_issues,
        "blocking_issues": blocking_issues,
        "warnings": warnings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run sermon-critic Gate 0 checks.")
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--min", dest="target_min", type=int, default=700)
    parser.add_argument("--max", dest="target_max", type=int, default=750)
    args = parser.parse_args()

    if args.target_min < 0 or args.target_max < args.target_min:
        parser.error("--min and --max must define a non-negative ascending range")

    text = args.manuscript.read_text(encoding="utf-8")
    print(
        json.dumps(
            analyze(text, args.target_min, args.target_max),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
