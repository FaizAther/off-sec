## Stack 7

### Goal

Similar to stack6 but returns a heap string; bypass ret check and redirect execution.

### Key idea

- This is a classic memory corruption exercise.
- Use GDB (optionally GEF) to confirm the stack layout and compute the exact offset.

### Offset / layout notes

Again: land return address in text/plt/libc (not stack range).

### Quick run

python3 stack.7.py
