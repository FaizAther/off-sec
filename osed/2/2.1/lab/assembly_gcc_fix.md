# Assembly Lab - GCC/MinGW Compilation Fix

## Problem

The assembly lab examples use Microsoft Visual C++ inline assembly syntax (`__asm { ... }`), which doesn't work with GCC/MinGW. GCC uses a different inline assembly syntax.

## Solution

GCC uses **AT&T syntax** for inline assembly, which is different from Intel syntax. Here are the corrected examples:

---

## Fixed Code Examples

### Example 1: Basic MOV Instruction (GCC Syntax)

**Original (MSVC - doesn't work with GCC):**
```c
__asm {
    mov eax, 42
    mov result, eax
}
```

**Fixed (GCC Syntax):**
```c
__asm__ (
    "movl $42, %%eax\n\t"
    "movl %%eax, %0"
    : "=m" (result)  // Output: result variable
    :                // No inputs
    : "%eax"         // Clobbered register
);
```

**Or simpler version using extended asm:**
```c
__asm__ (
    "movl $42, %0"
    : "=r" (result)  // Output: result in register
    :
    :
);
```

---

## Complete Fixed Examples

### Fixed Example 1: Basic Assembly Program

**File:** `assembly_basics.c`

```c
#include <stdio.h>

int main() {
    int result;
    
    // GCC inline assembly: Basic MOV instruction
    __asm__ (
        "movl $42, %%eax\n\t"      // Move immediate value 42 into EAX
        "movl %%eax, %0"           // Move EAX value into result variable
        : "=m" (result)            // Output: result variable in memory
        :                          // No inputs
        : "%eax"                   // Clobbered register
    );
    
    printf("Result: %d\n", result);
    getchar();  // Pause to keep program running
    return 0;
}
```

**Compile:**
```bash
gcc -m32 -g -o assembly_basics.exe assembly_basics.c
```

---

### Fixed Example 2: Register Operations

**File:** `register_ops.c`

```c
#include <stdio.h>

int main() {
    int result1, result2, result3;
    
    __asm__ (
        // Register-to-register operations
        "movl $100, %%eax\n\t"     // EAX = 100
        "movl $200, %%ebx\n\t"     // EBX = 200
        "movl %%eax, %%ecx\n\t"    // ECX = EAX (copy EAX to ECX)
        "movl %%ebx, %%edx\n\t"    // EDX = EBX (copy EBX to EDX)
        
        // Store results
        "movl %%eax, %0\n\t"       // result1 = EAX
        "movl %%ecx, %1\n\t"       // result2 = ECX
        "movl %%edx, %2"           // result3 = EDX
        : "=m" (result1), "=m" (result2), "=m" (result3)  // Outputs
        :                          // No inputs
        : "%eax", "%ebx", "%ecx", "%edx"  // Clobbered registers
    );
    
    printf("result1 = %d, result2 = %d, result3 = %d\n", 
           result1, result2, result3);
    getchar();
    return 0;
}
```

---

### Fixed Example 3: Arithmetic Operations

**File:** `arithmetic.c`

```c
#include <stdio.h>

int main() {
    int a = 100, b = 30;
    int add, sub, mul, div_result, mod;
    
    __asm__ (
        // Addition
        "movl %2, %%eax\n\t"       // Load a into EAX
        "addl %3, %%eax\n\t"       // EAX = EAX + b
        "movl %%eax, %0\n\t"       // Store in add
        
        // Subtraction
        "movl %2, %%eax\n\t"       // Load a into EAX
        "subl %3, %%eax\n\t"       // EAX = EAX - b
        "movl %%eax, %1"           // Store in sub
        
        : "=m" (add), "=m" (sub)   // Outputs
        : "m" (a), "m" (b)         // Inputs
        : "%eax"                   // Clobbered register
    );
    
    printf("a = %d, b = %d\n", a, b);
    printf("Add: %d, Sub: %d\n", add, sub);
    getchar();
    return 0;
}
```

---

## GCC Inline Assembly Syntax Guide

### Basic Syntax

```c
__asm__ (
    "assembly code"
    : outputs
    : inputs
    : clobbered registers
);
```

### Syntax Differences

| Feature | MSVC (Intel) | GCC (AT&T) |
|---------|-------------|------------|
| Syntax | `__asm { ... }` | `__asm__ ( "..." )` |
| Immediate | `mov eax, 42` | `movl $42, %eax` |
| Register | `eax` | `%eax` |
| Memory | `[eax]` | `(%eax)` |
| Size | `mov eax, [ebx]` | `movl (%ebx), %eax` |
| Comments | `// comment` | `/* comment */` |

### AT&T Syntax Rules

1. **Source and destination are reversed:**
   - Intel: `mov eax, ebx` (EAX = EBX)
   - AT&T: `movl %ebx, %eax` (EAX = EBX)

2. **Immediate values use `$` prefix:**
   - Intel: `mov eax, 42`
   - AT&T: `movl $42, %eax`

3. **Registers use `%` prefix:**
   - Intel: `eax`
   - AT&T: `%eax`

4. **Memory addressing uses parentheses:**
   - Intel: `mov eax, [ebx]`
   - AT&T: `movl (%ebx), %eax`

5. **Size suffixes:**
   - `b` = byte (8 bits)
   - `w` = word (16 bits)
   - `l` = long (32 bits)
   - `q` = quad (64 bits)

### Constraint Modifiers

- `=m` - Output in memory
- `=r` - Output in register
- `m` - Input from memory
- `r` - Input from register
- `+` - Read-write operand

### Example with Constraints

```c
int a = 10, b = 20, result;

__asm__ (
    "movl %1, %%eax\n\t"    // Load a (input 0)
    "addl %2, %%eax\n\t"    // Add b (input 1)
    "movl %%eax, %0"        // Store in result (output 0)
    : "=m" (result)         // Output 0: result in memory
    : "m" (a), "m" (b)      // Input 0: a, Input 1: b
    : "%eax"                // Clobbered register
);
```

---

## Alternative: Use Separate Assembly Files

If GCC inline assembly is too complex, you can use separate `.s` assembly files:

### Step 1: Create `assembly_basics.s`

```assembly
    .section .text
    .globl _main
_main:
    pushl %ebp
    movl %esp, %ebp
    subl $4, %esp
    
    movl $42, %eax
    movl %eax, -4(%ebp)
    
    movl -4(%ebp), %eax
    leave
    ret
```

### Step 2: Compile

```bash
gcc -m32 -g -o assembly_basics.exe assembly_basics.s
```

---

## Quick Reference: Common Instructions

### Data Movement

```c
// Move immediate to register
__asm__ ("movl $42, %%eax" : : : "%eax");

// Move register to variable
__asm__ ("movl %%eax, %0" : "=m" (result) : : "%eax");

// Move variable to register
__asm__ ("movl %0, %%eax" : : "m" (value) : "%eax");
```

### Arithmetic

```c
// Add
__asm__ ("addl %1, %0" : "+r" (result) : "r" (value) :);

// Subtract
__asm__ ("subl %1, %0" : "+r" (result) : "r" (value) :);

// Multiply
__asm__ ("imull %1, %0" : "+r" (result) : "r" (value) :);
```

### Control Flow

```c
// Compare
__asm__ (
    "cmpl %1, %0\n\t"
    "jne label\n\t"
    "label:"
    : "=r" (result)
    : "r" (value)
    :
);
```

---

## Updated Lab Examples

I'll update all the assembly lab examples to include both MSVC and GCC syntax. For now, use the GCC syntax examples above.

---

## Troubleshooting

### Error: "expected '(' before '{' token"
- **Cause:** Using MSVC syntax with GCC
- **Fix:** Use `__asm__ ( "..." )` instead of `__asm { ... }`

### Error: "unknown type name 'mov'"
- **Cause:** Assembly code not in string
- **Fix:** Put assembly code in quotes: `"movl $42, %%eax"`

### Error: "operand type mismatch"
- **Cause:** Wrong size suffix
- **Fix:** Use correct suffix: `movl` for 32-bit, `movw` for 16-bit, `movb` for 8-bit

---

## Recommendation

For learning purposes, I recommend:

1. **Use GCC syntax** if you're using MinGW
2. **Or use Visual Studio** if you prefer MSVC syntax
3. **Or use separate `.s` files** for pure assembly

The lab examples will be updated to support both compilers.


