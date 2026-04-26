## format4

### Goal

Redirect execution to `hello()` (prints `code execution redirected! you win`).

### Vulnerability

`printf(buffer)` where `buffer` is attacker-controlled.

### Exploit idea

Overwrite `exit@GOT` with the address of `hello()` using two `%hn` halfword writes.

### Corelan-style checklist (practical)

- **Primitive**: format string → arbitrary write via `%hn`
- **Refine**:
  - find the correct positional index for **both** pointers (`exit@got` and `exit@got+2`)
  - do two halfword writes to avoid printing billions of characters
- **Exploit chain**: `printf(buffer)` → overwrite GOT → `exit(1)` redirects to `hello()`

### Run

```bash
source ~/.local/bin/env
source .venv-pwn/bin/activate
python3 liveoverflow-labs/1.format/format.4.py
```
