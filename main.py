#!/usr/bin/env python3
"""Write the 23 November 2026 front page to the output directory.

The image is bundled with this repository as entry.png (JPEG bytes
under a .png name, as the competition allows). This program copies
those exact bytes to the output path on every run: no network, no
randomness, no timestamps in the output, so repeated runs are
byte-identical.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def resolve_output_dir() -> Path:
    """Honour MAKEFUN_OUTPUT_DIR, defaulting to /output."""
    raw = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if raw:
        return Path(raw)
    return Path("/output")


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        print(f"missing bundled image: {source}", file=sys.stderr)
        return 1
    out_dir = resolve_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    shutil.copyfile(source, target)
    # Self-check: the copy must be byte-identical to the bundled image.
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    target_hash = hashlib.sha256(target.read_bytes()).hexdigest()
    if source_hash != target_hash:
        print("copy mismatch: output differs from bundled image",
              file=sys.stderr)
        return 1
    print(f"wrote {target} ({target.stat().st_size} bytes, "
          f"sha256 {target_hash[:16]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
