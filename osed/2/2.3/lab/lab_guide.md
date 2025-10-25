# OSED Section 2.3 Lab: Accessing and Manipulating Memory from WinDbg

## Lab Overview
This lab provides hands-on experience with memory operations in WinDbg, including reading, writing, disassembly, and searching memory. Students will learn to manipulate memory effectively for exploit development.

## Prerequisites
- WinDbg Preview installed
- Basic understanding of assembly language
- Sample executable with known memory layout

## Lab Environment Setup

### Required Software:
- Windows 10/11 (64-bit)
- WinDbg Preview
- Visual Studio or MinGW for C compilation
- Sample C program with structures

### Sample C Program:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

typedef struct {
    int id;
    char name[32];
    float value;
    int *pointer;
} SampleStruct;

int global_array[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
char global_string[] = "Hello, World!";
SampleStruct global_struct = {100, "Test", 3.14, NULL};

int vulnerable_function(char *input) {
    char buffer[64];
    strcpy(buffer, input);
    return strlen(buffer);
}

int main() {
    int local_var = 42;
    char local_string[] = "Local String";
    SampleStruct local_struct = {200, "Local", 2.71, &local_var};
    
    printf("Global array[0]: %d\n", global_array[0]);
    printf("Global string: %s\n", global_string);
    printf("Local var: %d\n", local_var);
    
    // Call vulnerable function
    vulnerable_function("Safe input");
    
    Sleep(10000); // Keep process alive for debugging
    
    return 0;
}
```

## Lab Exercises

### Exercise 1: Memory Reading and Disassembly
**Duration:** 45 minutes

#### Objective:
Practice reading memory contents and disassembling code.

#### Steps:

1. **Compile and Launch Program**
   ```bash
   gcc -g -o memory_sample.exe memory_sample.c
   ```

2. **Attach WinDbg and Load Symbols**
   - Start memory_sample.exe
   - Attach WinDbg to process
   - Load symbols: `.reload`

3. **Read Memory Contents**
   ```windbg
   # Read different data types
   db 00400000
   dw 00400000
   dd 00400000
   dq 00400000
   
   # Read specific memory regions
   d global_array
   d global_string
   d local_var
   ```

4. **Disassemble Code**
   ```windbg
   # Disassemble main function
   uf main
   
   # Disassemble vulnerable function
   uf vulnerable_function
   
   # Disassemble from specific address
   u 00401000
   ```

5. **Analyze Memory Layout**
   ```windbg
   # View process memory layout
   !address
   
   # View loaded modules
   lm
   
   # View symbols
   x memory_sample!*
   ```

#### Expected Output:
```
00400000  48 65 6c 6c 6f 2c 20 57-6f 72 6c 64 21 00 00 00  Hello, World!...
00400010  01 00 00 00 02 00 00 00-03 00 00 00 04 00 00 00  ................
00400020  05 00 00 00 06 00 00 00-07 00 00 00 08 00 00 00  ................
```

### Exercise 2: Structure Analysis and Dumping
**Duration:** 45 minutes

#### Objective:
Analyze data structures and dump their contents from memory.

#### Steps:

1. **Dump Structure Types**
   ```windbg
   # Dump SampleStruct type information
   dt SampleStruct
   
   # Dump global structure
   dt SampleStruct global_struct
   
   # Dump local structure
   dt SampleStruct local_struct
   ```

2. **Analyze Structure Fields**
   ```windbg
   # Dump structure with field names
   dt -v SampleStruct
   
   # Dump specific fields
   dt SampleStruct global_struct id
   dt SampleStruct global_struct name
   dt SampleStruct global_struct value
   ```

3. **Pointer Analysis**
   ```windbg
   # Dump pointers
   dps global_struct
   dps local_struct
   
   # Follow pointers
   dds global_struct+0xc
   dds local_struct+0xc
   ```

4. **Memory Layout Analysis**
   ```windbg
   # Calculate structure sizes
   ? sizeof(SampleStruct)
   
   # Calculate field offsets
   ? &global_struct.name - &global_struct
   ? &global_struct.value - &global_struct
   ```

#### Expected Output:
```
SampleStruct
   +0x000 id                 : Int4B
   +0x004 name               : [32] Char
   +0x024 value              : Float
   +0x028 pointer            : Ptr32 Int4B

global_struct
   +0x000 id                 : 100
   +0x004 name               : "Test"
   +0x024 value              : 3.14
   +0x028 pointer            : 00000000
```

### Exercise 3: Memory Writing and Manipulation
**Duration:** 45 minutes

#### Objective:
Practice writing to memory and manipulating data structures.

#### Steps:

1. **Modify Global Variables**
   ```windbg
   # Modify global array
   ed global_array 999
   ed global_array+4 888
   
   # Modify global string
   ea global_string "Modified!"
   
   # Modify global structure
   ed global_struct 777
   ea global_struct+4 "Changed"
   ```

2. **Modify Local Variables**
   ```windbg
   # Find local variable addresses
   dv local_var
   dv local_string
   
   # Modify local variables
   ed local_var 123
   ea local_string "Updated"
   ```

3. **Inject Payload Data**
   ```windbg
   # Create shellcode pattern
   ea 0012ff80 "AAAA"
   ea 0012ff84 "BBBB"
   ea 0012ff88 "CCCC"
   
   # Verify injection
   d 0012ff80
   ```

4. **Simulate Buffer Overflow**
   ```windbg
   # Set breakpoint in vulnerable function
   bp vulnerable_function
   g
   
   # Modify buffer contents
   ea buffer "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
   
   # Continue execution
   g
   ```

#### Expected Output:
```
Modified global_array:
0012ff80  41 41 41 41 42 42 42 42-43 43 43 43 00 00 00 00  AAAABBBBCCCC....
```

### Exercise 4: Memory Search and Pattern Matching
**Duration:** 30 minutes

#### Objective:
Search memory space for specific patterns and data.

#### Steps:

1. **Search for Strings**
   ```windbg
   # Search for ASCII strings
   s -a 00400000 L?1000000 "Hello"
   s -a 00400000 L?1000000 "Test"
   s -a 00400000 L?1000000 "Local"
   ```

2. **Search for Binary Patterns**
   ```windbg
   # Search for specific bytes
   s -b 00400000 L?1000000 41 41 41 41
   s -b 00400000 L?1000000 48 65 6c 6c
   
   # Search for dwords
   s -d 00400000 L?1000000 0x41414141
   s -d 00400000 L?1000000 0x100
   ```

3. **Search for Pointers**
   ```windbg
   # Search for valid pointers
   s -d 00400000 L?1000000 00400000
   s -d 00400000 L?1000000 00120000
   ```

4. **Pattern Analysis**
   ```windbg
   # Analyze search results
   d <found_address>
   u <found_address>
   ```

#### Expected Output:
```
00400000  48 65 6c 6c 6f 2c 20 57-6f 72 6c 64 21 00 00 00  Hello, World!...
00400020  54 65 73 74 00 00 00 00-00 00 00 00 00 00 00 00  Test............
```

### Exercise 5: Register Inspection and Manipulation
**Duration:** 15 minutes

#### Objective:
Inspect and manipulate CPU registers.

#### Steps:

1. **Inspect All Registers**
   ```windbg
   # View all registers
   r
   
   # View specific register
   r eax
   r ebx
   r ecx
   ```

2. **Modify Registers**
   ```windbg
   # Modify general purpose registers
   r eax=0x12345678
   r ebx=0x87654321
   r ecx=0x11111111
   
   # Verify changes
   r
   ```

3. **Register Analysis**
   ```windbg
   # Analyze register relationships
   ? eax
   ? ebx
   ? ecx
   
   # Calculate register operations
   ? eax + ebx
   ? eax - ebx
   ```

#### Expected Output:
```
eax=12345678 ebx=87654321 ecx=11111111 edx=00000000 esi=00000000 edi=00000000
eip=00401000 esp=0012ff80 ebp=0012ff88 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000246
```

## Lab Deliverables

### 1. Memory Analysis Report
Create a document containing:
- Screenshots of memory contents
- Disassembly analysis
- Structure layout documentation
- Memory address calculations

### 2. Memory Manipulation Log
Complete the following:
- Memory modification records
- Payload injection results
- Register manipulation log
- Search pattern results

### 3. Exploit Simulation Summary
Document the following:
- Buffer overflow simulation
- Memory corruption analysis
- Exploit payload analysis
- Vulnerability assessment

## Troubleshooting

### Common Issues:

1. **Memory Access Violations**
   - Check memory permissions
   - Verify address validity
   - Use appropriate access methods
   - Check process privileges

2. **Symbol Resolution Problems**
   - Reload symbols
   - Check symbol path
   - Verify debug information
   - Use manual address resolution

3. **Structure Dumping Errors**
   - Verify structure definitions
   - Check memory alignment
   - Use correct data types
   - Validate memory addresses

## Assessment Criteria

### Excellent (90-100%):
- Complete memory analysis
- Successful structure dumping
- Effective memory manipulation
- Clear documentation

### Good (80-89%):
- Most memory operations successful
- Basic structure analysis
- Some memory manipulation
- Adequate documentation

### Satisfactory (70-79%):
- Limited memory analysis
- Few structure operations
- Minimal memory manipulation
- Basic documentation

### Needs Improvement (<70%):
- Incomplete memory analysis
- No structure operations
- No memory manipulation
- Inadequate documentation

## Next Steps
After completing this lab:
1. Review theory materials
2. Practice with additional programs
3. Prepare for Section 2.4: Controlling Program Execution
4. Experiment with different memory layouts

## Additional Resources
- WinDbg Memory Commands Reference
- x86 Assembly Language Guide
- Memory Management Documentation
- Exploit Development Tutorials
