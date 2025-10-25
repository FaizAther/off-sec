# OSED Section 2.1 Lab: Intermediate Level - Advanced x86 Architecture Analysis

## Lab Overview
This intermediate lab builds upon basic x86 architecture knowledge by introducing more complex scenarios, real-world applications, and advanced analysis techniques. Students will work with multi-threaded applications, complex data structures, and advanced memory layouts.

## Prerequisites
- Completion of beginner-level Section 2.1 labs
- Understanding of basic x86 architecture concepts
- Familiarity with WinDbg basic commands
- Basic understanding of C programming

## Lab Environment Setup

### Required Software:
- Windows 10/11 (64-bit)
- WinDbg Preview
- Visual Studio or MinGW for C compilation
- Process Monitor (ProcMon)
- Process Explorer

### Advanced Sample C Program:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>
#include <process.h>

// Complex data structures
typedef struct {
    int id;
    char name[64];
    float values[10];
    struct Node* next;
    void (*callback)(int);
} Node;

typedef struct {
    Node* head;
    Node* tail;
    int count;
    CRITICAL_SECTION cs;
} LinkedList;

// Global variables
LinkedList global_list;
int global_counter = 0;
char global_buffer[1024];
HANDLE global_mutex;

// Function prototypes
void init_linked_list(LinkedList* list);
void add_node(LinkedList* list, int id, const char* name);
void remove_node(LinkedList* list, int id);
void process_data(Node* node);
void callback_function(int value);
void worker_thread(void* param);
void complex_function(int* array, int size);
void vulnerable_function(char* input, int length);

// Initialize linked list
void init_linked_list(LinkedList* list) {
    list->head = NULL;
    list->tail = NULL;
    list->count = 0;
    InitializeCriticalSection(&list->cs);
}

// Add node to linked list
void add_node(LinkedList* list, int id, const char* name) {
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (new_node == NULL) return;
    
    new_node->id = id;
    strcpy(new_node->name, name);
    new_node->callback = callback_function;
    new_node->next = NULL;
    
    // Initialize values array
    for (int i = 0; i < 10; i++) {
        new_node->values[i] = (float)(id * i);
    }
    
    EnterCriticalSection(&list->cs);
    if (list->head == NULL) {
        list->head = new_node;
        list->tail = new_node;
    } else {
        list->tail->next = new_node;
        list->tail = new_node;
    }
    list->count++;
    LeaveCriticalSection(&list->cs);
}

// Remove node from linked list
void remove_node(LinkedList* list, int id) {
    EnterCriticalSection(&list->cs);
    Node* current = list->head;
    Node* previous = NULL;
    
    while (current != NULL) {
        if (current->id == id) {
            if (previous == NULL) {
                list->head = current->next;
            } else {
                previous->next = current->next;
            }
            if (current == list->tail) {
                list->tail = previous;
            }
            list->count--;
            free(current);
            break;
        }
        previous = current;
        current = current->next;
    }
    LeaveCriticalSection(&list->cs);
}

// Process data in node
void process_data(Node* node) {
    if (node == NULL) return;
    
    printf("Processing node ID: %d, Name: %s\n", node->id, node->name);
    
    // Calculate sum of values
    float sum = 0.0f;
    for (int i = 0; i < 10; i++) {
        sum += node->values[i];
    }
    
    printf("Sum of values: %.2f\n", sum);
    
    // Call callback function
    if (node->callback != NULL) {
        node->callback(node->id);
    }
}

// Callback function
void callback_function(int value) {
    printf("Callback called with value: %d\n", value);
    global_counter += value;
}

// Worker thread function
void worker_thread(void* param) {
    int thread_id = (int)(intptr_t)param;
    printf("Worker thread %d started\n", thread_id);
    
    for (int i = 0; i < 5; i++) {
        Sleep(100);
        add_node(&global_list, thread_id * 100 + i, "Worker Node");
        process_data(global_list.head);
    }
    
    printf("Worker thread %d finished\n", thread_id);
}

// Complex function with array processing
void complex_function(int* array, int size) {
    if (array == NULL || size <= 0) return;
    
    printf("Complex function processing array of size: %d\n", size);
    
    // Process array elements
    for (int i = 0; i < size; i++) {
        array[i] = array[i] * 2 + i;
    }
    
    // Nested loop processing
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            if (i != j) {
                array[i] += array[j] % 10;
            }
        }
    }
}

// Vulnerable function with potential buffer overflow
void vulnerable_function(char* input, int length) {
    char local_buffer[128];
    int local_var = 0x12345678;
    
    printf("Vulnerable function called with length: %d\n", length);
    
    // Potential buffer overflow - no bounds checking
    if (length > 0) {
        memcpy(local_buffer, input, length);
    }
    
    printf("Local buffer: %s\n", local_buffer);
    printf("Local var: 0x%x\n", local_var);
}

