# OSED Section 2.1: Assembly Language Beginner Lab
## Introduction to x86 Assembly - Step-by-Step Guide

**Difficulty Level:** Beginner  
**Estimated Time:** 4-5 hours  
**Skills:** x86 assembly basics, Register operations, Memory operations, Control flow

---

## Table of Contents

1. [Lab Overview](#lab-overview)
2. [Exercise 1: Understanding Assembly Basics](#exercise-1-understanding-assembly-basics)
3. [Exercise 2: Register Operations](#exercise-2-register-operations)
4. [Exercise 3: Memory Operations](#exercise-3-memory-operations)
5. [Exercise 4: Arithmetic Operations](#exercise-4-arithmetic-operations)
5. [Exercise 5: Control Flow](#exercise-5-control-flow)
6. [Exercise 6: Function Calls](#exercise-6-function-calls)
7. [Lab Deliverables](#lab-deliverables)

---

## Lab Overview

This lab provides hands-on experience with x86 assembly language. You'll learn to read, write, and understand assembly code through practical exercises using WinDbg and simple assembly programs.

### Prerequisites
- Basic understanding of x86 architecture (from theory section)
- WinDbg installed and configured
- Text editor for writing assembly code
- NASM assembler (or similar) - we'll use inline assembly in C for simplicity

### Lab Environment Setup

#### Required Software:
- Windows 10/11 (64-bit)
- WinDbg Preview
- Visual Studio or MinGW for compilation
- Text editor (Notepad++, VS Code, etc.)

#### Compilation Settings:
We'll use inline assembly in C++ for easier learning:

**Visual Studio:**
- Create a Windows Desktop Application (C++)
- Set platform to x86 (32-bit)
- Build → Build Solution (F7)
- Debug → Start Without Debugging (Ctrl+F5)

**Note:** This lab uses **Visual Studio inline assembly syntax** (Intel syntax), which is simpler than GCC's AT&T syntax.

---

## Exercise 1: Understanding Assembly Basics

**Duration:** 45 minutes  
**Objective:** Learn to read and understand basic assembly instructions

### Step 1.1: Create Your First Assembly Program

**Action:** Create a file named `assembly_basics.cpp`:

```cpp
#include <stdio.h>

int main() {
    int result;
    
    // Visual Studio inline assembly: Basic MOV instruction (Intel syntax)
    __asm {
        mov eax, 42          // Move immediate value 42 into EAX
        mov result, eax      // Move EAX value into result variable
    }
    
    printf("Result: %d\n", result);
    getchar();  // Pause to keep program running
    return 0;
}
```

**Visual Studio Syntax Notes:**
- Use `__asm { }` block (simpler than GCC)
- Direct variable names (no `%0`, `%1` needed)
- No constraints needed
- Intel syntax: `mov eax, 42` (destination, source)
- Comments use `//` or `/* */`

**Step-by-Step Instructions:**

1. **Open your text editor** (Notepad++, VS Code, etc.)

2. **Create new file** named `assembly_basics.c`

3. **Copy the code above** into the file

4. **Save the file** in a convenient location (e.g., `C:\OSED\assembly\assembly_basics.c`)

5. **Compile the program in Visual Studio:**
   - Set platform to **x86** (top toolbar dropdown)
   - Press **F7** (Build Solution)
   - Or: Build → Build Solution
   - **Expected:** "Build succeeded" in Output window

6. **Run the program:**
   - Press **Ctrl+F5** (Start Without Debugging)
   - Or: Debug → Start Without Debugging
   - **Expected:** Console window shows "Result: 42"

---

### Step 1.2: Run and Analyze in WinDbg

**Step-by-Step Instructions:**

1. **Launch WinDbg Preview**

2. **Open the executable:**
   - In WinDbg: `File` → `Open Executable...`
   - Navigate to `assembly_basics.exe`
   - Click `Open`

3. **Load symbols:**
   ```windbg
   .reload
   ```

4. **Set breakpoint at main:**
   ```windbg
   bp assembly_basics!main
   ```

5. **Run the program:**
   ```windbg
   g
   ```

6. **View the assembly code:**
   ```windbg
   u assembly_basics!main
   ```

**Expected Output:**
```assembly
assembly_basics!main:
00401000 55              push    ebp
00401001 8bec            mov     ebp,esp
00401003 83ec04          sub     esp,4
00401006 c745fc00000000  mov     dword ptr [ebp-4],0
0040100d b828000000      mov     eax,28h        ; This is our MOV EAX, 42
00401012 8945fc          mov     dword ptr [ebp-4],eax
...
```

**Analysis:**
- `mov eax,28h` - Moves 42 (0x28 in hex) into EAX register
- `mov dword ptr [ebp-4],eax` - Moves EAX value into local variable

7. **Step through the code:**
   ```windbg
   p          ; Step one instruction
   r          ; View registers
   p          ; Step again
   r          ; View registers again
   ```

8. **Observe register changes:**
   - Before: `eax=00000000`
   - After: `eax=0000002a` (42 in decimal, 0x2A in hex)

**Documentation:** Record the register values before and after the MOV instruction

---

### Step 1.3: Understanding Basic Instructions

**Step-by-Step Instructions:**

1. **Create a new file** `instruction_demo.cpp`:

```cpp
#include <stdio.h>

int main() {
    int a = 10, b = 20, c = 0;
    
    __asm {
        // MOV - Move data
        mov eax, a          // Load variable 'a' into EAX
        mov ebx, b          // Load variable 'b' into EBX
        
        // ADD - Addition
        add eax, ebx        // EAX = EAX + EBX (10 + 20 = 30)
        mov c, eax          // Store result in 'c'
    }
    
    printf("a = %d, b = %d, c = %d\n", a, b, c);
    getchar();
    return 0;
}
```

2. **Compile in Visual Studio:**
   - Press **F7** (Build Solution)

3. **Analyze in WinDbg:**
   ```windbg
   windbg instruction_demo.exe
   bp instruction_demo!main
   g
   u instruction_demo!main
   ```

4. **Step through and observe:**
   ```windbg
   p          ; Step to MOV EAX, a
   r eax      ; View EAX (should be 10)
   p          ; Step to MOV EBX, b
   r ebx      ; View EBX (should be 20)
   p          ; Step to ADD EAX, EBX
   r eax      ; View EAX (should be 30)
   ```

**Key Concepts Learned:**
- **MOV:** Copies data from source to destination
- **ADD:** Adds two values together
- **Register usage:** EAX, EBX are general-purpose registers

---

## Exercise 2: Register Operations

**Duration:** 60 minutes  
**Objective:** Master register operations and data movement

### Step 2.1: Register-to-Register Operations

**Step-by-Step Instructions:**

1. **Create file** `register_ops.cpp`:

```cpp
#include <stdio.h>

int main() {
    int result1, result2, result3;
    
    __asm {
        // Register-to-register operations
        mov eax, 100        // EAX = 100
        mov ebx, 200        // EBX = 200
        mov ecx, eax        // ECX = EAX (copy EAX to ECX)
        mov edx, ebx        // EDX = EBX (copy EBX to EDX)
        
        // Store results
        mov result1, eax    // result1 = 100
        mov result2, ecx    // result2 = 100
        mov result3, edx    // result3 = 200
    }
    
    printf("result1 = %d, result2 = %d, result3 = %d\n", 
           result1, result2, result3);
    getchar();
    return 0;
}
```

2. **Compile and run in Visual Studio:**
   - Press **F7** to build
   - Press **Ctrl+F5** to run

3. **Analyze in WinDbg:**
   ```windbg
   windbg register_ops.exe
   bp register_ops!main
   g
   ```

4. **Step through each instruction:**
   ```windbg
   p          ; Step to first MOV
   r          ; View all registers
   p          ; Step to next MOV
   r          ; View registers again
   ```

5. **Document register values:**
   Create a table:
   | Instruction | EAX | EBX | ECX | EDX |
   |-------------|-----|-----|-----|-----|
   | Initial | ? | ? | ? | ? |
   | After MOV EAX, 100 | 100 | ? | ? | ? |
   | After MOV EBX, 200 | 100 | 200 | ? | ? |
   | After MOV ECX, EAX | 100 | 200 | 100 | ? |
   | After MOV EDX, EBX | 100 | 200 | 100 | 200 |

---

### Step 2.2: Immediate Values

**Step-by-Step Instructions:**

1. **Create file** `immediate_values.cpp`:

```cpp
#include <stdio.h>

int main() {
    int a, b, c;
    
    __asm {
        // Immediate values (constants)
        mov eax, 0x12345678  // Hexadecimal immediate
        mov ebx, 255         // Decimal immediate
        mov ecx, 0AAh        // Binary 10101010 = 0xAA (h suffix for hex)
        
        mov a, eax
        mov b, ebx
        mov c, ecx
    }
    
    printf("a = 0x%x, b = %d, c = %d\n", a, b, c);
    getchar();
    return 0;
}
```

2. **Compile in Visual Studio:**
   - Press **F7** to build

3. **In WinDbg, examine the immediate values:**
   ```windbg
   u immediate_values!main
   ```

**Expected Output:**
```assembly
mov eax,12345678h    ; Notice the 'h' suffix for hex
mov ebx,0FFh         ; 255 in hex
```

**Key Concepts:**
- **Immediate values:** Constants embedded in instructions
- **Hexadecimal:** Use `0x` prefix or `h` suffix
- **Decimal:** Default format
- **Binary:** Use `0b` prefix (if supported)

---

### Step 2.3: Register Arithmetic

**Step-by-Step Instructions:**

1. **Create file** `register_arithmetic.cpp`:

```cpp
#include <stdio.h>

int main() {
    int add_result, sub_result, mul_result, div_result;
    
    __asm {
        mov eax, 50
        mov ebx, 10
        
        // Addition
        mov ecx, eax
        add ecx, ebx        // ECX = 50 + 10 = 60
        mov add_result, ecx
        
        // Subtraction
        mov ecx, eax
        sub ecx, ebx        // ECX = 50 - 10 = 40
        mov sub_result, ecx
        
        // Multiplication
        mov eax, 50
        mov ebx, 10
        mul ebx             // EAX = EAX * EBX = 500
        mov mul_result, eax
        
        // Division
        mov eax, 50
        mov ebx, 10
        mov edx, 0          // Clear EDX (required for division)
        div ebx             // EAX = EAX / EBX = 5
        mov div_result, eax
    }
    
    printf("Add: %d, Sub: %d, Mul: %d, Div: %d\n",
           add_result, sub_result, mul_result, div_result);
    getchar();
    return 0;
}
```

2. **Compile and test in Visual Studio:**
   - Press **F7** to build
   - Press **Ctrl+F5** to run

3. **Analyze in WinDbg:**
   ```windbg
   windbg register_arithmetic.exe
   bp register_arithmetic!main
   g
   ```

4. **Step through arithmetic operations:**
   ```windbg
   p          ; Step to ADD
   r eax ebx ecx
   p          ; After ADD
   r ecx      ; Should be 60
   ```

**Important Notes:**
- **MUL:** Multiplies EAX by operand, result in EDX:EAX
- **DIV:** Divides EDX:EAX by operand, quotient in EAX, remainder in EDX
- **EDX must be cleared** before division (or set for 64-bit dividend)

---

## Exercise 3: Memory Operations

**Duration:** 60 minutes  
**Objective:** Learn to read from and write to memory

### Step 3.1: Reading from Memory

**Step-by-Step Instructions:**

1. **Create file** `memory_read.cpp`:

```cpp
#include <stdio.h>

int main() {
    int value = 0x12345678;
    int result;
    
    __asm {
        // Read from memory variable
        mov eax, value      // Load value from memory into EAX
        mov result, eax     // Store EAX into result
    }
    
    printf("Original: 0x%x, Result: 0x%x\n", value, result);
    getchar();
    return 0;
}
```

2. **Compile in Visual Studio:**
   - Press **F7** to build

3. **In WinDbg, examine memory access:**
   ```windbg
   windbg memory_read.exe
   bp memory_read!main
   g
   u memory_read!main
   ```

4. **View the memory address:**
   ```windbg
   ? memory_read!value
   d memory_read!value
   ```

5. **Step through and observe:**
   ```windbg
   p          ; Step to MOV EAX, value
   r eax      ; EAX should contain 0x12345678
   d [ebp-4]  ; View local variable in memory
   ```

---

### Step 3.2: Writing to Memory

**Step-by-Step Instructions:**

1. **Create file** `memory_write.cpp`:

```cpp
#include <stdio.h>

int main() {
    int value = 0;
    
    __asm {
        // Write to memory variable
        mov eax, 0deadbeefh  // Load immediate value (h suffix for hex)
        mov value, eax       // Write EAX to memory variable
    }
    
    printf("Value after write: 0x%x\n", value);
    getchar();
    return 0;
}
```

2. **Compile and test in Visual Studio:**
   - Press **F7** to build
   - Press **Ctrl+F5** to run

3. **In WinDbg, observe memory changes:**
   ```windbg
   windbg memory_write.exe
   bp memory_write!main
   g
   ```

4. **Examine memory before write:**
   ```windbg
   ? memory_write!value
   d memory_write!value
   ```

5. **Step through write operation:**
   ```windbg
   p          ; Step to MOV EAX, 0xdeadbeef
   r eax      ; Verify EAX = 0xdeadbeef
   p          ; Step to MOV value, EAX
   d memory_write!value  ; Verify memory changed
   ```

---

### Step 3.3: Memory Addressing Modes

**Step-by-Step Instructions:**

1. **Create file** `addressing_modes.cpp`:

```cpp
#include <stdio.h>

int main() {
    int array[5] = {10, 20, 30, 40, 50};
    int result1, result2, result3;
    
    __asm {
        // Direct addressing - access variable directly
        mov eax, array[0]    // EAX = array[0] = 10
        mov result1, eax
        
        // Indexed addressing - access array element
        mov ebx, 2          // Index = 2
        mov eax, array[ebx*4] // EAX = array[2] = 30 (ebx*4 for int size)
        mov result2, eax
        
        // Pointer-based addressing
        lea esi, array      // Load address of array into ESI
        mov eax, [esi+12]   // EAX = array[3] = 40 (12 = 3*4 bytes)
        mov result3, eax
    }
    
    printf("result1 = %d, result2 = %d, result3 = %d\n",
           result1, result2, result3);
    getchar();
    return 0;
}
```

2. **Compile and test in Visual Studio:**
   - Press **F7** to build
   - Press **Ctrl+F5** to run

3. **Analyze addressing in WinDbg:**
   ```windbg
   windbg addressing_modes.exe
   bp addressing_modes!main
   g
   u addressing_modes!main
   ```

**Key Addressing Modes:**
- **Direct:** `mov eax, variable`
- **Register Indirect:** `mov eax, [ebx]`
- **Indexed:** `mov eax, array[ebx*4]`
- **Base+Index:** `mov eax, [esi+edi*4]`
- **Displacement:** `mov eax, [ebp-4]`

---

## Exercise 4: Arithmetic Operations

**Duration:** 45 minutes  
**Objective:** Master arithmetic instructions

### Step 4.1: Basic Arithmetic

**Step-by-Step Instructions:**

1. **Create file** `arithmetic.cpp`:

```cpp
#include <stdio.h>

int main() {
    int a = 100, b = 30;
    int add, sub, mul, div_result, mod;
    
    __asm {
        // Addition
        mov eax, a
        add eax, b          // EAX = a + b
        mov add, eax
        
        // Subtraction
        mov eax, a
        sub eax, b          // EAX = a - b
        mov sub, eax
        
        // Multiplication
        mov eax, a
        mov ebx, b
        mul ebx             // EAX = EAX * EBX (result in EDX:EAX)
        mov mul, eax
        
        // Division
        mov eax, a
        mov ebx, b
        mov edx, 0          // Clear EDX
        div ebx             // EAX = EAX / EBX, EDX = remainder
        mov div_result, eax
        mov mod, edx        // Remainder (modulo)
    }
    
    printf("a = %d, b = %d\n", a, b);
    printf("Add: %d, Sub: %d, Mul: %d, Div: %d, Mod: %d\n",
           add, sub, mul, div_result, mod);
    getchar();
    return 0;
}
```

2. **Compile and test in Visual Studio:**
   - Press **F7** to build
   - Press **Ctrl+F5** to run

3. **Analyze in WinDbg:**
   ```windbg
   windbg arithmetic.exe
   bp arithmetic!main
   g
   ```

4. **Step through each operation:**
   ```windbg
   p          ; Step to ADD
   r eax      ; View result
   p          ; Step to SUB
   r eax      ; View result
   p          ; Step to MUL
   r eax edx  ; View result (EDX:EAX for 64-bit)
   p          ; Step to DIV
   r eax edx  ; View quotient and remainder
   ```

---

### Step 4.2: Increment and Decrement

**Step-by-Step Instructions:**

1. **Create file** `inc_dec.cpp`:

```cpp
#include <stdio.h>

int main() {
    int value = 10;
    
    __asm {
        // Increment
        mov eax, value
        inc eax             // EAX = EAX + 1
        mov value, eax
        
        // Decrement
        dec eax             // EAX = EAX - 1
        mov value, eax
        
        // Add/Subtract immediate
        add eax, 5          // EAX = EAX + 5
        sub eax, 3          // EAX = EAX - 3
        mov value, eax
    }
    
    printf("Final value: %d\n", value);
    getchar();
    return 0;
}
```

2. **Compile and test in Visual Studio:**
   - Press **F7** to build
   - Press **Ctrl+F5** to run

**Key Instructions:**
- **INC:** Increment by 1 (faster than ADD EAX, 1)
- **DEC:** Decrement by 1 (faster than SUB EAX, 1)
- **ADD/SUB:** Can add/subtract any value

---

## Exercise 5: Control Flow

**Duration:** 60 minutes  
**Objective:** Learn conditional jumps and loops

### Step 5.1: Conditional Jumps

**Step-by-Step Instructions:**

1. **Create file** `conditional_jumps.cpp`:

```cpp
#include <stdio.h>

int main() {
    int a = 10, b = 20;
    int result = 0;
    
    __asm {
        mov eax, a
        mov ebx, b
        
        // Compare EAX and EBX
        cmp eax, ebx        // Compare a and b
        
        // Conditional jumps
        jg greater          // Jump if a > b
        jl less            // Jump if a < b
        je equal           // Jump if a == b
        
    greater:
        mov result, 1      // a > b
        jmp done
        
    less:
        mov result, -1     // a < b
        jmp done
        
    equal:
        mov result, 0      // a == b
        
    done:
        nop                // No operation (label placeholder)
    }
    
    printf("a = %d, b = %d, result = %d\n", a, b, result);
    getchar();
    return 0;
}
```

2. **Compile and test in Visual Studio:**
   - Press **F7** to build
   - Press **Ctrl+F5** to run

3. **Analyze in WinDbg:**
   ```windbg
   windbg conditional_jumps.exe
   bp conditional_jumps!main
   g
   u conditional_jumps!main
   ```

4. **Step through conditional logic:**
   ```windbg
   p          ; Step to CMP
   r eax ebx  ; View values being compared
   p          ; Step to conditional jump
   r efl      ; View flags register
   ```

**Common Conditional Jumps:**
- **JE/JZ:** Jump if equal/zero (ZF = 1)
- **JNE/JNZ:** Jump if not equal/zero (ZF = 0)
- **JG/JNLE:** Jump if greater (signed)
- **JL/JNGE:** Jump if less (signed)
- **JA/JNBE:** Jump if above (unsigned)
- **JB/JNAE:** Jump if below (unsigned)

---

### Step 5.2: Loops

**Step-by-Step Instructions:**

1. **Create file** `loops.cpp`:

```cpp
#include <stdio.h>

int main() {
    int sum = 0;
    
    __asm {
        mov ecx, 10         // Loop counter (10 iterations)
        mov eax, 0          // Sum accumulator
        
    loop_start:
        add eax, ecx        // Add counter to sum
        loop loop_start     // Decrement ECX, jump if ECX != 0
        
        mov sum, eax
    }
    
    printf("Sum of 10+9+8+...+1 = %d\n", sum);
    getchar();
    return 0;
}
```

2. **Compile and test in Visual Studio:**
   - Press **F7** to build
   - Press **Ctrl+F5** to run

3. **Analyze loop in WinDbg:**
   ```windbg
   windbg loops.exe
   bp loops!main
   g
   ```

4. **Step through loop iterations:**
   ```windbg
   p          ; Step into loop
   r ecx eax  ; View counter and sum
   p          ; Step through loop
   r ecx eax  ; Observe changes
   ```

**Loop Instructions:**
- **LOOP:** Decrements ECX, jumps if ECX != 0
- **LOOPE/LOOPZ:** Loop while equal/zero
- **LOOPNE/LOOPNZ:** Loop while not equal/zero

---

## Exercise 6: Function Calls

**Duration:** 45 minutes  
**Objective:** Understand function calling conventions

### Step 6.1: Simple Function Call

**Step-by-Step Instructions:**

1. **Create file** `function_call.cpp`:

```cpp
#include <stdio.h>

int add_numbers(int a, int b) {
    int result;
    __asm {
        mov eax, [ebp+8]    // First parameter (a)
        mov ebx, [ebp+12]   // Second parameter (b)
        add eax, ebx        // result = a + b
        mov result, eax
    }
    return result;
}

int main() {
    int sum = add_numbers(10, 20);
    printf("Sum: %d\n", sum);
    getchar();
    return 0;
}
```

2. **Compile and test in Visual Studio:**
   - Press **F7** to build
   - Press **Ctrl+F5** to run

3. **Analyze function call in WinDbg:**
   ```windbg
   windbg function_call.exe
   bp function_call!add_numbers
   g
   ```

4. **Examine stack frame:**
   ```windbg
   k          ; View stack trace
   d esp      ; View stack contents
   d ebp      ; View base pointer
   ```

5. **Examine parameters:**
   ```windbg
   d [ebp+8]  ; First parameter (a = 10)
   d [ebp+12] ; Second parameter (b = 20)
   ```

**Stack Frame Layout:**
```
[ebp+12]  Second parameter (b)
[ebp+8]   First parameter (a)
[ebp+4]   Return address
[ebp+0]   Previous EBP
[ebp-4]   Local variables
```

---

## Lab Deliverables

### 1. Assembly Code Collection
Create a folder containing all your assembly programs:
- `assembly_basics.cpp`
- `instruction_demo.cpp`
- `register_ops.cpp`
- `immediate_values.cpp`
- `register_arithmetic.cpp`
- `memory_read.cpp`
- `memory_write.cpp`
- `addressing_modes.cpp`
- `arithmetic.cpp`
- `inc_dec.cpp`
- `conditional_jumps.cpp`
- `loops.cpp`
- `function_call.cpp`

### 2. WinDbg Analysis Reports
For each exercise, document:
- **Assembly code disassembly** (screenshots)
- **Register values** before and after operations
- **Memory contents** at key points
- **Stack frame** analysis for function calls

### 3. Learning Summary
Write a summary covering:
- **Key concepts learned:** List all assembly instructions you learned
- **Register usage:** How each register is used
- **Memory operations:** Different addressing modes
- **Control flow:** How jumps and loops work
- **Challenges encountered:** What was difficult and why
- **Questions for further study:** Topics you want to explore more

---

## Troubleshooting

### Common Issues

**Issue 1: Compilation Errors in Visual Studio**
- **Error:** `error C4235: nonstandard extension used : '__asm' keyword not supported on this architecture`
  - **Cause:** Trying to compile for x64 (64-bit)
  - **Solution:** Set platform to **x86** (32-bit) in Visual Studio
  - **Fix:** Top toolbar → Change "x64" to "x86"

- **Error:** `unresolved external symbol`
  - **Cause:** Missing function implementation
  - **Solution:** Ensure all functions are implemented

- **Error:** `syntax error : missing ')' before '{'`
  - **Cause:** Incorrect `__asm` syntax
  - **Solution:** Use `__asm { }` with curly braces

**Issue 2: Program Crashes**
- **Solution:** Check register usage (don't modify ESP/EBP incorrectly)
- **Solution:** Ensure stack is balanced (push/pop match)
- **Solution:** Don't modify registers that Visual Studio is using

**Issue 3: Wrong Results**
- **Solution:** Verify register values in Visual Studio debugger
- **Solution:** Check memory addresses and offsets
- **Solution:** Ensure proper data sizes (byte, word, dword)
- **Solution:** Use Visual Studio debugger to step through assembly

**Issue 4: Can't Debug Assembly**
- **Solution:** Enable disassembly view: Debug → Windows → Disassembly
- **Solution:** View registers: Debug → Windows → Registers
- **Solution:** Set breakpoints before `__asm` block

### Visual Studio Debugging Tips

1. **View Disassembly:**
   - Debug → Windows → Disassembly (Alt+8)
   - See compiled assembly code

2. **View Registers:**
   - Debug → Windows → Registers (Alt+5)
   - See register values in real-time

3. **Step Through Assembly:**
   - F10 (Step Over) or F11 (Step Into)
   - Step through each assembly instruction

4. **Set Breakpoints:**
   - Click left margin or press F9
   - Breakpoints work in `__asm` blocks

---

## Next Steps

After completing this beginner assembly lab:
1. **Practice:** Modify the examples and experiment
2. **Review:** Go through each exercise again
3. **Extend:** Try creating your own assembly programs
4. **Prepare:** Move to intermediate assembly lab
5. **Study:** Read x86 instruction set reference

---

## Additional Resources

- **Intel x86 Manual:** https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- **x86 Assembly Cheat Sheet:** See `../resources/cheatsheets/x86-assembly.md`
- **Online Assembler:** https://defuse.ca/online-x86-assembler.htm
- **Assembly Tutorials:** https://www.tutorialspoint.com/assembly_programming/

---

**End of Assembly Beginner Lab**

