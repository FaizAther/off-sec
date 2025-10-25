# Code Samples for OSED Section 2

## Overview
This directory contains compilable code samples for all OSED Section 2 labs. All programs are designed to be analyzed with WinDbg and demonstrate specific debugging concepts.

---

## 📁 Directory Structure

```
code-samples/
├── 01-basic/               # Simple programs for beginners (3 files)
├── 02-memory/              # Memory layout demonstrations (2 files)
├── 03-functions/           # Function call conventions (1 file)
├── 04-structures/          # Data structures in memory (1 file)
├── 05-heap/                # Heap allocation examples (1 file)
├── 06-threads/             # Multi-threaded programs (1 file)
├── 07-exceptions/          # Exception handling (1 file)
├── 08-vulnerable/          # Vulnerable programs - educational (3 files)
├── scripts/                # Build and helper scripts (4 scripts)
├── Makefile                # Automated build system
└── README.md               # This file
```

---

## 🚀 Quick Start

### Installation Requirements

You need a C compiler to build these samples. Choose one of the following options:

#### Option 1: MinGW-w64 (Recommended for Windows)

**MinGW-w64** provides GCC compiler for Windows.

**Installation Steps:**

1. **Download MinGW-w64**
   - Go to: https://www.mingw-w64.org/downloads/
   - Or use: https://github.com/niXman/mingw-builds-binaries/releases
   - Download: `x86_64-posix-seh` version (latest)

2. **Install MinGW-w64**
   ```
   - Extract to: C:\mingw64
   - Add to PATH: C:\mingw64\bin
   ```

3. **Add to System PATH**
   ```
   Windows Search → "Environment Variables"
   → System Properties → Environment Variables
   → System Variables → Path → Edit → New
   → Add: C:\mingw64\bin
   → OK → OK → OK
   ```

4. **Verify Installation**
   ```cmd
   gcc --version
   make --version
   ```

   Expected output:
   ```
   gcc (x86_64-posix-seh-rev0, Built by MinGW-W64 project) 12.2.0
   GNU Make 4.3
   ```

#### Option 2: Visual Studio (Alternative)

**Visual Studio Community** (free) includes MSVC compiler.

**Installation Steps:**

1. **Download Visual Studio**
   - Go to: https://visualstudio.microsoft.com/downloads/
   - Download: Visual Studio Community (free)

2. **Install with C++ Workload**
   - Run installer
   - Select: "Desktop development with C++"
   - Install

3. **Compile from Developer Command Prompt**
   ```cmd
   # Open "Developer Command Prompt for VS"
   cl /Zi /Od hello.c
   ```

**Note**: The Makefile is designed for GCC. If using Visual Studio, compile manually or modify the Makefile.

#### Option 3: MSYS2 (Full Linux-like Environment)

**MSYS2** provides a complete Linux-like environment on Windows.

**Installation Steps:**

1. **Download MSYS2**
   - Go to: https://www.msys2.org/
   - Download installer
   - Install to: C:\msys64

2. **Update MSYS2**
   ```bash
   pacman -Syu
   ```

3. **Install GCC and Make**
   ```bash
   pacman -S mingw-w64-x86_64-gcc
   pacman -S make
   ```

4. **Use MSYS2 MinGW 64-bit terminal**
   - Launch: "MSYS2 MinGW 64-bit" from Start menu
   - Navigate to code-samples directory
   - Run: `make`

---

### Compilation

#### Using Makefile (Easiest)

```bash
# Compile all programs
make

# Compile specific category
make basic
make memory
make functions
make structures
make heap
make threads
make exceptions

# Test compilation
make test

# List all programs
make list

# Clean build
make clean

# Show help
make help
```

#### Manual Compilation (Individual Files)

**Using GCC (MinGW):**
```bash
# Basic template
gcc -g -O0 -o output.exe input.c

# Examples:
gcc -g -O0 -o hello.exe 01-basic/hello.c
gcc -g -O0 -o variables.exe 01-basic/variables.c
gcc -g -O0 -o memory_layout.exe 02-memory/memory_layout.c
gcc -g -O0 -o thread_basic.exe 06-threads/thread_basic.c
```

**Compiler Flags Explained:**
- `-g` : Include debug symbols (required for WinDbg)
- `-O0` : No optimization (easier to debug)
- `-o file.exe` : Output filename
- `-Wall` : Show all warnings (good practice)
- `-m32` : Compile as 32-bit (if needed)

