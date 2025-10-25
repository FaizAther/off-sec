# x86 Assembly Cheat Sheet

## Quick Reference for OSED Section 2

---

## 🎯 Registers (32-bit)

### General Purpose Registers

| Register | Purpose | Common Use |
|----------|---------|------------|
| **EAX** | Accumulator | Return values, arithmetic |
| **EBX** | Base | Base pointer for memory |
| **ECX** | Counter | Loop counter, shift operations |
| **EDX** | Data | I/O operations, large multiplications |
| **ESI** | Source Index | String/array source |
| **EDI** | Destination Index | String/array destination |
| **EBP** | Base Pointer | Stack frame base |
| **ESP** | Stack Pointer | Top of stack |
| **EIP** | Instruction Pointer | Next instruction address |

### 16-bit and 8-bit Subdivisions
```
32-bit: EAX
16-bit:  AX  (lower 16 bits of EAX)
8-bit :  AH  (high byte of AX)  |  AL  (low byte of AX)
```

### Segment Registers

| Register | Purpose |
|----------|---------|
| **CS** | Code Segment |
| **DS** | Data Segment |
| **SS** | Stack Segment |
| **ES** | Extra Segment |
| **FS** | Extra Segment (TEB in Windows) |
| **GS** | Extra Segment (used in 64-bit) |

### EFLAGS Register

| Flag | Bit | Name | Purpose |
|------|-----|------|---------|
| **CF** | 0 | Carry | Unsigned overflow |
| **PF** | 2 | Parity | Even parity |
| **AF** | 4 | Adjust | BCD arithmetic |
| **ZF** | 6 | Zero | Result is zero |
| **SF** | 7 | Sign | Result is negative |
| **TF** | 8 | Trap | Single-step debugging |
| **IF** | 9 | Interrupt | Interrupts enabled |
| **DF** | 10 | Direction | String operation direction |
| **OF** | 11 | Overflow | Signed overflow |

---

## 📊 Data Movement Instructions

### MOV - Move Data
```asm
mov eax, ebx        ; eax = ebx
mov eax, 0x42       ; eax = 0x42
mov eax, [ebx]      ; eax = *ebx (load from memory)
mov [ebx], eax      ; *ebx = eax (store to memory)
mov eax, [ebx+4]    ; eax = *(ebx+4)
```

### LEA - Load Effective Address
```asm
lea eax, [ebx+8]    ; eax = ebx + 8 (address calculation, no memory access)
lea eax, [ebx+ecx*4] ; eax = ebx + (ecx * 4)
```

### MOVZX/MOVSX - Move with Zero/Sign Extend
```asm
movzx eax, bl       ; Move byte to dword, zero-extend
movsx eax, bl       ; Move byte to dword, sign-extend
```

### XCHG - Exchange
```asm
xchg eax, ebx       ; Swap eax and ebx
```

---

## ➕ Arithmetic Instructions

### ADD/SUB - Addition/Subtraction
```asm
add eax, ebx        ; eax = eax + ebx
add eax, 5          ; eax = eax + 5
sub eax, ebx        ; eax = eax - ebx
sub eax, 10         ; eax = eax - 10
```

### INC/DEC - Increment/Decrement
```asm
inc eax             ; eax = eax + 1
dec eax             ; eax = eax - 1
```

### MUL/IMUL - Multiplication
```asm
mul ebx             ; EDX:EAX = EAX * EBX (unsigned)
imul ebx            ; EDX:EAX = EAX * EBX (signed)
imul eax, ebx       ; eax = eax * ebx
imul eax, ebx, 10   ; eax = ebx * 10
```

### DIV/IDIV - Division
```asm
div ebx             ; EAX = EDX:EAX / EBX, EDX = remainder (unsigned)
idiv ebx            ; EAX = EDX:EAX / EBX, EDX = remainder (signed)
```

### NEG - Negate
```asm
neg eax             ; eax = -eax (two's complement)
```

---

## 🔀 Bitwise/Logical Instructions

### AND/OR/XOR
```asm
and eax, ebx        ; eax = eax & ebx (bitwise AND)
or eax, ebx         ; eax = eax | ebx (bitwise OR)
xor eax, ebx        ; eax = eax ^ ebx (bitwise XOR)
xor eax, eax        ; eax = 0 (common idiom to zero register)
```

### NOT - Bitwise NOT
```asm
not eax             ; eax = ~eax (one's complement)
```

