# OSED Section 2.1 Lab: Introduction to x86 Architecture

**Difficulty Level:** Beginner
**Estimated Time:** 3.5 hours (2h theory + 1.5h lab)
**Skills:** Memory layout analysis, Register examination, Basic WinDbg usage

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

#### Detailed Step-by-Step Instructions:

**Step 1.1: Create the Sample Program**
1. Open a text editor (Notepad++, VS Code, or any editor)
2. Create a new file named `sample.c`
3. Copy the sample C program code from the Lab Environment Setup section
4. Save the file in a convenient location (e.g., `C:\OSED\lab\sample.c`)

**Step 1.2: Compile the Program**
1. Open Command Prompt or PowerShell
2. Navigate to the directory containing `sample.c`:
   ```bash
   cd C:\OSED\lab
   ```
3. Compile the program with debugging symbols:
   ```bash
   gcc -g -m32 -o sample.exe sample.c
   ```
   **Note:** The `-m32` flag compiles for 32-bit (x86) architecture
   **Note:** The `-g` flag includes debugging information
4. Verify the executable was created:
   ```bash
   dir sample.exe
   ```
   **Expected:** You should see `sample.exe` in the directory listing

**Step 1.3: Run the Program**
1. Execute the program:
   ```bash
   .\sample.exe
   ```
   **Expected Output:**
   ```
   Global: 42, Local: 100, Heap: 200
   ```
