/*
 * File: seh_basic.c
 * Purpose: Basic Structured Exception Handling (SEH)
 * Lab: OSED 2.8 - Exception Handling
 * Compile: gcc -g -O0 -o seh_basic.exe seh_basic.c
 *
 * Demonstrates:
 * - __try/__except blocks
 * - Exception filters
 * - Exception codes
 * - Debugging exceptions
 */

#include <stdio.h>
#include <windows.h>

void cause_access_violation() {
    printf("Attempting to write to NULL pointer...\n");
    int *null_ptr = NULL;
    *null_ptr = 42;  // This will cause access violation
    printf("This line never executes!\n");
}

void cause_divide_by_zero() {
    printf("Attempting division by zero...\n");
    int x = 10;
    int y = 0;
    int result = x / y;  // Division by zero
    printf("Result: %d (never shown)\n", result);
}

void handle_exceptions() {
    printf("\n=== Exception Test 1: Access Violation ===\n");

    __try {
        cause_access_violation();
    }
    __except(EXCEPTION_EXECUTE_HANDLER) {
        printf("Caught exception! Code: 0x%X (Access Violation)\n",
               GetExceptionCode());
    }

    printf("\n=== Exception Test 2: Division by Zero ===\n");

    __try {
        cause_divide_by_zero();
    }
    __except(EXCEPTION_EXECUTE_HANDLER) {
        printf("Caught exception! Code: 0x%X (Integer Divide by Zero)\n",
               GetExceptionCode());
    }

    printf("\n=== Exception Test 3: Custom Filter ===\n");

    __try {
        printf("Raising custom exception...\n");
        RaiseException(0xE0000001, 0, 0, NULL);
    }
    __except(GetExceptionCode() == 0xE0000001 ?
             EXCEPTION_EXECUTE_HANDLER : EXCEPTION_CONTINUE_SEARCH) {
        printf("Caught custom exception: 0x%X\n", GetExceptionCode());
    }
}

int main() {
    printf("PID: %d\n", GetCurrentProcessId());
    printf("\n=== SEH (Structured Exception Handling) Demo ===\n");

    printf("\n[WinDbg Commands]:\n");
    printf("sxe av              - Break on access violation\n");
    printf("sxd av              - Don't break on AV (default)\n");
    printf("sxe -c \"g\" av       - Continue on AV\n");
    printf(".exr -1             - Display last exception\n");
    printf(".ecxr               - Set context to exception\n");
    printf("!analyze -v         - Analyze exception\n\n");

    handle_exceptions();

    printf("\nAll exceptions handled successfully!\n");
    printf("Process alive for debugging...\n");
    Sleep(60000);

    return 0;
}
