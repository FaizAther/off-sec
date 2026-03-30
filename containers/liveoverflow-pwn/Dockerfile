# Ubuntu 14.04 Trusty — matches the distro era used in early LiveOverflow / Phoenix material.
# Trusty is EOL but package indexes remain on archive.ubuntu.com (do not use old-releases; it 404s for trusty).

FROM docker.io/library/ubuntu:14.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc-multilib \
    g++-multilib \
    gdb \
    git \
    curl \
    wget \
    vim \
    nano \
    file \
    binutils \
    netcat-openbsd \
    strace \
    ltrace \
    python \
    python-dev \
    python3 \
    python3-dev \
    libssl-dev \
    libffi-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Pwntools is omitted: Trusty’s Python 2 cannot speak modern PyPI TLS in practice.
# Early LiveOverflow episodes use gdb + gcc + small Python/shell; install pwntools on the
# host or use a newer sidecar image when you need it.

WORKDIR /home/pwner/labs

CMD ["sleep", "infinity"]
