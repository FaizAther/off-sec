/*
 * File: format_string.c
 * Purpose: Demonstrates format string vulnerability
 * Lab: OSED 2.7 - Advanced Exploitation
 * Compile: gcc -g -O0 -o format_string.exe format_string.c
 *
 * WARNING: This code is INTENTIONALLY VULNERABLE for educational purposes only.
 *
 * Demonstrates:
 * - Format string vulnerability
 * - Stack memory disclosure
 * - Arbitrary memory read
 * - %n write primitive (commented for safety)
 *
 * Debug with:
 * windbg format_string.exe
 * bp vulnerable_printf
 * g
 * dps esp
 */

#include <stdio.h>
#include <string.h>
#include <windows.h>

int secret_value = 0xDEADBEEF;
char secret_string[] = "FLAG{format_string_pwned}";

void vulnerable_printf(char *user_input) {
    printf("\n=== Vulnerable Function ===\n");
    printf("Stack address: 0x%p\n", &user_input);

    // VULNERABILITY: User input used directly as format string!
    printf(user_input);

    printf("\n=== Function Returning ===\n");
}

void safe_printf(char *user_input) {
    printf("\n=== Safe Function ===\n");
    // Correct: user input is data, not format string
    printf("%s", user_input);
    printf("\n");
}

int main(int argc, char *argv[]) {
    printf("=== Format String Vulnerability Demonstration ===\n\n");
    printf("Process ID: %d (0x%X)\n", GetCurrentProcessId(), GetCurrentProcessId());
    printf("\n");

    printf("Memory Targets:\n");
    printf("  secret_value:  0x%p = 0x%08X\n", &secret_value, secret_value);
    printf("  secret_string: 0x%p = \"%s\"\n", &secret_string, secret_string);
    printf("\n");

    if (argc < 2) {
        printf("Usage: %s <format_string>\n\n", argv[0]);
        printf("Examples:\n");
        printf("  Safe:      %s \"Hello World\"\n", argv[0]);
        printf("  Leak:      %s \"%%p %%p %%p %%p\"\n", argv[0]);
        printf("  Read str:  %s \"%%s\"\n", argv[0]);
        printf("  Read hex:  %s \"%%08x %%08x %%08x %%08x\"\n", argv[0]);
        printf("\n");
        printf("Debug Instructions:\n");
        printf("1. Attach WinDbg\n");
        printf("2. bp vulnerable_printf\n");
        printf("3. g\n");
        printf("4. Examine stack: dps esp L20\n");
        printf("5. Step through and observe output\n");
        printf("\n");

        char input[256];
        printf("Enter format string (or Ctrl+C): ");
        fgets(input, sizeof(input), stdin);
        input[strcspn(input, "\n")] = 0;

        vulnerable_printf(input);
        safe_printf(input);
    } else {
        vulnerable_printf(argv[1]);
        safe_printf(argv[1]);
    }

    printf("\n[*] Program completed\n");
    return 0;
}
