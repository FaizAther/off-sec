## heap1

### Goal

Redirect execution to `winner()` (prints `and we have a winner ...`) by abusing heap overflow across adjacent allocations.

### Vulnerability

`i1->name` and `i2->name` are allocated with `malloc(8)`, then:

- `strcpy(i1->name, argv[1])` can overflow past 8 bytes.
- `strcpy(i2->name, argv[2])` then writes wherever `i2->name` points.

### Exploit idea (classic)

1) Overflow `i1->name` to overwrite `i2->name` pointer so it points at a GOT entry (we use `puts@GOT`, because the program calls `puts` after the copies).
2) Use `argv[2]` to overwrite that GOT entry with the address of `winner()`.

`heap.1.py` brute-forces the exact overflow length (small range) because the chunk layout can vary slightly.

### Corelan-style checklist (practical)

- **Primitive**: heap overflow → pointer overwrite → arbitrary write
- **Trigger selection**: pick a function that is definitely called after corruption (here: `puts`)
- **Exploit chain**:
  - overwrite `i2->name` → point into `puts@GOT`
  - second `strcpy` writes `winner()` into that GOT slot
  - `puts("and that's a wrap folks!")` becomes a call to `winner()`
