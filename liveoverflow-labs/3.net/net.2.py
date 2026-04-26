#!/usr/bin/env python3

from __future__ import annotations

import time
from pathlib import Path

from pwn import log, p32, process, remote, u32

PORT = 2997
SUCCESS = b"you added them correctly"


def main() -> int:
    prog = str(Path(__file__).resolve().with_name("net2"))

    srv = process([prog])
    time.sleep(0.1)

    io = remote("127.0.0.1", PORT)
    nums = [u32(io.recvn(4, timeout=2)) for _ in range(4)]
    total = sum(nums) & 0xFFFFFFFF
    io.send(p32(total))
    out = io.recvall(timeout=2)
    io.close()
    srv.wait_for_close(timeout=2)

    if SUCCESS in out:
        log.success("net2 solved")
        return 0
    log.failure("net2 failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