### TEST - Logical Compare
```asm
test eax, eax       ; Set flags based on eax & eax (doesn't modify eax)
test eax, ebx       ; Set flags based on eax & ebx
```

### Shift Instructions
```asm
shl eax, 1          ; Shift left (multiply by 2)
shr eax, 1          ; Shift right (unsigned divide by 2)
sal eax, 1          ; Shift arithmetic left (same as shl)
sar eax, 1          ; Shift arithmetic right (signed divide by 2)
```

### Rotate Instructions
```asm
rol eax, 1          ; Rotate left
ror eax, 1          ; Rotate right
rcl eax, 1          ; Rotate through carry left
rcr eax, 1          ; Rotate through carry right
```

---

## 🔄 Control Flow Instructions

### JMP - Unconditional Jump
```asm
jmp label           ; Jump to label
jmp eax             ; Jump to address in eax
jmp [eax]           ; Jump to address stored at eax
jmp short label     ; Short jump (1-byte offset)
```

### Conditional Jumps

#### Unsigned Comparisons
```asm
ja/jnbe             ; Jump if above (CF=0 and ZF=0)
jae/jnb/jnc         ; Jump if above or equal (CF=0)
jb/jnae/jc          ; Jump if below (CF=1)
jbe/jna             ; Jump if below or equal (CF=1 or ZF=1)
```

#### Signed Comparisons
```asm
jg/jnle             ; Jump if greater (ZF=0 and SF=OF)
jge/jnl             ; Jump if greater or equal (SF=OF)
jl/jnge             ; Jump if less (SF≠OF)
jle/jng             ; Jump if less or equal (ZF=1 or SF≠OF)
```

#### Equality
```asm
je/jz               ; Jump if equal/zero (ZF=1)
jne/jnz             ; Jump if not equal/not zero (ZF=0)
```

#### Flag-Based
```asm
jc                  ; Jump if carry (CF=1)
jnc                 ; Jump if no carry (CF=0)
jo                  ; Jump if overflow (OF=1)
jno                 ; Jump if no overflow (OF=0)
js                  ; Jump if sign (SF=1)
jns                 ; Jump if no sign (SF=0)
jp/jpe              ; Jump if parity even
jnp/jpo             ; Jump if parity odd
```

### CMP - Compare
```asm
cmp eax, ebx        ; Compare eax with ebx (sets flags)
cmp eax, 42         ; Compare eax with 42
```

### Loop Instructions
```asm
loop label          ; Decrement ecx, jump if ecx != 0
loope/loopz label   ; Loop while equal/zero (and ecx != 0)
loopne/loopnz label ; Loop while not equal/not zero (and ecx != 0)
```

---

## 📞 Function Call Instructions

### CALL/RET - Function Calls
```asm
call function       ; Push EIP, jump to function
call eax            ; Call function at address in eax
call [eax]          ; Call function at address stored at eax
ret                 ; Pop EIP (return from function)
ret 0x10            ; Return and clean 0x10 bytes from stack
```

### PUSH/POP - Stack Operations
```asm
push eax            ; ESP -= 4; [ESP] = EAX
push 0x42           ; Push immediate value
pop eax             ; EAX = [ESP]; ESP += 4
pushad              ; Push all general purpose registers
popad               ; Pop all general purpose registers
pushfd              ; Push EFLAGS
popfd               ; Pop EFLAGS
```

---

## 📝 String Instructions

All string instructions use ESI (source) and EDI (destination). Direction controlled by DF flag (CLD = forward, STD = backward).

### MOVS - Move String
```asm
movsb               ; Move byte [ESI] to [EDI]
movsw               ; Move word
movsd               ; Move dword
rep movsd           ; Repeat ECX times
```

### STOS - Store String
```asm
stosb               ; Store AL at [EDI]
stosw               ; Store AX at [EDI]
stosd               ; Store EAX at [EDI]
rep stosd           ; Repeat ECX times
```

### LODS - Load String
```asm
lodsb               ; Load byte from [ESI] to AL
lodsw               ; Load word to AX
lodsd               ; Load dword to EAX
```

### SCAS - Scan String
```asm
scasb               ; Compare AL with [EDI]
scasw               ; Compare AX with [EDI]
scasd               ; Compare EAX with [EDI]
repne scasb         ; Scan while not equal (find character)
```