int main() {
    HANDLE threads[3];
    int array[20];
    
    printf("Starting advanced x86 architecture analysis program...\n");
    
    // Initialize global resources
    init_linked_list(&global_list);
    global_mutex = CreateMutex(NULL, FALSE, NULL);
    
    // Initialize array
    for (int i = 0; i < 20; i++) {
        array[i] = i * 10;
    }
    
    // Add some initial nodes
    add_node(&global_list, 1, "Main Node 1");
    add_node(&global_list, 2, "Main Node 2");
    add_node(&global_list, 3, "Main Node 3");
    
    // Process initial data
    Node* current = global_list.head;
    while (current != NULL) {
        process_data(current);
        current = current->next;
    }
    
    // Create worker threads
    for (int i = 0; i < 3; i++) {
        threads[i] = (HANDLE)_beginthread(worker_thread, 0, (void*)(intptr_t)(i + 1));
    }
    
    // Wait for threads to complete
    WaitForMultipleObjects(3, threads, TRUE, INFINITE);
    
    // Complex function processing
    complex_function(array, 20);
    
    // Vulnerable function call
    vulnerable_function("This is a test string that might cause issues", 50);
    
    printf("Program completed. Global counter: %d\n", global_counter);
    printf("Final list count: %d\n", global_list.count);
    
    Sleep(20000); // Keep process alive for debugging
    
    return 0;
}
```

## Lab Exercises

### Exercise 1: Multi-Threaded Memory Analysis
**Duration:** 45 minutes
**Difficulty:** Intermediate

#### Objective:
Analyze memory layout and register states in a multi-threaded application.

#### Tasks:

1. **Compile and Launch Program**
   ```bash
   gcc -g -o advanced_sample.exe advanced_sample.c
   ```

2. **Multi-Thread Analysis**
   ```windbg
   # Attach to process
   # Load symbols
   .reload
   
   # Analyze threads
   !threads
   ~
   
   # Switch between threads
   ~0s
   ~1s
   ~2s
   ```

3. **Thread-Specific Memory Analysis**
   ```windbg
   # Analyze each thread's stack
   ~0 k
   ~1 k
   ~2 k
   
   # Analyze thread-local storage
   !tls
   ```

4. **Synchronization Analysis**
   ```windbg
   # Analyze critical sections
   !cs
   
   # Analyze mutexes
   !handle
   ```

#### Expected Challenges:
- Understanding thread context switching
- Analyzing thread-specific memory regions
- Understanding synchronization primitives

### Exercise 2: Complex Data Structure Analysis
**Duration:** 60 minutes
**Difficulty:** Intermediate

#### Objective:
Analyze complex linked list data structures and their memory layout.

#### Tasks:

1. **Structure Analysis**
   ```windbg
   # Analyze Node structure
   dt Node
   dt LinkedList
   
   # Analyze global list
   dt LinkedList global_list
   ```

2. **Linked List Traversal**
   ```windbg
   # Follow linked list pointers
   dps global_list.head
   dps global_list.tail
   
   # Analyze individual nodes
   dt Node global_list.head
   dt Node global_list.head.next
   ```

3. **Function Pointer Analysis**
   ```windbg
   # Analyze callback functions
   dps global_list.head.callback
   
   # Disassemble callback function
   uf callback_function
   ```

4. **Memory Corruption Detection**
   ```windbg
   # Check for heap corruption
   !heap
   !heap -p -a
   ```

#### Expected Challenges:
- Understanding pointer relationships
- Analyzing function pointers
- Detecting memory corruption

### Exercise 3: Advanced Register Analysis
**Duration:** 45 minutes
**Difficulty:** Intermediate

#### Objective:
Analyze register states during complex function calls and thread execution.

#### Tasks:

1. **Function Call Analysis**
   ```windbg
   # Set breakpoints on complex functions
   bp complex_function
   bp process_data
   
   # Analyze register states
   r
   k
   ```

2. **Register Manipulation**
   ```windbg
   # Modify registers during execution
   r eax=0xdeadbeef
   r ebx=0xcafebabe
   
   # Continue execution
   g
   ```

3. **Stack Analysis**
   ```windbg
   # Analyze stack frames
   k
   d esp
   d ebp
   ```

#### Expected Challenges:
- Understanding register usage in complex functions
- Analyzing stack frame relationships
- Manipulating execution flow

## Lab Deliverables

### 1. Multi-Threaded Analysis Report
- Thread analysis results
- Memory layout documentation
- Synchronization analysis
- Performance observations

### 2. Data Structure Analysis
- Structure layout analysis
- Pointer relationship mapping
- Function pointer analysis
- Memory corruption assessment

### 3. Advanced Register Analysis
- Register state documentation
- Function call analysis
- Stack frame analysis
- Execution flow analysis

## Assessment Criteria

### Excellent (90-100%):
- Complete multi-threaded analysis
- Thorough data structure understanding
- Advanced register manipulation
- Clear documentation

### Good (80-89%):
- Most analysis completed
- Basic data structure understanding
- Some register manipulation
- Adequate documentation

### Satisfactory (70-79%):
- Limited analysis
- Minimal data structure understanding
- Few register operations
- Basic documentation

### Needs Improvement (<70%):
- Incomplete analysis
- Poor data structure understanding
- No register manipulation
- Inadequate documentation

## Troubleshooting

### Common Issues:

1. **Thread Analysis Complexity**
   - Use thread-specific commands
   - Analyze one thread at a time
   - Document thread relationships

2. **Data Structure Complexity**
   - Start with simple structures
   - Follow pointers systematically
   - Use visualization techniques

3. **Register State Confusion**
   - Focus on key registers
   - Understand calling conventions
   - Document register changes

## Next Steps
After completing this intermediate lab:
1. Practice with additional complex programs
2. Prepare for advanced-level labs
3. Experiment with different data structures
4. Study multi-threading concepts

## Additional Resources
- Windows Threading Documentation
- Data Structure Analysis Techniques
- Advanced WinDbg Commands
- Multi-Threaded Programming Guides
