/*
 * File: malloc_simple.c
 * Purpose: Basic heap allocation and deallocation
 * Lab: OSED 2.3 - Heap Management
 * Compile: gcc -g -O0 -o malloc_simple.exe malloc_simple.c
 *
 * Demonstrates:
 * - malloc/free operations
 * - Heap memory location
 * - Multiple allocations
 * - Heap fragmentation
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

int main() {
    printf("PID: %d\n\n", GetCurrentProcessId());
    printf("=== Heap Allocation Demo ===\n\n");

    // Multiple heap allocations
    int *heap1 = (int*)malloc(sizeof(int) * 10);
    char *heap2 = (char*)malloc(100);
    int *heap3 = (int*)malloc(sizeof(int));
    char *heap4 = (char*)malloc(1024);

    // Initialize values
    for(int i = 0; i < 10; i++) {
        heap1[i] = i * 100;
    }
    strcpy(heap2, "Hello from heap!");
    *heap3 = 0xDEADBEEF;

    printf("Heap Allocations:\n");
    printf("  heap1 (40 bytes):   0x%p\n", heap1);
    printf("  heap2 (100 bytes):  0x%p\n", heap2);
    printf("  heap3 (4 bytes):    0x%p\n", heap3);
    printf("  heap4 (1024 bytes): 0x%p\n", heap4);

    printf("\nValues:\n");
    printf("  heap1[0] = %d\n", heap1[0]);
    printf("  heap2 = \"%s\"\n", heap2);
    printf("  *heap3 = 0x%X\n", *heap3);

    printf("\n[WinDbg Commands]:\n");
    printf("!heap                        - List all heaps\n");
    printf("!heap -s                     - Heap summary\n");
    printf("!heap -a 0x%p        - Analyze this address\n", heap1);
    printf("!address 0x%p        - Check region\n", heap1);
    printf("db 0x%p-10 L30       - View heap header + data\n", heap1);

    printf("\nFreeing heap2 to show fragmentation...\n");
    free(heap2);
    heap2 = NULL;

    printf("After free(heap2), heap still allocated:\n");
    printf("  heap1: 0x%p (still valid)\n", heap1);
    printf("  heap2: 0x%p (freed)\n", heap2);
    printf("  heap3: 0x%p (still valid)\n", heap3);
    printf("  heap4: 0x%p (still valid)\n", heap4);

    printf("\nProcess alive for 60 seconds...\n");
    Sleep(60000);

    // Cleanup
    free(heap1);
    free(heap3);
    free(heap4);

    return 0;
}