**Using Visual Studio (cl.exe):**
```cmd
# Basic compilation
cl program.c

# With debug symbols
cl /Zi program.c

# 32-bit
cl /Zi program.c /link /MACHINE:X86

# No optimizations
cl /Od /Zi program.c
```

---

### After Compilation

**Where are the executables?**
```
code-samples/bin/
├── hello.exe
├── variables.exe
├── calculations.exe
├── memory_layout.exe
├── stack_demo.exe
├── calling_conventions.exe
├── struct_basic.exe
├── malloc_simple.exe
├── thread_basic.exe
├── seh_basic.exe
├── buffer_overflow.exe    (⚠️ vulnerable)
├── format_string.exe      (⚠️ vulnerable)
└── use_after_free.exe     (⚠️ vulnerable)
```

**How to run them?**
```bash
# From code-samples directory:
./bin/hello.exe
./bin/memory_layout.exe
./bin/thread_basic.exe
```

**How to debug with WinDbg?**
```bash
# Method 1: Launch with WinDbg
windbg bin/hello.exe

# Method 2: Run then attach
./bin/hello.exe
# Note the PID from output
windbg -p <PID>
```

---

### Troubleshooting

#### Problem: "gcc" is not recognized

**Solution:**
```
1. Verify GCC is installed
2. Check PATH environment variable includes: C:\mingw64\bin
3. Restart command prompt after PATH changes
4. Test: gcc --version
```

#### Problem: "make" is not recognized

**Solution:**
```
MinGW-w64 includes make.exe
Verify C:\mingw64\bin is in PATH
Or download make separately
Test: make --version
```

#### Problem: Compilation errors

**Solution:**
```bash
# Ensure you're in the code-samples directory
cd C:\Users\User\off-sec\osed\2\resources\code-samples

# Check GCC version (should be 8.0+)
gcc --version

# Try compiling a simple file first
gcc -g -o hello.exe 01-basic/hello.c

# Check for specific error messages
```

#### Problem: "undefined reference" errors

**Solution:**
```bash
# For Windows API functions, ensure you're on Windows
# GCC on Windows automatically links kernel32.dll

# If still problems, explicitly link:
gcc -g -o program.exe source.c -lkernel32
```

#### Problem: Programs compile but won't run

**Solution:**
```cmd
# Check if antivirus is blocking
# Run from command prompt to see error messages
.\bin\hello.exe

# Check for missing DLLs
# Make sure using MinGW GCC, not Cygwin
```

---

## 📚 Sample Categories

### 01-basic/ - Basic Programs ✅
Simple programs for understanding WinDbg basics.

| File | Status | Purpose | Lab |
|------|--------|---------|-----|
| `hello.c` | ✅ Created | Basic executable structure | 2.1 |
| `variables.c` | ✅ Created | Variable storage locations | 2.1 |
| `calculations.c` | ✅ Created | Arithmetic operations | 2.1 |

**All files complete and ready to compile!**

### 02-memory/ - Memory Layout ✅
Programs demonstrating memory organization.

| File | Status | Purpose | Lab |
|------|--------|---------|-----|
| `memory_layout.c` | ✅ Created | All memory sections demo | 2.1 |
| `stack_demo.c` | ✅ Created | Stack frame structure | 2.1, 2.3 |

**More samples can be added as needed**

### 03-functions/ - Function Calls ✅
Different calling conventions and patterns.

| File | Status | Purpose | Lab |
|------|--------|---------|-----|
| `calling_conventions.c` | ✅ Created | Compare cdecl/stdcall/fastcall | 2.1 |

**More samples can be added as needed**

### 04-structures/ - Data Structures ✅
Complex data types in memory.

| File | Status | Purpose | Lab |
|------|--------|---------|-----|
| `struct_basic.c` | ✅ Created | Structure layout and padding | 2.3 |

**More samples can be added as needed**

### 05-heap/ - Heap Management ✅
Dynamic memory allocation patterns.

| File | Status | Purpose | Lab |
|------|--------|---------|-----|
| `malloc_simple.c` | ✅ Created | malloc/free, heap analysis | 2.3 |

**More samples can be added as needed**

### 06-threads/ - Multi-Threading ✅
Thread creation and synchronization.

| File | Status | Purpose | Lab |
|------|--------|---------|-----|
| `thread_basic.c` | ✅ Created | CreateThread, multi-thread debugging | 2.2 |

