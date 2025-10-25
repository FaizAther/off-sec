/*
 * File: calling_conventions.c
 * Purpose: Compare __cdecl, __stdcall, __fastcall conventions
 * Lab: OSED 2.1 - Calling Conventions
 * Compile: gcc -g -O0 -o calling_conventions.exe calling_conventions.c
 */

#include <stdio.h>
#include <windows.h>

// cdecl - caller cleans stack
int __cdecl add_cdecl(int a, int b) {
    return a + b;
}

// stdcall - callee cleans stack
int __stdcall add_stdcall(int a, int b) {
    return a + b;
}

// fastcall - first 2 args in registers (ECX, EDX)
int __fastcall add_fastcall(int a, int b) {
    return a + b;
}

int main() {
    int x = 10, y = 20;
    int result;

    printf("PID: %d\n\n", GetCurrentProcessId());
    printf("=== Calling Convention Comparison ===\n\n");

    printf("Set breakpoints:\n");
    printf("bp calling_conventions!add_cdecl\n");
    printf("bp calling_conventions!add_stdcall\n");
    printf("bp calling_conventions!add_fastcall\n\n");

    printf("Calling __cdecl...\n");
    result = add_cdecl(x, y);
    printf("Result: %d\n\n", result);

    printf("Calling __stdcall...\n");
    result = add_stdcall(x, y);
    printf("Result: %d\n\n", result);

    printf("Calling __fastcall...\n");
    result = add_fastcall(x, y);
    printf("Result: %d\n\n", result);

    printf("[WinDbg] At each BP: r (check registers), k (stack), p (step)\n");
    printf("Watch: stack args, register usage, ret instructions\n");

    Sleep(60000);
    return 0;
}
