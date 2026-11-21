#!/usr/bin/env python3
"""Entry point for the news-image-20261120 bounty.

The image summing up Friday 20 November 2026's world news was drawn
at build time and ships beside this file as entry.png. This program
only copies that image to the grader's output path.

Python 3.13, standard library only, no network access. When run
outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
from pathlib import Path

IMAGE_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # the bounty caps the entry image at 1 MiB


def main() -> None:
    here: Path = Path(__file__).resolve().parent
    source: Path = here / IMAGE_NAME
    # Fail loudly on a truncated, non-PNG, or oversized file instead of
    # shipping bytes the gate would reject as "not a whole image".
    with open(source, "rb") as fh:
        magic: bytes = fh.read(8)
    if magic != PNG_MAGIC:
        raise SystemExit("entry.png is not a whole PNG image")
    if source.stat().st_size > MAX_BYTES:
        raise SystemExit("entry.png exceeds the 1 MiB limit")
    out_dir: Path = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target: Path = out_dir / IMAGE_NAME
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise SystemExit("copy incomplete: size mismatch for entry.png")


if __name__ == "__main__":
    main()
