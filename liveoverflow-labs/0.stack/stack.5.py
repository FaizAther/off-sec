#!/usr/bin/env python3
# Python 3.4+ compatible helper patterns.
import os, sys, stat, subprocess, tempfile
from pathlib import Path

def which(cmd):
    for d in os.environ.get("PATH", "").split(os.pathsep):
        p = str(Path(d) / cmd)
        if os.path.exists(p) and os.access(p, os.X_OK):
            return p
    return None

def ensure_executable(p):
    st = p.stat()
    if st.st_mode & stat.S_IXUSR:
        return
    p.chmod(st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

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

def gcc_build(out_path, src_path, extra=None):
    cc = which("gcc")
    if not cc:
        return False, "gcc not found\n"
    cmd = [cc, "-g", "-fno-stack-protector", "-z", "execstack", "-no-pie", "-o", str(out_path), str(src_path)]
    if extra:
        cmd[1:1] = extra
    rc, out = run_capture(cmd)
    return rc == 0 and Path(out_path).exists(), out

def main():
    here = Path(__file__).resolve().parent
    src = here / "stack.5.c"
    outbin = here / "stack5"
    ok, out = gcc_build(outbin, src)
    sys.stdout.write(out)
    if not ok:
        return 2
    ensure_executable(outbin)
    print("[!] TODO: exploit automation not yet generated for this level.")
    print("    Use GDB to compute offsets/addresses, then update this script.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