2. **Important:** Keep the program running (don't close the window yet)
   - The program will exit quickly, so you may need to add a pause:
   - Edit `sample.c` and add `getchar();` before `return 0;` to keep it running

**Step 1.4: Launch WinDbg**
1. Open WinDbg Preview from the Start Menu
2. Wait for WinDbg to fully load
3. You should see the WinDbg command window

**Step 1.5: Attach to the Process**
1. In WinDbg, go to: `File` → `Attach to Process...`
2. In the process list, find `sample.exe`
   - If you don't see it, make sure the program is still running
   - You may need to run the program again
3. Click on `sample.exe` in the list
4. Click the `Attach` button
5. WinDbg will break into the process (execution will pause)

**Step 1.6: Load Symbols**
1. In the WinDbg command window, type:
   ```windbg
   .reload
   ```
2. Press Enter
3. Wait for symbols to load (may take a few seconds)
4. You should see output like:
   ```
   Reloading current modules
   ModLoad: 00400000 00405000   sample.exe
   ```

**Step 1.7: Analyze Memory Layout**
1. Type the following command to see all memory regions:
   ```windbg
   !address
   ```
2. Press Enter
3. **This will produce a lot of output** - scroll through it
4. To get a summary, type:
   ```windbg
   !address -summary
   ```
5. Press Enter

**Step 1.8: Identify Memory Segments**

**A. Text Segment (Executable Code):**
1. Type:
   ```windbg
   !address -f:Image
   ```
2. Look for the base address (typically starts at 0x00400000)
3. **Document:** Write down the base address of the executable

**B. Data Segment (Initialized Global Variables):**
1. Find the address of `global_var`:
   ```windbg
   x sample!global_var
   ```
2. **Document:** Write down the address of `global_var`
3. Examine its contents:
   ```windbg
   d sample!global_var
   ```
4. **Verify:** You should see the value 42 (0x2A in hex)

**C. BSS Segment (Uninitialized Global Variables):**
1. Find the address of `uninitialized_var`:
   ```windbg
   x sample!uninitialized_var
   ```
2. **Document:** Write down the address
3. Examine its contents:
   ```windbg
   d sample!uninitialized_var
   ```
4. **Note:** This should be zero or uninitialized

**D. Heap (Dynamically Allocated Memory):**
1. Type:
   ```windbg
   !address -f:Heap
   ```
2. **Document:** Write down the heap base address
3. To see heap details:
   ```windbg
   !heap
   ```

**E. Stack (Local Variables and Function Calls):**
1. Type:
   ```windbg
   !address -f:Stack
   ```
2. **Document:** Write down the stack base address
3. View current stack:
   ```windbg
   k
   ```
4. View stack pointer:
   ```windbg
   r esp
   ```

**Step 1.9: Document Your Findings**
Create a table with the following information:
- **Segment Name** | **Base Address** | **Size** | **Permissions**
- Text Segment | 0x00400000 | ? | Execute, Read
- Data Segment | ? | ? | Read, Write
- BSS Segment | ? | ? | Read, Write
- Heap | ? | ? | Read, Write
- Stack | ? | ? | Read, Write

**Step 1.10: Calculate Offsets**
1. Calculate the offset between Text and Data segments:
   ```windbg
   ? sample!global_var - 0x00400000
   ```
2. **Document:** Write down the offset

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

#### Detailed Step-by-Step Instructions:

**Step 2.1: View All Registers**
1. In WinDbg (with the process attached), type:
   ```windbg
   r
   ```
2. Press Enter
3. **Expected Output:**
   ```
   eax=00000000 ebx=00000000 ecx=00000000 edx=00000000 esi=00000000 edi=00000000
   eip=00401000 esp=0012ff80 ebp=0012ff88 iopl=0         nv up ei pl zr na pe nc
   cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000246
   ```
4. **Document:** Take a screenshot or copy this output

**Step 2.2: Understand Register Categories**

**A. General Purpose Registers (32-bit):**
1. **EAX (Accumulator):**
   - Type: `r eax`
   - **Purpose:** Primary register for arithmetic operations, function return values
   - **Current Value:** Note the current value
   - **Example:** After `add eax, 5`, EAX contains the result

2. **EBX (Base):**
   - Type: `r ebx`
   - **Purpose:** Base pointer for memory addressing
   - **Current Value:** Note the current value

3. **ECX (Counter):**
   - Type: `r ecx`
   - **Purpose:** Loop counters, string operations
   - **Current Value:** Note the current value

4. **EDX (Data):**
   - Type: `r edx`
   - **Purpose:** Secondary data register, I/O operations
   - **Current Value:** Note the current value

5. **ESI (Source Index):**
   - Type: `r esi`
   - **Purpose:** Source pointer for string/memory operations
   - **Current Value:** Note the current value

6. **EDI (Destination Index):**
   - Type: `r edi`
   - **Purpose:** Destination pointer for string/memory operations
   - **Current Value:** Note the current value

7. **EBP (Base Pointer):**
   - Type: `r ebp`
   - **Purpose:** Points to base of current stack frame
   - **Current Value:** Note the current value (this is important!)
   - **Note:** EBP is used to access function parameters and local variables

8. **ESP (Stack Pointer):**
   - Type: `r esp`
   - **Purpose:** Points to top of stack
   - **Current Value:** Note the current value (this is very important!)
   - **Note:** ESP changes as items are pushed/popped from stack

**Step 2.3: Examine Control Registers**

1. **EIP (Instruction Pointer):**
   - Type: `r eip`
   - **Purpose:** Points to next instruction to execute
   - **Current Value:** This is the address of the current instruction
   - **Critical:** Controlling EIP is key to exploit development!
   - View the instruction at EIP:
     ```windbg
     u eip
     ```

2. **EFLAGS (Flags Register):**
   - Type: `r efl`
   - **Purpose:** Contains processor status flags
   - **Current Value:** Note the flags (shown as abbreviations in `r` output)
   - **Common Flags:**
     - **ZF (Zero Flag):** Set if result is zero
     - **CF (Carry Flag):** Set if arithmetic produces carry
     - **SF (Sign Flag):** Set if result is negative
     - **OF (Overflow Flag):** Set if signed arithmetic overflows

**Step 2.4: Analyze Segment Registers**

1. **CS (Code Segment):**
   - Type: `r cs`
   - **Purpose:** Points to code segment descriptor
   - **Current Value:** Note the value (typically 0x001b)

2. **DS (Data Segment):**
   - Type: `r ds`
   - **Purpose:** Points to data segment descriptor
   - **Current Value:** Note the value (typically 0x0023)

3. **SS (Stack Segment):**
   - Type: `r ss`
   - **Purpose:** Points to stack segment descriptor
   - **Current Value:** Note the value (typically 0x0023)

4. **ES, FS, GS (Extra Segments):**
   - Type: `r es`, `r fs`, `r gs`
   - **Purpose:** Additional segment registers
   - **FS Special:** In Windows, FS points to Thread Information Block (TIB)
   - View FS contents:
     ```windbg
     d fs:[0]
     ```

**Step 2.5: Register Manipulation Practice**

1. **Save Current Register State:**
   - Type: `r`
   - **Document:** Copy the output (this is your baseline)

2. **Modify EAX Register:**
   ```windbg
   r eax=0x12345678
   ```
   - Press Enter
   - Verify the change:
     ```windbg
     r eax
     ```
   - **Expected:** EAX should now be 0x12345678

3. **Modify Multiple Registers:**
   ```windbg
   r ebx=0xdeadbeef
   r ecx=0xcafebabe
   ```
   - Verify:
     ```windbg
     r
     ```

4. **Modify ESP (Stack Pointer) - BE CAREFUL!**
   ```windbg
   r esp=esp+4
   ```
   - **Warning:** Modifying ESP incorrectly can crash the program
   - **Purpose:** This demonstrates how stack manipulation works

5. **Modify EIP (Instruction Pointer) - ADVANCED:**
   ```windbg
   r eip=eip+10
   ```
   - **Warning:** This will change program execution flow!
   - **Purpose:** This is how exploits redirect execution
   - View new instruction:
     ```windbg
     u eip
     ```

**Step 2.6: Register Analysis During Execution**

1. **Set a Breakpoint:**
   ```windbg
   bp sample!main
   ```
2. **Continue Execution:**
   ```windbg
   g
   ```
3. **View Registers at Breakpoint:**
   ```windbg
   r
   ```
4. **Step One Instruction:**
   ```windbg
   p
   ```
5. **View Registers Again:**
   ```windbg
   r
   ```
6. **Compare:** Note which registers changed

**Step 2.7: Document Register Analysis**
Create a table:
- **Register** | **Purpose** | **Initial Value** | **After Modification** | **Notes**
- EAX | Accumulator | ? | ? | ?
- EBX | Base | ? | ? | ?
- ... (continue for all registers)

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

### Exercise 4: Advanced Memory Mapping (Advanced)
**Duration:** 45 minutes

#### Objective:
Analyze complex memory mappings including shared memory, memory-mapped files, and kernel/user space boundaries.

#### Steps:

1. **Create Enhanced Test Program**
   ```c
   #include <stdio.h>
   #include <windows.h>

   int main() {
       HANDLE hMapFile;
       LPVOID pBuf;

       // Create memory-mapped file
       hMapFile = CreateFileMapping(
           INVALID_HANDLE_VALUE,
           NULL,
           PAGE_READWRITE,
           0,
           4096,
           TEXT("MySharedMemory"));

       pBuf = MapViewOfFile(hMapFile, FILE_MAP_ALL_ACCESS, 0, 0, 4096);

       printf("Mapped address: %p\n", pBuf);

       // Allocate various memory types
       LPVOID heap = HeapAlloc(GetProcessHeap(), 0, 1024);
       LPVOID virtual = VirtualAlloc(NULL, 8192, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);

       printf("Press Enter to continue...\n");
       getchar();

       UnmapViewOfFile(pBuf);
       CloseHandle(hMapFile);
       HeapFree(GetProcessHeap(), 0, heap);
       VirtualFree(virtual, 0, MEM_RELEASE);

       return 0;
   }
   ```

2. **Analyze Memory Types**
   ```windbg
   !address -summary
   !address -f:MEM_MAPPED
   !address -f:Heap
   !address -f:Stack
   ```

3. **Examine Page Table Entries**
   ```windbg
   !pte <address>
   !vtop <process_cr3> <virtual_address>
   ```

4. **Identify Kernel/User Boundary**
   - Locate 0x80000000 boundary on 32-bit systems
   - Analyze memory protection mechanisms
   - Document address space layout randomization (ASLR)

5. **Challenge Tasks**
   - Calculate the total private committed memory
   - Identify all executable regions
   - Find memory regions with write+execute permissions (potential security issues)

#### Expected Output:
```
--- Usage Summary ---------------- RgnCount ----------- Total Size -------- %ofBusy %ofTotal
Free                                     68        7ffa`5e8e0000 ( 127.978 TB)           99.98%
<unknown>                               193           0`1a050000 ( 416.312 MB)  99.71%    0.00%
Image                                   293           0`0c0a1000 ( 192.629 MB)   0.29%    0.00%
Stack                                     8           0`00280000 (   2.500 MB)   0.00%    0.00%
```

### Exercise 5: Register State Analysis During Function Calls (Intermediate)
**Duration:** 40 minutes

#### Objective:
Track register state changes across function boundaries and understand calling conventions.

#### Steps:

1. **Create Multi-Function Program**
   ```c
   #include <stdio.h>

   int __cdecl add(int a, int b) {
       int result = a + b;
       return result;
   }

   int __stdcall multiply(int a, int b) {
       int result = a * b;
       return result;
   }

   int __fastcall subtract(int a, int b) {
       int result = a - b;
       return result;
   }

   int main() {
       int x = 10, y = 20;
       int sum = add(x, y);
       int product = multiply(x, y);
       int diff = subtract(x, y);

       printf("Sum: %d, Product: %d, Diff: %d\n", sum, product, diff);
       return 0;
   }
   ```

2. **Set Breakpoints on Functions**
   ```windbg
   bp sample!add
   bp sample!multiply
   bp sample!subtract
   g
   ```

3. **Analyze Calling Conventions**
   - __cdecl: Arguments pushed right-to-left on stack
   - __stdcall: Callee cleans stack
   - __fastcall: First two arguments in ECX, EDX

4. **Track Register Changes**
   ```windbg
   r  # Before function call
   p  # Step through
   r  # After function call
   ```

5. **Document Stack Frame**
   ```windbg
   k  # Stack trace
   dps esp L10  # Display stack contents
   ```

#### Expected Output:
Document how each calling convention affects:
- Stack layout
- Register usage
- Return value handling
- Stack cleanup responsibility

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
