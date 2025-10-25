# OSED Section 2.5 Lab: Additional WinDbg Features

## Lab Overview
This lab provides hands-on experience with advanced WinDbg features, including module listing, symbol examination, calculator usage, data formatting, and pseudo registers. Students will learn to utilize WinDbg's built-in utilities effectively.

## Prerequisites
- WinDbg Preview installed
- Basic understanding of WinDbg commands
- Sample executable with multiple modules

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

// Global variables
int global_int = 42;
char global_string[] = "Global String";
float global_float = 3.14f;

// Function declarations
void function_a(int param);
void function_b(char *str);
void function_c(int *ptr);
void vulnerable_function(char *input);

// Function implementations
void function_a(int param) {
    printf("Function A: %d\n", param);
    global_int += param;
}

void function_b(char *str) {
    printf("Function B: %s\n", str);
    strcpy(global_string, str);
}

void function_c(int *ptr) {
    printf("Function C: %p\n", ptr);
    if (ptr != NULL) {
        *ptr = 100;
    }
}

void vulnerable_function(char *input) {
    char buffer[64];
    int local_var = 200;
    
    printf("Vulnerable function: %s\n", input);
    strcpy(buffer, input);
    
    printf("Buffer: %s\n", buffer);
    printf("Local var: %d\n", local_var);
}

int main() {
    int local_var = 10;
    char test_string[] = "Test String";
    int *test_ptr = &local_var;
    
    printf("Starting program...\n");
    
    // Call functions
    function_a(5);
    function_b("Hello World");
    function_c(test_ptr);
    
    // Call vulnerable function
    vulnerable_function("Safe input");
    
    printf("Program completed.\n");
    
    Sleep(10000); // Keep process alive for debugging
    
    return 0;
}
```

## Lab Exercises

### Exercise 1: Module and Symbol Listing
**Duration:** 30 minutes

#### Objective:
Practice listing modules and examining symbols in WinDbg.

#### Steps:

1. **Compile and Launch Program**
   ```bash
   gcc -g -o features_sample.exe features_sample.c
   ```

2. **Attach WinDbg and Load Symbols**
   - Start features_sample.exe
   - Attach WinDbg to process
   - Load symbols: `.reload`

3. **List Modules**
   ```windbg
   # List all modules
   lm
   
   # List modules with verbose information
   lm v
   
   # List specific module
   lm m features_sample
   
   # List kernel modules
   lm k
   ```

4. **Examine Symbols**
   ```windbg
   # List all symbols for main module
   x features_sample!*
   
   # List symbols matching pattern
   x features_sample!function_*
   x features_sample!global_*
   
   # List symbols at specific address
   x 00401000
   ```

5. **Analyze Module Information**
   ```windbg
   # Get module information
   !lmi features_sample
   
   # Get module base address
   ? features_sample
   
   # Calculate module size
   ? features_sample+1000 - features_sample
   ```

#### Expected Output:
```
start    end        module name
00400000 00401000   features_sample   (deferred)             
77c00000 77d00000   ntdll      (deferred)             
77a00000 77b00000   kernel32   (deferred)             
77b00000 77c00000   msvcrt     (deferred)             

