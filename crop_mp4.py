#!/usr/bin/env python3
import argparse
import subprocess
import json
import sys
from pathlib import Path
from typing import Optional


def run_cmd(cmd):
    """Run a shell command and raise if it fails."""
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Command failed: {' '.join(cmd)}\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
    return result.stdout


def get_duration(input_file: str) -> float:
    """Get video duration in seconds using ffprobe."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-print_format", "json",
        "-show_format",
        input_file,
    ]
    out = run_cmd(cmd)
    info = json.loads(out)
    duration_str = info["format"]["duration"]
    return float(duration_str)


def parse_time_str(ts: Optional[str]) -> Optional[float]:
    """Parse time string to seconds.

    Supported formats:
      - "12" or "12.5"       -> seconds
      - "MM:SS"              -> minutes and seconds
      - "HH:MM:SS"           -> hours, minutes, seconds
    """
    if ts is None:
        return None

    ts = ts.strip()
    if not ts:
        return None

    if ":" not in ts:
        # pure seconds (int or float)
        return float(ts)

    parts = ts.split(":")
    if len(parts) == 2:
        # MM:SS
        m, s = parts
        return int(m) * 60 + float(s)
    elif len(parts) == 3:
        # HH:MM:SS
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    else:
        raise ValueError(f"Unsupported time format: {ts}")


def cut_video(input_file: str, output_file: str,
              t1_str: Optional[str], t2_str: Optional[str]) -> None:
    """Cut video between t1 and t2 and save to output_file.

    If t1 is None -> start from 0.
    If t2 is None or t2 > duration -> cut to the end.
    """
    input_path = Path(input_file)
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_file}")

    duration = get_duration(str(input_path))

    # Parse time strings
    t1 = parse_time_str(t1_str)
    t2 = parse_time_str(t2_str)

    # Apply default values
    if t1 is None:
        t1 = 0.0
    if t1 < 0:
        t1 = 0.0

    if t1 >= duration:
        raise ValueError(
            f"t1 ({t1} s) is greater than or equal to video duration ({duration} s)."
        )

    if t2 is None or t2 > duration:
        t2 = duration

    if t2 <= t1:
        raise ValueError(
            f"t2 ({t2} s) must be greater than t1 ({t1} s)."
        )

    clip_len = t2 - t1

    # ffmpeg: -ss <start> -i input -t <duration> -c copy output
    cmd = [
        "ffmpeg",
        "-y",              # overwrite output without asking
        "-ss", f"{t1}",
        "-i", str(input_path),
        "-t", f"{clip_len}",
        "-c", "copy",      # stream copy, no re-encode
        str(output_file),
    ]
    print("Running:", " ".join(cmd))
    run_cmd(cmd)
    print(f"Done. Output saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Cut a segment from an MP4 file using ffmpeg."
    )
    parser.add_argument("input", help="Input MP4 file")
    parser.add_argument("output", help="Output MP4 file")
    parser.add_argument(
        "--t1",
        help="Start time (e.g. '10', '01:23', '00:01:23'). If missing, start from 0.",
        default=None,
    )
    parser.add_argument(
        "--t2",
        help="End time (e.g. '20', '02:00', '00:02:00'). "
             "If missing or > duration, cut to the end.",
        default=None,
    )

    args = parser.parse_args()

    try:
        cut_video(args.input, args.output, args.t1, args.t2)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
