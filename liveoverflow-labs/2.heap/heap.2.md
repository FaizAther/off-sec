## heap2

### Goal

Trigger the “already logged in” path: program prints **`you have logged in already!`**.

### Vulnerability

On `auth ...` the program does:

- `auth = malloc(sizeof(auth));` ← allocates only sizeof(pointer), not `struct auth`
- `memset(auth, 0, sizeof(auth));` ← clears only a few bytes

Then later `service ...` uses `strdup` to allocate another chunk near `auth`.

Finally `login` checks `auth->auth` which can end up reading attacker-controlled bytes due to the under-allocation / heap layout.

### Exploit idea

Send commands to shape the heap so that `auth->auth` becomes non-zero.

`heap.2.py` brute-forces the `service` string length to make the check pass reliably.

### Corelan-style checklist (practical)

- **Primitive**: under-allocation + dangling semantics → struct field reads attacker-controlled memory
- **Refine**: brute a small parameter (`service` length) so the same script works across allocator variations
- **Validation**: success string is deterministic (`you have logged in already!`)
