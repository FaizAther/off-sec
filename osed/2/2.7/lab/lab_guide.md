# OSED Section 2.7 Lab: Advanced Reverse Engineering Challenges

**Difficulty Level:** Expert
**Estimated Time:** 6 hours (3h theory + 3h lab)
**Skills:** Advanced debugging, Code analysis, Pattern recognition, Exploit identification

## Lab Overview
This lab presents advanced reverse engineering challenges including obfuscated code analysis, packed binaries, and complex control flow manipulation. Students will apply all previous WinDbg skills to analyze sophisticated programs.

## Prerequisites
- Completion of Sections 2.1-2.6
- Advanced WinDbg proficiency
- Understanding of assembly language
- Familiarity with common obfuscation techniques
- Knowledge of PE file structure

## Lab Environment Setup

### Required Software:
- Windows 10/11 (64-bit)
- WinDbg Preview with symbol support
- Visual Studio 2019+ or MinGW
- PE analysis tools (PE-bear, CFF Explorer)
- Python 3.x for scripting
- IDA Free or Ghidra (optional, for comparison)

### Sample Programs Provided:
Multiple challenge binaries of increasing complexity

## Lab Exercises

### Exercise 1: Opaque Predicate Analysis
**Duration:** 60 minutes

#### Objective:
Identify and bypass opaque predicates used to confuse static analysis tools.

#### Background:
Opaque predicates are conditional statements that always evaluate to the same result but are designed to appear dynamic to confuse reverse engineers.

#### Challenge Program:
```c
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Opaque predicate: x^2 >= 0 always true for real numbers
int opaque_true(int x) {
    return (x * x) >= 0;
}

// Opaque predicate: x^2 + x + 1 is odd always true
int opaque_true2(int x) {
    return ((x * x) + x + 1) & 1;
}

void secret_function() {
    printf("You found the secret!\n");
    printf("Flag: OSED{0p4qu3_pr3d1c4t35_d3f34t3d}\n");
}

void decoy_function1() {
    printf("This is a decoy path.\n");
}

void decoy_function2() {
    printf("Another decoy path.\n");
}

int main() {
    int x = 42;
    int y = 13;

    // Opaque predicate - always true
    if (opaque_true(x)) {
        if (opaque_true2(y)) {
            // Real path hidden behind opaque predicates
            secret_function();
        } else {
            decoy_function1();
        }
    } else {
        decoy_function2();
    }

    // Additional obfuscation
    for (int i = 0; i < 100; i++) {
        if (opaque_true(i)) {
            // Junk code
            int temp = i * i;
        }
    }

    return 0;
}
```

#### Steps:

1. **Compile with Optimizations Disabled**
   ```bash
   gcc -O0 -g -o opaque.exe opaque.c
   ```

2. **Load in WinDbg and Analyze Control Flow**
   ```windbg
   bp main
   g
   uf main
   ```

3. **Identify Opaque Predicates**
   - Look for mathematical operations that always yield the same result
   - Trace variable values through calculations
   - Identify unreachable code paths

4. **Dynamic Analysis**
   ```windbg
   bp opaque!opaque_true
   bp opaque!opaque_true2
   g
   r
   t  # Step through to see return value
   ```

5. **Patch to Reveal Hidden Code**
   ```windbg
   # Modify jump conditions
   u opaque!main
   eb <address_of_jz> 0x90 0x90  # NOP the conditional jump
   ```

6. **Extract Flag**
   - Force execution of secret_function
   - Document all opaque predicates found

#### Deliverables:
- List of all opaque predicates with mathematical proof of invariance
- Control flow graph showing real vs. decoy paths
- WinDbg script to automatically bypass opaque predicates
- Flag extracted from hidden function

### Exercise 2: Simple XOR Packer Analysis
**Duration:** 90 minutes

#### Objective:
Reverse engineer a self-modifying program that unpacks itself at runtime using XOR encryption.

#### Challenge Program:
```c
#include <stdio.h>
#include <string.h>
#include <windows.h>

// XOR key
unsigned char key[] = {0xDE, 0xAD, 0xBE, 0xEF};

// Encrypted payload (will contain encrypted shellcode)
unsigned char encrypted_payload[] = {
    0xB1, 0xC8, 0xD1, 0x82, 0xB5, 0xC8, 0xDB, 0x8F,
    0xB5, 0xCE, 0xD2, 0x8A, 0xB1, 0xCC, 0xD7, 0x82,
    0xB1, 0xC8, 0xDE, 0x86, 0xB7, 0xCD, 0xD0, 0x8F,
    0xB1, 0xCE, 0xD7, 0x8B, 0xB5, 0xC9, 0xDB, 0x82,
    0x00
};

void decrypt_and_execute() {
    size_t payload_size = sizeof(encrypted_payload) - 1;
    unsigned char *decrypted = (unsigned char *)VirtualAlloc(
        NULL,
        payload_size,
        MEM_COMMIT | MEM_RESERVE,
        PAGE_EXECUTE_READWRITE
    );

    // XOR decryption
    for (size_t i = 0; i < payload_size; i++) {
        decrypted[i] = encrypted_payload[i] ^ key[i % sizeof(key)];
    }

    // In real malware, this would execute shellcode
    // For educational purposes, we just print
    printf("Decrypted message: %s\n", decrypted);

    VirtualFree(decrypted, 0, MEM_RELEASE);
}

int main() {
    printf("Packed program starting...\n");
    decrypt_and_execute();
    printf("Execution complete.\n");
    return 0;
}
```

