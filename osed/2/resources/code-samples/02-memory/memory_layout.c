/*
 * File: memory_layout.c
 * Purpose: Demonstrate all memory sections in one program
 * Lab: OSED 2.1 - Introduction to x86 Architecture
 * Compile: gcc -g -O0 -o memory_layout.exe memory_layout.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

// Data segment - initialized globals
int initialized_global = 42;
char initialized_string[] = "Hello, Data Segment!";

// BSS segment - uninitialized globals
int uninitialized_global;
char uninitialized_buffer[1024];

// Text segment (code) - this function
void analyze_memory() {
    // Stack - local variables
    int local_variable = 100;
    char local_buffer[64];

    // Heap - dynamic allocation
    int *heap_variable = (int*)malloc(sizeof(int));
    *heap_variable = 200;

    printf("\n=== Memory Layout Analysis ===\n\n");

    printf("TEXT SEGMENT (Code):\n");
    printf("  Function address: 0x%p\n", analyze_memory);
    printf("  main address:     0x%p\n", main);

    printf("\nDATA SEGMENT (Initialized Globals):\n");
    printf("  initialized_global:  0x%p = %d\n", &initialized_global, initialized_global);
    printf("  initialized_string:  0x%p = \"%s\"\n", &initialized_string, initialized_string);

    printf("\nBSS SEGMENT (Uninitialized Globals):\n");
    printf("  uninitialized_global: 0x%p = %d\n", &uninitialized_global, uninitialized_global);
    printf("  uninitialized_buffer: 0x%p\n", &uninitialized_buffer);

    printf("\nSTACK:\n");
    printf("  local_variable: 0x%p = %d\n", &local_variable, local_variable);
    printf("  local_buffer:   0x%p\n", &local_buffer);

    printf("\nHEAP:\n");
    printf("  heap_variable:  0x%p = %d\n", heap_variable, *heap_variable);

    printf("\n[WinDbg Commands]:\n");
    printf("!address                 - View all memory regions\n");
    printf("!address 0x%p - Check code section\n", main);
    printf("!address 0x%p - Check data section\n", &initialized_global);
    printf("!address 0x%p - Check stack\n", &local_variable);
    printf("!address 0x%p - Check heap\n", heap_variable);

    free(heap_variable);
}

int main() {
    printf("PID: %d (0x%X)\n", GetCurrentProcessId(), GetCurrentProcessId());
    analyze_memory();

    printf("\nKeeping process alive for debugging...\n");
    Sleep(60000);
    return 0;
}
