# OSED Section 2.1: Assembly Language Intermediate Lab
## Advanced x86 Assembly - Step-by-Step Guide

**Difficulty Level:** Intermediate  
**Estimated Time:** 5-6 hours  
**Skills:** Advanced instructions, String operations, Stack manipulation, Calling conventions

---

## Table of Contents

1. [Lab Overview](#lab-overview)
2. [Exercise 1: Advanced Instructions](#exercise-1-advanced-instructions)
3. [Exercise 2: String Operations](#exercise-2-string-operations)
4. [Exercise 3: Stack Operations](#exercise-3-stack-operations)
5. [Exercise 4: Calling Conventions](#exercise-4-calling-conventions)
6. [Exercise 5: Bitwise Operations](#exercise-5-bitwise-operations)
7. [Exercise 6: Advanced Control Flow](#exercise-6-advanced-control-flow)
8. [Lab Deliverables](#lab-deliverables)

---

## Lab Overview

This intermediate lab builds on beginner assembly knowledge, introducing advanced instructions, string operations, stack manipulation, and calling conventions essential for exploit development.

### Prerequisites
- Completion of Assembly Beginner Lab
- Understanding of basic x86 instructions
- Familiarity with WinDbg
- Understanding of stack frames

---

## Exercise 1: Advanced Instructions

**Duration:** 60 minutes  
**Objective:** Master advanced x86 instructions

### Step 1.1: LEA (Load Effective Address)

**Step-by-Step Instructions:**

1. **Create file** `lea_instruction.c`:

```c
#include <stdio.h>

int main() {
    int array[5] = {10, 20, 30, 40, 50};
    int *ptr;
    int value;
    
    __asm {
        // LEA loads the address, not the value
        lea eax, array          // EAX = address of array
        mov ptr, eax            // Store address in pointer
        
        // Compare with MOV
        mov ebx, array[0]       // EBX = value at array[0] (10)
        
        // Use LEA for address arithmetic
        lea ecx, [eax + 8]      // ECX = address of array[2]
        mov edx, [ecx]          // EDX = value at array[2] (30)
        mov value, edx
    }
    
    printf("Array address: %p\n", ptr);
    printf("Array[0] value: %d\n", array[0]);
    printf("Array[2] value: %d\n", value);
    getchar();
    return 0;
}
```

2. **Compile and analyze:**
   ```bash
   gcc -m32 -g -o lea_instruction.exe lea_instruction.c
   ```

3. **In WinDbg, examine LEA:**
   ```windbg
   windbg lea_instruction.exe
   bp lea_instruction!main
   g
   u lea_instruction!main
   ```

4. **Compare LEA vs MOV:**
   ```windbg
   p          ; Step to LEA
   r eax      ; View address loaded
   p          ; Step to MOV
   r ebx      ; View value loaded
   ```

**Key Concept:**
- **LEA:** Calculates address but doesn't access memory
- **MOV:** Accesses memory to get value
- **LEA is faster** for address arithmetic

---

### Step 1.2: XCHG (Exchange)

**Step-by-Step Instructions:**

1. **Create file** `xchg_instruction.c`:

```c
#include <stdio.h>

int main() {
    int a = 10, b = 20;
    
    __asm {
        mov eax, a
        mov ebx, b
        
        // Exchange values
        xchg eax, ebx        // Swap EAX and EBX
        
        mov a, eax
        mov b, ebx
    }
    
    printf("After exchange: a = %d, b = %d\n", a, b);
    getchar();
    return 0;
}
```

2. **Compile and test:**
   ```bash
   gcc -m32 -g -o xchg_instruction.exe xchg_instruction.c
   .\xchg_instruction.exe
   ```

3. **Observe in WinDbg:**
   ```windbg
   windbg xchg_instruction.exe
   bp xchg_instruction!main
   g
   ```

4. **Step through exchange:**
   ```windbg
   p          ; Before XCHG
   r eax ebx  ; EAX=10, EBX=20
   p          ; After XCHG
   r eax ebx  ; EAX=20, EBX=10
   ```

---

### Step 1.3: NOP and Other Instructions

**Step-by-Step Instructions:**

1. **Create file** `misc_instructions.c`:

```c
#include <stdio.h>

int main() {
    int value = 0x12345678;
    int result1, result2, result3;
    
    __asm {
        // NOP - No operation (useful for padding)
        nop
        
        // NOT - Bitwise NOT
        mov eax, value
        not eax              // EAX = ~EAX
        mov result1, eax
        
        // NEG - Two's complement negation
        mov eax, 10
        neg eax              // EAX = -10
        mov result2, eax
        
        // TEST - Like CMP but doesn't modify operands
        mov eax, 5
        test eax, eax        // Test if EAX is zero
        jnz not_zero         // Jump if not zero
        
    not_zero:
        mov result3, 1
    }
    
    printf("NOT result: 0x%x\n", result1);
    printf("NEG result: %d\n", result2);
    printf("TEST result: %d\n", result3);
    getchar();
    return 0;
}
```

2. **Compile and analyze:**
   ```bash
   gcc -m32 -g -o misc_instructions.exe misc_instructions.c
   ```

3. **Examine in WinDbg:**
   ```windbg
   windbg misc_instructions.exe
   bp misc_instructions!main
   g
   u misc_instructions!main
   ```

---

## Exercise 2: String Operations

**Duration:** 75 minutes  
**Objective:** Master string manipulation instructions

### Step 2.1: MOVS (Move String)

**Step-by-Step Instructions:**

1. **Create file** `string_operations.c`:

```c
#include <stdio.h>
#include <string.h>

int main() {
    char source[20] = "Hello, World!";
    char destination[20];
    
    __asm {
        // Set up for string operations
        lea esi, source       // ESI = source address
        lea edi, destination  // EDI = destination address
        mov ecx, 13          // Length of string
        
        // Direction flag: 0 = forward (increment)
        cld                  // Clear direction flag (forward)
        
        // Move string byte by byte
    move_loop:
        movsb                // MOV [EDI], [ESI]; INC ESI; INC EDI
        loop move_loop       // Decrement ECX, loop if not zero
        
        // Null terminate
        mov byte ptr [edi], 0
    }
    
    printf("Source: %s\n", source);
    printf("Destination: %s\n", destination);
    getchar();
    return 0;
}
```

2. **Compile and test:**
   ```bash
   gcc -m32 -g -o string_operations.exe string_operations.c
   .\string_operations.exe
   ```

3. **Analyze in WinDbg:**
   ```windbg
   windbg string_operations.exe
   bp string_operations!main
   g
   ```

4. **Step through string move:**
   ```windbg
   p          ; Step to loop
   r esi edi ecx
   d esi L13  ; View source string
   p          ; Step through loop
   d edi L13  ; View destination string
   ```

**String Instructions:**
- **MOVSB/MOVSW/MOVSD:** Move string (byte/word/dword)
- **CMPSB/CMPSW/CMPSD:** Compare strings
- **SCASB/SCASW/SCASD:** Scan string
- **LODSB/LODSW/LODSD:** Load string
- **STOSB/STOSW/STOSD:** Store string

---

### Step 2.2: String Comparison

**Step-by-Step Instructions:**

1. **Create file** `string_compare.c`:

```c
#include <stdio.h>
#include <string.h>

int main() {
    char str1[] = "Hello";
    char str2[] = "Hello";
    char str3[] = "World";
    int result1, result2;
    
    __asm {
        // Compare str1 and str2
        lea esi, str1
        lea edi, str2
        mov ecx, 5          // Length
        
        cld                 // Forward direction
        repe cmpsb          // Compare while equal
        
        // After REPE CMPSB:
        // If strings equal: ECX = 0, ZF = 1
        // If strings differ: ECX != 0, ZF = 0
        je equal1
        mov result1, 0      // Not equal
        jmp next_compare
        
    equal1:
        mov result1, 1      // Equal
        
    next_compare:
        // Compare str1 and str3
        lea esi, str1
        lea edi, str3
        mov ecx, 5
        
        cld
        repe cmpsb
        
        je equal2
        mov result2, 0      // Not equal
        jmp done
        
    equal2:
        mov result2, 1      // Equal
        
    done:
        nop
    }
    
    printf("str1 == str2: %d\n", result1);
    printf("str1 == str3: %d\n", result2);
    getchar();
    return 0;
}
```

2. **Compile and test:**
   ```bash
   gcc -m32 -g -o string_compare.exe string_compare.c
   .\string_compare.exe
   ```

---

## Exercise 3: Stack Operations

**Duration:** 60 minutes  
**Objective:** Master stack manipulation

### Step 3.1: PUSH and POP

**Step-by-Step Instructions:**

1. **Create file** `stack_operations.c`:

```c
#include <stdio.h>

int main() {
    int value1, value2, value3;
    
    __asm {
        // Push values onto stack
        push 10             // Push immediate value
        push 20
        push 30
        
        // Pop values from stack (LIFO - Last In First Out)
        pop eax             // EAX = 30 (last pushed)
        mov value3, eax
        
        pop eax             // EAX = 20
        mov value2, eax
        
        pop eax             // EAX = 10 (first pushed)
        mov value1, eax
    }
    
    printf("Popped values: %d, %d, %d\n", value1, value2, value3);
    getchar();
    return 0;
}
```

2. **Compile and test:**
   ```bash
   gcc -m32 -g -o stack_operations.exe stack_operations.c
   .\stack_operations.exe
   ```

3. **Analyze stack in WinDbg:**
   ```windbg
   windbg stack_operations.exe
   bp stack_operations!main
   g
   ```

4. **Observe stack changes:**
   ```windbg
   r esp      ; View stack pointer
   d esp      ; View stack contents
   p          ; Step to PUSH
   r esp      ; ESP decreased by 4
   d esp      ; View new stack value
   ```

**Stack Behavior:**
- **PUSH:** Decrements ESP by 4, stores value at [ESP]
- **POP:** Loads value from [ESP], increments ESP by 4
- **Stack grows downward** (toward lower addresses)

---

### Step 3.2: Stack Frame Setup

**Step-by-Step Instructions:**

1. **Create file** `stack_frame.c`:

```c
#include <stdio.h>

int add(int a, int b) {
    int result;
    __asm {
        // Standard function prologue
        push ebp            // Save old base pointer
        mov ebp, esp        // Set new base pointer
        
        // Allocate space for local variables
        sub esp, 4          // Allocate 4 bytes for 'result'
        
        // Access parameters
        mov eax, [ebp+8]    // First parameter (a)
        mov ebx, [ebp+12]   // Second parameter (b)
        add eax, ebx
        mov [ebp-4], eax    // Store in local variable
        
        // Function epilogue
        mov eax, [ebp-4]    // Return value in EAX
        mov esp, ebp        // Restore stack pointer
        pop ebp             // Restore old base pointer
        ret                 // Return
    }
}

int main() {
    int sum = add(10, 20);
    printf("Sum: %d\n", sum);
    getchar();
    return 0;
}
```

2. **Compile and analyze:**
   ```bash
   gcc -m32 -g -o stack_frame.exe stack_frame.c
   ```

3. **Examine stack frame in WinDbg:**
   ```windbg
   windbg stack_frame.exe
   bp stack_frame!add
   g
   ```

4. **View stack frame structure:**
   ```windbg
   k          ; Stack trace
   r ebp esp  ; View base and stack pointers
   d ebp      ; View stack frame
   ```

**Stack Frame Layout:**
```
High Address
[ebp+12]  Second parameter (b)
[ebp+8]   First parameter (a)
[ebp+4]   Return address
[ebp+0]   Previous EBP (saved)
[ebp-4]   Local variables
Low Address (ESP points here)
```

---

## Exercise 4: Calling Conventions

**Duration:** 75 minutes  
**Objective:** Understand different calling conventions

### Step 4.1: __cdecl Convention

**Step-by-Step Instructions:**

1. **Create file** `cdecl_convention.c`:

```c
#include <stdio.h>

// __cdecl: Caller cleans stack, parameters pushed right-to-left
int __cdecl add_cdecl(int a, int b, int c) {
    int result;
    __asm {
        mov eax, [ebp+8]    // First parameter (a) - pushed last
        add eax, [ebp+12]   // Second parameter (b)
        add eax, [ebp+16]   // Third parameter (c) - pushed first
        mov result, eax
    }
    return result;
}

int main() {
    int sum;
    
    __asm {
        // __cdecl: Push parameters right-to-left
        push 30             // Push c first (rightmost)
        push 20             // Push b
        push 10             // Push a last (leftmost)
        
        call add_cdecl      // Call function
        
        // Caller cleans stack (remove 12 bytes = 3 params * 4)
        add esp, 12         // Clean up stack
        
        mov sum, eax        // Get return value
    }
    
    printf("Sum: %d\n", sum);
    getchar();
    return 0;
}
```

2. **Compile and analyze:**
   ```bash
   gcc -m32 -g -o cdecl_convention.exe cdecl_convention.c
   ```

3. **Examine calling convention:**
   ```windbg
   windbg cdecl_convention.exe
   bp cdecl_convention!main
   g
   ```

4. **Step through call:**
   ```windbg
   p          ; Step to PUSH
   d esp      ; View stack
   p          ; Continue stepping
   d esp      ; Observe stack changes
   ```

**__cdecl Characteristics:**
- Parameters pushed **right-to-left**
- **Caller** cleans stack
- Return value in **EAX**
- Supports **variable arguments**

---

### Step 4.2: __stdcall Convention

**Step-by-Step Instructions:**

1. **Create file** `stdcall_convention.c`:

```c
#include <stdio.h>

// __stdcall: Callee cleans stack, parameters pushed right-to-left
int __stdcall add_stdcall(int a, int b) {
    int result;
    __asm {
        mov eax, [ebp+8]    // First parameter
        add eax, [ebp+12]   // Second parameter
        mov result, eax
        // Callee cleans stack with RET 8 (8 = 2 params * 4 bytes)
    }
    return result;
}

int main() {
    int sum;
    
    __asm {
        // __stdcall: Push parameters right-to-left
        push 20             // Push b first
        push 10             // Push a last
        
        call add_stdcall    // Call function
        // No stack cleanup needed - callee does it
        
        mov sum, eax
    }
    
    printf("Sum: %d\n", sum);
    getchar();
    return 0;
}
```

2. **Compile and analyze:**
   ```bash
   gcc -m32 -g -o stdcall_convention.exe stdcall_convention.c
   ```

**__stdcall Characteristics:**
- Parameters pushed **right-to-left**
- **Callee** cleans stack (RET n)
- Return value in **EAX**
- Used by Windows API

---

### Step 4.3: __fastcall Convention

**Step-by-Step Instructions:**

1. **Create file** `fastcall_convention.c`:

```c
#include <stdio.h>

// __fastcall: First 2 params in ECX, EDX, rest on stack
int __fastcall add_fastcall(int a, int b, int c) {
    int result;
    __asm {
        // First two parameters already in ECX and EDX
        mov eax, ecx        // a is in ECX
        add eax, edx        // b is in EDX
        add eax, [ebp+8]    // c is on stack
        mov result, eax
    }
    return result;
}

int main() {
    int sum;
    
    __asm {
        // __fastcall: First 2 params in registers
        mov ecx, 10         // First parameter in ECX
        mov edx, 20         // Second parameter in EDX
        push 30             // Third parameter on stack
        
        call add_fastcall
        add esp, 4          // Clean up stack (only one param)
        
        mov sum, eax
    }
    
    printf("Sum: %d\n", sum);
    getchar();
    return 0;
}
```

2. **Compile and analyze:**
   ```bash
   gcc -m32 -g -o fastcall_convention.exe fastcall_convention.c
   ```

**__fastcall Characteristics:**
- First **2 parameters** in **ECX, EDX**
- Remaining parameters on **stack**
- **Caller** cleans stack
- **Faster** for small functions

---

## Exercise 5: Bitwise Operations

**Duration:** 45 minutes  
**Objective:** Master bitwise instructions

### Step 5.1: AND, OR, XOR

**Step-by-Step Instructions:**

1. **Create file** `bitwise_operations.c`:

```c
#include <stdio.h>

int main() {
    int a = 0b10101010;  // 0xAA
    int b = 0b11001100;  // 0xCC
    int and_result, or_result, xor_result;
    
    __asm {
        mov eax, a
        mov ebx, b
        
        // AND operation
        and eax, ebx        // EAX = EAX & EBX
        mov and_result, eax
        
        // OR operation
        mov eax, a
        or eax, ebx         // EAX = EAX | EBX
        mov or_result, eax
        
        // XOR operation
        mov eax, a
        xor eax, ebx        // EAX = EAX ^ EBX
        mov xor_result, eax
    }
    
    printf("a = 0x%x, b = 0x%x\n", a, b);
    printf("AND: 0x%x\n", and_result);
    printf("OR:  0x%x\n", or_result);
    printf("XOR: 0x%x\n", xor_result);
    getchar();
    return 0;
}
```

2. **Compile and test:**
   ```bash
   gcc -m32 -g -o bitwise_operations.exe bitwise_operations.c
   .\bitwise_operations.exe
   ```

3. **Analyze in WinDbg:**
   ```windbg
   windbg bitwise_operations.exe
   bp bitwise_operations!main
   g
   ```

---

### Step 5.2: Shift Operations

**Step-by-Step Instructions:**

1. **Create file** `shift_operations.c`:

```c
#include <stdio.h>

int main() {
    int value = 0x12345678;
    int shl_result, shr_result, sal_result, sar_result;
    
    __asm {
        // SHL - Shift Left (logical)
        mov eax, value
        shl eax, 4          // EAX = EAX << 4
        mov shl_result, eax
        
        // SHR - Shift Right (logical)
        mov eax, value
        shr eax, 4          // EAX = EAX >> 4 (unsigned)
        mov shr_result, eax
        
        // SAL - Shift Arithmetic Left (same as SHL)
        mov eax, value
        sal eax, 2          // EAX = EAX << 2
        mov sal_result, eax
        
        // SAR - Shift Arithmetic Right (signed)
        mov eax, 0x80000000 // Negative number
        sar eax, 4          // EAX = EAX >> 4 (signed, preserves sign)
        mov sar_result, eax
    }
    
    printf("Original: 0x%x\n", value);
    printf("SHL 4:    0x%x\n", shl_result);
    printf("SHR 4:    0x%x\n", shr_result);
    printf("SAL 2:    0x%x\n", sal_result);
    printf("SAR 4:    0x%x\n", sar_result);
    getchar();
    return 0;
}
```

2. **Compile and test:**
   ```bash
   gcc -m32 -g -o shift_operations.exe shift_operations.c
   .\shift_operations.exe
   ```

---

## Exercise 6: Advanced Control Flow

**Duration:** 60 minutes  
**Objective:** Master advanced control flow techniques

### Step 6.1: Switch Statements

**Step-by-Step Instructions:**

1. **Create file** `switch_statement.c`:

```c
#include <stdio.h>

int main() {
    int value = 2;
    int result = 0;
    
    __asm {
        mov eax, value
        
        // Switch statement using jump table
        cmp eax, 0
        je case0
        cmp eax, 1
        je case1
        cmp eax, 2
        je case2
        cmp eax, 3
        je case3
        jmp default_case
        
    case0:
        mov result, 100
        jmp end_switch
        
    case1:
        mov result, 200
        jmp end_switch
        
    case2:
        mov result, 300
        jmp end_switch
        
    case3:
        mov result, 400
        jmp end_switch
        
    default_case:
        mov result, 0
        
    end_switch:
        nop
    }
    
    printf("Value: %d, Result: %d\n", value, result);
    getchar();
    return 0;
}
```

2. **Compile and analyze:**
   ```bash
   gcc -m32 -g -o switch_statement.exe switch_statement.c
   ```

---

## Lab Deliverables

### 1. Complete Code Collection
All intermediate assembly programs with comments

### 2. WinDbg Analysis
Detailed analysis of:
- Stack frame structures
- Calling convention implementations
- String operation execution
- Bitwise operation results

### 3. Comparison Report
Compare:
- __cdecl vs __stdcall vs __fastcall
- Different string operation methods
- Stack manipulation techniques

---

## Next Steps

After completing intermediate assembly lab:
1. Practice with real-world code
2. Analyze compiler-generated assembly
3. Study exploit development techniques
4. Prepare for advanced topics

---

**End of Assembly Intermediate Lab**


