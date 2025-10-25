/*
 * File: buffer_overflow.c
 * Purpose: Demonstrates classic stack buffer overflow vulnerability
 * Lab: OSED 2.6, 2.7 - Vulnerability Analysis
 * Compile: gcc -g -O0 -fno-stack-protector -o buffer_overflow.exe buffer_overflow.c
 *
 * WARNING: This code is INTENTIONALLY VULNERABLE for educational purposes only.
 * Never use patterns like this in production code.
 *
 * Demonstrates:
 * - Stack buffer overflow
 * - Unsafe strcpy usage
 * - Return address overwrite potential
 * - Stack frame corruption
 *
 * Debug with:
 * windbg buffer_overflow.exe
 * bp vulnerable_function
 * g
 * k
 * dps esp
 */

#include <stdio.h>
#include <string.h>
#include <windows.h>

// Vulnerable function - no bounds checking
void vulnerable_function(char *user_input) {
    char buffer[64];  // Small fixed-size buffer

    printf("[*] Buffer address: 0x%p\n", buffer);
    printf("[*] Function address: 0x%p\n", vulnerable_function);
    printf("[*] Input length: %d bytes\n", strlen(user_input));

    // VULNERABILITY: No bounds checking!
    // If user_input > 64 bytes, we overflow the buffer
    strcpy(buffer, user_input);

    printf("[*] Buffer contents: %s\n", buffer);
    printf("[*] Function returning...\n");
}

void secret_function() {
    printf("\n");
    printf("========================================\n");
    printf("    SECRET FUNCTION EXECUTED!\n");
    printf("========================================\n");
    printf("\n");
    printf("This function should never be called directly.\n");
    printf("If you see this, you've successfully redirected execution!\n");
    printf("\n");
    printf("Secret function address: 0x%p\n", secret_function);
}

int main(int argc, char *argv[]) {
    printf("=== Stack Buffer Overflow Demonstration ===\n\n");
    printf("Process ID: %d (0x%X)\n", GetCurrentProcessId(), GetCurrentProcessId());
    printf("Main function: 0x%p\n", main);
    printf("Secret function: 0x%p\n", secret_function);
    printf("\n");

    if (argc < 2) {
        printf("Usage: %s <input_string>\n\n", argv[0]);
        printf("Examples:\n");
        printf("  Safe:   %s \"Hello World\"\n", argv[0]);
        printf("  Unsafe: %s \"%s\"\n", argv[0], "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
        printf("\n");
        printf("Debug Instructions:\n");
        printf("1. Attach WinDbg to this process\n");
        printf("2. Set breakpoint: bp vulnerable_function\n");
        printf("3. Examine stack: k; dps esp\n");
        printf("4. Step through and observe overflow\n");
        printf("\n");

        // Interactive mode for debugging
        char input[256];
        printf("Enter input (or press Ctrl+C): ");
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = 0;  // Remove newline

        vulnerable_function(input);
    } else {
        vulnerable_function(argv[1]);
    }

    printf("\n[*] Program completed successfully\n");
    return 0;
}
