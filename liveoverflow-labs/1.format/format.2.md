## format2

### Goal

Set global `target == 64`.

### Vulnerability

Reads attacker input into `buffer` and then does `printf(buffer);` (format-string bug).

### Exploit idea

- Put `&target` at the start of the input.
- Use `%n` to write the number of bytes printed so far.
- Brute a small positional index range until it works.

### Run

```bash
source ~/.local/bin/env
source .venv-pwn/bin/activate
python3 liveoverflow-labs/1.format/format.2.py
```
