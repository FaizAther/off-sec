# ARM Assembly Cheat Sheet (ARMv7 + AArch64)

## Quick Reference for Exploit Dev / Reversing

---

## 🧠 Big picture: ARM vs x86
- **ARM is load/store**: most operations work on registers; memory is accessed via explicit loads/stores.
- **AArch64 (ARM64)** has more registers and cleaner rules than ARMv7.
- **Calling conventions matter** a lot when building ROP chains or understanding function args/returns.

---

## 🎯 AArch64 (ARM64) registers

### General purpose
| Name | Notes |
|------|------|
| **X0–X7** | Function args (0..7) |
| **X0** | Return value |
| **X8** | Often syscall number register on Linux (see syscalls section) |
| **X9–X15** | Scratch/temporaries |
| **X19–X28** | Callee-saved (non-volatile) |
| **X29** | Frame pointer (**FP**) |
| **X30** | Link register (**LR**) |
| **SP** | Stack pointer |
| **PC** | Program counter (not directly writable like a GPR) |

### 32-bit views
- **Wn** is the low 32-bits of **Xn** (e.g. `W0` is low 32 of `X0`).

---

## 📞 AArch64 calling convention (AAPCS64)

- **Args**: `X0–X7` (additional args spilled to stack)
- **Return**: `X0` (and sometimes `X1` for large returns)
- **Callee-saved**: `X19–X28`, `FP (X29)`, `LR (X30)` is saved by the callee if it needs to call other functions
- **Stack alignment**: **16-byte aligned**

Example: `puts("hi")` (conceptual)
```asm
adrp x0, msg@PAGE
add  x0, x0, msg@PAGEOFF
bl   puts

msg: .asciz "hi"
```

---

## 🧱 AArch64 function prologue/epilogue (common pattern)

### Prologue
```asm
stp x29, x30, [sp, #-0x10]!
mov x29, sp
sub sp, sp, #0x20
```

### Epilogue
```asm
add sp, sp, #0x20
ldp x29, x30, [sp], #0x10
ret
```

Notes:
- `stp/ldp` store/load pairs (common for saving FP/LR).
- `ret` returns to `LR` (X30) by default.

---

## 📊 AArch64 data movement (loads/stores)

```asm
ldr x0, [x1]          ; x0 = *(uint64*)x1
ldr w0, [x1]          ; w0 = *(uint32*)x1
str x0, [x1]          ; *(uint64*)x1 = x0

ldr x0, [x1, #0x20]   ; base + immediate offset
ldr x0, [x1, x2]      ; base + register offset
ldr x0, [x1, x2, lsl #3] ; base + (x2 << 3) (scaled index)
```

Common addressing forms:
- `[base, #imm]`
- `[base, reg]`
- `[base, reg, lsl #k]` (scaled indexing)

---

## ➕ AArch64 arithmetic / logic

```asm
add x0, x1, x2        ; x0 = x1 + x2
sub x0, x1, #0x10     ; x0 = x1 - 0x10
and x0, x1, x2
orr x0, x1, x2
eor x0, x1, x2        ; xor

lsl x0, x1, #3        ; shift left
lsr x0, x1, #1        ; logical shift right
asr x0, x1, #1        ; arithmetic shift right
```

---

## 🔄 AArch64 control flow

```asm
b   label             ; unconditional branch
bl  func              ; branch-with-link (sets LR = return address)
ret                   ; return (uses LR)

cmp x0, #0
beq zero
bne nonzero

cbz x0, is_zero       ; compare-and-branch-if-zero
cbnz x0, not_zero
```

Conditional branches use flags set by `cmp` / arithmetic instructions.

---

## 🧨 AArch64 syscalls (Linux)

Linux AArch64 convention:
- **Syscall number**: `X8`
- **Args**: `X0–X5`
- **Return**: `X0`
- Instruction: `svc #0`

Example: `exit(0)` (syscall 93)
```asm
mov x8, #93
mov x0, #0
svc #0
```

Example: `write(1, buf, len)` (syscall 64)
```asm
mov x8, #64
mov x0, #1           ; fd
mov x1, x2           ; buf pointer in x2 (example)
mov x2, #3           ; len
svc #0
```

---

## 🎯 ARMv7 (32-bit ARM) registers

| Register | Notes |
|----------|------|
| **R0–R3** | Function args, scratch |
| **R0** | Return value |
| **R4–R11** | Callee-saved (non-volatile) |
| **R12** | Intra-procedure scratch (IP) |
| **R13** | Stack pointer (**SP**) |
| **R14** | Link register (**LR**) |
| **R15** | Program counter (**PC**) |

---

## 📞 ARMv7 calling convention (AAPCS)

- **Args**: `R0–R3`, extra args on stack
- **Return**: `R0`
- **Callee-saved**: `R4–R11` (and `LR` if needed)
- **Stack alignment**: typically 8-byte aligned (varies by ABI/platform)

---

## 🧱 ARMv7 prologue/epilogue (common)

```asm
push {r4, r5, r11, lr}
add  r11, sp, #0
sub  sp, sp, #0x20

; ...

add  sp, sp, #0x20
pop  {r4, r5, r11, pc}
```

Notes:
- `pop {..., pc}` returns by restoring `PC` (common epilogue idiom).

---

## 📊 ARMv7 loads/stores (the core of ARM)

```asm
ldr r0, [r1]          ; r0 = *(uint32*)r1
str r0, [r1]          ; *(uint32*)r1 = r0

ldr r0, [r1, #4]      ; base + imm
ldr r0, [r1, r2]      ; base + reg
ldr r0, [r1, r2, lsl #2] ; scaled index
```

Byte/halfword variants:
```asm
ldrb r0, [r1]         ; load byte (zero-extend)
ldrh r0, [r1]         ; load halfword (zero-extend)
strb r0, [r1]
strh r0, [r1]
```

---

## 🔄 ARMv7 control flow

```asm
b   label
bl  func              ; sets LR
bx  lr                ; return (branch to LR)

cmp r0, #0
beq zero
bne nonzero
```

---

## 🧨 ARMv7 syscalls (Linux EABI)

Linux ARM EABI convention:
- **Syscall number**: `R7`
- **Args**: `R0–R6`
- **Return**: `R0`
- Instruction: `svc #0` (older docs may show `swi 0`)

Example: `exit(0)` (syscall 1)
```asm
mov r7, #1
mov r0, #0
svc #0
```

---

## 🧩 Exploit-dev patterns you’ll see on ARM

### Link register (LR) is part of the “return”
- On many ARM binaries, corrupting saved **LR** (ARMv7) or saved **X30** (AArch64) is analogous to smashing a saved return address on x86.

### Gadgets often end in `ret` / `bx lr` / `pop {..., pc}`
- ARMv7 “return gadgets” frequently use `pop {…, pc}`.
- AArch64 often uses `ret` (implicit LR) or `ret xN` (return to register).

### Thumb vs ARM mode (ARMv7)
- Some binaries use Thumb mode. The low bit of a function pointer can indicate Thumb (`addr | 1`).
- Disassembly and gadget selection depends on mode.

---

## 💡 Pro tips (debugging/reversing)
- When tracking arguments, first locate the call site and watch **arg registers** (`R0–R3` or `X0–X7`).
- For stack frames, find where **FP/LR** are saved (`push {..., lr}` or `stp x29, x30, ...`).
- On AArch64, many constants are built using `adrp/add` or `movz/movk` sequences.

---

**Version**: 1.0 | **Last Updated**: April 2026  
**For**: ARMv7 + AArch64 reversing / exploit dev