**More samples can be added as needed**

### 07-exceptions/ - Exception Handling ✅
SEH and exception mechanisms.

| File | Status | Purpose | Lab |
|------|--------|---------|-----|
| `seh_basic.c` | ✅ Created | SEH __try/__except basics | 2.8 |

**More advanced exception examples in Lab 2.8**

### 08-vulnerable/ - Vulnerable Programs ✅
**⚠️ Educational purposes only - FOR LEARNING ONLY**

| File | Status | Purpose | Lab |
|------|--------|---------|-----|
| `buffer_overflow.c` | ✅ Created | Classic stack buffer overflow | 2.6, 2.7 |
| `format_string.c` | ✅ Created | Format string vulnerability | 2.7 |
| `use_after_free.c` | ✅ Created | Heap use-after-free | 2.7 |

**WARNING**: These programs contain intentional vulnerabilities. Only use in isolated environments for learning.

---

## 🔨 Compilation Guide

### Creating Debug Builds

**Full Debug Information:**
```bash
gcc -g -O0 -fno-stack-protector -o program.exe program.c
```

Parameters:
- `-g`: Include debug symbols
- `-O0`: No optimization
- `-fno-stack-protector`: Disable stack canaries (for learning)
- `-m32`: Force 32-bit (on 64-bit systems)

**With Specific Features:**
```bash
# Disable ASLR (for learning)
gcc -g -O0 -no-pie -o program.exe program.c

# Disable DEP (Windows)
gcc -g -O0 -Wl,--nxcompat=no -o program.exe program.c
```

### Visual Studio Builds

```cmd
# Debug build
cl /Zi /Od /MDd program.c

# Release with symbols
cl /Zi /O2 /MD program.c

# 32-bit
cl /Zi /Od /MDd program.c /link /MACHINE:X86

# Disable security features (learning)
cl /Zi /Od /GS- /DYNAMICBASE:NO program.c
```

---

## 🎯 Usage Examples

### Example 1: Basic Debugging
```bash
# Compile
gcc -g -o hello.exe 01-basic/hello.c

# Debug with WinDbg
windbg hello.exe

# In WinDbg:
bp main
g
k
```

### Example 2: Memory Analysis
```bash
# Compile
gcc -g -o memory_layout.exe 02-memory/memory_layout.c

# Debug
windbg memory_layout.exe

# In WinDbg:
bp main
g
!address
dt variables
```

### Example 3: Function Call Analysis
```bash
# Compile with specific convention
gcc -g -o cdecl.exe 03-functions/cdecl_demo.c

# Debug
windbg cdecl.exe

# In WinDbg:
bp function_name
g
k
dps esp
```

---

## 📝 Best Practices

### When Writing Sample Code

1. **Keep it Simple**: Focus on one concept per program
2. **Add Comments**: Explain what each section demonstrates
3. **Include Sleep()**: Keep process alive for debugging
4. **Print Output**: Help verify program behavior
5. **Use Meaningful Names**: Variables and functions should be clear
6. **Add Debug Helpers**: Print addresses, values, etc.

### Example Template
```c
#include <stdio.h>
#include <windows.h>

// PURPOSE: Demonstrates [concept]
// LAB: Section 2.X - [topic]
// COMPILE: gcc -g -o program.exe program.c

int main() {
    printf("Program starting...\n");
    printf("PID: %d\n", GetCurrentProcessId());

    // Your code here

    printf("Press Ctrl+C to exit or wait...\n");
    Sleep(60000);  // Keep alive for debugging

    return 0;
}
```

---

## 🔍 Debugging Tips

### Attaching WinDbg
```bash
# Launch with WinDbg
windbg program.exe

# Attach to running process
windbg -p <PID>

# Attach by name
windbg -pn program.exe
```

### Common Debug Session
```windbg
# 1. Set symbol path
.symfix
.reload

# 2. Set breakpoint
bp main

# 3. Run
g

# 4. Analyze
k          # Stack trace
r          # Registers
dv         # Local variables
!address   # Memory layout
```

---

## ⚠️ Security Considerations

### Vulnerable Code
All programs in `08-vulnerable/` are **intentionally insecure** for educational purposes.

**DO NOT:**
- Use this code in production
- Deploy on internet-facing systems
- Use without understanding the vulnerabilities

