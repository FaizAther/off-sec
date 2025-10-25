/*
 * File: struct_basic.c
 * Purpose: Demonstrate structure layout in memory
 * Lab: OSED 2.3 - Memory Structures
 * Compile: gcc -g -O0 -o struct_basic.exe struct_basic.c
 *
 * Demonstrates:
 * - Structure member layout
 * - Structure alignment/padding
 * - Accessing structure members in memory
 */

#include <stdio.h>
#include <string.h>
#include <windows.h>

// Simple structure
struct Person {
    char name[32];
    int age;
    float height;
    int id;
};

// Structure with different sized members
struct Mixed {
    char a;      // 1 byte
    int b;       // 4 bytes (padding after 'a')
    short c;     // 2 bytes
    char d;      // 1 byte (padding after to align struct)
};

int main() {
    struct Person person1;
    struct Mixed mixed;

    printf("PID: %d\n\n", GetCurrentProcessId());
    printf("=== Structure Memory Layout ===\n\n");

    // Initialize person
    strcpy(person1.name, "John Doe");
    person1.age = 30;
    person1.height = 5.9f;
    person1.id = 12345;

    // Initialize mixed
    mixed.a = 'A';
    mixed.b = 0x12345678;
    mixed.c = 0x9ABC;
    mixed.d = 'Z';

    printf("Person Structure:\n");
    printf("  Entire struct:   0x%p (size: %zu bytes)\n", &person1, sizeof(person1));
    printf("  name:            0x%p (offset: %zu)\n", &person1.name, (char*)&person1.name - (char*)&person1);
    printf("  age:             0x%p (offset: %zu)\n", &person1.age, (char*)&person1.age - (char*)&person1);
    printf("  height:          0x%p (offset: %zu)\n", &person1.height, (char*)&person1.height - (char*)&person1);
    printf("  id:              0x%p (offset: %zu)\n", &person1.id, (char*)&person1.id - (char*)&person1);

    printf("\nMixed Structure (showing padding):\n");
    printf("  Entire struct:   0x%p (size: %zu bytes)\n", &mixed, sizeof(mixed));
    printf("  a (char):        0x%p (offset: %zu)\n", &mixed.a, (char*)&mixed.a - (char*)&mixed);
    printf("  b (int):         0x%p (offset: %zu) [3 bytes padding before this]\n", &mixed.b, (char*)&mixed.b - (char*)&mixed);
    printf("  c (short):       0x%p (offset: %zu)\n", &mixed.c, (char*)&mixed.c - (char*)&mixed);
    printf("  d (char):        0x%p (offset: %zu)\n", &mixed.d, (char*)&mixed.d - (char*)&mixed);

    printf("\n[WinDbg Commands]:\n");
    printf("dt struct Person 0x%p       - Display structure\n", &person1);
    printf("dt struct Mixed 0x%p        - Show padding\n", &mixed);
    printf("db 0x%p L%zu         - View raw bytes\n", &mixed, sizeof(mixed));

    Sleep(60000);
    return 0;
}