#### Steps:

1. **Initial Analysis**
   ```windbg
   bp main
   g
   lm  # List modules
   !address -f:Image  # Find image base
   ```

2. **Identify Decryption Routine**
   ```windbg
   bp packed!decrypt_and_execute
   g
   uf decrypt_and_execute
   ```

3. **Set Memory Breakpoint on Decryption**
   ```windbg
   # Find encrypted_payload address
   x packed!encrypted_payload
   # Set hardware breakpoint on memory access
   ba r4 <encrypted_payload_address>
   g
   ```

4. **Capture Decryption Process**
   ```windbg
   # Step through XOR loop
   bp packed!decrypt_and_execute+<offset_of_loop>
   g
   # Watch memory change
   db <encrypted_payload_address> L20
   p  # Step
   db <decrypted_address> L20
   ```

5. **Extract Decryption Key**
   ```windbg
   db packed!key L4
   ```

6. **Dump Decrypted Payload**
   ```windbg
   .writemem decrypted_payload.bin <decrypted_address> L<size>
   ```

7. **Python Script to Decrypt**
   ```python
   # Create automated decryption script
   encrypted = bytes([0xB1, 0xC8, 0xD1, 0x82, ...])
   key = bytes([0xDE, 0xAD, 0xBE, 0xEF])
   decrypted = bytes([encrypted[i] ^ key[i % len(key)] for i in range(len(encrypted))])
   print(decrypted)
   ```

#### Deliverables:
- Complete analysis report of packing mechanism
- Extracted XOR key and algorithm documentation
- Decrypted payload (hex dump and ASCII)
- Python unpacker script
- Memory timeline showing encryption/decryption states

### Exercise 3: Control Flow Flattening Defeat
**Duration:** 90 minutes

#### Objective:
Reverse engineer a program using control flow flattening to obscure program logic.

#### Challenge Program:
```c
#include <stdio.h>
#include <stdlib.h>

// Control flow flattening example
void flattened_logic(int input) {
    int state = 0;
    int result = 0;

    while (1) {
        switch (state) {
            case 0:
                printf("Stage 1: Initialization\n");
                result = input;
                state = 1;
                break;

            case 1:
                printf("Stage 2: Processing\n");
                result *= 2;
                state = (result > 100) ? 3 : 2;
                break;

            case 2:
                printf("Stage 3: Adjustment\n");
                result += 50;
                state = 3;
                break;

            case 3:
                printf("Stage 4: Validation\n");
                if (result == 142) {
                    state = 4;
                } else {
                    state = 5;
                }
                break;

            case 4:
                printf("Success! Flag: OSED{fl4tt3n3d_fl0w_un0bfusc4t3d}\n");
                return;

            case 5:
                printf("Incorrect input.\n");
                return;

            default:
                printf("Invalid state.\n");
                return;
        }
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <number>\n", argv[0]);
        return 1;
    }

    int input = atoi(argv[1]);
    flattened_logic(input);

    return 0;
}
```

#### Steps:

1. **Initial Dynamic Analysis**
   ```windbg
   bp flattened!flattened_logic
   g
   uf flattened!flattened_logic
   ```

2. **Identify State Machine**
   - Locate switch statement dispatcher
   - Map state values to code blocks
   - Identify state transition logic

3. **Create State Transition Graph**
   ```windbg
   # Track state variable
   bp flattened!flattened_logic+<switch_offset>
   g
   r  # Record state value
   g  # Continue
   # Repeat to build complete graph
   ```

4. **Reconstruct Original Control Flow**
   - Document entry state
   - Map all state transitions
   - Identify terminal states
   - Determine winning conditions

5. **Solve Challenge**
   - Calculate required input value
   - Work backwards from success state
   - Verify solution

6. **Script State Machine Extraction**
   ```python
   # Create WinDbg script to auto-extract state transitions
   states = {}
   # Parse switch cases
   # Build transition table
   # Generate DOT file for visualization
   ```

