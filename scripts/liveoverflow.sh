#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${ROOT_DIR}/liveoverflow-playlist.yaml"
SERVICE_NAME="liveoverflow-pwn"
IMAGE_NAME="liveoverflow-pwn:14.04"
SOLVER_SERVICE="liveoverflow-solver"

usage() {
  cat <<'EOF'
Usage: scripts/liveoverflow.sh <command>

Commands:
  ensure        Ensure image+container exist and are running
  up            docker compose up -d --build
  down          docker compose down
  shell         Exec an interactive shell in the container
  image         Print the image name (liveoverflow-pwn:14.04)
  ps            Show container status

Build inside container:
  build-all     Build all lab binaries inside the container (make -C liveoverflow-labs build-all)
  clean         Remove built binaries inside the mounted lab folder
  solver-shell  Exec an interactive shell in the solver container
  solve-all     Run all available solvers in solver container

Examples:
  scripts/liveoverflow.sh ensure
  scripts/liveoverflow.sh shell
  scripts/liveoverflow.sh build-all
  scripts/liveoverflow.sh solve-all

EOF
}

need_docker() {
  command -v docker >/dev/null 2>&1 || { echo "docker not found" >&2; exit 2; }
  docker version >/dev/null 2>&1 || { echo "docker daemon not reachable" >&2; exit 2; }
  docker compose version >/dev/null 2>&1 || { echo "docker compose plugin not available" >&2; exit 2; }
}

container_status() {
  docker ps -a --format '{{.Names}}\t{{.Image}}\t{{.Status}}' | awk -v n="${SERVICE_NAME}" '$1==n{print $0}'
}

is_running() {
  docker ps --format '{{.Names}}' | grep -qx "${SERVICE_NAME}"
}

ensure() {
  need_docker
  if ! docker image inspect "${IMAGE_NAME}" >/dev/null 2>&1; then
    echo "[*] Building image ${IMAGE_NAME}"
    docker compose -f "${COMPOSE_FILE}" build "${SERVICE_NAME}"
  fi

  if ! docker ps -a --format '{{.Names}}' | grep -qx "${SERVICE_NAME}"; then
    echo "[*] Creating container ${SERVICE_NAME}"
    docker compose -f "${COMPOSE_FILE}" up -d "${SERVICE_NAME}"
  fi

  if ! is_running; then
    echo "[*] Starting container ${SERVICE_NAME}"
    docker compose -f "${COMPOSE_FILE}" up -d "${SERVICE_NAME}"
  fi

  # solver container (modern userspace for running pwntools scripts)
  if ! docker ps -a --format '{{.Names}}' | grep -qx "${SOLVER_SERVICE}"; then
    echo "[*] Creating container ${SOLVER_SERVICE}"
    docker compose -f "${COMPOSE_FILE}" up -d "${SOLVER_SERVICE}"
  fi
  if ! docker ps --format '{{.Names}}' | grep -qx "${SOLVER_SERVICE}"; then
    echo "[*] Starting container ${SOLVER_SERVICE}"
    docker compose -f "${COMPOSE_FILE}" up -d "${SOLVER_SERVICE}"
  fi
}

up() {
  need_docker
  docker compose -f "${COMPOSE_FILE}" up -d --build
}

down() {
  need_docker
  docker compose -f "${COMPOSE_FILE}" down
}

shell_() {
  ensure
  exec docker exec -it "${SERVICE_NAME}" bash
}

solver_shell() {
  ensure
  exec docker exec -it "${SOLVER_SERVICE}" bash
}

image() {
  echo "${IMAGE_NAME}"
}

ps() {
  need_docker
  echo "NAME	IMAGE	STATUS"
  container_status || true
}

build_all() {
  ensure
  exec docker exec -i "${SERVICE_NAME}" bash -lc "cd /home/pwner/labs && make -C . build-all"
}

clean() {
  ensure
  exec docker exec -i "${SERVICE_NAME}" bash -lc "cd /home/pwner/labs && make -C . clean"
}

solve_all() {
  ensure
  # build first in pwn container, then execute solvers in solver container
  docker exec -i "${SERVICE_NAME}" bash -lc "cd /home/pwner/labs && make -C . build-all" >/dev/null
  exec docker exec -i "${SOLVER_SERVICE}" bash -lc "cd /workspace && python3 liveoverflow-labs/run_all_solvers.py"
}

cmd="${1:-}"
case "${cmd}" in
  ensure) ensure ;;
  up) up ;;
  down) down ;;
  shell) shell_ ;;
  solver-shell) solver_shell ;;
  image) image ;;
  ps) ps ;;
  build-all) build_all ;;
  clean) clean ;;
  solve-all) solve_all ;;
  -h|--help|"") usage ;;
  *) echo "Unknown command: ${cmd}" >&2; usage; exit 2 ;;
esac

