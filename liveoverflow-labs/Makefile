.PHONY: help build-all clean \
        build-stack build-format build-heap build-net build-final

CC=gcc
# Default "training lab" flags.
# -m32: build 32-bit i386 (matches classic protostar-style offsets)
# -g: debug symbols for GDB
# -fno-stack-protector: disable SSP
# -z execstack: executable stack (some classic labs assume this)
CFLAGS_COMMON=-m32 -g -fno-stack-protector -z execstack

help:
	@echo "Targets:"
	@echo "  build-all     Build all lab binaries (32-bit)"
	@echo "  build-stack   Build stack binaries"
	@echo "  build-format  Build format binaries"
	@echo "  build-heap    Build heap binaries"
	@echo "  build-net     Build net binaries"
	@echo "  build-final   Build final binaries"
	@echo "  clean         Remove built binaries"

build-all: build-stack build-format build-heap build-net build-final

build-stack:
	$(CC) $(CFLAGS_COMMON) -o 0.stack/stack0 0.stack/stack.0.c
	$(CC) $(CFLAGS_COMMON) -o 0.stack/stack1 0.stack/stack.1.c
	$(CC) $(CFLAGS_COMMON) -o 0.stack/stack2 0.stack/stack.2.c
	$(CC) $(CFLAGS_COMMON) -o 0.stack/stack4 0.stack/stack.4.c
	$(CC) $(CFLAGS_COMMON) -o 0.stack/stack5 0.stack/stack.5.c
	$(CC) $(CFLAGS_COMMON) -o 0.stack/stack6 0.stack/stack.6.c
	$(CC) $(CFLAGS_COMMON) -o 0.stack/stack7 0.stack/stack.7.c

build-format:
	$(CC) $(CFLAGS_COMMON) -o 1.format/format0 1.format/0.c
	$(CC) $(CFLAGS_COMMON) -o 1.format/format1 1.format/1.c
	$(CC) $(CFLAGS_COMMON) -o 1.format/format2 1.format/2.c
	$(CC) $(CFLAGS_COMMON) -o 1.format/format3 1.format/3.c
	$(CC) $(CFLAGS_COMMON) -o 1.format/format4 1.format/4.c

build-heap:
	$(CC) $(CFLAGS_COMMON) -o 2.heap/heap0 2.heap/0.c
	$(CC) $(CFLAGS_COMMON) -o 2.heap/heap1 2.heap/1.c
	$(CC) $(CFLAGS_COMMON) -o 2.heap/heap2 2.heap/2.c
	$(CC) $(CFLAGS_COMMON) -o 2.heap/heap3 2.heap/3.c

build-net:
	$(CC) $(CFLAGS_COMMON) -o 3.net/net0 3.net/0.c
	$(CC) $(CFLAGS_COMMON) -o 3.net/net1 3.net/1.c
	$(CC) $(CFLAGS_COMMON) -o 3.net/net2 3.net/2.c

build-final:
	$(CC) $(CFLAGS_COMMON) -o 4.final/final0 4.final/0.c
	$(CC) $(CFLAGS_COMMON) -o 4.final/final1 4.final/1.c
	$(CC) $(CFLAGS_COMMON) -o 4.final/final2 4.final/2.c

clean:
	@rm -f \
	  0.stack/stack0 0.stack/stack1 0.stack/stack2 0.stack/stack4 0.stack/stack5 0.stack/stack6 0.stack/stack7 \
	  1.format/format0 1.format/format1 1.format/format2 1.format/format3 1.format/format4 \
	  2.heap/heap0 2.heap/heap1 2.heap/heap2 2.heap/heap3 \
	  3.net/net0 3.net/net1 3.net/net2 \
	  4.final/final0 4.final/final1 4.final/final2

