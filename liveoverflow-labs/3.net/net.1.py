#!/usr/bin/env python3

from __future__ import annotations

import time
from pathlib import Path

from pwn import log, p32, process, remote, u32

PORT = 2998
SUCCESS = b"you correctly sent the data"


def main() -> int:
    prog = str(Path(__file__).resolve().with_name("net1"))

    srv = process([prog])
    time.sleep(0.1)

    io = remote("127.0.0.1", PORT)
    raw = io.recvn(4, timeout=2)
    wanted = u32(raw)
    io.sendline(str(wanted).encode())
    out = io.recvall(timeout=2)
    io.close()
    srv.wait_for_close(timeout=2)

    if SUCCESS in out:
        log.success("net1 solved")
        return 0
    log.failure("net1 failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
