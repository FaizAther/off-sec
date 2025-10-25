/*
 * File: calculations.c
 * Purpose: Basic arithmetic to observe register usage
 * Lab: OSED 2.1 - Introduction to x86 Architecture
 * Compile: gcc -g -O0 -o calculations.exe calculations.c
 */

#include <stdio.h>
#include <windows.h>

int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int main() {
    int x = 10;
    int y = 20;
    int sum, product;

    printf("PID: %d\n", GetCurrentProcessId());
    printf("\n=== Arithmetic Operations ===\n");

    // Set breakpoint here to observe register values
    sum = add(x, y);
    product = multiply(x, y);

    printf("x = %d, y = %d\n", x, y);
    printf("Sum = %d\n", sum);
    printf("Product = %d\n", product);

    printf("\n[WinDbg]: bp calculations!add\n");
    printf("[WinDbg]: g; r; k; p\n");

    Sleep(60000);
    return 0;
}