**DO:**
- Study in isolated environment
- Use for learning exploit mitigation
- Practice secure coding by contrast
- Understand what NOT to do

### Safe Environment
- Use virtual machines
- Isolate from network
- Take snapshots before running
- Never run as administrator unless necessary

---

## 📦 Compiled Binaries

After running `make`, compiled executables will be in the `bin/` directory:

```
bin/
├── hello.exe
├── variables.exe
├── calculations.exe
├── memory_layout.exe
├── stack_demo.exe
├── calling_conventions.exe
├── struct_basic.exe
├── malloc_simple.exe
├── thread_basic.exe
├── seh_basic.exe
├── buffer_overflow.exe    (⚠️ vulnerable)
├── format_string.exe      (⚠️ vulnerable)
└── use_after_free.exe     (⚠️ vulnerable)
```

**Note**: Always compile from source for the best learning experience.

---

## 🛠️ Build System

### Makefile (Available)
The Makefile provides automated compilation:
```bash
make          # Compile all
make basic    # Compile basic category
make clean    # Remove binaries
make help     # Show all targets
```

### Build Scripts ✅
The scripts/ directory contains helper scripts:

**For Linux/MSYS2:**
- `compile_all.sh` - Batch compilation with color output and statistics
- `clean.sh` - Interactive cleanup script
- `verify.sh` - Verification and testing script

**For Windows:**
- `test.bat` - Quick verification batch script

**Usage:**
```bash
# Compile all (Linux/MSYS2)
./scripts/compile_all.sh

# Compile specific category
./scripts/compile_all.sh vulnerable

# Verify compilation
./scripts/verify.sh

# Clean build
./scripts/clean.sh

# Windows quick test
scripts\test.bat
```

---

## 📖 Additional Resources

### Learning Path
1. Start with `01-basic/`
2. Progress through categories in order
3. Compile and debug each program
4. Modify code to experiment
5. Create your own variations

### Documentation
Each source file includes:
- Purpose statement
- Relevant lab section
- Compilation command
- Key concepts demonstrated
- Expected behavior

### Support
- Check README in each category
- Refer to lab guides for context
- Use WinDbg cheat sheet
- Consult theory materials

---

## 🔄 Contributing

### Adding New Samples
1. Place in appropriate category
2. Follow naming convention
3. Include header comment block
4. Add to category README
5. Test compilation
6. Verify debugging experience

### Sample Header Template
```c
/*
 * File: program_name.c
 * Purpose: Brief description
 * Lab: OSED 2.X - Topic
 * Compile: gcc -g -o program.exe program.c
 *
 * Demonstrates:
 * - Concept 1
 * - Concept 2
 *
 * Debug with:
 * windbg program.exe
 * bp main; g; k
 */
```

---

## 📊 Sample Statistics

| Category | Files | Total Lines | Difficulty |
|----------|-------|-------------|------------|
| 01-basic | 3 | ~150 | Beginner |
| 02-memory | 2 | ~110 | Beginner |
| 03-functions | 1 | ~55 | Intermediate |
| 04-structures | 1 | ~90 | Intermediate |
| 05-heap | 1 | ~85 | Intermediate |
| 06-threads | 1 | ~95 | Advanced |
| 07-exceptions | 1 | ~70 | Advanced |
| 08-vulnerable | 3 | ~320 | Expert |

**Total**: 13 code samples, ~975 lines of code
**Scripts**: 4 build/test scripts

---

## 📅 Updates

### Version 1.0 - December 2024
- Initial collection
- All basic categories
- Build scripts
- Documentation

### Completed in This Version
- ✅ 13 compilable C programs across 8 categories
- ✅ 3 vulnerable program examples for exploitation practice
- ✅ Comprehensive Makefile for automated builds
- ✅ 4 build/test helper scripts (Linux + Windows)
- ✅ Complete installation and compilation guide

### Planned Future Additions
- Additional calling convention examples (__thiscall, __vectorcall)
- More complex memory layout demonstrations
- Advanced heap manipulation and corruption samples
- ROP chain examples
- Shellcode injection demonstrations

---

## 📧 Feedback

Found an issue? Have a suggestion?
- Check existing samples
- Test compilation
- Verify debugging experience
- Suggest improvements

---

**Version**: 1.0
**Last Updated**: December 2024
**For**: OSED Section 2 - WinDbg and x86 Architecture

*All code samples are for educational purposes only.*