#### Deliverables:
- State transition diagram (DOT/graphviz format)
- Reconstructed original C code (de-flattened)
- Winning input value with calculation proof
- WinDbg automation script for state extraction

### Exercise 4: Anti-Debugging Detection and Bypass
**Duration:** 90 minutes

#### Objective:
Identify and defeat multiple anti-debugging techniques in a single program.

#### Challenge Program:
```c
#include <stdio.h>
#include <windows.h>

// Check if being debugged via PEB
int check_peb_being_debugged() {
    BOOL debugged = FALSE;

    __asm {
        mov eax, fs:[0x30]      // PEB
        movzx eax, byte ptr [eax+2]  // BeingDebugged flag
        mov debugged, eax
    }

    return debugged;
}

// Check debug port
int check_remote_debugger() {
    BOOL debugged = FALSE;
    CheckRemoteDebuggerPresent(GetCurrentProcess(), &debugged);
    return debugged;
}

// Timing-based detection
int check_timing() {
    DWORD start = GetTickCount();

    // Simple operation
    int x = 0;
    for (int i = 0; i < 10; i++) {
        x += i;
    }

    DWORD end = GetTickCount();

    // If too slow, likely being debugged
    return (end - start) > 1000;
}

// Hardware breakpoint detection
int check_hardware_breakpoints() {
    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_DEBUG_REGISTERS;

    if (GetThreadContext(GetCurrentThread(), &ctx)) {
        if (ctx.Dr0 || ctx.Dr1 || ctx.Dr2 || ctx.Dr3) {
            return 1;  // Hardware breakpoint detected
        }
    }
    return 0;
}

void reveal_secret() {
    printf("Flag: OSED{4nt1_d3bug_byp4ss3d_succ3ssfully}\n");
    printf("Congratulations on defeating all anti-debug checks!\n");
}

int main() {
    printf("Starting protected program...\n");

    // Multiple anti-debug checks
    if (check_peb_being_debugged()) {
        printf("PEB debugger detected! Exiting.\n");
        return 1;
    }

    if (check_remote_debugger()) {
        printf("Remote debugger detected! Exiting.\n");
        return 2;
    }

    if (check_timing()) {
        printf("Timing anomaly detected! Exiting.\n");
        return 3;
    }

    if (check_hardware_breakpoints()) {
        printf("Hardware breakpoints detected! Exiting.\n");
        return 4;
    }

    // All checks passed
    reveal_secret();

    return 0;
}
```

#### Steps:

1. **Initial Run to Identify Checks**
   ```windbg
   bp main
   g
   # Program will likely detect debugger and exit
   ```

2. **Bypass PEB BeingDebugged Flag**
   ```windbg
   # Method 1: Modify PEB directly
   dt _PEB @$peb
   eb @$peb+2 0  # Set BeingDebugged to 0

   # Method 2: Patch check function
   uf antidebug!check_peb_being_debugged
   eb <return_address> 0xB8 0x00 0x00 0x00 0x00 0xC3  # mov eax, 0; ret
   ```

3. **Bypass Remote Debugger Check**
   ```windbg
   # Method 1: Hook CheckRemoteDebuggerPresent
   bp kernel32!CheckRemoteDebuggerPresent
   # When hit, modify return value

   # Method 2: Patch the check
   bp antidebug!check_remote_debugger
   g
   r eax=0  # Force return 0
   ```

4. **Bypass Timing Check**
   ```windbg
   # Method 1: Hook GetTickCount
   bp kernel32!GetTickCount
   # Return consistent values

   # Method 2: Patch timing check
   bp antidebug!check_timing
   g
   r eax=0
   ```

5. **Bypass Hardware Breakpoint Check**
   ```windbg
   # Don't use hardware breakpoints, or
   # Clear debug registers before GetThreadContext
   bp kernel32!GetThreadContext
   g
   # Modify CONTEXT structure to zero out Dr0-Dr3
   ```

6. **Automated Bypass Script**
   ```windbg
   $$ WinDbg script to bypass all checks
   bp antidebug!check_peb_being_debugged ".echo Bypassing PEB check; r eax=0; gc"
   bp antidebug!check_remote_debugger ".echo Bypassing remote debugger; r eax=0; gc"
   bp antidebug!check_timing ".echo Bypassing timing; r eax=0; gc"
   bp antidebug!check_hardware_breakpoints ".echo Bypassing HW BP; r eax=0; gc"
   g
   ```

#### Deliverables:
- Documentation of all anti-debug techniques found
- Bypass methods for each technique
- WinDbg script for automated bypass
- Comparison of different bypass approaches
- Flag extracted from reveal_secret()

## Comprehensive Challenge: The Vault

**Duration:** 120 minutes

### Objective:
Combine all learned techniques to crack a multi-stage protected vault program.

