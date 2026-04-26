## `format1` walkthrough

### Goal

Make the global `target` non-zero.

### Vulnerability

`printf(string)` uses attacker input as a **format string**.

### Exploit idea (32-bit)

- Place the address of `target` at the start of the input (so it will eventually be consumed as a “fake” printf argument).
- Find the correct stack argument index \(k\) where that address is read.
- Use `%k$n` to write the number of bytes printed so far into `target`.

### Run

Use `format.1.py` (auto-finds the stack index and writes to `target`).
