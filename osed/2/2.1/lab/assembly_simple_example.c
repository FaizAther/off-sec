/*
 * Simple Assembly Example - GCC Compatible
 * This is the simplest way to use assembly with GCC
 */

#include <stdio.h>

int main() {
    int result;
    
    // Simplest form: Direct assignment using register constraint
    __asm__ (
        "movl $42, %0"     // Move 42 directly to output register
        : "=r" (result)    // Output: result in any register
        :                 // No inputs
        :                 // No clobbered registers
    );
    
    printf("Result: %d\n", result);
    
    // Example 2: Addition
    int a = 10, b = 20, sum;
    
    __asm__ (
        "movl %1, %%eax\n\t"   // Load a into EAX
        "addl %2, %%eax\n\t"   // Add b to EAX
        "movl %%eax, %0"       // Store result
        : "=r" (sum)           // Output: sum in register
        : "m" (a), "m" (b)     // Inputs: a and b from memory
        : "%eax"               // EAX is clobbered
    );
    
    printf("Sum: %d\n", sum);
    
    getchar();
    return 0;
}

/*
 * Compile:
 * gcc -m32 -g -o assembly_simple.exe assembly_simple_example.c
 * 
 * Key Points:
 * 1. Use __asm__ instead of __asm
 * 2. Assembly code goes in quotes
 * 3. Use %% for registers (double %)
 * 4. Use %0, %1, %2 for operands
 * 5. Constraints: "=r" (output register), "m" (memory)
 */


