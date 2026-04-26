## Stack 5

### Goal

Control RIP (return address) to redirect execution.

### Key idea

- This is a classic memory corruption exercise.
- Use GDB (optionally GEF) to confirm the stack layout and compute the exact offset.

### Offset / layout notes

Same as stack4; ret2win / shellcode depending on build flags.

### Quick run

python3 stack.5.py
