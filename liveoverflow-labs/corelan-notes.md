## Corelan-style exploit workflow (adapted to these labs)

These notes are inspired by Corelan’s exploit-dev tutorials, adapted to **Linux 32-bit** labs with **GDB + pwntools**.

### Repro first

- **Know your build flags** (PIE/canary/NX/RELRO).
- **Pin the environment**: we compile inside `liveoverflow-pwn` (Ubuntu 14.04) and exploit from the host (Ubuntu 24.04).

### Crash → control → refine

- **Crash**: make the program misbehave in a controlled way.
- **Control**: verify you can control the thing that matters (a variable, a pointer, EIP/RIP, a GOT entry).
- **Refine**: remove guesswork:
  - compute offsets from live output / debugger
  - resolve symbols from the ELF
  - avoid hardcoded addresses when possible

### Stack/format primitives

- **Find offsets**: cyclic patterns (pwntools `cyclic`) or debugger address subtraction.
- **Format strings**:
  - start by finding the positional index (where your pointer(s) land)
  - then build `%n`/`%hn` writes
  - for 32-bit, prefer **two halfword writes** for full pointers/words

### Heap primitives

- **Heap overflow**: confirm adjacency and overwrite distance.
- **Arbitrary write**: often achieved via pointer overwrite (e.g. overwrite a `char *` field).
- **Control-flow redirect**:
  - overwrite a function pointer
  - or overwrite a GOT entry for a function that will be called later (`puts`, `exit`, etc.)

### Automation (Corelan principle: repeatability)

Each solver script should:

- compile the target in-container
- compute offsets/addresses dynamically
- execute the exploit
- assert on a success string

