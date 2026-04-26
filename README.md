# off-sec

Personal OffSec notes + labs.

## LiveOverflow / stack labs (Docker-friendly)

This repo includes a small “LiveOverflow-style” lab setup intended to run on a **Linux x86_64 VM** with Docker.

### Bootstrap / build (recommended)

From repo root:

```bash
make ensure
make build-all
make shell
```

To see the image name:

```bash
make image
```

### Bring up the containers

From repo root:

```bash
docker compose -f liveoverflow-playlist.yaml build
docker compose -f liveoverflow-playlist.yaml up -d
```

Enter the main lab container:

```bash
docker exec -it liveoverflow-pwn bash
```

Labs are mounted at `/home/pwner/labs` inside the container from `./liveoverflow-labs`.

### Stack 0 (`liveoverflow-labs/stack.0/stack0`)

- **Walkthrough**: `liveoverflow-labs/stack.0/stack.0.md`
- **Automation script** (solve + optional non-interactive GDB batch): `liveoverflow-labs/stack.0/stack.0.py`

Run inside the container:

```bash
cd /home/pwner/labs/stack.0
python3 stack.0.py --no-gdb
python3 stack.0.py
```

Run on the VM (outside Docker):

```bash
cd /home/xubuntu/git/off-sec/liveoverflow-labs/stack.0
python3 ./stack.0.py --no-gdb
python3 ./stack.0.py
```

#### Note on GDB ASLR warning in containers

If you see `Error disabling address space randomization: Operation not permitted`, it’s because the container doesn’t allow GDB to disable ASLR by default. This doesn’t matter for `stack0` (offset-based overwrite), but you can allow it by adding the following to the service in `liveoverflow-playlist.yaml`:

```yaml
cap_add:
  - SYS_PTRACE
security_opt:
  - seccomp:unconfined
```

### Stack 1 (`liveoverflow-labs/stack.1/stack1`)

- **Walkthrough**: `liveoverflow-labs/stack.1/stack.1.md`
- **Automation script**: `liveoverflow-labs/stack.1/stack.1.py`

Run inside the container:

```bash
cd /home/pwner/labs/stack.1
python3 stack.1.py --no-gdb
python3 stack.1.py
```
