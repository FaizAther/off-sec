.PHONY: help ensure up down shell image ps build-all clean
.PHONY: solver-shell solve-all

help:
	@echo "Targets:"
	@echo "  ensure     Ensure docker image+container exist and running"
	@echo "  up         Bring up docker compose (build if needed)"
	@echo "  down       Stop docker compose"
	@echo "  shell      Open shell in liveoverflow-pwn container"
	@echo "  image      Print image name"
	@echo "  ps         Show container status"
	@echo "  build-all  Build all lab binaries inside container"
	@echo "  clean      Remove built lab binaries"
	@echo "  solver-shell  Open shell in solver container"
	@echo "  solve-all     Build + run all solvers in containers"

ensure:
	@bash scripts/liveoverflow.sh ensure

up:
	@bash scripts/liveoverflow.sh up

down:
	@bash scripts/liveoverflow.sh down

shell:
	@bash scripts/liveoverflow.sh shell

image:
	@bash scripts/liveoverflow.sh image

ps:
	@bash scripts/liveoverflow.sh ps

build-all:
	@bash scripts/liveoverflow.sh build-all

clean:
	@bash scripts/liveoverflow.sh clean

solver-shell:
	@bash scripts/liveoverflow.sh solver-shell

solve-all:
	@bash scripts/liveoverflow.sh solve-all

