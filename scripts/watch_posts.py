#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POSTS_DIR = ROOT / "posts"
BUILD_SCRIPT = ROOT / "scripts" / "build_posts.py"
POLL_SECONDS = 1.0


def snapshot() -> dict[Path, tuple[int, int]]:
    files: dict[Path, tuple[int, int]] = {}
    for path in POSTS_DIR.rglob("*"):
        if path.is_file():
            stat = path.stat()
            files[path] = (stat.st_mtime_ns, stat.st_size)
    return files


def build() -> None:
    result = subprocess.run(
        [sys.executable, str(BUILD_SCRIPT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    timestamp = time.strftime("%H:%M:%S")
    if result.returncode == 0:
        print(f"[{timestamp}] rebuilt writing pages")
    else:
        print(f"[{timestamp}] build failed", file=sys.stderr)
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)


def main() -> None:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Watching {POSTS_DIR}")
    build()
    last = snapshot()

    try:
        while True:
            time.sleep(POLL_SECONDS)
            current = snapshot()
            if current != last:
                build()
                last = current
    except KeyboardInterrupt:
        print("\nStopped watching posts.")


if __name__ == "__main__":
    main()
