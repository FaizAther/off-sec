## Stack 2

### Goal

Overflow `buffer` to overwrite function pointer `fp` and call `win()`.

### Key idea

- This is a classic memory corruption exercise.
- Use GDB (optionally GEF) to confirm the stack layout and compute the exact offset.

### Offset / layout notes

Compute `&fp - &buffer` in GDB, then overwrite `fp` with address of `win` (from `nm`).

### Quick run

python3 stack.2.py
