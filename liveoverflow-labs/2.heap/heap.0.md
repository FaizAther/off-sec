## `heap0` walkthrough

### Goal

Overwrite the heap-allocated function pointer so the program calls `winner()` and prints **`level passed`**.

### Vulnerability

Two chunks are allocated back-to-back:

- `d = malloc(sizeof(struct data))` where `struct data { char name[64]; }`
- `f = malloc(sizeof(struct fp))` where `struct fp { int (*fp)(); }`

Then:

- `strcpy(d->name, argv[1]);` can overflow `name[64]` into the next chunk.

### Heap sketch

```
heap addresses increase →

┌───────────────────────────┐
│ chunk for d (64-byte name) │  d points here
├───────────────────────────┤
│ chunk for f (fp pointer)   │  f points here
└───────────────────────────┘

overflow d->name  ───────────────►  overwrite f->fp
```

### Exploit idea

The program prints:

`data is at 0x...., fp is at 0x....`

So we can compute the exact overwrite distance at runtime:

\[
\text{distance} = fp\_addr - data\_addr
\]

Payload:

- `b"A"*distance + p32(addr_of_winner)`

### Run

Use `heap.0.py` (builds `heap0`, parses addresses from output, crafts payload, and checks for `level passed`).

### Corelan-style checklist (practical)

- **Primitive**: heap overflow → function pointer overwrite
- **Validate adjacency**: parse the program’s printed `data`/`fp` pointers
- **Remove guesswork**: compute `dist = fp - data` from live output
- **Exploit chain**: overflow → overwrite `f->fp` with `winner()` → observe `level passed`
