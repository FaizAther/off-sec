/*
 * Assembly Basics - GCC Compatible Version
 * This file uses GCC inline assembly syntax (AT&T)
 */

#include <stdio.h>

int main() {
    int result;
    
    // GCC inline assembly: Basic MOV instruction
    // AT&T syntax: movl $42, %eax (move immediate 42 to EAX)
    __asm__ (
        "movl $42, %%eax\n\t"      // Move immediate value 42 into EAX
        "movl %%eax, %0"           // Move EAX value into result variable
        : "=m" (result)            // Output: result variable in memory
        :                          // No inputs
        : "%eax"                  // Clobbered register (EAX is modified)
    );
    
    printf("Result: %d\n", result);
    getchar();  // Pause to keep program running
    return 0;
}

/*
 * Compilation:
 * gcc -m32 -g -o assembly_basics.exe assembly_basics_gcc.c
 * 
 * Explanation:
 * - movl: move long (32-bit)
 * - $42: immediate value 42
 * - %%eax: register EAX (double % because it's in a string)
 * - %0: first output operand (result)
 * - "=m": output constraint (memory)
 * - "%eax": clobbered register list
 */


