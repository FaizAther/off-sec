FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python3-full \
    gdb \
    make \
    file \
    git \
    curl \
    libc6-i386 lib32stdc++6 lib32gcc-s1 \
    socat netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# pwntools (modern Python) inside a venv (PEP 668 safe)
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir pwntools

WORKDIR /workspace

CMD ["sleep", "infinity"]