### CMPS - Compare String
```asm
cmpsb               ; Compare [ESI] with [EDI]
cmpsw               ; Compare words
cmpsd               ; Compare dwords
repe cmpsd          ; Compare while equal
```

### REP Prefixes
```asm
rep                 ; Repeat ECX times
repe/repz           ; Repeat while equal/zero
repne/repnz         ; Repeat while not equal/not zero
```

---

## 🎚️ Special Instructions

### NOP - No Operation
```asm
nop                 ; Do nothing (0x90)
```

### HLT - Halt
```asm
hlt                 ; Halt processor (privileged)
```

### INT - Software Interrupt
```asm
int 0x80            ; Linux system call (32-bit)
int 0x2e            ; Windows system call (old)
int 3               ; Breakpoint (0xCC)
```

### CPUID - CPU Identification
```asm
cpuid               ; Get CPU info (EAX=leaf, returns info in EAX/EBX/ECX/EDX)
```

### RDTSC - Read Time-Stamp Counter
```asm
rdtsc               ; EDX:EAX = CPU timestamp counter
```

---

## 🏗️ Stack Frame Convention

### Typical Function Prologue
```asm
push ebp            ; Save old base pointer
mov ebp, esp        ; Set new base pointer
sub esp, 0x20       ; Allocate local variables (32 bytes)
```

### Typical Function Epilogue
```asm
mov esp, ebp        ; Restore stack pointer
pop ebp             ; Restore old base pointer
ret                 ; Return to caller
```

### Alternative Epilogue
```asm
leave               ; Equivalent to: mov esp, ebp; pop ebp
ret
```

---

## 📋 Calling Conventions

### __cdecl (C Declaration)
- **Caller cleans stack**
- Arguments pushed right-to-left
- Return value in EAX

```asm
; Caller:
push arg2
push arg1
call function
add esp, 8          ; Caller cleans

; Callee:
push ebp
mov ebp, esp
; [ebp+8] = arg1, [ebp+12] = arg2
mov eax, result
pop ebp
ret                 ; Don't clean stack
```

### __stdcall (Standard Call)
- **Callee cleans stack**
- Arguments pushed right-to-left
- Return value in EAX

```asm
; Caller:
push arg2
push arg1
call function
; No cleanup needed

; Callee:
push ebp
mov ebp, esp
; [ebp+8] = arg1, [ebp+12] = arg2
mov eax, result
pop ebp
ret 8               ; Callee cleans 8 bytes
```

### __fastcall
- **First 2 args in ECX, EDX**
- Rest pushed right-to-left
- Callee cleans stack

```asm
; Caller:
mov ecx, arg1
mov edx, arg2
push arg3
call function

; Callee:
; ECX = arg1, EDX = arg2, [esp+4] = arg3
```

---

## 🧮 Addressing Modes

### Immediate
```asm
mov eax, 0x42       ; Direct value
```

### Register
```asm
mov eax, ebx        ; Register to register
```

### Direct Memory
```asm
mov eax, [0x401000] ; Load from fixed address
```

### Register Indirect
```asm
mov eax, [ebx]      ; Load from address in ebx
```

### Indexed
```asm
mov eax, [ebx+ecx]  ; Base + Index
```

### Scaled Indexed
```asm
mov eax, [ebx+ecx*4] ; Base + (Index * Scale)
; Scale can be 1, 2, 4, or 8
```

### Based Indexed with Displacement
```asm
mov eax, [ebx+ecx*4+8] ; Base + (Index * Scale) + Displacement
```

---

## 💾 Common Instruction Encodings

| Instruction | Opcode (hex) | Bytes |
|-------------|--------------|-------|
| `nop` | 90 | 1 |
| `ret` | C3 | 1 |
| `int 3` | CC | 1 |
| `push eax` | 50 | 1 |
| `pop eax` | 58 | 1 |
| `call rel32` | E8 | 5 |
| `jmp rel32` | E9 | 5 |
| `jmp short` | EB | 2 |
| `mov eax, imm32` | B8 | 5 |

---

## 🔍 Common Patterns in Exploits

### Zero a Register
```asm
xor eax, eax        ; Shorter than mov eax, 0
```

### Stack Alignment
```asm
and esp, 0xFFFFFFF0 ; Align ESP to 16-byte boundary
```

### Function Pointer Call
```asm
call [eax]          ; Call function at address stored at eax
jmp [eax]           ; Jump to address stored at eax
```