### Challenge Description:
You are provided with a binary `vault.exe` that implements:
- XOR-encrypted code sections
- Control flow flattening
- Opaque predicates
- Anti-debugging checks
- Multi-stage password verification

Your goal: Extract the master password and final flag.

### Provided Binary Characteristics:
```
- PE32 executable
- Custom packer with XOR encryption
- 3-stage password verification
- Anti-tamper checks
- Self-modifying code
```

### Challenge Stages:

#### Stage 1: Bypass Anti-Debug
- Identify and bypass all anti-debug mechanisms
- Document each technique found

#### Stage 2: Unpack Code
- Locate unpacking stub
- Extract encryption key
- Dump decrypted sections

#### Stage 3: Deobfuscate Control Flow
- Map flattened control flow
- Identify real vs fake paths
- Reconstruct original logic

#### Stage 4: Crack Password Verification
- Reverse engineer password algorithm
- Find valid passwords for each stage
- Extract final flag

### Hints:
1. Use hardware breakpoints on write to catch unpacking
2. The XOR key is derived from a checksum
3. State machine has 12 states, only 6 are real
4. Final password is an MD5 hash comparison
5. Flag format: OSED{...}

### Deliverables:
- Complete reverse engineering report (minimum 5 pages)
- All extracted passwords
- Unpacker script
- Deobfuscated source code reconstruction
- WinDbg automation scripts used
- Final flag

## Assessment Criteria

### Excellent (90-100%):
- All challenges completed successfully
- Comprehensive documentation of techniques
- Working automation scripts
- Clear explanation of methodologies
- All flags captured
- Comprehensive challenge completed with full report

### Good (80-89%):
- Most challenges completed (3-4 out of 5)
- Good documentation
- Some automation scripts
- Flags captured
- Comprehensive challenge attempted

### Satisfactory (70-79%):
- Basic challenges completed (2-3)
- Adequate documentation
- Manual analysis only
- Some flags captured
- Comprehensive challenge partially completed

### Needs Improvement (<70%):
- Minimal challenges completed (0-1)
- Poor documentation
- No flags captured
- Comprehensive challenge not attempted

## Lab Deliverables

### 1. Technical Analysis Report
For each exercise, provide:
- Problem description and objectives
- Methodology and approach
- Tools and techniques used
- Step-by-step solution
- Challenges encountered
- Lessons learned

### 2. Code and Scripts
- WinDbg automation scripts
- Python unpacker/decoder scripts
- Patched binaries (if applicable)
- Deobfuscated source reconstructions

### 3. Flags Document
- All captured flags
- Proof of completion (screenshots)
- Explanation of how each was obtained

### 4. Comprehensive Challenge Report
- Executive summary
- Detailed technical analysis
- All stages documented
- Complete solution with master password
- Final flag with proof

## Troubleshooting

### Common Issues:

1. **Anti-Debug Detection Still Triggering**
   - Check all PEB fields, not just BeingDebugged
   - Use ScyllaHide or similar anti-anti-debug plugin
   - Patch checks at assembly level

2. **Unpacker Not Executing Correctly**
   - Verify memory permissions (PAGE_EXECUTE_READWRITE)
   - Check if self-modifying code is involved
   - Use memory breakpoints instead of code breakpoints

3. **Control Flow Too Complex**
   - Start with dynamic analysis to understand program behavior
   - Build state transition table incrementally
   - Use graphing tools to visualize

4. **Timing Checks Always Failing**
   - Don't use step-by-step execution on timing-sensitive code
   - Use conditional breakpoints that auto-continue
   - Patch timing check functions entirely

## Next Steps

After completing this lab:
1. Review all techniques learned in Sections 2.1-2.7
2. Practice on real-world packed malware samples (in isolated VM)
3. Prepare for Section 2.8: Advanced Anti-Debugging and Evasion
4. Explore automated deobfuscation tools (Unicorn, Triton, etc.)
5. Study advanced topics: VM-based obfuscation, code virtualization

## Additional Resources

### Tools:
- ScyllaHide (anti-anti-debug plugin)
- x64dbg (alternative debugger)
- Binary Ninja / IDA Pro (static analysis)
- Ghidra (free RE framework)
- PE-bear, CFF Explorer (PE analysis)

### Reading:
- "Practical Malware Analysis" by Sikorski & Honig
- "The Art of Memory Forensics"
- "Practical Reverse Engineering" by Dang et al.
- Research papers on obfuscation techniques

### Online Resources:
- crackmes.one (practice challenges)
- root-me.org (RE challenges)
- reversing.kr (Korean RE challenges)
- RPISEC Modern Binary Exploitation course

### Communities:
- r/ReverseEngineering
- OpenSecurityTraining2.org
- Reverse Engineering Stack Exchange
