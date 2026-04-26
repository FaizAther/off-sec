# OffSec Tooling Cheat Sheet (GDB/GEF + Vim + tmux + Python bytes + pwntools)

## Quick Reference for Exploit Dev Labs

---

## 🚀 GDB (everyday workflow)

### Launch / attach / core
```bash
gdb ./a.out
gdb --args ./a.out arg1 arg2
gdb -p <pid>
gdb ./a.out core
```

### Must-have settings
```gdb
set pagination off
set disassembly-flavor intel
set confirm off
```

### Break, run, step
```gdb
b main
b *0x401234
r
c
si
ni
finish
```

### Inspect state quickly
```gdb
info registers
bt
x/20gx $rsp
x/40wx $esp
x/16i $rip
p/x $rip
```

### Useful “info”
```gdb
info functions
info files
info proc mappings
info threads
```

### Common use-cases (recipes)

#### Catch crash + locate the bad write / RIP control
```gdb
run
bt
info registers
x/32gx $rsp
```

#### Find where a string is in memory
```gdb
find &__data_start__, +9999999, "AAAA"
```

#### Follow fork (targets that spawn)
```gdb
set follow-fork-mode child
set detach-on-fork off
```

#### Disable ASLR (local only)
```gdb
set disable-randomization on
```

---

## 🧩 GEF (GDB Enhanced Features)

### Install (typical)
```bash
# One-liner install (writes ~/.gdbinit)
bash -c "$(curl -fsSL https://gef.blah.cat/sh)"
```

### Startup sanity check
```gdb
gef config
help gef
```

### Everyday GEF commands
```gdb
context
context regs
context stack
vmmap
checksec
hexdump $rsp
pattern create 200
pattern search $rsp
```

### Use-cases + examples

#### Compute offset to RIP/EIP after a crash
```gdb
run $(python3 - <<'PY'
from pwn import cyclic
print(cyclic(400).decode())
PY
)

# after crash:
pattern search $rip
# (or $eip on 32-bit)
```

#### Identify memory region protections (NX/PIE/RELRO)
```gdb
checksec
vmmap
```

---

## ✍️ Vim (for exploit/dev + reversing)

### Fast navigation for “weird files”
```vim
:set number relativenumber
:set nowrap
:set list
:set hlsearch incsearch ignorecase smartcase
```

### Search patterns that come up a lot
```vim
/\v0x[0-9a-fA-F]+          " hex addresses
/\v[A-Za-z_]\w*\(          " function calls
/\v(%[0-9]+\$)?n           " printf %n and positional %<k>$n
```

### Block edits (stack traces, asm, hex dumps)
```
Ctrl+v   (select block)
I        (insert at left edge for all selected lines)
A        (append at right edge for all selected lines)
Esc      (apply)
```

### Hex view/edit quick workflow
```bash
xxd -g 1 -c 16 file.bin | vim -
```

---

## 🧱 tmux (repeatable exploit-dev layout)

### Essential session workflow
```bash
tmux new -s pwn
tmux attach -t pwn
tmux ls
```

### Pane layout for labs (common)
- Pane 1: editor (vim)
- Pane 2: build/run (make, gcc, python)
- Pane 3: debugger (gdb + GEF)
- Pane 4: notes / manpages

### Keys you’ll use constantly (prefix = Ctrl+b)
```
Ctrl+b "    split horizontal
Ctrl+b %    split vertical
Ctrl+b o    next pane
Ctrl+b z    zoom pane
Ctrl+b [    copy/scroll mode
Ctrl+b d    detach
```

### Use-case: re-run last command while watching debugger
- Keep compilation + program run in one pane, GDB attached in another.
- Use copy mode (`Ctrl+b [`) to scroll logs without breaking the running process.

---

## 🐍 Python bytes + binary parsing packages (stdlib-first)

### Core tools
- **`struct`**: pack/unpack integers with endianness
- **`int.to_bytes` / `int.from_bytes`**: quick conversions
- **`binascii`**: hexlify/unhexlify
- **`codecs`**: encoding/decoding helpers
- **`pathlib`**: reliable file paths

