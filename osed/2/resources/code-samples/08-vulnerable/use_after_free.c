/*
 * File: use_after_free.c
 * Purpose: Demonstrates use-after-free vulnerability
 * Lab: OSED 2.7 - Heap Exploitation
 * Compile: gcc -g -O0 -o use_after_free.exe use_after_free.c
 *
 * WARNING: This code is INTENTIONALLY VULNERABLE for educational purposes only.
 *
 * Demonstrates:
 * - Use-after-free vulnerability
 * - Heap memory corruption
 * - Dangling pointer exploitation
 * - Object reuse attacks
 *
 * Debug with:
 * windbg use_after_free.exe
 * bp main
 * g
 * !heap -stat
 * !heap -flt s <size>
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

typedef struct {
    char name[32];
    int id;
    void (*print_info)(void*);
} User;

void print_user_info(void *user_ptr) {
    User *u = (User*)user_ptr;
    printf("  Name: %s\n", u->name);
    printf("  ID: %d\n", u->id);
}

void evil_function(void *ptr) {
    printf("\n");
    printf("========================================\n");
    printf("    EVIL FUNCTION EXECUTED!\n");
    printf("========================================\n");
    printf("\n");
    printf("This should never be called!\n");
    printf("Heap corruption detected!\n");
}

int main() {
    printf("=== Use-After-Free Demonstration ===\n\n");
    printf("Process ID: %d (0x%X)\n", GetCurrentProcessId(), GetCurrentProcessId());
    printf("\n");

    printf("Function addresses:\n");
    printf("  print_user_info: 0x%p\n", print_user_info);
    printf("  evil_function:   0x%p\n", evil_function);
    printf("\n");

    // Allocate User object
    printf("[1] Allocating User object...\n");
    User *user1 = (User*)malloc(sizeof(User));
    printf("    Allocated at: 0x%p\n", user1);

    strcpy(user1->name, "Alice");
    user1->id = 1001;
    user1->print_info = print_user_info;

    printf("[2] User object initialized:\n");
    user1->print_info(user1);

    // Free the object
    printf("\n[3] Freeing User object...\n");
    free(user1);
    printf("    Object freed (but pointer still exists!)\n");

    // VULNERABILITY: user1 is now a dangling pointer
    printf("\n[4] Pointer value after free: 0x%p\n", user1);
    printf("    This is a DANGLING POINTER!\n");

    // Allocate something else of same size
    printf("\n[5] Allocating new data of same size...\n");
    char *attacker_data = (char*)malloc(sizeof(User));
    printf("    Allocated at: 0x%p\n", attacker_data);

    // Fill with controlled data
    memset(attacker_data, 'B', sizeof(User));
    // Could overwrite function pointer here in real exploit

    printf("\n[6] Attempting to use freed object...\n");
    printf("    WARNING: This will likely crash or behave unexpectedly!\n\n");

    // VULNERABILITY: Use-after-free!
    // The memory at user1 now contains attacker_data
    printf("Dangling pointer contents:\n");
    printf("  Name field: ");
    for (int i = 0; i < 32; i++) {
        printf("%02X ", (unsigned char)user1->name[i]);
    }
    printf("\n");
    printf("  ID field: 0x%08X\n", user1->id);
    printf("  Function pointer: 0x%p\n", user1->print_info);

    // Uncomment to trigger crash/corruption:
    // printf("\n[7] Calling function through freed object...\n");
    // user1->print_info(user1);  // CRASH or execute attacker-controlled address!

    printf("\n");
    printf("Debug Instructions:\n");
    printf("1. Attach WinDbg\n");
    printf("2. Set breakpoints at malloc/free calls\n");
    printf("3. Use: !heap -stat\n");
    printf("4. Track heap chunk: !heap -flt s %d\n", (int)sizeof(User));
    printf("5. Examine memory at 0x%p before and after free\n", user1);
    printf("\n");

    printf("Press Enter to continue (cleanup)...\n");
    getchar();

    // Cleanup (in real exploit, might not reach here)
    free(attacker_data);

    printf("[*] Program completed\n");
    return 0;
}
