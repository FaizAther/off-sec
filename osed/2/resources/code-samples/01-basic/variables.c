/*
 * File: variables.c
 * Purpose: Demonstrate different variable storage locations
 * Lab: OSED 2.1 - Introduction to x86 Architecture
 * Compile: gcc -g -o variables.exe variables.c
 *
 * Demonstrates:
 * - Global variables (data segment)
 * - Local variables (stack)
 * - Static variables
 * - Register usage
 */

#include <stdio.h>
#include <windows.h>

// Global variables - stored in data segment
int global_initialized = 42;
int global_uninitialized;

// Static global
static int static_global = 100;

void print_variable_info() {
    // Local variables - stored on stack
    int local_var = 10;
    static int static_local = 20;

    printf("\n=== Variable Storage Analysis ===\n");
    printf("Global (initialized): 0x%p = %d\n", &global_initialized, global_initialized);
    printf("Global (uninitialized): 0x%p = %d\n", &global_uninitialized, global_uninitialized);
    printf("Static Global: 0x%p = %d\n", &static_global, static_global);
    printf("Local Variable: 0x%p = %d\n", &local_var, local_var);
    printf("Static Local: 0x%p = %d\n", &static_local, static_local);

    printf("\n[WinDbg Commands to Try:]\n");
    printf("x variables!global_*     - List global variables\n");
    printf("dv                       - Display local variables\n");
    printf("!address 0x%p    - Check memory region\n", &global_initialized);
    printf("!address 0x%p    - Check memory region\n", &local_var);
}

int main() {
    printf("PID: %d\n", GetCurrentProcessId());

    print_variable_info();

    printf("\nProcess alive for 60 seconds...\n");
    Sleep(60000);

    return 0;
}
