# OSED Section 2.4 Lab: Controlling the Program Execution in WinDbg

## Lab Overview
This lab provides hands-on experience with execution control in WinDbg, including breakpoint management, hardware breakpoints, and code stepping. Students will learn to control program execution effectively for exploit development.

## Prerequisites
- WinDbg Preview installed
- Basic understanding of program execution flow
- Sample executable with multiple functions

## Lab Environment Setup

### Required Software:
- Windows 10/11 (64-bit)
- WinDbg Preview
- Visual Studio or MinGW for C compilation
- Sample C program with multiple functions

### Sample C Program:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

int global_counter = 0;

void function_a(int param) {
    printf("Function A called with param: %d\n", param);
    global_counter++;
    Sleep(100);
}

void function_b(char *str) {
    printf("Function B called with string: %s\n", str);
    global_counter += 2;
    Sleep(200);
}

void function_c(int *ptr) {
    printf("Function C called with pointer: %p\n", ptr);
    if (ptr != NULL) {
        *ptr = 42;
    }
    global_counter += 3;
    Sleep(300);
}

void vulnerable_function(char *input) {
    char buffer[64];
    int local_var = 100;
    
    printf("Vulnerable function called\n");
    strcpy(buffer, input);
    
    printf("Buffer: %s\n", buffer);
    printf("Local var: %d\n", local_var);
    printf("Global counter: %d\n", global_counter);
}

