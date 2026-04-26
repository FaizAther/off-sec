## format3

### Goal

Set global `target == 0x01025544`.

### Vulnerability

`printf(buffer)` where `buffer` is attacker-controlled (format string).

### Exploit idea

Use two `%hn` writes (halfword) to write:

- low 16 bits to `&target`
- high 16 bits to `&target+2`

Brute a small positional index range for the first pointer.

### Run

```bash
source ~/.local/bin/env
source .venv-pwn/bin/activate
python3 liveoverflow-labs/1.format/format.3.py
```
