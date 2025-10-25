/*
 * File: thread_basic.c
 * Purpose: Basic thread creation and management
 * Lab: OSED 2.2 - Multi-Process/Thread Debugging
 * Compile: gcc -g -O0 -o thread_basic.exe thread_basic.c
 *
 * Demonstrates:
 * - CreateThread API
 * - Multiple threads execution
 * - Thread synchronization basics
 * - Debugging multiple threads
 */

#include <stdio.h>
#include <windows.h>

volatile int shared_counter = 0;

DWORD WINAPI ThreadFunction1(LPVOID lpParam) {
    int thread_id = *(int*)lpParam;

    printf("Thread %d started (TID: %d)\n", thread_id, GetCurrentThreadId());

    for(int i = 0; i < 5; i++) {
        shared_counter++;
        printf("  Thread %d: Counter = %d\n", thread_id, shared_counter);
        Sleep(1000);
    }

    printf("Thread %d exiting\n", thread_id);
    return 0;
}

DWORD WINAPI ThreadFunction2(LPVOID lpParam) {
    int thread_id = *(int*)lpParam;

    printf("Thread %d started (TID: %d)\n", thread_id, GetCurrentThreadId());

    for(int i = 0; i < 3; i++) {
        printf("  Thread %d: Working... (shared_counter = %d)\n", thread_id, shared_counter);
        Sleep(1500);
    }

    printf("Thread %d exiting\n", thread_id);
    return 0;
}

int main() {
    HANDLE hThread1, hThread2, hThread3;
    DWORD dwThread1, dwThread2, dwThread3;
    int id1 = 1, id2 = 2, id3 = 3;

    printf("PID: %d\n", GetCurrentProcessId());
    printf("Main Thread TID: %d\n\n", GetCurrentThreadId());
    printf("=== Multi-Threading Demo ===\n\n");

    // Create threads
    printf("Creating threads...\n");
    hThread1 = CreateThread(NULL, 0, ThreadFunction1, &id1, 0, &dwThread1);
    hThread2 = CreateThread(NULL, 0, ThreadFunction2, &id2, 0, &dwThread2);
    hThread3 = CreateThread(NULL, 0, ThreadFunction1, &id3, 0, &dwThread3);

    if(hThread1 == NULL || hThread2 == NULL || hThread3 == NULL) {
        printf("Thread creation failed!\n");
        return 1;
    }

    printf("\nThreads created:\n");
    printf("  Thread 1: TID %d\n", dwThread1);
    printf("  Thread 2: TID %d\n", dwThread2);
    printf("  Thread 3: TID %d\n", dwThread3);

    printf("\n[WinDbg Commands]:\n");
    printf("~                - List all threads\n");
    printf("~*k              - Stack trace for all threads\n");
    printf("~0s              - Switch to thread 0\n");
    printf("~~[%d]s       - Switch to specific TID\n", dwThread1);
    printf("!threads         - Detailed thread info\n");

    printf("\nMain thread waiting for workers...\n");

    // Wait for threads to complete
    WaitForSingleObject(hThread1, INFINITE);
    WaitForSingleObject(hThread2, INFINITE);
    WaitForSingleObject(hThread3, INFINITE);

    printf("\nAll threads completed. Final counter: %d\n", shared_counter);

    // Cleanup
    CloseHandle(hThread1);
    CloseHandle(hThread2);
    CloseHandle(hThread3);

    printf("\nKeeping process alive for debugging...\n");
    Sleep(30000);

    return 0;
}
