# OSED Section 2.1 Theory: Introduction to x86 Architecture

## Table of Contents
1. [Program Memory](#program-memory)
2. [CPU Registers](#cpu-registers)
3. [Memory Addressing](#memory-addressing)
4. [Memory Protection](#memory-protection)
5. [Practical Applications](#practical-applications)

---

## Program Memory

### Virtual Memory Concepts

Modern x86 systems use **virtual memory**, which provides each process with its own isolated address space. This abstraction allows programs to operate as if they have access to the entire memory system, while the operating system manages the actual physical memory allocation.

#### Key Concepts:
- **Virtual Address Space**: The range of addresses a process can use (typically 4GB for 32-bit processes)
- **Physical Memory**: The actual RAM hardware
- **Memory Management Unit (MMU)**: Hardware that translates virtual addresses to physical addresses
- **Page Tables**: Data structures used by the MMU for address translation

### Memory Layout Overview

A typical Windows process memory layout consists of several distinct regions:

```
High Memory (0xFFFFFFFF)
├── Kernel Space (0x80000000 - 0xFFFFFFFF)
├── User Stack (grows downward)
├── Unused Memory
├── User Heap (grows upward)
├── BSS Segment (uninitialized global variables)
├── Data Segment (initialized global variables)
├── Text Segment (executable code)
└── Low Memory (0x00000000)
```

### Process Memory Structure

#### 1. Text Segment (Code)
- **Purpose**: Contains the executable machine code
- **Characteristics**: Read-only, executable
- **Location**: Typically starts at 0x00400000 for Windows executables
- **Size**: Depends on program complexity

#### 2. Data Segment
- **Purpose**: Contains initialized global and static variables
- **Characteristics**: Read-write, non-executable
- **Examples**: `int global_var = 42;`, `char global_string[] = "Hello";`

#### 3. BSS Segment
- **Purpose**: Contains uninitialized global and static variables
- **Characteristics**: Read-write, non-executable, zero-initialized
- **Examples**: `int uninitialized_var;`, `char buffer[1024];`

#### 4. Heap
- **Purpose**: Dynamic memory allocation
- **Characteristics**: Read-write, non-executable, grows upward
- **Management**: Controlled by malloc/free, new/delete
- **Fragmentation**: Can become fragmented over time

#### 5. Stack
- **Purpose**: Local variables, function parameters, return addresses
- **Characteristics**: Read-write, non-executable, grows downward
- **Management**: Automatic (LIFO - Last In, First Out)
- **Size**: Limited (typically 1-8MB)

### Memory Organization Details

#### Stack Frame Structure
When a function is called, a new stack frame is created:

```
High Address
├── Previous Stack Frame
├── Function Parameters (pushed right to left)
├── Return Address (EIP)
├── Previous Frame Pointer (EBP)
├── Local Variables
├── Saved Registers
└── Current Stack Frame (ESP points here)
Low Address
```

#### Heap Management
The heap is managed by the Windows Heap Manager:
- **Heap Blocks**: Allocated memory chunks
- **Free Lists**: Linked lists of free blocks
- **Heap Headers**: Metadata about each block
- **Fragmentation**: External and internal fragmentation

---

## CPU Registers

### Register Categories

x86 processors have several categories of registers, each serving specific purposes:

#### 1. General Purpose Registers (32-bit)

| Register | Purpose | Common Usage |
|----------|---------|--------------|
| **EAX** | Accumulator | Primary register for arithmetic operations, function return values |
| **EBX** | Base | Base pointer for memory addressing |
| **ECX** | Counter | Loop counters, string operations |
| **EDX** | Data | Secondary data register, I/O operations |
| **ESI** | Source Index | Source pointer for string/memory operations |
| **EDI** | Destination Index | Destination pointer for string/memory operations |
| **EBP** | Base Pointer | Points to base of current stack frame |
| **ESP** | Stack Pointer | Points to top of stack |

#### Register Usage Conventions
- **Caller-saved**: EAX, ECX, EDX (caller must save before function call)
- **Callee-saved**: EBX, ESI, EDI, EBP (callee must save and restore)

#### 2. Segment Registers (16-bit)

| Register | Purpose | Description |
|----------|---------|-------------|
| **CS** | Code Segment | Points to code segment descriptor |
| **DS** | Data Segment | Points to data segment descriptor |
| **SS** | Stack Segment | Points to stack segment descriptor |
| **ES** | Extra Segment | Additional data segment |
| **FS** | Extra Segment | Thread-local storage (Windows) |
| **GS** | Extra Segment | Additional segment register |

#### 3. Control Registers

| Register | Purpose | Description |
|----------|---------|-------------|
| **EIP** | Instruction Pointer | Points to next instruction to execute |
| **EFLAGS** | Flags Register | Contains processor status flags |

#### EFLAGS Register Bits
- **CF** (Carry Flag): Set if arithmetic operation produces carry/borrow
- **PF** (Parity Flag): Set if result has even number of 1 bits
- **AF** (Auxiliary Carry): Set if BCD arithmetic produces carry
- **ZF** (Zero Flag): Set if result is zero
- **SF** (Sign Flag): Set if result is negative
- **TF** (Trap Flag): Used for single-step debugging
- **IF** (Interrupt Flag): Controls interrupt handling
- **DF** (Direction Flag): Controls string operation direction
- **OF** (Overflow Flag): Set if signed arithmetic overflows

### Register Operations

#### Register-to-Register Operations
```assembly
mov eax, ebx        ; Copy EBX to EAX
add eax, ecx        ; Add ECX to EAX
sub edx, eax        ; Subtract EAX from EDX
```

#### Memory-to-Register Operations
```assembly
mov eax, [0x00400000]    ; Load from memory address
mov eax, [ebx]          ; Load from address in EBX
mov eax, [ebx + 4]      ; Load from EBX + offset
```

#### Register-to-Memory Operations
```assembly
mov [0x00400000], eax    ; Store EAX to memory address
mov [ebx], eax          ; Store EAX to address in EBX
mov [ebx + 4], eax      ; Store EAX to EBX + offset
```

---

## Memory Addressing

### Addressing Modes

x86 processors support several addressing modes for accessing memory:

#### 1. Immediate Addressing
```assembly
mov eax, 42              ; Load immediate value 42 into EAX
mov ebx, 0x12345678      ; Load immediate value into EBX
```

#### 2. Register Addressing
```assembly
mov eax, ebx             ; Copy EBX to EAX
add eax, ecx             ; Add ECX to EAX
```

#### 3. Direct Addressing
```assembly
mov eax, [0x00400000]    ; Load from absolute address
mov [0x00400000], eax    ; Store to absolute address
```

#### 4. Register Indirect Addressing
```assembly
mov eax, [ebx]           ; Load from address in EBX
mov [ebx], eax           ; Store to address in EBX
```

#### 5. Indexed Addressing
```assembly
mov eax, [ebx + 4]       ; Load from EBX + 4
mov eax, [ebx + ecx]     ; Load from EBX + ECX
```

#### 6. Base-Indexed Addressing
```assembly
mov eax, [ebx + esi]     ; Load from EBX + ESI
mov eax, [ebx + esi + 4] ; Load from EBX + ESI + 4
```

### Address Calculation

#### Linear Addressing
Modern x86 systems use **flat memory model** with linear addressing:
- **Linear Address**: Virtual address used by programs
- **Physical Address**: Actual address in physical memory
- **Translation**: MMU converts linear to physical addresses

#### Segmented Addressing (Legacy)
Older x86 systems used segmented addressing:
- **Segment:Offset**: Address = (Segment × 16) + Offset
- **Segment Registers**: CS, DS, SS, ES, FS, GS
- **Protected Mode**: Modern systems use protected mode segments

### Memory Alignment

#### Data Alignment
- **Natural Alignment**: Data should be aligned to its size
- **4-byte alignment**: 32-bit integers should be at addresses divisible by 4
- **Performance Impact**: Misaligned access can cause performance penalties
- **Exception**: Misaligned access can cause exceptions on some processors

#### Stack Alignment
- **Stack Alignment**: Stack should be aligned to 4-byte boundaries
- **Function Calls**: Compiler ensures proper stack alignment
- **Assembly Code**: Manual assembly must maintain alignment

---

## Memory Protection

### Protection Mechanisms

#### 1. Read/Write/Execute Permissions
- **Read Permission**: Allows reading from memory location
- **Write Permission**: Allows writing to memory location
- **Execute Permission**: Allows executing code from memory location
- **Combinations**: Memory can have any combination of these permissions

#### 2. Memory Protection Units
- **Page Tables**: Define permissions for each memory page
- **Segment Descriptors**: Define permissions for memory segments
- **Ring Levels**: Different privilege levels (0 = kernel, 3 = user)

#### 3. Segmentation
- **Code Segments**: Typically read-only, executable
- **Data Segments**: Typically read-write, non-executable
- **Stack Segments**: Typically read-write, non-executable

### Memory Protection Violations

#### 1. Access Violations
- **Read Violation**: Attempting to read from non-readable memory
- **Write Violation**: Attempting to write to non-writable memory
- **Execute Violation**: Attempting to execute non-executable memory

#### 2. Segmentation Faults
- **Invalid Address**: Accessing memory outside valid range
- **Null Pointer**: Dereferencing null pointer
- **Stack Overflow**: Exceeding stack limits

#### 3. Page Faults
- **Page Not Present**: Accessing unmapped memory page
- **Protection Violation**: Accessing page with insufficient permissions
- **Invalid Address**: Accessing invalid virtual address

### Windows Memory Protection

#### 1. Virtual Memory Manager
- **Page Management**: Manages physical memory pages
- **Address Translation**: Converts virtual to physical addresses
- **Memory Mapping**: Maps files and devices to memory

#### 2. Access Control
- **User Mode**: Limited access to system resources
- **Kernel Mode**: Full access to system resources
- **System Calls**: Controlled interface between user and kernel mode

#### 3. Security Features
- **ASLR**: Address Space Layout Randomization
- **DEP**: Data Execution Prevention
- **CFG**: Control Flow Guard
- **SMEP**: Supervisor Mode Execution Prevention

---

## Practical Applications

### Exploit Development Context

Understanding x86 architecture is crucial for exploit development:

#### 1. Buffer Overflow Exploitation
- **Stack Layout**: Understanding stack frame structure
- **Return Address**: Locating and overwriting return addresses
- **Shellcode Placement**: Finding suitable memory locations
- **Register Manipulation**: Controlling execution flow

#### 2. Memory Corruption Analysis
- **Heap Analysis**: Understanding heap management
- **Use-After-Free**: Exploiting freed memory references
- **Double-Free**: Exploiting multiple free operations
- **Integer Overflows**: Exploiting arithmetic operations

#### 3. Debugging Techniques
- **Register Analysis**: Understanding register states during execution
- **Memory Inspection**: Analyzing memory contents
- **Execution Flow**: Tracing program execution
- **Vulnerability Identification**: Finding security issues

### Lab Correlation

The concepts covered in this theory section directly correlate with Lab 2.1:

#### Lab Exercise 1: Memory Layout Analysis
- **Theory**: Program memory structure, virtual memory concepts
- **Practice**: Using WinDbg to analyze memory layout
- **Application**: Identifying text, data, heap, and stack segments

#### Lab Exercise 2: Register Analysis
- **Theory**: CPU registers, register purposes, register operations
- **Practice**: Examining register contents in WinDbg
- **Application**: Understanding register states during execution

#### Lab Exercise 3: Memory Address Calculation
- **Theory**: Memory addressing modes, address calculation
- **Practice**: Calculating offsets and addresses
- **Application**: Understanding memory organization

### Advanced Topics

#### 1. 64-bit Architecture Differences
- **Register Extensions**: RAX, RBX, RCX, RDX, etc.
- **Additional Registers**: R8-R15 general purpose registers
- **Addressing**: 64-bit addressing capabilities
- **Calling Conventions**: Different parameter passing

#### 2. Modern Security Features
- **NX Bit**: No-execute bit for memory pages
- **SMEP**: Supervisor Mode Execution Prevention
- **SMAP**: Supervisor Mode Access Prevention
- **Intel CET**: Control-flow Enforcement Technology

#### 3. Performance Considerations
- **Cache Effects**: CPU cache impact on memory access
- **Branch Prediction**: CPU branch prediction mechanisms
- **Pipeline Effects**: Instruction pipeline considerations
- **Memory Bandwidth**: Memory access performance

---

## Summary

This theory section provides the foundational knowledge needed for exploit development:

1. **Memory Understanding**: How programs use memory and how memory is organized
2. **Register Knowledge**: Understanding CPU registers and their purposes
3. **Addressing Skills**: How to calculate and work with memory addresses
4. **Protection Awareness**: Understanding memory protection mechanisms

These concepts form the basis for all subsequent exploit development topics and are essential for effective debugging and vulnerability analysis.

The hands-on labs will reinforce these theoretical concepts through practical exercises using WinDbg, providing the foundation needed for advanced exploit development techniques.
