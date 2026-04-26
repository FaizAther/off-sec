## Stack 6

### Goal

Bypass a naive ret-address stack-region check and still control flow.

### Key idea

- This is a classic memory corruption exercise.
- Use GDB (optionally GEF) to confirm the stack layout and compute the exact offset.

### Offset / layout notes

Program inspects return address; prefer ret2libc / ret2plt that lands outside the forbidden range.

### Quick run

python3 stack.6.py
