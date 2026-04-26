## `format0` walkthrough

### Goal

Make the local `target` equal `0xdeadbeef`.

### Vulnerability

`sprintf(buffer, string)` will happily write more than 64 bytes into `buffer`, overflowing into adjacent locals (including `target`).

### Stack sketch (typical 32-bit build)

```
high addresses
┌──────────────┐
│ saved EIP     │
├──────────────┤
│ saved EBP     │
├──────────────┤
│ target (4B)   │  <-- overwrite this to 0xdeadbeef
├──────────────┤
│ buffer[64]    │  <-- sprintf writes here
└──────────────┘
low addresses
```

### Exploit idea

- Find offset: `&target - &buffer`
- Send payload: `b"A"*offset + p32(0xdeadbeef)`

### Run

Use `format.0.py` (compiles + finds offset via GDB + runs payload).
