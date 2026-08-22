#!/usr/bin/env python3
"""
build_clip.py

Cuts one or more verse ranges out of a "공동체 성경읽기" style chapter-reading
mp4 and stitches them into a single clip, optionally appending the closing
"인도자 / 회중" call-and-response caption used in 벧엘교회's finished
성경봉독 videos.

This bundles the whole pipeline that was worked out by hand for the first
Matthew 11:16-19, 25-30 clip: OCR-based verse-boundary detection, clean
(non-crossfading) cut points, crossfade stitching between kept ranges, and a
freshly-composited ending caption that reuses the last kept frame as its
background so the text swap looks like the source's own transitions.

IMPORTANT -- run this command more than once if needed. Video encoding a
multi-minute clip can take longer than a single shell command is comfortably
given to finish, so this script checkpoints its progress into a work
directory and only does ONE step per run. If you see "Run this same command
again to continue.", just run the exact same command again -- it will pick
up where it left off. When you see "ALL DONE", the output file is finished.

Usage:
    python3 build_clip.py \
        --source "마태복음 11장.mp4" \
        --ranges "16-19,25-30" \
        --output "final.mp4"
    # (run the same command again each time it asks, until ALL DONE)

    # skip the ending caption entirely
    python3 build_clip.py --source in.mp4 --ranges "3-5" --output out.mp4 --no-ending

    # override the caption text/color (rarely needed -- see references/style_notes.md)
    python3 build_clip.py --source in.mp4 --ranges "1-8" --output out.mp4 \
        --ending-line1 "인도자 : 이 말씀은 하나님의 말씀입니다." \
        --ending-line2 "회   중 : 하나님, 감사합니다." \
        --ending-color 251,32,0

Requires: ffmpeg, ffprobe, tesseract, Python Pillow (pip install pillow).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verse_timeline import build_timeline, ffprobe_dims  # noqa: E402

DEFAULT_LINE1 = "인도자 : 이 말씀은 하나님의 말씀입니다."
DEFAULT_LINE2 = "회   중 : 하나님, 감사합니다."
DEFAULT_COLOR = "251,32,0"
FONT_CANDIDATES = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
]


def run(cmd, **kw):
    kw.setdefault("check", True)
    kw.setdefault("capture_output", True)
    kw.setdefault("text", True)
    return subprocess.run(cmd, **kw)


def ffprobe_media_params(path):
    v = run(["ffprobe", "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", path]).stdout.strip()
    a = run(["ffprobe", "-v", "error", "-select_streams", "a:0",
             "-show_entries", "stream=sample_rate,channels", "-of", "csv=p=0", path]).stdout.strip()
    sr, ch = a.split(",")
    return v, int(sr), int(ch)


def get_duration(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries",
                       "format=duration", "-of", "csv=p=0", path]).stdout.strip())


def parse_ranges(ranges_str):
    out = []
    for part in ranges_str.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            out.append((int(a), int(b)))
        else:
            out.append((int(part), int(part)))
    return out


def detect_silences(source, noise_db=-20, min_dur=0.12):
    """
    Run ffmpeg's silencedetect filter over the whole source's audio track and
    return a list of (start, end) second tuples for every detected quiet gap.

    This is what lets segment cuts land in an actual pause in the narration
    instead of a fixed guessed offset -- the guessed offset (end_buffer) is
    usually close, but "close" can still land half a syllable into the next
    word, which is exactly the "audio cuts off" defect this is fixing.

    -20dB was chosen empirically, not -30dB: this template has a constant
    background music bed under the narration, so true digital silence never
    happens, but the bed alone reliably measures quieter than -20dB while the
    narrator is paused between verses. At -30dB almost none of the ~30
    per-verse pauses in a real chapter file were detected at all (only the
    intro and the very end registered); at -20dB essentially every verse
    boundary produced a real, usable 0.12-0.6s gap, matching the actual
    template's crossfade timing. If this is ever re-tuned for a different
    recording, sanity-check the count of detected gaps against the number of
    verse transitions in the timeline -- they should roughly match.
    """
    p = run(["ffmpeg", "-i", source, "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}",
             "-f", "null", "-"], check=False)
    text = p.stderr or ""
    starts, ends = [], []
    for line in text.splitlines():
        line = line.strip()
        if "silence_start:" in line:
            try:
                starts.append(float(line.split("silence_start:")[1].strip().split()[0]))
            except ValueError:
                pass
        elif "silence_end:" in line:
            try:
                part = line.split("silence_end:")[1].strip()
                ends.append(float(part.split("|")[0].strip()))
            except ValueError:
                pass
    return list(zip(starts, ends))


def _find_silence_after(t_ref, silences, window_back=0.6, window_fwd=3.0):
    """Find the silence gap that best represents 'the narrator just paused'
    near t_ref. Returns (start, end) or None."""
    candidates = [(s, e) for s, e in silences if t_ref - window_back <= s <= t_ref + window_fwd]
    if not candidates:
        return None
    candidates.sort(key=lambda se: abs(se[0] - t_ref))
    return candidates[0]


def find_bounds(timeline, start_verse, end_verse, start_buffer=0.15, end_buffer=0.4, silences=None):
    """
    Given the {second: verse_number_string} timeline, find a clean (start, end)
    time range covering start_verse..end_verse inclusive.

    The template crossfades between verses in well under a second, and it
    always starts right at a verse-number transition. Empirically, the frame
    exactly at the first second a verse's number is read is *almost* clean and
    fully resolves ~0.1-0.3s later; the last second a verse's number is read
    stays clean for another ~0.3-0.5s before the next crossfade begins. The
    buffers below reflect that -- if a particular cut still shows a hint of
    the neighboring verse, nudge the buffer for that call, or re-check with
    peek frames (see SKILL.md "Sanity-check the cut points" step).

    If `silences` (from detect_silences) is given, the end point is further
    snapped forward into the nearest real audio pause at/after the heuristic
    end_buffer guess, so the cut never lands mid-word/mid-sentence even if
    end_buffer alone would have been a little early or late. This is the fix
    for narration getting clipped at the end of a segment.
    """
    matches_start = sorted(sec for sec, v in timeline.items() if v == str(start_verse))
    matches_end = sorted(sec for sec, v in timeline.items() if v == str(end_verse))
    if not matches_start:
        raise ValueError(f"Verse {start_verse} not found on screen anywhere in the video")
    if not matches_end:
        raise ValueError(f"Verse {end_verse} not found on screen anywhere in the video")
    t0 = matches_start[0] + start_buffer
    visual_t1 = matches_end[-1] + end_buffer
    audio_t1 = visual_t1
    note = "heuristic cut (no silence data supplied)"

    if silences:
        pad = 0.12
        hit = _find_silence_after(visual_t1, silences, window_back=0.6, window_fwd=3.0)
        far = False
        if not hit:
            # No nearby pause -- widen the search rather than risk cutting
            # mid-speech. Audio clarity matters more than exact timing.
            hit = _find_silence_after(visual_t1, silences, window_back=0.6, window_fwd=8.0)
            far = True
        if hit:
            s_start, s_end = hit
            candidate = s_start + pad if (s_end - s_start > pad + 0.02) else (s_start + s_end) / 2
            # Never propose an audio end earlier than the safe visual cut --
            # only extend forward from it.
            audio_t1 = max(candidate, visual_t1)
            if audio_t1 > visual_t1 + 0.02:
                # The template's on-screen crossfade to the next verse can
                # begin slightly before the narrator actually finishes
                # reading -- the real pause lands after the visual cutoff.
                # Cutting the video there too would let a sliver of the next
                # (possibly skipped) verse's image bleed in; extract_segment
                # handles this by freezing the video at visual_t1 while
                # letting the audio play on to audio_t1.
                note = (f"{'far ' if far else ''}narration continues {audio_t1 - visual_t1:.2f}s past the "
                        f"clean visual cut (pause[{s_start:.2f},{s_end:.2f}]) -- video will freeze there, "
                        f"audio kept intact")
            else:
                note = f"{'far ' if far else ''}silence-snapped end -> pause[{s_start:.2f},{s_end:.2f}]s"
        else:
            note = "WARNING: no silence gap found nearby -- falling back to heuristic cut"

    if visual_t1 <= t0 or audio_t1 <= t0:
        raise ValueError(
            f"Computed end is not after start {t0}s for verses {start_verse}-{end_verse}; "
            "double check the range is in ascending on-screen order."
        )
    return t0, visual_t1, audio_t1, note


def extract_segment(source, t0, video_t1, out_path, fade_in=0.0, fade_out=0.0, audio_t1=None):
    """
    Cut [t0, video_t1) out of source. Optionally bake a white fade-in/out
    directly into this cut instead of doing a separate pass over the whole
    assembled clip later -- re-encoding a whole multi-minute clip a second
    time just to add a fraction-of-a-second fade is needlessly expensive (and,
    on a resource-constrained sandbox, can be slow enough to blow past a
    single command's time budget), whereas baking it into a segment that's
    already being re-encoded is free.

    If `audio_t1` is given and is later than `video_t1` (see find_bounds),
    the narrator is still speaking a little past the clean visual cutoff.
    Rather than choose between "chop the narration" and "let the next verse's
    image bleed in for a moment", this freezes the video on its last clean
    frame from video_t1 onward while the audio keeps playing naturally
    through to audio_t1 -- nothing of the next (possibly skipped) verse is
    ever shown, and the narration is never cut short.

    IMPORTANT: -ss is placed BEFORE -i (not after). Seeking after -i plus a
    -vf filter graph reliably hung indefinitely against these source files
    (they carry an extra embedded MJPEG cover-art video stream alongside the
    real one, which seems to be what accurate post-input seeking trips over
    once a filter is attached). Seeking before -i avoids it completely and,
    since the output here is always re-encoded (never stream-copied), it is
    just as frame-accurate -- ffmpeg still decodes forward from the nearest
    keyframe to the exact requested time, it just does the seek at the
    demuxer level instead. Because -ss now happens before -i, the endpoint
    must be given as a duration (-t) rather than an absolute time (-to).
    """
    freeze_extra = 0.0
    if audio_t1 is not None and audio_t1 > video_t1:
        freeze_extra = audio_t1 - video_t1
        dur = audio_t1 - t0
    else:
        dur = video_t1 - t0

    vf_parts, af_parts = [], []
    if freeze_extra > 0:
        video_dur = round(video_t1 - t0, 3)
        vf_parts.append(
            f"trim=start=0:end={video_dur},setpts=PTS-STARTPTS,"
            f"tpad=stop_mode=clone:stop_duration={round(freeze_extra, 3)}"
        )
    if fade_in > 0:
        vf_parts.append(f"fade=t=in:st=0:d={fade_in}:color=white")
        af_parts.append(f"afade=t=in:st=0:d={fade_in}")
    if fade_out > 0:
        fout_start = round(dur - fade_out, 3)
        vf_parts.append(f"fade=t=out:st={fout_start}:d={fade_out}:color=white")
        af_parts.append(f"afade=t=out:st={fout_start}:d={fade_out}")
    cmd = ["ffmpeg", "-y", "-ss", str(t0), "-i", source, "-t", str(dur)]
    if vf_parts:
        cmd += ["-vf", ",".join(vf_parts)]
    if af_parts:
        cmd += ["-af", ",".join(af_parts)]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", out_path]
    run(cmd)


def xfade_pair(a_path, b_path, out_path, transition=0.5):
    dur_a = get_duration(a_path)
    offset = max(dur_a - transition, 0)
    run(["ffmpeg", "-y", "-i", a_path, "-i", b_path, "-filter_complex",
         f"[0:v][1:v]xfade=transition=fade:duration={transition}:offset={offset}[v];"
         f"[0:a][1:a]acrossfade=d={transition}[a]",
         "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", out_path])


def grab_last_frame(video_path, out_png, pad=0.1):
    run(["ffmpeg", "-y", "-sseof", f"-{pad}", "-i", video_path, "-frames:v", "1", out_png])


def make_ending_frame(base_png, line1, line2, color_rgb, out_png):
    im = Image.open(base_png).convert("RGB")
    w, h = im.size
    px = im.load()

    def is_offwhite(p, tol=6):
        return all(abs(c - 253) <= tol for c in p[:3])

    # Find where the white panel starts blending into the illustration by
    # scanning a row near the bottom of the frame -- verse text never reaches
    # that low, so the only thing that can make a column non-white there is
    # the real gradient, not text getting mistaken for it.
    probe_y = int(h * 0.92)
    grad_start = w
    for x in range(0, w, 4):
        if not is_offwhite(px[x, probe_y]):
            grad_start = x
            break

    minx, maxx, miny, maxy = w, 0, h, 0
    for y in range(0, h, 2):
        for x in range(0, min(grad_start, w), 2):
            r, g, b = px[x, y][:3]
            is_dark = r < 100 and g < 100 and b < 100
            is_green_label = g > 100 and r < 100 and b < 120 and g > r and g > b
            if is_dark or is_green_label:
                minx, maxx = min(minx, x), max(maxx, x)
                miny, maxy = min(miny, y), max(maxy, y)

    draw = ImageDraw.Draw(im)
    if maxx >= minx:
        draw.rectangle(
            [0, max(0, miny - 40), min(grad_start - 5, w), min(h, maxy + 80)],
            fill=(253, 253, 253),
        )

    font_path = FONT_CANDIDATES[0] if os.path.exists(FONT_CANDIDATES[0]) else FONT_CANDIDATES[1]
    font_size = round(46 * h / 1080)
    font = ImageFont.truetype(font_path, font_size) if os.path.exists(font_path) else ImageFont.load_default()
    x_text = round(185 * w / 1920)
    y1 = round(470 * h / 1080)
    y2 = round(550 * h / 1080)
    draw.text((x_text, y1), line1, font=font, fill=tuple(color_rgb))
    draw.text((x_text, y2), line2, font=font, fill=tuple(color_rgb))
    im.save(out_png)


def make_ending_clip(frame_png, out_path, hold, fps_str, sample_rate, channels, fade_out=0.0):
    layout = "stereo" if channels == 2 else "mono"
    cmd = ["ffmpeg", "-y", "-loop", "1", "-i", frame_png,
           "-f", "lavfi", "-i", f"anullsrc=channel_layout={layout}:sample_rate={sample_rate}",
           "-t", str(hold), "-r", fps_str, "-pix_fmt", "yuv420p"]
    if fade_out > 0:
        fout_start = round(hold - fade_out, 3)
        cmd += ["-vf", f"fade=t=out:st={fout_start}:d={fade_out}:color=white",
                "-af", f"afade=t=out:st={fout_start}:d={fade_out}"]
    cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k", "-shortest", out_path]
    run(cmd)


def say_continue():
    print("Run this same command again to continue.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True)
    ap.add_argument("--ranges", required=True, help="e.g. '16-19,25-30' or a single '12-14'")
    ap.add_argument("--output", required=True)
    ap.add_argument(
        "--workdir",
        help=(
            "Checkpoint/scratch directory (default: a stable folder under the "
            "system temp dir, named after --output). IMPORTANT: this must be a "
            "normal scratch filesystem, not a delivery/outputs folder that "
            "forbids deleting or overwriting files once written -- some "
            "sandboxes have exactly that restriction on their final-output "
            "directory, and this script repeatedly overwrites its progress "
            "files as it goes. Only the finished --output file is written into "
            "wherever you point --output."
        ),
    )
    ap.add_argument("--timeline", help="Reuse a previously computed timeline.json instead of recomputing")
    ap.add_argument("--crop-rel", default="0.0729,0.1759,0.0781,0.0417")
    ap.add_argument("--start-buffer", type=float, default=0.15)
    ap.add_argument("--end-buffer", type=float, default=0.4)
    ap.add_argument("--transition", type=float, default=0.5, help="Crossfade duration between kept ranges and into the ending caption")
    ap.add_argument("--skip-pause", type=float, default=0.6,
                    help="Silent held-frame pause inserted after a kept range, before crossfading "
                         "into the next kept range -- marks a verse-skip join so it doesn't feel "
                         "like an instant jump. Set to 0 to disable.")
    ap.add_argument("--no-ending", action="store_true", help="Skip the 인도자/회중 ending caption entirely")
    ap.add_argument("--ending-line1", default=DEFAULT_LINE1)
    ap.add_argument("--ending-line2", default=DEFAULT_LINE2)
    ap.add_argument("--ending-color", default=DEFAULT_COLOR, help="R,G,B")
    ap.add_argument("--ending-hold", type=float, default=4.5, help="Seconds the ending caption stays on screen")
    ap.add_argument("--head-fade", type=float, default=0.35)
    ap.add_argument("--tail-fade", type=float, default=0.5)
    args = ap.parse_args()

    ranges = parse_ranges(args.ranges)
    if args.workdir:
        workdir = args.workdir
    else:
        import hashlib
        import tempfile as _tempfile
        key = hashlib.sha1(os.path.abspath(args.output).encode("utf-8")).hexdigest()[:12]
        workdir = os.path.join(_tempfile.gettempdir(), f"bible_clip_{key}")
    os.makedirs(workdir, exist_ok=True)

    timeline_path = os.path.join(workdir, "timeline.json")

    # STEP 1: verse timeline (parallel OCR pass over the whole source video)
    if args.timeline:
        if not os.path.exists(timeline_path):
            with open(args.timeline, encoding="utf-8") as f:
                raw = json.load(f)
            with open(timeline_path, "w", encoding="utf-8") as f:
                json.dump(raw, f, ensure_ascii=False)
    if not os.path.exists(timeline_path):
        print("STEP: detecting verse timeline (parallel OCR pass)...")
        timeline, _ = build_timeline(args.source, args.crop_rel)
        with open(timeline_path, "w", encoding="utf-8") as f:
            json.dump({str(k): v for k, v in timeline.items()}, f, ensure_ascii=False, indent=2)
        print(f"STEP DONE: timeline ({len(timeline)} samples) -> {timeline_path}")
        say_continue()
        return

    with open(timeline_path, encoding="utf-8") as f:
        raw = json.load(f)
    timeline = {float(k): v for k, v in raw.items()}

    # STEP 1.5: audio silence gaps across the whole source. Used to snap
    # segment end-points into a real pause in the narration instead of a
    # fixed guessed offset, so cuts never land mid-word (see find_bounds).
    silences_path = os.path.join(workdir, "silences.json")
    if not os.path.exists(silences_path):
        print("STEP: detecting audio silence gaps (so cuts never land mid-speech)...")
        silences = detect_silences(args.source)
        with open(silences_path, "w", encoding="utf-8") as f:
            json.dump(silences, f)
        print(f"STEP DONE: {len(silences)} silence gaps found -> {silences_path}")
        say_continue()
        return
    with open(silences_path, encoding="utf-8") as f:
        silences = [tuple(x) for x in json.load(f)]

    # STEP 2: cut each requested range into its own segment (one per run).
    # The head fade-in is baked into segment 0's own encode, and (only when
    # there's no ending caption to carry it instead) the tail fade-out is
    # baked into the last segment's encode -- see extract_segment's docstring
    # for why this is done here instead of as a separate final pass.
    seg_paths = [os.path.join(workdir, f"seg_{i:02d}.mp4") for i in range(len(ranges))]
    last_note_path = os.path.join(workdir, "last_segment_note.txt")
    for i, (sv, ev) in enumerate(ranges):
        if os.path.exists(seg_paths[i]):
            continue
        t0, video_t1, audio_t1, note = find_bounds(
            timeline, sv, ev, args.start_buffer, args.end_buffer, silences=silences)
        fade_in = args.head_fade if i == 0 else 0.0
        fade_out = args.tail_fade if (args.no_ending and i == len(ranges) - 1) else 0.0
        print(f"STEP: cutting verses {sv}-{ev}: {t0:.2f}s -> {video_t1:.2f}s ({note})")
        extract_segment(args.source, t0, video_t1, seg_paths[i], fade_in=fade_in, fade_out=fade_out,
                         audio_t1=audio_t1)
        if i == len(ranges) - 1:
            # Remember whether this final cut found a real pause to land in --
            # STEP 4 uses this to decide whether the ending caption needs an
            # extra blank-space cushion before it (see "no room for caption"
            # fallback in STEP 4 below).
            with open(last_note_path, "w", encoding="utf-8") as f:
                f.write(note)
        print(f"STEP DONE: segment {i} -> {seg_paths[i]}")
        say_continue()
        return

    # STEP 2.5: when multiple ranges are being stitched together (i.e. a
    # verse-skip join in the middle), pad every non-last segment with a brief
    # silent held-frame pause before it gets crossfaded into the next range.
    # Without this, a skip reads as an instant, slightly jarring jump; the
    # user asked for "a little gap/pause" to be felt at exactly these joins
    # (this only applies between kept ranges -- not before the ending caption,
    # which already gets its own natural crossfade-in).
    needs_pad = len(ranges) > 1 and args.skip_pause > 0
    pad_paths = [os.path.join(workdir, f"seg_{i:02d}_pad.mp4") for i in range(len(ranges))]
    if needs_pad:
        for i in range(len(ranges) - 1):
            if os.path.exists(pad_paths[i]):
                continue
            print(f"STEP: adding a {args.skip_pause}s pause after range {i} (verse-skip join)")
            hold_frame = os.path.join(workdir, f"seg_{i:02d}_holdframe.png")
            grab_last_frame(seg_paths[i], hold_frame, pad=0.05)
            pause_clip = os.path.join(workdir, f"seg_{i:02d}_pauseclip.mp4")
            fps_str, sample_rate, channels = ffprobe_media_params(args.source)
            make_ending_clip(hold_frame, pause_clip, args.skip_pause, fps_str, sample_rate, channels)
            run(["ffmpeg", "-y", "-i", seg_paths[i], "-i", pause_clip, "-filter_complex",
                 "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
                 "-map", "[v]", "-map", "[a]",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-b:a", "192k", pad_paths[i]])
            print(f"STEP DONE: padded range {i} -> {pad_paths[i]}")
            say_continue()
            return

    chain_inputs = [
        (pad_paths[i] if (needs_pad and i < len(ranges) - 1) else seg_paths[i])
        for i in range(len(ranges))
    ]

    # STEP 3: crossfade-chain the segments together, two at a time (one merge per run)
    chain_path = os.path.join(workdir, "chain_final.mp4")
    if not os.path.exists(chain_path):
        chain_progress = os.path.join(workdir, "chain_progress.mp4")
        # `current` is whichever file already represents the front of the
        # chain; `done_count` is how many segments' worth of content it holds.
        # With no progress yet, chain_inputs[0] itself already represents 1
        # segment (the starting point), so done_count starts at 1, not 0.
        current = chain_progress if os.path.exists(chain_progress) else chain_inputs[0]
        done_count = 1
        marker_path = os.path.join(workdir, "chain_progress.count")
        if os.path.exists(marker_path):
            done_count = int(open(marker_path).read().strip())
            current = chain_progress
        if len(chain_inputs) == 1:
            # Copy (not move/rename) -- STEP 2's own "already done" check looks
            # for seg_paths[0] to still exist, so renaming it away here would
            # make a later re-run of this command redo that cut for nothing.
            shutil.copy2(chain_inputs[0], chain_path)
            print(f"STEP DONE: only one range requested, no crossfade needed -> {chain_path}")
            say_continue()
            return
        if done_count < len(chain_inputs):
            nxt = chain_inputs[done_count]
            # NOTE: keep this a plain "*.mp4" name -- ffmpeg guesses the muxer
            # from the file extension, and a double extension like
            # "foo.mp4.tmp" makes it fail with "Unable to find a suitable
            # output format" instead of writing an mp4.
            out = os.path.join(workdir, f"chain_progress_next_{done_count}.mp4")
            print(f"STEP: crossfading segment {done_count} onto the chain")
            xfade_pair(current, nxt, out, transition=args.transition)
            os.replace(out, chain_progress)
            done_count += 1
            with open(marker_path, "w") as f:
                f.write(str(done_count))
            if done_count == len(chain_inputs):
                os.replace(chain_progress, chain_path)
                print(f"STEP DONE: all segments chained -> {chain_path}")
            else:
                print(f"STEP DONE: chained {done_count}/{len(chain_inputs)} segments")
            say_continue()
            return

    # STEP 3.5: if the very last kept segment's end-cut had no natural audio
    # pause nearby to snap into (the WARNING case in find_bounds), the
    # narration may still be trailing right up to where the ending caption
    # would crossfade in. Rather than risk that collision, add a small blank/
    # silent cushion first -- this is the "if there's truly no room, it's OK
    # to add blank space" fallback the user asked for.
    last_note = ""
    if os.path.exists(last_note_path):
        with open(last_note_path, encoding="utf-8") as f:
            last_note = f.read()
    needs_cushion = (not args.no_ending) and ("WARNING" in last_note)
    cushion_path = os.path.join(workdir, "chain_cushioned.mp4")
    chain_for_ending = chain_path
    if needs_cushion:
        if not os.path.exists(cushion_path):
            print("STEP: no natural pause found before the ending caption -- adding a blank cushion")
            cushion_frame = os.path.join(workdir, "cushion_holdframe.png")
            grab_last_frame(chain_path, cushion_frame, pad=0.05)
            cushion_clip = os.path.join(workdir, "cushion_clip.mp4")
            fps_str, sample_rate, channels = ffprobe_media_params(args.source)
            make_ending_clip(cushion_frame, cushion_clip, 0.5, fps_str, sample_rate, channels)
            run(["ffmpeg", "-y", "-i", chain_path, "-i", cushion_clip, "-filter_complex",
                 "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]",
                 "-map", "[v]", "-map", "[a]",
                 "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
                 "-c:a", "aac", "-b:a", "192k", cushion_path])
            print(f"STEP DONE: cushioned chain -> {cushion_path}")
            say_continue()
            return
        chain_for_ending = cushion_path

    # STEP 4: build + crossfade in the ending caption (its own encode bakes in
    # the tail fade-out, since it's the last thing on screen)
    with_ending_path = os.path.join(workdir, "with_ending.mp4")
    final_path = chain_path
    if not args.no_ending and not os.path.exists(with_ending_path):
        ending_frame = os.path.join(workdir, "ending_frame.png")
        ending_clip = os.path.join(workdir, "ending_clip.mp4")
        if not os.path.exists(ending_clip):
            print("STEP: compositing ending caption frame + clip")
            last_frame = os.path.join(workdir, "last_frame.png")
            grab_last_frame(chain_for_ending, last_frame)
            color_rgb = tuple(int(c) for c in args.ending_color.split(","))
            make_ending_frame(last_frame, args.ending_line1, args.ending_line2, color_rgb, ending_frame)
            fps_str, sample_rate, channels = ffprobe_media_params(args.source)
            make_ending_clip(ending_frame, ending_clip, args.ending_hold, fps_str, sample_rate, channels,
                              fade_out=args.tail_fade)
            print(f"STEP DONE: ending clip -> {ending_clip}")
            say_continue()
            return
        print("STEP: crossfading ending caption onto the chained clip")
        xfade_pair(chain_for_ending, ending_clip, with_ending_path,
                   transition=min(args.transition + 0.1, args.ending_hold))
        print(f"STEP DONE: {with_ending_path}")
        say_continue()
        return
    if not args.no_ending:
        final_path = with_ending_path

    # STEP 5: copy the finished scratch file to --output. This is a plain
    # file copy (not a re-encode), so it is fast even for a long clip -- all
    # the fades were already baked into the small terminal encodes above, so
    # there's no expensive whole-clip re-encode left to do here. Only ever
    # *copying* into --output also means a timeout never leaves a
    # half-written, corrupt file sitting there (some delivery/outputs folders
    # won't let you delete or overwrite a file once it exists, so a corrupt
    # partial write would be unrecoverable).
    print("STEP: copying finished clip to --output")
    shutil.copy2(final_path, args.output)
    print(f"ALL DONE -> {args.output}")


if __name__ == "__main__":
    main()
