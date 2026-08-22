#!/usr/bin/env python3
"""
verse_timeline.py

Builds a second-by-second map of which Bible verse number is on screen in a
"공동체 성경읽기 / Public Reading of Scripture" style chapter-reading mp4
(the format used for 벧엘교회 성경봉독 videos: green chapter/subtitle line top
left, verse number, bold Korean verse text, italic English text below, a
still illustration on the right, and a small "공동체 성경읽기" logo top right).

It works by sampling one frame per second, cropping the small verse-number
region, and OCR-reading just the digits. This is far more reliable than
trying to OCR the full verse text, and it is resolution independent because
the crop box is expressed as a fraction of the frame size.

The per-frame crop+OCR work is spread across a thread pool because each unit
is a short-lived subprocess (ffmpeg, then tesseract) -- running them one at a
time for a several-minute chapter can take longer than a single shell command
is normally given to finish, so this parallelizes across CPU cores instead.

Output: a JSON object mapping second (as a string) -> verse number string
(empty string "" if no digits were confidently read, which typically means
a title card, a mid-transition frame, or the very end of the video).

Usage:
    python3 verse_timeline.py --source "마태복음 11장.mp4" --out timeline.json

Requires: ffmpeg, ffprobe, tesseract (all on PATH).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor


def ffprobe_dims(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-of", "csv=s=x:p=0", path],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    w, h = out.split("x")
    return int(w), int(h)


def _ocr_one(args):
    src, crop_box, tmpdir, i = args
    cx, cy, cw, ch = crop_box
    crop_path = os.path.join(tmpdir, f"crop_{i:05d}.png")
    subprocess.run(
        ["ffmpeg", "-y", "-i", src, "-vf", f"crop={cw}:{ch}:{cx}:{cy}", crop_path],
        check=True, capture_output=True,
    )
    proc = subprocess.run(
        ["tesseract", crop_path, "-", "--psm", "7",
         "-c", "tessedit_char_whitelist=0123456789"],
        capture_output=True, text=True,
    )
    os.remove(crop_path)
    return proc.stdout.strip()


def build_timeline(source, crop_rel="0.0729,0.1759,0.0781,0.0417", fps=1.0, workers=12):
    w, h = ffprobe_dims(source)
    rx, ry, rw, rh = (float(v) for v in crop_rel.split(","))
    crop_box = (int(rx * w), int(ry * h), int(rw * w), int(rh * h))

    tmpdir = tempfile.mkdtemp(prefix="vtl_")
    try:
        frames_dir = os.path.join(tmpdir, "frames")
        os.makedirs(frames_dir, exist_ok=True)
        subprocess.run(
            ["ffmpeg", "-y", "-i", source, "-vf", f"fps={fps}",
             os.path.join(frames_dir, "f_%05d.png")],
            check=True, capture_output=True,
        )
        files = sorted(os.listdir(frames_dir))
        jobs = [
            (os.path.join(frames_dir, fname), crop_box, tmpdir, i)
            for i, fname in enumerate(files)
        ]
        with ThreadPoolExecutor(max_workers=workers) as ex:
            texts = list(ex.map(_ocr_one, jobs))
        timeline = {round(i / fps, 2): txt for i, txt in enumerate(texts)}
        return timeline, (w, h)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, help="Path to the chapter-reading mp4")
    ap.add_argument("--out", default="timeline.json", help="Where to write the JSON timeline")
    ap.add_argument("--fps", type=float, default=1.0, help="Sampling rate (1 fps is plenty)")
    ap.add_argument("--workers", type=int, default=12, help="Parallel ffmpeg/tesseract workers")
    ap.add_argument(
        "--crop-rel",
        default="0.0729,0.1759,0.0781,0.0417",
        help=(
            "x,y,w,h as a fraction of the frame, describing the box around the "
            "verse-number digits. The default is calibrated for the standard "
            "1920x1080 '공동체 성경읽기' template (see references/style_notes.md). "
            "If a new template is ever used, recalibrate by cropping a frame and "
            "eyeballing the box with an image viewer."
        ),
    )
    args = ap.parse_args()

    timeline, (w, h) = build_timeline(args.source, args.crop_rel, args.fps, args.workers)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in timeline.items()}, f, ensure_ascii=False, indent=2)
    print(f"Wrote {args.out} ({len(timeline)} samples, {w}x{h} source)")


if __name__ == "__main__":
    main()
