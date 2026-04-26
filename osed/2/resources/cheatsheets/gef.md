# GEF Cheat Sheet (usage + “GEF Python” via GDB Python)

## Notes
- GEF is a **GDB plugin**. You can use it like normal GDB, plus GEF commands.
- “GEF Python” in practice usually means: **write GDB Python commands** (works with or without GEF), and optionally take advantage of GEF’s nicer context while you debug.
- GEF’s internal Python APIs can change between versions; the most stable path is **GDB’s Python API**.

---

## 🚀 Install / update / verify

### Install (typical one-liner)
This downloads a single `gef.py` and wires it into your GDB startup (usually by writing a `source ...` line into `~/.gdbinit`). After install, new GDB sessions should automatically have GEF commands.

```bash
bash -c "$(curl -fsSL https://gef.blah.cat/sh)"
```

### Verify inside GDB
If these commands work, GEF is loaded. If `help gef` fails, your `.gdbinit` isn’t sourcing GEF or GDB is starting with `-nx`.

```gdb
help gef
gef config
context
```

---

## 🧭 Everyday GEF commands (high-signal)

### Context + focused views
`context` is the main “what’s going on right now?” view. The subviews let you reduce noise when you only care about regs/stack/code.

```gdb
context
context regs
context stack
context code
```

### Memory maps + protections
Use these early. They answer: PIE? NX? RELRO? where are the mappings? which regions are RWX? where is libc?

```gdb
vmmap
checksec
```

### Stack/memory helpers
`hexdump` gives raw bytes; `dereference` tries to follow pointers and annotate them (great for stack frames and saved RIP chains).

```gdb
hexdump $rsp
dereference $rsp
```

### Patterns (offset finding)
GEF’s pattern tools are for turning “I crashed” into an exact overwrite offset:
- `pattern create N` generates a unique cyclic string
- `pattern search $rip` tells you which offset ended up in RIP/EIP

```gdb
pattern create 400
pattern search $rip
pattern search $rsp
```

### Searching memory
This is handy when you suspect your input is in memory (e.g. after `read()`, `gets()`, `recv()`), or when hunting for known strings/markers.

```gdb
search-pattern AAAA
search-pattern 0x41414141
```

---

## 🎯 Common workflows (recipes)

### Workflow: overflow → crash → offset → validate control
1) Send cyclic pattern.
2) Crash.
3) Use `pattern search` on `RIP/EIP` (or stack) to get offset.

Example (conceptual):
This example runs the program with a cyclic pattern generated on the fly, then (after the crash) you search RIP for the offset. Replace `$rip` with `$eip` for 32-bit.

```gdb
run $(python3 - <<'PY'
from pwn import cyclic
print(cyclic(600).decode())
PY
)

# crash, then:
pattern search $rip
```

### Workflow: “what’s mapped, what’s executable, where’s libc?”
This is your “mitigations + base addresses” triage sequence. In practice you’ll use the output to:
- decide between shellcode vs ROP (NX)
- compute PIE base (PIE)
- identify libc base (leaks + mappings)

```gdb
checksec
vmmap
info proc mappings
```

---

## 🐍 GDB Python: writing your own commands (works with GEF installed)

### Minimal custom command template
Create `~/.gdbinit.d/mycmd.py` (or any file you `source`) with:

This defines a new command you can call from the GDB prompt. The key pieces:
- subclass `gdb.Command`
- choose a name (`"mycmd"`)
- implement `invoke()`

```python
import gdb

class MyCmd(gdb.Command):
    """mycmd: example custom GDB command"""

    def __init__(self):
        super().__init__("mycmd", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        gdb.write("Hello from GDB Python!\n")

MyCmd()
```

Then in GDB:
`source` loads the Python file into the current session. If you want it always loaded, you can add a `source ...` line in your `.gdbinit` (or a per-project `.gdbinit`).

```gdb
source ~/.gdbinit.d/mycmd.py
mycmd
```

---

## 🧩 “Complex” GDB Python examples (useful in exploit dev)

### 1) Print mappings in a cleaner way
Why: GDB’s mapping output varies by distro/version and can be noisy. This command filters for lines that look like address ranges so you can eyeball base addresses faster.

