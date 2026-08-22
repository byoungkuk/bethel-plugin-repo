#!/usr/bin/env python3
"""
nearest_sunday.py

Print the yyyymmdd date of the Sunday nearest to a given date (default:
today). Used for the output filename convention
`yyyymmdd_성경봉독(해당교회력).mp4` -- this script only computes the date part;
the liturgical season name (해당교회력) is not something a date calculation can
produce reliably, so SKILL.md has Claude confirm/ask about that separately.

Usage:
    python3 nearest_sunday.py                # nearest Sunday to today
    python3 nearest_sunday.py --date 2026-07-04
"""
import argparse
import datetime


def nearest_sunday(d):
    # Python's date.weekday(): Monday=0 ... Sunday=6
    days_since_last_sunday = (d.weekday() - 6) % 7
    prev_sunday = d - datetime.timedelta(days=days_since_last_sunday)
    if d == prev_sunday:
        return prev_sunday
    next_sunday = prev_sunday + datetime.timedelta(days=7)
    dist_prev = (d - prev_sunday).days
    dist_next = (next_sunday - d).days
    # Tie only happens if... it can't, Sundays are 7 days apart so the
    # midpoint is always a Wed/Thu, never equidistant. Kept for clarity.
    return next_sunday if dist_next < dist_prev else prev_sunday


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--date", help="YYYY-MM-DD (default: today)")
    args = ap.parse_args()
    d = datetime.date.fromisoformat(args.date) if args.date else datetime.date.today()
    s = nearest_sunday(d)
    print(s.strftime("%Y%m%d"))


if __name__ == "__main__":
    main()
