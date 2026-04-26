## Stack 4

### Goal

Control RIP (return address) to redirect execution to `win()`.

### Key idea

- This is a classic memory corruption exercise.
- Use GDB (optionally GEF) to confirm the stack layout and compute the exact offset.

### Offset / layout notes

Find offset to saved RIP (cyclic pattern), then ret2win to `win`.

### Quick run

python3 stack.4.py
