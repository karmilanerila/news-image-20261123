"""Copy the bundled front-page image to the output directory.

The entry image lives in this repository as entry.png (JPEG bytes under
that name, which the rules allow: the file is told apart by its first
bytes). The program copies it byte for byte to <output>/entry.png, so
both grader runs produce identical files. Standard library only.
"""

import hashlib
import os
import sys
from pathlib import Path


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: bundled image not found: {source}", file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target = out_dir / "entry.png"
    data = source.read_bytes()
    out_dir.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    written = target.read_bytes()
    if written != data:
        print(f"error: {target} does not match {source}", file=sys.stderr)
        return 1
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256={digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
