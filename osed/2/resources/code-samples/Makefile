# Makefile for OSED Section 2 Code Samples
# Purpose: Compile all C programs for debugging practice
# Usage: make all (or just 'make')

# Compiler settings
CC = gcc
CFLAGS = -g -O0 -Wall
LDFLAGS =
OUTDIR = bin

# All source files
BASIC_SRCS = $(wildcard 01-basic/*.c)
MEMORY_SRCS = $(wildcard 02-memory/*.c)
FUNC_SRCS = $(wildcard 03-functions/*.c)
STRUCT_SRCS = $(wildcard 04-structures/*.c)
HEAP_SRCS = $(wildcard 05-heap/*.c)
THREAD_SRCS = $(wildcard 06-threads/*.c)
EXCEPT_SRCS = $(wildcard 07-exceptions/*.c)
VULN_SRCS = $(wildcard 08-vulnerable/*.c)

ALL_SRCS = $(BASIC_SRCS) $(MEMORY_SRCS) $(FUNC_SRCS) $(STRUCT_SRCS) $(HEAP_SRCS) $(THREAD_SRCS) $(EXCEPT_SRCS) $(VULN_SRCS)

# Vulnerable programs need special compilation flags
VULN_CFLAGS = -g -O0 -fno-stack-protector -Wall

# Generate executable names
BASIC_EXES = $(patsubst %.c,$(OUTDIR)/%.exe,$(notdir $(BASIC_SRCS)))
MEMORY_EXES = $(patsubst %.c,$(OUTDIR)/%.exe,$(notdir $(MEMORY_SRCS)))
FUNC_EXES = $(patsubst %.c,$(OUTDIR)/%.exe,$(notdir $(FUNC_SRCS)))
STRUCT_EXES = $(patsubst %.c,$(OUTDIR)/%.exe,$(notdir $(STRUCT_SRCS)))
HEAP_EXES = $(patsubst %.c,$(OUTDIR)/%.exe,$(notdir $(HEAP_SRCS)))
THREAD_EXES = $(patsubst %.c,$(OUTDIR)/%.exe,$(notdir $(THREAD_SRCS)))
EXCEPT_EXES = $(patsubst %.c,$(OUTDIR)/%.exe,$(notdir $(EXCEPT_SRCS)))
VULN_EXES = $(patsubst %.c,$(OUTDIR)/%.exe,$(notdir $(VULN_SRCS)))

ALL_EXES = $(BASIC_EXES) $(MEMORY_EXES) $(FUNC_EXES) $(STRUCT_EXES) $(HEAP_EXES) $(THREAD_EXES) $(EXCEPT_EXES) $(VULN_EXES)

# Default target
all: $(OUTDIR) $(ALL_EXES)
	@echo "All programs compiled successfully!"
	@echo "Executables in: $(OUTDIR)/"

# Create output directory
$(OUTDIR):
	mkdir -p $(OUTDIR)

# Compile basic programs
$(OUTDIR)/%.exe: 01-basic/%.c
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Compile memory programs
$(OUTDIR)/%.exe: 02-memory/%.c
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Compile function programs
$(OUTDIR)/%.exe: 03-functions/%.c
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Compile structure programs
$(OUTDIR)/%.exe: 04-structures/%.c
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Compile heap programs
$(OUTDIR)/%.exe: 05-heap/%.c
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Compile thread programs
$(OUTDIR)/%.exe: 06-threads/%.c
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Compile exception programs
$(OUTDIR)/%.exe: 07-exceptions/%.c
	@echo "Compiling $<..."
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

# Compile vulnerable programs (with disabled protections)
$(OUTDIR)/%.exe: 08-vulnerable/%.c
	@echo "Compiling $< (⚠️ vulnerable, protections disabled)..."
	$(CC) $(VULN_CFLAGS) -o $@ $< $(LDFLAGS)

# Individual categories
basic: $(OUTDIR) $(BASIC_EXES)
	@echo "Basic programs compiled!"

memory: $(OUTDIR) $(MEMORY_EXES)
	@echo "Memory programs compiled!"

functions: $(OUTDIR) $(FUNC_EXES)
	@echo "Function programs compiled!"

structures: $(OUTDIR) $(STRUCT_EXES)
	@echo "Structure programs compiled!"

heap: $(OUTDIR) $(HEAP_EXES)
	@echo "Heap programs compiled!"

threads: $(OUTDIR) $(THREAD_EXES)
	@echo "Thread programs compiled!"

exceptions: $(OUTDIR) $(EXCEPT_EXES)
	@echo "Exception programs compiled!"

vulnerable: $(OUTDIR) $(VULN_EXES)
	@echo "⚠️  WARNING: Vulnerable programs compiled!"
	@echo "⚠️  These contain intentional vulnerabilities - use for learning only!"

# Test - compile and run hello
test: $(OUTDIR)/hello.exe
	@echo "Running hello.exe..."
	./$(OUTDIR)/hello.exe

# Clean
clean:
	rm -rf $(OUTDIR)
	@echo "Cleaned build directory"

# List all programs
list:
	@echo "Available programs:"
	@echo "  Basic:"
	@for file in $(BASIC_SRCS); do echo "    - $$(basename $$file)"; done
	@echo "  Memory:"
	@for file in $(MEMORY_SRCS); do echo "    - $$(basename $$file)"; done
	@echo "  Functions:"
	@for file in $(FUNC_SRCS); do echo "    - $$(basename $$file)"; done
	@echo "  Structures:"
	@for file in $(STRUCT_SRCS); do echo "    - $$(basename $$file)"; done
	@echo "  Heap:"
	@for file in $(HEAP_SRCS); do echo "    - $$(basename $$file)"; done
	@echo "  Threads:"
	@for file in $(THREAD_SRCS); do echo "    - $$(basename $$file)"; done
	@echo "  Exceptions:"
	@for file in $(EXCEPT_SRCS); do echo "    - $$(basename $$file)"; done
	@echo "  Vulnerable (⚠️):"
	@for file in $(VULN_SRCS); do echo "    - $$(basename $$file)"; done

# Help
help:
	@echo "OSED Section 2 - Code Samples Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make              - Compile all programs"
	@echo "  make all          - Same as 'make'"
	@echo "  make basic        - Compile only basic programs"
	@echo "  make memory       - Compile only memory programs"
	@echo "  make functions    - Compile only function programs"
	@echo "  make structures   - Compile only structure programs"
	@echo "  make heap         - Compile only heap programs"
	@echo "  make threads      - Compile only thread programs"
	@echo "  make exceptions   - Compile only exception programs"
	@echo "  make vulnerable   - Compile only vulnerable programs (⚠️)"
	@echo "  make test         - Compile and run hello.exe"
	@echo "  make list         - List all available programs"
	@echo "  make clean        - Remove all compiled files"
	@echo "  make help         - Show this help"
	@echo ""
	@echo "Compiler: $(CC)"
	@echo "Flags: $(CFLAGS)"
	@echo "Output: $(OUTDIR)/"

.PHONY: all basic memory functions structures heap threads exceptions vulnerable test clean list help