int main() {
    int local_var = 10;
    char test_string[] = "Test String";
    int *test_ptr = &local_var;
    
    printf("Starting program execution...\n");
    
    // Call functions multiple times
    for (int i = 0; i < 3; i++) {
        function_a(i);
        function_b(test_string);
        function_c(test_ptr);
    }
    
    // Call vulnerable function
    vulnerable_function("Safe input");
    
    printf("Program completed. Global counter: %d\n", global_counter);
    
    Sleep(10000); // Keep process alive for debugging
    
    return 0;
}
```

## Lab Exercises

### Exercise 1: Software Breakpoint Management
**Duration:** 30 minutes

#### Objective:
Practice setting and managing software breakpoints.

#### Steps:

1. **Compile and Launch Program**
   ```bash
   gcc -g -o execution_sample.exe execution_sample.c
   ```

2. **Attach WinDbg and Load Symbols**
   - Start execution_sample.exe
   - Attach WinDbg to process
   - Load symbols: `.reload`

3. **Set Software Breakpoints**
   ```windbg
   # Set breakpoint at main function
   bp main
   
   # Set breakpoint at function_a
   bp function_a
   
   # Set breakpoint at vulnerable_function
   bp vulnerable_function
   
   # List all breakpoints
   bl
   ```

4. **Manage Breakpoint States**
   ```windbg
   # Disable breakpoint
   bd 0
   
   # Enable breakpoint
   be 0
   
   # Clear breakpoint
   bc 0
   
   # List breakpoints again
   bl
   ```

5. **Execute with Breakpoints**
   ```windbg
   # Continue execution
   g
   
   # When breakpoint hits, examine state
   r
   k
   ```

#### Expected Output:
```
0 e 00401000     0001 (0001)  0:**** execution_sample!main
1 e 00401020     0001 (0001)  0:**** execution_sample!function_a
2 e 00401040     0001 (0001)  0:**** execution_sample!vulnerable_function
```

### Exercise 2: Unresolved Function Breakpoints
**Duration:** 30 minutes

#### Objective:
Use unresolved function breakpoints to monitor dynamic loading.

#### Steps:

1. **Set Unresolved Breakpoints**
   ```windbg
   # Set unresolved breakpoint on printf
   bu printf
   
   # Set unresolved breakpoint on strcpy
   bu strcpy
   
   # Set unresolved breakpoint on Sleep
   bu Sleep
   
   # List unresolved breakpoints
   bl
   ```

2. **Monitor Function Resolution**
   ```windbg
   # Continue execution
   g
   
   # When unresolved breakpoint resolves, examine
   r
   k
   
   # Check if function is loaded
   lm
   ```

3. **Analyze Dynamic Loading**
   ```windbg
   # Check loaded modules
   lm
   
   # Check symbols for resolved functions
   x kernel32!Sleep
   x msvcrt!printf
   ```

#### Expected Output:
```
0 e 00401000     0001 (0001)  0:**** execution_sample!main
1 e 00401020     0001 (0001)  0:**** execution_sample!function_a
2 e 00401040     0001 (0001)  0:**** execution_sample!vulnerable_function
3 e 77c00000     0001 (0001)  0:**** kernel32!Sleep
4 e 77a00000     0001 (0001)  0:**** msvcrt!printf
```

### Exercise 3: Breakpoint-Based Actions
**Duration:** 30 minutes

#### Objective:
Implement breakpoint-based actions and conditional breakpoints.

#### Steps:

1. **Set Conditional Breakpoints**
   ```windbg
   # Set breakpoint with condition
   bp function_a "j @eax > 1; 'eax > 1'; g"
   
   # Set breakpoint with action
   bp function_b ".printf \"Function B called with: %s\\n\", @ecx; g"
   
   # Set breakpoint with multiple actions
   bp vulnerable_function "r; k; g"
   ```

2. **Implement Action Commands**
   ```windbg
   # Set breakpoint with stack trace
   bp function_c "k; g"
   
   # Set breakpoint with register dump
   bp main "r; g"
   
   # Set breakpoint with memory dump
   bp vulnerable_function "d esp; g"
   ```

3. **Test Action Execution**
   ```windbg
   # Continue execution and observe actions
   g
   
   # Check action output
   # Verify conditional breakpoints
   # Analyze action results
   ```

#### Expected Output:
```
Function B called with: Test String
Function C called with pointer: 0012ff80
Vulnerable function called
```

### Exercise 4: Hardware Breakpoints
**Duration:** 30 minutes

#### Objective:
Set and manage hardware breakpoints for memory access monitoring.

#### Steps:

1. **Set Memory Access Breakpoints**
   ```windbg
   # Set read breakpoint on global_counter
   ba r4 global_counter
   
   # Set write breakpoint on global_counter
   ba w4 global_counter
   
   # Set execute breakpoint on function
   ba e4 function_a
   ```

2. **Monitor Memory Access**
   ```windbg
   # Continue execution
   g
   
   # When hardware breakpoint hits, examine
   r
   k
   
   # Check memory contents
   d global_counter
   ```

3. **Analyze Hardware Breakpoints**
   ```windbg
   # List hardware breakpoints
   bl
   
   # Check debug registers
   r dr0
   r dr1
   r dr2
   r dr3
   r dr7
   ```

#### Expected Output:
```
0 e 00401000     0001 (0001)  0:**** execution_sample!main
1 e 00401020     0001 (0001)  0:**** execution_sample!function_a
2 e 00401040     0001 (0001)  0:**** execution_sample!vulnerable_function
3 e 00401060     0001 (0001)  0:**** execution_sample!function_b
4 e 00401080     0001 (0001)  0:**** execution_sample!function_c
5 e 004010a0     0001 (0001)  0:**** execution_sample!vulnerable_function
```

### Exercise 5: Code Stepping and Execution Control
**Duration:** 30 minutes

#### Objective:
Practice code stepping techniques and execution control.

#### Steps:

1. **Step Through Code Execution**
   ```windbg
   # Set breakpoint at main
   bp main
   g
   
   # Step over instructions
   p
   p
   p
   
   # Step into function calls
   t
   t
   t
   ```

2. **Control Execution Flow**
   ```windbg
   # Step out of function
   gu
   
   # Continue execution
   g
   
   # Step with exception handling
   gh
   ```

3. **Analyze Execution Path**
   ```windbg
   # Trace execution path
   k
   
   # Check register states
   r
   
   # Analyze memory contents
   d esp
   ```

#### Expected Output:
```
eax=00000000 ebx=00000000 ecx=00000000 edx=00000000 esi=00000000 edi=00000000
eip=00401000 esp=0012ff80 ebp=0012ff88 iopl=0         nv up ei pl zr na pe nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00000246
```

## Lab Deliverables

### 1. Breakpoint Management Report
Create a document containing:
- Screenshots of breakpoint configurations
- Breakpoint state management log
- Execution control documentation
- Breakpoint analysis results

### 2. Execution Control Log
Complete the following:
- Software breakpoint records
- Unresolved breakpoint analysis
- Action command results
- Hardware breakpoint monitoring

### 3. Code Stepping Summary
Document the following:
- Code stepping techniques
- Execution flow analysis
- Function tracing results
- Execution control methods

## Troubleshooting

### Common Issues:

1. **Breakpoints Not Hitting**
   - Check breakpoint addresses
   - Verify symbol resolution
   - Ensure correct process attachment
   - Check breakpoint states

2. **Hardware Breakpoint Limitations**
   - Limited number of hardware breakpoints
   - Debug register conflicts
   - Memory alignment requirements
   - Permission restrictions

3. **Execution Control Problems**
   - Process termination
   - Exception handling issues
   - Memory access violations
   - Symbol resolution errors

## Assessment Criteria

### Excellent (90-100%):
- Complete breakpoint management
- Successful execution control
- Effective code stepping
- Clear documentation

### Good (80-89%):
- Most breakpoints working
- Basic execution control
- Some code stepping
- Adequate documentation

### Satisfactory (70-79%):
- Limited breakpoint functionality
- Minimal execution control
- Few code stepping operations
- Basic documentation

### Needs Improvement (<70%):
- Incomplete breakpoint management
- No execution control
- No code stepping
- Inadequate documentation

## Next Steps
After completing this lab:
1. Review theory materials
2. Practice with additional programs
3. Prepare for Section 2.5: Additional WinDbg Features
4. Experiment with different execution scenarios

## Additional Resources
- WinDbg Breakpoint Commands Reference
- x86 Debug Register Documentation
- Execution Control Tutorials
- Debugging Techniques Guides
