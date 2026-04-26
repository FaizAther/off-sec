#!/usr/bin/env python3

from __future__ import annotations

import re
import time
from pathlib import Path

from pwn import log, p32, process, remote

PORT = 2999
SUCCESS = b"Thank you"


def main() -> int:
    prog = str(Path(__file__).resolve().with_name("net0"))

    # Start server (accepts one client and exits).
    srv = process([prog])
    time.sleep(0.1)

    io = remote("127.0.0.1", PORT)
    banner = io.recvline(timeout=2) + io.recvline(timeout=0.2)
    m = re.search(rb"Please send '(\d+)'", banner)
    if not m:
        log.failure("failed to parse wanted from banner")
        log.info(banner.decode("latin-1", "replace"))
        io.close()
        srv.close()
        return 2
    wanted = int(m.group(1))
    io.send(p32(wanted))
    out = io.recvall(timeout=2)
    io.close()
    srv.wait_for_close(timeout=2)

    if SUCCESS in out:
        log.success("net0 solved")
        return 0
    log.failure("net0 failed")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
