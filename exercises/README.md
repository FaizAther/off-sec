# Exercises: Protostar / Exploit Education & Cryptopals

This folder groups **binary exploitation** practice (Protostar-style levels) and **applied cryptography** practice (Cryptopals). Together they cover disjoint but complementary skills: turning broken **memory** and **protocol implementations** into reliable attacks.

## Layout

| Path | Purpose |
|------|---------|
| [`protostar/GUIDE.md`](protostar/GUIDE.md) | **Protostar / Phoenix** — modules 0–5, diagrams, gdb, pwntools, gdb/Python appendix |
| [`protostar/`](protostar/) | Your exploits, notes, binaries (e.g. `stack/`, `heap/`) |
| [`cryptopals/challenges.md`](cryptopals/challenges.md) | Full **1–66** Cryptopals index with links |
| [`../containers/liveoverflow-pwn/`](../containers/liveoverflow-pwn/) | Dockerfile for a Linux lab (gcc, gdb, multilib) |
| [`../liveoverflow-labs/`](../liveoverflow-labs/) | Host directory often bind-mounted into the lab container |

---

## Protostar & Exploit Education (gdb · assembly · stack · heap · net)

**Official pages**

- [Protostar (historical)](https://exploit.education/protostar/) — classic stack / format / heap / network intro VM.
- [Phoenix (current)](https://exploit.education/phoenix/) — maintained successor with the same learning arc.
- VM / ISO downloads: [Exploit Education — Downloads](https://exploit.education/downloads/) (Protostar ISO under “Older resources”; Phoenix qcow2 / `.deb` under Phoenix).

**Typical VM access** (see each site for details): user `user` / `user`; levels often under `/opt/protostar/bin` (Protostar) or the Phoenix layout. Core dumps may use a non-default `core_pattern` (e.g. under `/tmp`).

### Skill map

| Topic | What you learn | Example Protostar sections |
|--------|----------------|---------------------------|
| **Assembly & gdb** | Reading `disassemble`, registers (`EIP`, `ESP`, `EBP`), `stepi`, `info reg`, examining stack memory (`x/…`) | All levels — start with Stack Zero / One |
| **Stack** | Buffer overflows, saved return address, control flow, intro shellcode | Stack Zero → Stack Six / Seven |
| **Format strings** | `printf` attacks, `%n` / arbitrary read–write, GOT / function pointers | Format Zero → Four |
| **Heap** | Chunks, `malloc`/`free`, classic corruption patterns | Heap Zero → Three |
| **Networking** | Sockets, endianness, remote stack exploitation | Net Zero → Two; Final levels combine ideas |

### Suggested workflow

1. Run the **official VM** (QEMU, UTM, or VirtualBox) so ASLR/NX match the course material.
2. For each binary: `file`, `checksec` (if available), `objdump -d`, then **gdb** with breakpoints on the vulnerable path.
3. Keep exploit code under `protostar/` (e.g. `protostar/stack/stack_n.py`) — Python 3 + [pwntools](https://docs.pwntools.com/) on the host is fine if the target runs in the VM and you connect with `remote()`.

---

## Cryptopals (crypto implementations & attacks)

**Site:** [cryptopals.com](https://cryptopals.com/) — eight sets, **66 challenges**, no spoilers in this README.

**Index:** [cryptopals/challenges.md](cryptopals/challenges.md) lists every challenge with a direct link.

**Rough themes by set**

| Sets | Focus |
|------|--------|
| 1–2 | Encoding, XOR, AES modes (ECB/CBC), padding |
| 3–4 | Oracles, CTR, MT19937, MACs, length extension, timing |
| 5–6 | Diffie–Hellman, SRP, RSA, DSA, Bleichenbacher-style attacks |
| 7–8 | Hash constructions, collisions, RC4 biases, ECC, GCM |

**Workflow:** implement attacks in the language you prefer (Python 3 is common); use stdlib plus small deps (e.g. `pycryptodome`) where allowed by the challenge. Put solutions under `cryptopals/solutions/` if you want a clean tree (create as you go).

---

## Running both tracks in parallel

- **Protostar / Phoenix** → evenings with **gdb** and a VM; emphasizes **systems** intuition.
- **Cryptopals** → emphasizes **precise byte manipulation** and **number theory** later; good on the host machine without a pwn VM.

They do not depend on each other; alternating keeps variety. A sane default is: finish Cryptopals Set 1 while working through the first few Stack levels, so both “byte feel” and “stack layout” grow together.

---

## Legal & ethics

Use these materials **only** on infrastructure you own or are explicitly authorized to test. Protostar/Cryptopals are **intentionally vulnerable** teaching environments; the same techniques are illegal against real systems without permission.