### Endianness + packing examples
```python
import struct, binascii

x = 0xdeadbeef
le32 = struct.pack("<I", x)          # b'\xef\xbe\xad\xde'
be32 = struct.pack(">I", x)

print(binascii.hexlify(le32))        # b'efbeadde'
print(struct.unpack("<I", le32)[0])  # 3735928559

print(x.to_bytes(4, "little"))
print(int.from_bytes(le32, "little"))
```

### Byte-string building patterns that don’t hurt you later
```python
payload = b""
payload += b"A" * 40
payload += (0x401016).to_bytes(8, "little")  # x86_64 return address
```

### “Print without breaking bytes”
```python
data = b"\x00\xffABC\n"
print(data)                 # bytes repr
print(data.hex())           # stable printable form
print(repr(data))
```

---

## 🧰 pwntools (Python pwn tools)

### Install (typical)
```bash
python3 -m pip install --user pwntools
```

### Minimal skeleton (local + remote)
```python
from pwn import *

context.binary = elf = ELF("./chall", checksec=False)
context.log_level = "info"

def start():
    if args.REMOTE:
        return remote("host", 31337)
    return process(elf.path)

p = start()
p.sendlineafter(b"> ", b"AAAA")
print(p.recvline())
```

### Packing/unpacking helpers (preferred over manual struct)
```python
from pwn import *

p32(0xdeadbeef)          # little-endian 32-bit
p64(0xdeadbeefcafebabe)  # little-endian 64-bit
u32(b"\xef\xbe\xad\xde")
u64(p64(0x1337))
```

### Generate + find cyclic offsets
```python
from pwn import *

pat = cyclic(400)
off = cyclic_find(0x6161616c)      # 32-bit value from EIP (little-endian)
off64 = cyclic_find(b"laaa")       # bytes from RIP
```

### Attach GDB quickly (with optional script)
```python
from pwn import *

p = process("./chall")
gdb.attach(p, gdbscript="""
set pagination off
b *main
c
""")
```

### ELF + symbols + GOT/PLT + libc base workflows
```python
from pwn import *

elf = ELF("./chall", checksec=False)
puts_plt = elf.plt["puts"]
puts_got = elf.got["puts"]
main = elf.symbols["main"]
```

### ROP chain basics
```python
from pwn import *

elf = ELF("./chall", checksec=False)
rop = ROP(elf)
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
```

### Format string helpers (use-case: overwrite a GOT entry / write-what-where)
```python
from pwn import *

# Example: write 0xdeadbeef to target address using a known offset
payload = fmtstr_payload(offset=6, writes={0x404050: 0xdeadbeef}, write_size="short")
```

---

## 🎯 Common lab use-cases (end-to-end patterns)

### Use-case: “Crash → offset → control RIP → test ret”
```python
from pwn import *

elf = context.binary = ELF("./chall", checksec=False)
p = process(elf.path)
p.sendline(cyclic(400))
p.wait()

core = p.corefile
off = cyclic_find(core.read(core.rsp, 8))
log.info("offset = %d", off)

payload = b"A"*off + p64(0x401016)
process(elf.path).sendline(payload)
```

### Use-case: “Leak a pointer, compute base, call win()”
```python
from pwn import *

elf = context.binary = ELF("./chall", checksec=False)
p = process(elf.path)

# Example placeholder: parse leak like "leak: 0x7ffff7dd18c0"
p.recvuntil(b"leak: ")
leak = int(p.recvline().strip(), 16)
log.info("leak = %#x", leak)

# You’d plug in the correct symbol/offset here (libc, PIE, etc.)
# base = leak - libc.symbols["puts"]
# win = base + <offset>
```

---

## 📚 Pointers to existing repo sheets
- `osed/2/resources/cheatsheets/gdb-essentials.md`
- `osed/2/resources/cheatsheets/vim-essentials.md`
- `osed/2/resources/cheatsheets/tmux-essentials.md`

---

**Version**: 1.0 | **Last Updated**: April 2026  
**For**: Exploit-dev labs (GDB/GEF + editing + bytes + pwntools)

