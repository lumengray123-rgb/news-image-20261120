#!/usr/bin/env python3
"""Deliver the finished news image to the grader's output folder.

The entry artwork (entry.png) lives next to this script. This program
checks that the artwork is a genuine, reasonably sized PNG and then
copies it to the output directory the grader provides, confirming the
copy landed intact before exiting.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

PNG_SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
MAX_IMAGE_BYTES = 1024 * 1024  # 1 MiB ceiling imposed by the bounty kit
IMAGE_NAME = "entry.png"


def die(message: str) -> "SystemExit":
    """Print a fatal error to stderr and exit non-zero."""
    print(f"main.py: {message}", file=sys.stderr)
    return SystemExit(1)


def locate_artwork() -> Path:
    """Return the path of the entry image sitting beside this script."""
    return Path(__file__).resolve().parent / IMAGE_NAME


def output_directory() -> Path:
    """Return the grader's output directory (env override, else /output)."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "") or "/output"
    return Path(raw)


def inspect_artwork(path: Path) -> None:
    """Refuse to ship the image unless it looks like a valid small PNG."""
    if not path.is_file():
        raise die(f"artwork missing: {path}")

    size = path.stat().st_size
    if size == 0:
        raise die(f"artwork is empty: {path}")
    if size > MAX_IMAGE_BYTES:
        raise die(
            f"artwork too large: {size} bytes (limit {MAX_IMAGE_BYTES})"
        )

    with path.open("rb") as handle:
        header = handle.read(len(PNG_SIGNATURE))
    if header != PNG_SIGNATURE:
        raise die("artwork does not start with the PNG signature")


def digest_of(path: Path) -> str:
    """Return the SHA-256 hex digest of a file's bytes."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def deliver(source: Path, target_dir: Path) -> Path:
    """Copy the artwork into target_dir and prove the copy is exact."""
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE_NAME
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        raise die(
            f"copy incomplete: wrote {target.stat().st_size} bytes "
            f"but source is {source.stat().st_size} bytes"
        )
    if digest_of(target) != digest_of(source):
        raise die("copy failed integrity check: SHA-256 digest mismatch")
    return target


def main() -> None:
    source = locate_artwork()
    inspect_artwork(source)
    target = deliver(source, output_directory())
    print(f"delivered {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
