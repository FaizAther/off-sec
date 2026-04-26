# Protostar (Exploit Education) in this repo

This repo can download and run the official **Protostar v2** ISO and provides a workspace for writing **verified** solutions for:

- stack
- format
- heap
- net
- final

Protostar is historically a **32-bit** training VM; the most reliable way to run it today is as a VM (QEMU).

## Quick start (QEMU)

1) Download the ISO (official Exploit Education release):

```bash
cd protostar
./download.sh
```

2) Boot it under QEMU (with SSH forwarded to localhost:2222):

```bash
./run-qemu.sh
```

3) Login inside the VM

- **user** / **user**
- **root** / **godmode**

Levels live at:

- `/opt/protostar/bin`
- sources at `/opt/protostar/src`

## Extract levels into the repo (optional but handy)

Once the VM is running, you can copy the binaries and sources out into `protostar/extracted/` using `scp` over the forwarded SSH port (2222).

If you don’t want to set up keys, you can do it interactively after the VM is up:

```bash
ssh -p 2222 user@127.0.0.1
```

Then (from another terminal on the host) you can copy:

```bash
mkdir -p protostar/extracted
scp -P 2222 -r user@127.0.0.1:/opt/protostar/bin protostar/extracted/
scp -P 2222 -r user@127.0.0.1:/opt/protostar/src protostar/extracted/
```

## Solutions layout

Solutions are intended to be **repeatable** and **verifiable**:

- `protostar/solutions/<category><level>/`
  - `README.md` (walkthrough + diagrams)
  - `solve.py` (automation; typically drives the program via SSH and checks success output)

## Notes

- Expect ASLR/NX to be disabled in Protostar by design.
- Some solutions require running commands *inside* the VM (e.g. for net levels).

