# OSED Section 2.1 Lab: Introduction to x86 Architecture

## Lab Overview
This lab provides hands-on experience with x86 architecture concepts, focusing on memory layout analysis and CPU register examination using WinDbg.

## Prerequisites
- WinDbg installed and configured
- Basic understanding of Windows processes
- Simple C program for analysis

## Lab Environment Setup

### Required Software:
- Windows 10/11 (64-bit)
- WinDbg Preview
- Visual Studio or MinGW for C compilation
- Process Monitor (optional)

### Sample C Program:
```c
#include <stdio.h>
#include <stdlib.h>

int global_var = 42;
int uninitialized_var;

int main() {
    int local_var = 100;
    int *heap_var = malloc(sizeof(int));
    *heap_var = 200;
    
    printf("Global: %d, Local: %d, Heap: %d\n", 
           global_var, local_var, *heap_var);
    
    free(heap_var);
    return 0;
}
```

## Lab Exercises

### Exercise 1: Memory Layout Analysis
**Duration:** 30 minutes

#### Objective:
Analyze the memory layout of a running process and identify different memory segments.

#### Steps:

1. **Compile and Run Sample Program**
   ```bash
   gcc -g -o sample.exe sample.c
   ```

2. **Launch WinDbg and Attach to Process**
   - Start WinDbg Preview
   - File → Attach to Process
   - Select your sample.exe process

3. **Analyze Memory Layout**
   ```windbg
   !address
   !address /f:*
   ```

4. **Identify Memory Segments**
   - Text segment (executable code)
   - Data segment (initialized global variables)
   - BSS segment (uninitialized global variables)
   - Heap (dynamically allocated memory)
   - Stack (local variables and function calls)

5. **Document Findings**
   - Record base addresses for each segment
   - Note segment sizes and permissions
   - Calculate offsets between segments

#### Expected Output:
```
+--- Usage: <region> <committed> <private>
|   +--- Type: <MEM_PRIVATE> <MEM_COMMIT>
|   |   +--- Protection: <PAGE_EXECUTE_READ>
|   |   |   +--- State: <MEM_COMMIT>
|   |   |   |   +--- Usage: <Image>
|   |   |   |   |   +--- Type: <MEM_IMAGE>
|   |   |   |   |   +--- AllocBase: <0x400000>
|   |   |   |   |   +--- Base: <0x400000>
|   |   |   |   |   +--- End: <0x401000>
|   |   |   |   |   +--- Size: <0x1000>
```

### Exercise 2: CPU Register Analysis
**Duration:** 30 minutes

#### Objective:
Examine CPU registers and understand their contents and purposes.

#### Steps:

1. **View All Registers**
   ```windbg
   r
   ```

2. **Analyze General Purpose Registers**
   - EAX: Accumulator register
   - EBX: Base register
   - ECX: Counter register
   - EDX: Data register
   - ESI: Source index
   - EDI: Destination index
   - EBP: Base pointer
   - ESP: Stack pointer

3. **Examine Control Registers**
   - EIP: Instruction pointer
   - EFLAGS: Flags register

4. **Analyze Segment Registers**
   - CS: Code segment
   - DS: Data segment
   - SS: Stack segment
   - ES, FS, GS: Extra segments

5. **Register Manipulation**
   ```windbg
   r eax=0x12345678
   r
   ```

#### Expected Output:
```
eax=00000000 ebx=00000000 ecx=00000000 edx=00000000 esi=00000000 edi=00000000
eip=00401000 esp=0012ff80 ebp=0012ff88 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000246
```

### Exercise 3: Memory Address Calculation
**Duration:** 15 minutes

#### Objective:
Practice calculating memory addresses and understanding addressing modes.

#### Steps:

1. **Calculate Segment Offsets**
   - Find base address of each segment
   - Calculate relative offsets
   - Determine absolute addresses

2. **Address Arithmetic**
   ```windbg
   ? 0x401000 - 0x400000
   ```

3. **Memory Dumping**
   ```windbg
   d 0x400000
   d 0x401000
   ```

4. **Symbol Resolution**
   ```windbg
   x sample!*
   ```

## Lab Deliverables

### 1. Memory Layout Report
Create a document containing:
- Screenshots of memory layout analysis
- Address calculations
- Segment identification and descriptions
- Memory permission analysis

### 2. Register Analysis Worksheet
Complete the following:
- Register identification table
- Register purpose descriptions
- Register manipulation log
- Step-by-step execution trace

### 3. Lab Summary
Write a brief summary covering:
- Key concepts learned
- Challenges encountered
- Practical applications
- Questions for further study

## Troubleshooting

### Common Issues:

1. **WinDbg Not Attaching**
   - Ensure process is running
   - Check user permissions
   - Verify process architecture (x86 vs x64)

2. **Symbols Not Loading**
   - Use `.sympath` to set symbol path
   - Load symbols with `.reload`
   - Check symbol server connectivity

3. **Memory Access Errors**
   - Verify process permissions
   - Check memory protection
   - Use appropriate access methods

## Assessment Criteria

### Excellent (90-100%):
- Complete memory layout analysis
- Accurate register identification
- Proper address calculations
- Clear documentation

### Good (80-89%):
- Most memory segments identified
- Basic register understanding
- Some address calculations
- Adequate documentation

### Satisfactory (70-79%):
- Basic memory analysis
- Limited register knowledge
- Few address calculations
- Minimal documentation

### Needs Improvement (<70%):
- Incomplete analysis
- Poor register understanding
- No address calculations
- Inadequate documentation

## Next Steps
After completing this lab:
1. Review theory materials
2. Practice with additional programs
3. Prepare for Section 2.2: Introduction to Windows Debugger
4. Experiment with different memory layouts

## Additional Resources
- WinDbg Help Documentation
- Intel x86 Architecture Manual
- Windows Internals Book
- Assembly Language Tutorials