```python
import gdb
import re

class Mappings(gdb.Command):
    """mappings: print /proc/<pid>/maps-like output via GDB"""

    def __init__(self):
        super().__init__("mappings", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        try:
            out = gdb.execute("info proc mappings", to_string=True)
        except gdb.error as e:
            gdb.write(f"error: {e}\n")
            return

        # GDB output varies; keep it simple: just echo lines that look like mappings.
        for line in out.splitlines():
            if re.search(r"0x[0-9a-fA-F]+\s+0x[0-9a-fA-F]+", line):
                gdb.write(line + "\n")

Mappings()
```

Usage:
Put the script in your working dir and source it per target.

```gdb
source mappings.py
mappings
```

### 2) Hexdump an address range (`hd <addr> <len>`)
Why: `x/` in GDB is powerful but fiddly. This gives you a predictable hexdump with ASCII, good for payload verification and stack inspection.

```python
import gdb

class HD(gdb.Command):
    """hd <addr> <len>: hexdump memory with fixed formatting"""

    def __init__(self):
        super().__init__("hd", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        argv = arg.split()
        if len(argv) != 2:
            gdb.write("usage: hd <addr> <len>\n")
            return

        addr = int(gdb.parse_and_eval(argv[0]))
        n = int(gdb.parse_and_eval(argv[1]))

        inferior = gdb.selected_inferior()
        mem = inferior.read_memory(addr, n).tobytes()

        width = 16
        for i in range(0, len(mem), width):
            chunk = mem[i:i+width]
            hexs = " ".join(f"{b:02x}" for b in chunk)
            asc = "".join(chr(b) if 32 <= b < 127 else "." for b in chunk)
            gdb.write(f"{addr+i:016x}  {hexs:<47}  |{asc}|\n")

HD()
```

Usage:
Examples:
- `hd $rsp 128` dumps the top of the stack
- `hd $rip 64` is useful if you have an executable mapping and want to see bytes at an address (but usually `x/i` is better for code)

```gdb
hd $rsp 128
```

### 3) Resolve a symbol quickly (`symaddr puts`)
Why: When symbols exist (non-stripped, or loaded from libc), this turns “what is the address of X right now?” into a one-liner.

```python
import gdb

class SymAddr(gdb.Command):
    """symaddr <name>: print address of symbol if resolvable"""

    def __init__(self):
        super().__init__("symaddr", gdb.COMMAND_USER)

    def invoke(self, arg, from_tty):
        name = arg.strip()
        if not name:
            gdb.write("usage: symaddr <symbol>\n")
            return
        try:
            v = gdb.parse_and_eval(name)
            gdb.write(f"{name} = {int(v):#x}\n")
        except gdb.error as e:
            gdb.write(f"error: {e}\n")

SymAddr()
```

Usage:
If the symbol can’t be resolved, you’ll see a GDB Python error (e.g. stripped binary without symbols).

```gdb
symaddr main
symaddr puts
```

---

## 🧰 Hooking execution (breakpoints + stop events)

### Print registers automatically on every stop
This is a tiny “stop hook” that triggers on any breakpoint, single-step, or signal stop. It’s useful when you’re doing repetitive stepping and want registers printed without re-typing commands.

```python
import gdb

def on_stop(event):
    try:
        regs = gdb.execute("info registers", to_string=True)
        gdb.write("\n--- STOP ---\n")
        gdb.write(regs + "\n")
    except gdb.error:
        pass

gdb.events.stop.connect(on_stop)
```

Tip: If this gets noisy, only print on specific breakpoints or when `RIP` changes into a range you care about.

---

## 🧪 “GEF + Python” practical approach

### Recommended layout
- Use **GEF for interactive triage**: `context`, `vmmap`, `checksec`, `pattern search`
- Use **GDB Python for repeatability**: small commands like `hd`, `symaddr`, stop hooks
- Keep your Python scripts in a folder and `source` them per target

---

**Version**: 1.0 | **Last Updated**: April 2026  
**For**: GDB + GEF users who want Python automation

