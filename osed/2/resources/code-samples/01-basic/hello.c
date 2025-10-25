/*
 * File: hello.c
 * Purpose: Basic executable structure for initial WinDbg familiarization
 * Lab: OSED 2.1 - Introduction to x86 Architecture
 * Compile: gcc -g -o hello.exe hello.c
 *
 * Demonstrates:
 * - Basic program structure
 * - Process creation
 * - Simple output
 * - Keeping process alive for debugging
 *
 * Debug with:
 * windbg hello.exe
 * bp main
 * g
 * k
 */

#include <stdio.h>
#include <windows.h>

int main() {
    DWORD pid = GetCurrentProcessId();

    printf("==============================================\n");
    printf("  Basic WinDbg Demonstration Program\n");
    printf("==============================================\n\n");

    printf("[+] Process ID: %d (0x%X)\n", pid, pid);
    printf("[+] Program started successfully\n\n");

    printf("Debug Instructions:\n");
    printf("1. Attach WinDbg to PID %d\n", pid);
    printf("2. Set breakpoint: bp hello!main\n");
    printf("3. Examine: k (stack), r (registers)\n\n");

    printf("[*] Process will remain active for 60 seconds...\n");
    printf("[*] Press Ctrl+C to exit early\n\n");

    Sleep(60000);  // Keep process alive for debugging

    printf("[+] Program terminating normally\n");
    return 0;
}
