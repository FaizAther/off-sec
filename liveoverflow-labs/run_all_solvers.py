#!/usr/bin/env python3

"""
Run all solver scripts that are expected to work in-container.

This is executed inside the `liveoverflow-solver` container (Ubuntu 24.04 + pwntools).
It assumes binaries were built in `liveoverflow-pwn` and are present in the shared volume.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


SOLVERS = [
    # stack
    "liveoverflow-labs/0.stack/stack.0.py",
    "liveoverflow-labs/0.stack/stack.1.py",
    "liveoverflow-labs/0.stack/stack.2.py",
    # format (working ones)
    "liveoverflow-labs/1.format/format.1.py",
    "liveoverflow-labs/1.format/format.2.py",
    "liveoverflow-labs/1.format/format.3.py",
    "liveoverflow-labs/1.format/format.4.py",
    # heap
    "liveoverflow-labs/2.heap/heap.0.py",
    "liveoverflow-labs/2.heap/heap.1.py",
    "liveoverflow-labs/2.heap/heap.2.py",
    # net
    "liveoverflow-labs/3.net/net.0.py",
    "liveoverflow-labs/3.net/net.1.py",
    "liveoverflow-labs/3.net/net.2.py",
]


def run_one(rel: str) -> tuple[int, str]:
    p = subprocess.run(
        ["/opt/venv/bin/python", str(ROOT / rel)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return p.returncode, p.stdout


def main() -> int:
    failures = 0
    for rel in SOLVERS:
        rc, out = run_one(rel)
        status = "OK" if rc == 0 else f"FAIL({rc})"
        print(f"{status} {rel}")
        if rc != 0:
            failures += 1
            print(out)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())

