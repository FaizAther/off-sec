/*
 * File: stack_demo.c
 * Purpose: Demonstrate stack frame structure and growth
 * Lab: OSED 2.1, 2.3 - Stack analysis
 * Compile: gcc -g -O0 -fno-stack-protector -o stack_demo.exe stack_demo.c
 */

#include <stdio.h>
#include <windows.h>

void level3(int a, int b, int c) {
    int local3 = 300;
    printf("  Level 3: locals at 0x%p, ESP at ~0x%p\n", &local3, &local3);
    printf("  Args: %d, %d, %d\n", a, b, c);
    printf("  [WinDbg]: k (stack trace), dv (locals), dps esp (stack dump)\n");
    Sleep(5000);
}

void level2(int x, int y) {
    int local2 = 200;
    printf(" Level 2: locals at 0x%p\n", &local2);
    level3(x, y, local2);
}

void level1(int n) {
    int local1 = 100;
    printf("Level 1: locals at 0x%p\n", &local1);
    level2(n, local1);
}

int main() {
    int main_local = 42;

    printf("PID: %d\n\n", GetCurrentProcessId());
    printf("=== Stack Frame Demo ===\n");
    printf("Main: locals at 0x%p\n", &main_local);

    printf("\nWatching stack grow downward...\n");
    level1(main_local);

    printf("\nStack unwinding complete.\n");
    Sleep(60000);
    return 0;
}
