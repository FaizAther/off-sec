# Python for Exploit Dev (bytes, processes, parsing, tooling)

## High-signal patterns you’ll reuse constantly

---

## 🧱 Bytes, ints, endianness (the core)

### `struct` (correct, explicit, fast)
Use `struct` when you’re modeling C types (u32/u64, headers, stack values). The format string (`<` little-endian, `>` big-endian) makes intent explicit and prevents “wrong endian” bugs.

```python
import struct

struct.pack("<I", 0x41424344)     # little-endian u32
struct.pack(">Q", 0x1337)         # big-endian u64

val = struct.unpack("<Q", b"\x01\x00\x00\x00\x00\x00\x00\x00")[0]
```

### `int.to_bytes` / `int.from_bytes` (simple conversions)
This is great for quick packing/unpacking without remembering format strings. Use `signed=` correctly if the target treats values as signed.

```python
x = 0xdeadbeef
b = x.to_bytes(4, "little", signed=False)
y = int.from_bytes(b, "little", signed=False)
```

### Never “accidentally str”
Exploit payloads should stay as `bytes`. Printing `.hex()` avoids terminal/control characters and makes diffs stable.

```python
payload = b"A" * 32 + b"\x00" + b"B" * 8
print(payload.hex())
```

---

## 🧰 Binary parsing patterns

### Read exact N bytes (file)
Good for parsing binaries or saving “known good” blobs. `Path.read_bytes()` is a simple, reliable one-liner.

```python
from pathlib import Path

data = Path("blob.bin").read_bytes()
magic = data[:4]
```

### Parse a C-style struct from bytes
The key idea: slice out the exact bytes for your struct fields, then `struct.unpack()` them in one shot.

```python
import struct

hdr = b"\x7fELF" + b"\x02" * 12
magic, klass = hdr[:4], hdr[4]

# Example: parse two u32 little-endian fields
buf = b"\x01\x00\x00\x00\xff\x00\x00\x00"
a, b = struct.unpack("<II", buf)
```

### Safe slicing helper
Use this when parsing: it turns silent truncation bugs into loud failures.

```python
def take(buf: bytes, off: int, n: int) -> bytes:
    out = buf[off:off+n]
    if len(out) != n:
        raise ValueError("short read")
    return out
```

---

## 🧪 Processes: `subprocess` done right

### Run a command, capture output, fail loudly
This is a “pwntools-free” way to run targets in scripts:
- `stdout=PIPE` captures output for parsing
- `stderr=STDOUT` merges errors into the same stream
- `timeout=` prevents infinite hangs

```python
import subprocess

cp = subprocess.run(
    ["./chall", "AAAA"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=False,
    check=False,
    timeout=2,
)
out = cp.stdout
```

### Pipe data in (stdin)
Use this when the program expects stdin input (menus, network-style services). `Popen` gives you streaming I/O, unlike `run()` which is one-shot.

```python
import subprocess

p = subprocess.Popen(
    ["./chall"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
)
p.stdin.write(b"AAAA\n")
p.stdin.flush()
line = p.stdout.readline()
```

---

## 🧵 Networking (raw sockets) — when you don’t want dependencies

This is the lowest-friction “talk TCP” option. It won’t handle prompts/parsing for you, so you’ll usually add a small recv loop and delimiters.

```python
import socket

with socket.create_connection(("127.0.0.1", 31337), timeout=2) as s:
    s.sendall(b"hello\n")
    data = s.recv(4096)
```

---

## 🧾 Parsing leaks reliably (regex + strict conversions)

Leaked pointers show up in messy output. Regex is a fast way to find `0x...` anywhere in a line, then `int(..., 16)` turns it into a real integer you can subtract offsets from.

```python
import re

line = b"leak: 0x7ffff7dd18c0\n"
m = re.search(rb"0x[0-9a-fA-F]+", line)
if not m:
    raise ValueError("no hex in line")
leak = int(m.group(0), 16)
```

---

## 🧠 “Exploit script hygiene”

### `argparse` with common flags
If you’re not using pwntools’ `args`, `argparse` gives you a predictable interface (remote host/port, optional GDB mode, etc.).

```python
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--remote", action="store_true")
ap.add_argument("--host", default="127.0.0.1")
ap.add_argument("--port", type=int, default=31337)
ap.add_argument("--gdb", action="store_true")
args = ap.parse_args()
```

### Logging that doesn’t get in your way
Prefer short logs over `print()`: easy to toggle verbosity, and it’s clearer when parsing output vs. debug output.

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger("pwn")
log.info("starting")
```

---

## 🔁 “Complex” byte-building helpers you actually want

### Pack helpers (stdlib-only)
These mirror pwntools’ `p32/p64/u32/u64` and are handy when you want zero dependencies. Masking keeps values in-range.

```python
import struct

def p32(x: int) -> bytes: return struct.pack("<I", x & 0xffffffff)
def p64(x: int) -> bytes: return struct.pack("<Q", x & 0xffffffffffffffff)
def u32(b: bytes) -> int: return struct.unpack("<I", b[:4])[0]
def u64(b: bytes) -> int: return struct.unpack("<Q", b[:8])[0]
```

### Build a ROP-like payload without pwntools
This `flat()` accepts a mix of `bytes` and integers and concatenates them. The example assumes 64-bit; swap to `p32` for 32-bit.

```python
def flat(*parts) -> bytes:
    out = b""
    for p in parts:
        if isinstance(p, (bytes, bytearray)):
            out += bytes(p)
        elif isinstance(p, int):
            out += p64(p)  # assume 64-bit
        else:
            raise TypeError(type(p))
    return out

payload = flat(b"A"*40, 0x401016, 0x4011aa, 0x404018)
```

---

## 🧩 Testing assumptions (fast sanity checks)

### Check offsets, sizes, and alignment
Small asserts prevent you from spending 30 minutes debugging a typo in an offset or an address width mismatch.

```python
assert len(b"A"*40) == 40
assert (0x401016).to_bytes(8, "little")[0] == 0x16
```

### Print “binary safe” debug output
When payloads include NULs and non-printables, a hexdump is the fastest “what did I actually send?” check.

```python
def hexdump(b: bytes, width=16) -> str:
    out = []
    for i in range(0, len(b), width):
        chunk = b[i:i+width]
        hexs = " ".join(f"{x:02x}" for x in chunk)
        out.append(f"{i:04x}: {hexs}")
    return "\n".join(out)

print(hexdump(payload))
```

---

## 📚 Commonly useful stdlib modules (exploit dev)
- **`struct`**: pack/unpack
- **`subprocess`**: run/pipe programs
- **`re`**: parse leaks
- **`socket`**: raw net I/O
- **`pathlib`**: path-safe files
- **`tempfile`**: generate scripts (gdb, etc.)
- **`ctypes`**: quick ABI poking / packing edge cases

---

**Version**: 1.0 | **Last Updated**: April 2026  
**For**: exploit-dev Python scripts (stdlib + good habits)