### Get EIP (Position Independent Code)
```asm
call $+5            ; Call next instruction
pop eax             ; EAX now contains current EIP
```

### POP-POP-RET (SEH Exploitation)
```asm
pop edi             ; First pop
pop edi             ; Second pop
ret                 ; Return to overwritten address
```

### ROP Gadget Examples
```asm
pop eax; ret        ; Load value into EAX
pop ebx; pop ecx; ret ; Load multiple registers
mov eax, [ebx]; ret ; Dereference pointer
add esp, 0x10; ret  ; Stack pivot
```

---

## 🛠️ Useful Tricks

### Set Register to -1
```asm
xor eax, eax        ; eax = 0
dec eax             ; eax = 0xFFFFFFFF
```

### Swap Without Temp
```asm
xor eax, ebx
xor ebx, eax
xor eax, ebx        ; eax and ebx swapped
```

### Multiply by Power of 2
```asm
shl eax, 3          ; eax *= 8 (faster than imul)
```

### Check if Zero
```asm
test eax, eax       ; Faster than cmp eax, 0
jz is_zero
```

### Copy String
```asm
cld                 ; Clear direction flag (forward)
mov ecx, length
rep movsb           ; Copy ECX bytes from ESI to EDI
```

---

## 📊 Flag Behavior

### Arithmetic Instructions Set Flags
```
CF - Carry out of MSB (unsigned overflow)
ZF - Result is zero
SF - Result is negative (MSB = 1)
OF - Signed overflow
PF - Even parity of result
AF - Auxiliary carry (BCD)
```

### Instructions That DON'T Set Flags
```asm
mov                 ; Doesn't affect flags
lea                 ; Doesn't affect flags
```

### Instructions That Set ALL Arithmetic Flags
```asm
add, sub, cmp       ; Set all arithmetic flags
```

### Instructions That Clear/Set Specific Flags
```asm
clc                 ; Clear carry flag
stc                 ; Set carry flag
cmc                 ; Complement carry flag
cld                 ; Clear direction flag
std                 ; Set direction flag
```

---

## 🎯 Shellcode Techniques

### NULL-Free Instructions

**Avoid:**
```asm
mov eax, 0          ; Contains NULL bytes
```

**Use instead:**
```asm
xor eax, eax        ; NULL-free
```

**Avoid:**
```asm
push 0              ; Contains NULL
```

**Use instead:**
```asm
xor eax, eax
push eax
```

### Position-Independent Code (PIC)
```asm
call get_eip
get_eip:
pop ebx             ; EBX = current EIP
; Now use EBX as base for relative addressing
```

---

## 📚 Quick Reference Tables

### Register Preservation (Calling Conventions)

| Register | __cdecl | __stdcall | __fastcall |
|----------|---------|-----------|------------|
| EAX | Volatile | Volatile | Volatile |
| EBX | Non-volatile | Non-volatile | Non-volatile |
| ECX | Volatile | Volatile | Arg 1 |
| EDX | Volatile | Volatile | Arg 2 |
| ESI | Non-volatile | Non-volatile | Non-volatile |
| EDI | Non-volatile | Non-volatile | Non-volatile |
| EBP | Non-volatile | Non-volatile | Non-volatile |
| ESP | Non-volatile | Non-volatile | Non-volatile |

### Data Sizes

| Type | Size | Range (unsigned) | Range (signed) |
|------|------|------------------|----------------|
| Byte | 1 byte | 0 - 255 | -128 - 127 |
| Word | 2 bytes | 0 - 65535 | -32768 - 32767 |
| Dword | 4 bytes | 0 - 4294967295 | -2147483648 - 2147483647 |
| Qword | 8 bytes | 0 - 2^64-1 | -2^63 - 2^63-1 |

---

## 💡 Pro Tips

1. **XOR for zeroing** is shorter and faster than MOV
2. **LEA for arithmetic** doesn't affect flags
3. **TEST vs CMP** when checking for zero
4. **INC/DEC don't affect CF** - useful in loops
5. **XCHG with EAX** has shorter encoding
6. **LEAVE** = MOV ESP, EBP + POP EBP
7. **PUSHAD/POPAD** save all at once
8. **Direction flag** matters for string operations!
9. **RET n** cleans n bytes from stack
10. **Alignment matters** for performance

---

**Version**: 1.0 | **Last Updated**: December 2024
**For**: OSED Section 2 - WinDbg and x86 Architecture

*Keep this reference handy when analyzing assembly code!*
