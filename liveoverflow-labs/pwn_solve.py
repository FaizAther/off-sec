#!/usr/bin/env python3
"""
Host-side helpers for solving the labs with pwntools.

Design:
- Compile binaries inside the `liveoverflow-pwn` container (Ubuntu 14.04, gcc-multilib).
- Drive the binaries from the host using pwntools, by spawning:
    docker exec -i liveoverflow-pwn <program> ...

This avoids fighting pwntools install on Python 3.4 inside the container.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from pwn import context


REPO_ROOT = Path(__file__).resolve().parents[1]
LABS_ROOT = REPO_ROOT / "liveoverflow-labs"
CONTAINER = "liveoverflow-pwn"


def docker_exec(argv: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    cmd = ["docker", "exec", "-i", CONTAINER] + argv
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check, text=True)


def docker_exec_shell(cmd: str, *, check: bool = True) -> subprocess.CompletedProcess:
    return docker_exec(["bash", "-lc", cmd], check=check)


def compile_in_container(workdir_rel: str, out_name: str, sources: list[str], extra_cflags: list[str] | None = None) -> Path:
    """
    Compile into the mounted repo path (so the host can read the ELF for symbols/GOT).
    """
    extra = " ".join(extra_cflags or [])
    srcs = " ".join(sources)
    cmd = (
        f"cd /home/pwner/labs/{workdir_rel} && "
        f"gcc -m32 -g -fno-stack-protector -z execstack {extra} -o {out_name} {srcs}"
    )
    cp = docker_exec_shell(cmd, check=True)
    if cp.stdout.strip():
        print(cp.stdout, end="" if cp.stdout.endswith("\n") else "\n")
    out_path = LABS_ROOT / workdir_rel / out_name
    if not out_path.exists():
        raise FileNotFoundError(out_path)
    return out_path


def set_pwn_context():
    # Keep output readable; can be overridden per-solver.
    context.log_level = os.environ.get("PWN_LOG_LEVEL", "error")
    context.terminal = ["bash", "-lc"]


def docker_execve_argv(
    program_path: str,
    argv_bytes: list[bytes],
    *,
    cwd: str | None = None,
    tty: bool = False,
) -> list[bytes]:
    """
    Return a `docker exec ... python3 -c ...` argv that will execve() the target
    with byte-exact argv entries inside the container.

    This avoids Docker CLI / locale issues with non-ASCII bytes in arguments.
    """
    import base64

    b64_args = [base64.b64encode(a).decode("ascii") for a in argv_bytes]
    b64_prog = base64.b64encode(program_path.encode("utf-8")).decode("ascii")
    b64_cwd = base64.b64encode((cwd or "").encode("utf-8")).decode("ascii")

    py = (
        "import os,base64,sys;"
        "prog=base64.b64decode('" + b64_prog + "');"
        "cwd=base64.b64decode('" + b64_cwd + "').decode('utf-8','ignore');"
        "args=[base64.b64decode(s) for s in " + repr(b64_args) + "];"
        "env=os.environ.copy();"
        "sys.stdout.flush();"
        "sys.stderr.flush();"
        "os.chdir(cwd) if cwd else None;"
        "os.execve(prog, args, env)"
    )

    cmd = [b"docker", b"exec", b"-i"]
    if tty:
        cmd.append(b"-t")
    cmd += [CONTAINER.encode("ascii"), b"python3", b"-c", py.encode("utf-8")]
    return cmd