Symbols for features_sample:
00401000 features_sample!main
00401020 features_sample!function_a
00401040 features_sample!function_b
00401060 features_sample!function_c
00401080 features_sample!vulnerable_function
```

### Exercise 2: WinDbg Calculator Usage
**Duration:** 30 minutes

#### Objective:
Use WinDbg as a calculator for address arithmetic and expression evaluation.

#### Steps:

1. **Basic Calculator Operations**
   ```windbg
   # Simple arithmetic
   ? 10 + 20
   ? 0x1000 - 0x100
   ? 0x2000 * 2
   ? 0x4000 / 4
   
   # Address arithmetic
   ? 0x00400000 + 0x1000
   ? 0x00401000 - 0x00400000
   ```

2. **Register Calculations**
   ```windbg
   # Calculate with registers
   ? eax
   ? ebx + ecx
   ? esp - 4
   ? ebp + 8
   
   # Register analysis
   ? eip
   ? eip + 0x100
   ```

3. **Address Analysis**
   ```windbg
   # Analyze addresses
   ? 0x00400000
   ? 0x00401000
   ? 0x00400000 + 0x1000
   
   # Calculate offsets
   ? 0x00401000 - 0x00400000
   ? global_int - main
   ? function_a - main
   ```

4. **Expression Evaluation**
   ```windbg
   # Complex expressions
   ? (0x1000 + 0x2000) * 2
   ? 0x4000 / (0x1000 + 0x1000)
   ? 0x8000 - (0x1000 + 0x2000)
   ```

#### Expected Output:
```
Evaluate expression: 10 + 20 = 0000001e
Evaluate expression: 0x1000 - 0x100 = 00000f00
Evaluate expression: 0x2000 * 2 = 00004000
Evaluate expression: 0x4000 / 4 = 00001000
```

### Exercise 3: Data Output Formatting
**Duration:** 30 minutes

#### Objective:
Practice different data output formats in WinDbg.

#### Steps:

1. **Basic Data Dumping**
   ```windbg
   # Dump bytes
   db 0x00400000
   db global_int
   db global_string
   
   # Dump words
   dw 0x00400000
   dw global_int
   
   # Dump dwords
   dd 0x00400000
   dd global_int
   
   # Dump qwords
   dq 0x00400000
   dq global_int
   ```

2. **Custom Format Dumping**
   ```windbg
   # Dump with specific length
   db 0x00400000 L20
   dd 0x00400000 L10
   
   # Dump range
   db 0x00400000 0x00400020
   dd 0x00400000 0x00400040
   
   # Dump with different formats
   da global_string
   du global_string
   ```

3. **Structured Data Dumping**
   ```windbg
   # Dump structures
   dt global_int
   dt global_string
   dt global_float
   
   # Dump with verbose information
   dt -v global_int
   dt -v global_string
   ```

#### Expected Output:
```
00400000  2a 00 00 00 47 6c 6f 62-61 6c 20 53 74 72 69 6e  *...Global Strin
00400010  67 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  g...............
00400020  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
```

### Exercise 4: Pseudo Register Usage
**Duration:** 30 minutes

#### Objective:
Work with pseudo registers for advanced analysis.

#### Steps:

1. **Basic Pseudo Register Usage**
   ```windbg
   # Use pseudo registers
   ? $exentry
   ? $exreturn
   ? $ra
   ? $retreg
   
   # Analyze pseudo register values
   r $exentry
   r $exreturn
   ```

2. **Exception Handling Analysis**
   ```windbg
   # Set breakpoint on exception
   bp $exentry
   
   # Continue execution
   g
   
   # Analyze exception
   ? $exentry
   ? $exreturn
   ```

3. **Function Return Analysis**
   ```windbg
   # Set breakpoint on function
   bp function_a
   
   # Continue execution
   g
   
   # Analyze return
   ? $ra
   ? $retreg
   ```

4. **Pseudo Register Applications**
   ```windbg
   # Use pseudo registers in expressions
   ? $ra + 4
   ? $exentry - 0x1000
   ? $retreg * 2
   ```

#### Expected Output:
```
Evaluate expression: $exentry = 77c00000
Evaluate expression: $exreturn = 77c00000
Evaluate expression: $ra = 00401000
Evaluate expression: $retreg = 00000000
```

## Lab Deliverables

### 1. Module Analysis Report
Create a document containing:
- Screenshots of module listings
- Symbol examination results
- Module relationship analysis
- Address calculations

### 2. Calculator Usage Log
Complete the following:
- Calculator operation examples
- Address arithmetic results
- Expression evaluation records
- Register analysis

### 3. Data Formatting Examples
Document the following:
- Different output formats
- Custom formatting examples
- Structured data analysis
- Format comparison results

### 4. Pseudo Register Analysis
Document the following:
- Pseudo register usage
- Exception handling analysis
- Function return analysis
- Pseudo register applications

## Troubleshooting

### Common Issues:

1. **Module Listing Problems**
   - Check symbol loading
   - Verify process attachment
   - Ensure correct module names
   - Check module permissions

2. **Calculator Errors**
   - Verify expression syntax
   - Check address validity
   - Ensure proper data types
   - Validate register values

3. **Data Formatting Issues**
   - Check address validity
   - Verify data types
   - Ensure proper format specifiers
   - Check memory permissions

## Assessment Criteria

### Excellent (90-100%):
- Complete module analysis
- Successful calculator usage
- Effective data formatting
- Clear documentation

### Good (80-89%):
- Most module operations successful
- Basic calculator usage
- Some data formatting
- Adequate documentation

### Satisfactory (70-79%):
- Limited module analysis
- Few calculator operations
- Minimal data formatting
- Basic documentation

### Needs Improvement (<70%):
- Incomplete module analysis
- No calculator usage
- No data formatting
- Inadequate documentation

## Next Steps
After completing this lab:
1. Review theory materials
2. Practice with additional programs
3. Prepare for Section 2.6: Wrapping Up
4. Experiment with different WinDbg features

## Additional Resources
- WinDbg Advanced Commands Reference
- WinDbg Calculator Documentation
- Data Formatting Guides
- Pseudo Register Tutorials
