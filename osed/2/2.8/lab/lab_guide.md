# OSED Section 2.8 Lab: Advanced Anti-Debugging and Evasion Techniques

**Difficulty Level:** Expert
**Estimated Time:** 7 hours (3.5h theory + 3.5h lab)
**Skills:** Advanced anti-debugging bypass, Kernel debugging, Hypervisor detection, Exploit development evasion

## Lab Overview
This lab covers cutting-edge anti-debugging and evasion techniques used in modern malware and protected software. Students will learn to identify and bypass advanced protections including timing attacks, exception-based anti-debug, heaven's gate, and hypervisor detection.

## Prerequisites
- Completion of Sections 2.1-2.7
- Expert-level WinDbg proficiency
- Deep understanding of Windows internals
- Kernel debugging experience (recommended)
- Assembly language mastery
- Understanding of CPU exceptions and interrupts

## Lab Environment Setup

### Required Software:
- Windows 10/11 (64-bit) - Recommended: VM for kernel debugging
- WinDbg Preview with kernel debugging setup
- Visual Studio 2019+ with SDK
- VMware Workstation or VirtualBox (for nested virtualization tests)
- ScyllaHide plugin for x64dbg/WinDbg
- HyperDbg or similar hypervisor debugger (optional)

### Required Knowledge:
- PEB/TEB structures
- Windows exception handling
- CPU architecture internals
- Kernel/user mode boundaries
- Virtualization technology basics

## Lab Exercises

### Exercise 1: Exception-Based Anti-Debugging
**Duration:** 75 minutes

#### Objective:
Master exception-based anti-debugging techniques including INT3 scanning, SEH manipulation, and vectored exception handlers.

#### Challenge Program:
```c
#include <windows.h>
#include <stdio.h>

volatile BOOL debugger_detected = FALSE;

// Vectored Exception Handler
LONG WINAPI VectoredHandler(PEXCEPTION_POINTERS ExceptionInfo) {
    if (ExceptionInfo->ExceptionRecord->ExceptionCode == EXCEPTION_BREAKPOINT) {
        // If we hit a breakpoint exception, check if it's ours
        BYTE* eip = (BYTE*)ExceptionInfo->ContextRecord->Eip;

        if (*eip == 0xCC) {  // INT3
            // Skip the INT3
            ExceptionInfo->ContextRecord->Eip++;
            return EXCEPTION_CONTINUE_EXECUTION;
        }
    }
    return EXCEPTION_CONTINUE_SEARCH;
}

// Check for INT3 scanning
void check_int3_patches() {
    BYTE* code = (BYTE*)check_int3_patches;

    // Scan first 20 bytes of this function for INT3
    for (int i = 0; i < 20; i++) {
        if (code[i] == 0xCC) {
            printf("Breakpoint detected in code!\n");
            debugger_detected = TRUE;
            return;
        }
    }
}

// Single-step detection using trap flag
void check_single_step() {
    CONTEXT ctx;
    ctx.ContextFlags = CONTEXT_CONTROL;
    GetThreadContext(GetCurrentThread(), &ctx);

    // Check trap flag in EFLAGS
    if (ctx.EFlags & 0x100) {
        debugger_detected = TRUE;
        printf("Single-step detected!\n");
    }
}

// SEH-based detection
void check_seh_manipulation() {
    __try {
        // Deliberate divide by zero
        int x = 0;
        int y = 5 / x;
    }
    __except(EXCEPTION_EXECUTE_HANDLER) {
        // If we get here, exception was caught normally
        // If debugger catches it first, we might not reach here
        return;
    }

    // If we reach here, exception wasn't handled properly
    debugger_detected = TRUE;
}

// UnhandledExceptionFilter check
LONG WINAPI CustomUnhandledExceptionFilter(PEXCEPTION_POINTERS ExceptionInfo) {
    printf("Custom exception filter called.\n");
    return EXCEPTION_CONTINUE_EXECUTION;
}

void check_unhandled_exception_filter() {
    LPTOP_LEVEL_EXCEPTION_FILTER old = SetUnhandledExceptionFilter(
        CustomUnhandledExceptionFilter
    );

    LPTOP_LEVEL_EXCEPTION_FILTER current = SetUnhandledExceptionFilter(old);

    // Debugger may have set it to NULL
    if (current == NULL) {
        debugger_detected = TRUE;
        printf("UnhandledExceptionFilter was nullified!\n");
    }
}

// OutputDebugString timing
void check_outputdebugstring_timing() {
    DWORD start, end;

    start = GetTickCount();
    OutputDebugStringA("Debug test");
    end = GetTickCount();

    // When debugger present, OutputDebugString is much faster
    if (end - start < 1) {
        debugger_detected = TRUE;
        printf("OutputDebugString timing anomaly!\n");
    }
}

void reveal_secrets() {
    printf("\n=== SECRETS REVEALED ===\n");
    printf("Flag 1: OSED{3xc3pt10n_b4s3d_4nt1d3bug}\n");
    printf("Master Key: 0xDEADBEEFCAFEBABE\n");
    printf("========================\n");
}

int main() {
    printf("Advanced Anti-Debug Challenge Starting...\n\n");

    // Install vectored exception handler
    AddVectoredExceptionHandler(1, VectoredHandler);

    // Run all checks
    check_int3_patches();
    check_single_step();
    check_seh_manipulation();
    check_unhandled_exception_filter();
    check_outputdebugstring_timing();

    if (!debugger_detected) {
        reveal_secrets();
    } else {
        printf("\nDebugger detected! Secrets hidden.\n");
        return 1;
    }

    return 0;
}
```

#### Steps:

1. **Analyze Exception-Based Checks**
   ```windbg
   bp main
   g
   # Analyze each check function
   uf exception_checks!check_int3_patches
   uf exception_checks!check_seh_manipulation
   ```

2. **Bypass INT3 Scanning**
   ```windbg
   # Don't set breakpoints in scanned code
   # Use hardware breakpoints instead
   ba e1 exception_checks!check_int3_patches

   # Or patch the check
   bp exception_checks!check_int3_patches
   g
   r eax=0  # Force no detection
   ```

3. **Bypass SEH Checks**
   ```windbg
   # Handle exceptions properly
   sxe -c "g" av  # Set access violation to auto-continue

   # Or skip exception-throwing code
   bp exception_checks!check_seh_manipulation+<div_offset>
   g
   # Modify to avoid division
   r ecx=1  # Change divisor to non-zero
   ```

4. **Bypass UnhandledExceptionFilter Check**
   ```windbg
   # Hook SetUnhandledExceptionFilter
   bp kernel32!SetUnhandledExceptionFilter
   g
   # Always return non-NULL value
   ```

5. **Bypass Timing Checks**
   ```windbg
   # Hook GetTickCount and OutputDebugString
   bp kernel32!GetTickCount ".if @$retreg == <second_call_ret> { r eax=@eax+0n1000 }; gc"
   ```

6. **Complete Bypass Strategy**
   ```windbg
   $$ Comprehensive bypass script
   bp exception_checks!check_int3_patches ".echo Bypassing INT3 check; r eax=0; .echo Complete; gc"
   bp exception_checks!check_single_step ".echo Bypassing single-step; r eax=0; gc"
   bp exception_checks!check_seh_manipulation ".echo Bypassing SEH; gc"
   bp exception_checks!check_unhandled_exception_filter ".echo Bypassing UIEF; gc"
   bp exception_checks!check_outputdebugstring_timing ".echo Bypassing timing; gc"

   $$ Prevent debugger_detected from being set
   ba w4 exception_checks!debugger_detected ".echo Debugger flag write blocked; r eax=0; gc"

   g
   ```

#### Deliverables:
- Analysis of each exception-based technique
- WinDbg bypass script for all checks
- Documentation of exception handler manipulation
- Captured flags
- Comparison with ScyllaHide effectiveness

### Exercise 2: Heaven's Gate (WOW64 Transitions)
**Duration:** 90 minutes

#### Objective:
Understand and bypass anti-debugging techniques using WOW64 transitions between 32-bit and 64-bit code.

#### Background:
On 64-bit Windows, 32-bit applications run under WOW64 (Windows-on-Windows 64-bit). Heaven's Gate is a technique where 32-bit code switches to 64-bit mode to evade 32-bit debuggers.

#### Challenge Program:
```c
#include <windows.h>
#include <stdio.h>

#ifdef _WIN64
#error This program must be compiled as 32-bit (x86)
#endif

// Heaven's Gate: Switch to 64-bit mode from 32-bit code
BOOL check_debugger_via_heaven_gate() {
    BOOL debugged = FALSE;

    // This inline assembly switches to 64-bit mode
    __asm {
        push 0x33               // 64-bit code segment
        call next
        next:
        add dword ptr [esp], 5  // Offset to 64-bit code
        retf                    // Far return to 64-bit mode

        // Now executing in 64-bit mode (in 32-bit WinDbg, you can't see this!)
        // Read PEB64 directly
        db 0x65, 0x48, 0x8B, 0x04, 0x25, 0x60, 0x00, 0x00, 0x00  // mov rax, gs:[60h]  ; PEB64
        db 0x8A, 0x40, 0x02                                        // mov al, byte ptr [rax+2]  ; BeingDebugged
        db 0x88, 0x45, 0xFC                                        // mov byte ptr [ebp-4], al  ; Store result

        // Return to 32-bit mode
        call go_back
        go_back:
        mov dword ptr [esp+4], 0x23  // 32-bit code segment
        add dword ptr [esp], 0x0D    // Offset
        retf                         // Far return to 32-bit

        // Back in 32-bit mode
        mov al, byte ptr [ebp-4]
        mov debugged, al
    }

    return debugged;
}

// Direct syscall to NtQueryInformationProcess (bypassing hooks)
typedef NTSTATUS (NTAPI *NtQueryInformationProcess_t)(
    HANDLE ProcessHandle,
    DWORD ProcessInformationClass,
    PVOID ProcessInformation,
    ULONG ProcessInformationLength,
    PULONG ReturnLength
);

BOOL check_debugger_via_syscall() {
    // ProcessDebugPort = 7
    DWORD debugPort = 0;

    // Get ntdll base
    HMODULE ntdll = GetModuleHandleA("ntdll.dll");

    // Find NtQueryInformationProcess
    NtQueryInformationProcess_t NtQIP =
        (NtQueryInformationProcess_t)GetProcAddress(ntdll, "NtQueryInformationProcess");

    // Call it
    NTSTATUS status = NtQIP(
        GetCurrentProcess(),
        7,  // ProcessDebugPort
        &debugPort,
        sizeof(debugPort),
        NULL
    );

    return (debugPort != 0);
}

void reveal_flag() {
    printf("\nFlag: OSED{h34v3ns_g4t3_cr0ss3d_succ3ssfully}\n");
    printf("Advanced bypass completed!\n");
}

int main() {
    printf("Heaven's Gate Anti-Debug Test\n\n");

    BOOL detected1 = check_debugger_via_heaven_gate();
    BOOL detected2 = check_debugger_via_syscall();

    if (detected1) {
        printf("Debugger detected via Heaven's Gate!\n");
    }

    if (detected2) {
        printf("Debugger detected via syscall!\n");
    }

    if (!detected1 && !detected2) {
        reveal_flag();
    } else {
        printf("Debugging detected. Access denied.\n");
    }

    return 0;
}
```

#### Compilation:
```bash
# Must compile as 32-bit on 64-bit Windows
cl /Zi /Fe:heavensgate.exe heavensgate.c /link /MACHINE:X86
```

#### Steps:

1. **Initial Analysis with 32-bit Debugger**
   ```windbg
   # Use x64 WinDbg, not x86!
   # Open 32-bit binary
   bp main
   g
   ```

2. **Identify Heaven's Gate Transition**
   ```windbg
   # Look for far return (retf) instructions
   uf heavensgate!check_debugger_via_heaven_gate

   # Find segment switch
   u heavensgate!check_debugger_via_heaven_gate L50
   ```

3. **Debug 64-bit Code Section**
   ```windbg
   # Set breakpoint before retf
   bp heavensgate!check_debugger_via_heaven_gate+<offset_before_retf>
   g

   # After retf, you're in 64-bit mode
   # Switch WinDbg to 64-bit disassembly
   .effmach amd64

   # Now you can see 64-bit code
   u @rip
   ```

4. **Bypass PEB64 Check**
   ```windbg
   # Find GS segment PEB access
   # Set breakpoint on mov rax, gs:[60h]
   ba e1 @rip
   p

   # Modify PEB64 BeingDebugged flag
   .formats gs:[60h]
   eb gs:[60h]+0x2 0  # Set BeingDebugged to 0

   # Or patch the check result
   ```

5. **Bypass Direct Syscall**
   ```windbg
   # Hook NtQueryInformationProcess before syscall
   bp ntdll!NtQueryInformationProcess
   g

   # Modify return value after call
   pt  # Step to return
   # Modify debugPort in memory to 0
   ```

6. **Alternative: Patch Binary**
   ```windbg
   # Patch the check functions to always return 0
   eb heavensgate!check_debugger_via_heaven_gate <bytes_for_mov_eax_0_ret>
   eb heavensgate!check_debugger_via_syscall <bytes_for_mov_eax_0_ret>
   ```

#### Deliverables:
- Complete analysis of Heaven's Gate transition
- Annotated disassembly of 32-bit and 64-bit code sections
- Documentation of PEB vs PEB64 structures
- WinDbg script for debugging both modes
- Flag capture proof
- Notes on why 32-bit debuggers fail

### Exercise 3: Hypervisor and VM Detection
**Duration:** 90 minutes

#### Objective:
Identify and bypass virtual machine and hypervisor detection techniques.

#### Challenge Program:
```c
#include <windows.h>
#include <stdio.h>
#include <intrin.h>

// CPUID-based VM detection
BOOL detect_vm_cpuid() {
    int cpuInfo[4] = {0};

    // CPUID leaf 0x1
    __cpuid(cpuInfo, 1);

    // Hypervisor present bit (ECX bit 31)
    if (cpuInfo[2] & (1 << 31)) {
        return TRUE;
    }

    // Check vendor string
    __cpuid(cpuInfo, 0x40000000);
    char vendor[13];
    memcpy(vendor + 0, &cpuInfo[1], 4);
    memcpy(vendor + 4, &cpuInfo[2], 4);
    memcpy(vendor + 8, &cpuInfo[3], 4);
    vendor[12] = '\0';

    // VMware: "VMwareVMware"
    // VirtualBox: "VBoxVBoxVBox"
    // Hyper-V: "Microsoft Hv"
    // KVM: "KVMKVMKVM"

    if (strstr(vendor, "VMware") || strstr(vendor, "VBox") ||
        strstr(vendor, "Microsoft Hv") || strstr(vendor, "KVM")) {
        printf("VM detected via CPUID: %s\n", vendor);
        return TRUE;
    }

    return FALSE;
}

// RDTSC timing-based detection
BOOL detect_vm_timing() {
    unsigned __int64 tsc1, tsc2, diff;

    tsc1 = __rdtsc();

    // Execute a few instructions
    for (volatile int i = 0; i < 10; i++);

    tsc2 = __rdtsc();
    diff = tsc2 - tsc1;

    // In VM, RDTSC might show larger differences
    if (diff > 1000) {
        printf("VM detected via RDTSC timing: %llu cycles\n", diff);
        return TRUE;
    }

    return FALSE;
}

// I/O port-based VMware detection
BOOL detect_vmware_port() {
    BOOL detected = FALSE;

    __try {
        __asm {
            push edx
            push ecx
            push ebx

            mov eax, 'VMXh'  // VMware magic value
            mov ebx, 0       // IN port number
            mov ecx, 10      // Command (get version)
            mov edx, 'VX'    // Port number

            in eax, dx       // VMware backdoor I/O port

            cmp ebx, 'VMXh'  // Check if VMware responded
            jne not_vmware

            mov detected, 1

            not_vmware:
            pop ebx
            pop ecx
            pop edx
        }
    }
    __except(EXCEPTION_EXECUTE_HANDLER) {
        // If exception, not VMware
        detected = FALSE;
    }

    return detected;
}

// Check for VM-specific registry keys
BOOL detect_vm_registry() {
    HKEY hKey;
    const char* vm_keys[] = {
        "HARDWARE\\Description\\System\\SystemBiosVersion",  // Check for "VBOX", "VMware"
        "HARDWARE\\Description\\System\\VideoBiosVersion",
        "HARDWARE\\DEVICEMAP\\Scsi\\Scsi Port 0\\Scsi Bus 0\\Target Id 0\\Logical Unit Id 0",  // "Identifier"
        NULL
    };

    for (int i = 0; vm_keys[i] != NULL; i++) {
        if (RegOpenKeyExA(HKEY_LOCAL_MACHINE, vm_keys[i], 0, KEY_READ, &hKey) == ERROR_SUCCESS) {
            char value[256];
            DWORD size = sizeof(value);

            if (RegQueryValueExA(hKey, "SystemBiosVersion", NULL, NULL, (LPBYTE)value, &size) == ERROR_SUCCESS ||
                RegQueryValueExA(hKey, "VideoBiosVersion", NULL, NULL, (LPBYTE)value, &size) == ERROR_SUCCESS ||
                RegQueryValueExA(hKey, "Identifier", NULL, NULL, (LPBYTE)value, &size) == ERROR_SUCCESS) {

                if (strstr(value, "VBOX") || strstr(value, "VMware") ||
                    strstr(value, "Virtual") || strstr(value, "Hyper-V")) {
                    printf("VM detected in registry: %s\n", value);
                    RegCloseKey(hKey);
                    return TRUE;
                }
            }

            RegCloseKey(hKey);
        }
    }

    return FALSE;
}

// Check for VM-specific files
BOOL detect_vm_files() {
    const char* vm_files[] = {
        "C:\\Windows\\System32\\drivers\\vmmouse.sys",    // VMware
        "C:\\Windows\\System32\\drivers\\vmhgfs.sys",     // VMware
        "C:\\Windows\\System32\\drivers\\VBoxMouse.sys",  // VirtualBox
        "C:\\Windows\\System32\\drivers\\VBoxGuest.sys",  // VirtualBox
        "C:\\Windows\\System32\\drivers\\VBoxSF.sys",     // VirtualBox
        NULL
    };

    for (int i = 0; vm_files[i] != NULL; i++) {
        DWORD attr = GetFileAttributesA(vm_files[i]);
        if (attr != INVALID_FILE_ATTRIBUTES) {
            printf("VM detected via file: %s\n", vm_files[i]);
            return TRUE;
        }
    }

    return FALSE;
}

// MAC address check for VM patterns
BOOL detect_vm_mac_address() {
    // VMware MAC: 00:05:69, 00:0C:29, 00:1C:14, 00:50:56
    // VirtualBox MAC: 08:00:27
    // This would require API calls to enumerate network adapters
    // Simplified version here

    printf("Note: MAC address checking not implemented in this demo\n");
    return FALSE;
}

void reveal_flag() {
    printf("\n=== VM DETECTION BYPASSED ===\n");
    printf("Flag: OSED{n0_vm_d3t3ct3d_p4tc4_w1n}\n");
    printf("=============================\n");
}

int main() {
    printf("Hypervisor/VM Detection Challenge\n\n");

    BOOL vm_detected = FALSE;

    if (detect_vm_cpuid()) {
        printf("[!] VM detected via CPUID\n");
        vm_detected = TRUE;
    }

    if (detect_vm_timing()) {
        printf("[!] VM detected via timing\n");
        vm_detected = TRUE;
    }

    if (detect_vmware_port()) {
        printf("[!] VMware detected via I/O port\n");
        vm_detected = TRUE;
    }

    if (detect_vm_registry()) {
        printf("[!] VM detected via registry\n");
        vm_detected = TRUE;
    }

    if (detect_vm_files()) {
        printf("[!] VM detected via files\n");
        vm_detected = TRUE;
    }

    detect_vm_mac_address();

    if (!vm_detected) {
        reveal_flag();
    } else {
        printf("\nVirtual machine detected. This program requires physical hardware.\n");
        return 1;
    }

    return 0;
}
```

#### Steps:

1. **Analyze VM Detection Methods**
   ```windbg
   bp vmdetect!main
   g
   # Step through each detection function
   ```

2. **Bypass CPUID Checks**
   ```windbg
   # Hook __cpuid intrinsic
   bp vmdetect!detect_vm_cpuid
   g

   # After CPUID instruction, modify registers
   # CPUID is compiled to "cpuid" instruction
   # Find it: u @eip L20
   # Set breakpoint after it
   ba e1 <address_after_cpuid>
   g

   # Clear hypervisor bit (ECX bit 31)
   r ecx=@ecx & ~(1 << 31)

   # Modify vendor string in memory
   # Find where cpuInfo is stored
   # Overwrite with "GenuineIntel" or "AuthenticAMD"
   ```

3. **Bypass RDTSC Timing**
   ```windbg
   # Hook __rdtsc or manipulate return values
   bp vmdetect!detect_vm_timing
   g

   # Step to both RDTSC calls
   # Make them return close values
   # Or patch the comparison
   ```

4. **Bypass I/O Port Detection**
   ```windbg
   # The IN instruction will cause exception on real hardware
   # In VMware, it succeeds

   # Force exception to occur
   sxe -c ".echo Forcing VMware port exception; gc" gp

   # Or patch the check
   bp vmdetect!detect_vmware_port
   g
   r eax=0  # Force return FALSE
   ```

5. **Bypass Registry Checks**
   ```windbg
   # Hook registry APIs
   bp kernelbase!RegOpenKeyExA "j (poi(@esp+4) == <vm_keys_string_addr>) '.echo Blocking VM reg key; r eax=2; .echo Done; gc'; 'gc'"

   # Or modify registry strings in memory after read
   bp kernelbase!RegQueryValueExA
   # After success, modify the returned string
   ```

6. **Bypass File Checks**
   ```windbg
   # Hook GetFileAttributesA
   bp kernelbase!GetFileAttributesA ".if (poi(@esp+4) == <vm_file_path>) { .echo Hiding VM file; r eax=0xFFFFFFFF; gc } .else { gc }"
   ```

7. **Comprehensive Bypass Script**
   ```windbg
   $$ VM Detection Bypass Master Script

   $$ CPUID bypass
   bp vmdetect!detect_vm_cpuid ".echo [BYPASS] CPUID check; r eax=0; gc"

   $$ Timing bypass
   bp vmdetect!detect_vm_timing ".echo [BYPASS] Timing check; r eax=0; gc"

   $$ I/O port bypass
   bp vmdetect!detect_vmware_port ".echo [BYPASS] VMware port; r eax=0; gc"

   $$ Registry bypass
   bp vmdetect!detect_vm_registry ".echo [BYPASS] Registry check; r eax=0; gc"

   $$ File bypass
   bp vmdetect!detect_vm_files ".echo [BYPASS] File check; r eax=0; gc"

   g
   ```

#### Deliverables:
- Comprehensive analysis of all VM detection methods
- Bypass techniques for each method
- WinDbg automation script for complete bypass
- Documentation of CPUID masking techniques
- Flag capture
- Comparison: bypass vs. bare metal execution

### Exercise 4: Kernel-Mode Anti-Debug Bypass
**Duration:** 120 minutes

#### Objective:
Work with kernel-level anti-debugging techniques and learn to bypass them using kernel debugging.

#### Setup Requirements:
- Two machines (or VM + host) for kernel debugging
- Kernel debugging enabled on target
- WinDbg configured for kernel debugging

#### Challenge Description:
A kernel driver is installed that:
- Monitors debug events
- Detects attached debuggers
- Protects target process memory
- Implements anti-debugging at kernel level

#### Challenge Program (User-Mode Component):
```c
#include <windows.h>
#include <stdio.h>

#define IOCTL_CHECK_DEBUGGER CTL_CODE(FILE_DEVICE_UNKNOWN, 0x800, METHOD_BUFFERED, FILE_ANY_ACCESS)
#define IOCTL_PROTECT_PROCESS CTL_CODE(FILE_DEVICE_UNKNOWN, 0x801, METHOD_BUFFERED, FILE_ANY_ACCESS)

BOOL check_via_kernel_driver() {
    HANDLE hDevice = CreateFileA(
        "\\\\.\\AntiDebugDriver",
        GENERIC_READ | GENERIC_WRITE,
        0,
        NULL,
        OPEN_EXISTING,
        0,
        NULL
    );

    if (hDevice == INVALID_HANDLE_VALUE) {
        printf("Driver not loaded.\n");
        return FALSE;
    }

    BOOL debugged = FALSE;
    DWORD bytesReturned;

    DeviceIoControl(
        hDevice,
        IOCTL_CHECK_DEBUGGER,
        NULL,
        0,
        &debugged,
        sizeof(debugged),
        &bytesReturned,
        NULL
    );

    CloseHandle(hDevice);
    return debugged;
}

void reveal_kernel_flag() {
    printf("\n=== KERNEL ANTI-DEBUG DEFEATED ===\n");
    printf("Flag: OSED{k3rn3l_m0d3_4nt1d3bug_pwn3d}\n");
    printf("Master Achievement Unlocked!\n");
    printf("===================================\n");
}

int main() {
    printf("Kernel-Mode Anti-Debug Challenge\n\n");

    if (check_via_kernel_driver()) {
        printf("Kernel driver detected debugging!\n");
        return 1;
    }

    reveal_kernel_flag();
    return 0;
}
```

#### Kernel Driver (Simplified Concepts):
```c
// This is a simplified representation - actual kernel driver development is complex

// In DriverEntry:
// - Register process creation callback
// - Register debug object callback
// - Set up IOCTL handler

// Debug detection in kernel:
BOOLEAN IsProcessBeingDebugged(PEPROCESS Process) {
    // Check if debug port is set
    HANDLE DebugPort = NULL;

    // ObReferenceObjectByHandle with debug object type
    // If succeeds, process is being debugged

    return (DebugPort != NULL);
}

// IOCTL Handler:
NTSTATUS DeviceControl(PDEVICE_OBJECT DeviceObject, PIRP Irp) {
    PIO_STACK_LOCATION stack = IoGetCurrentIrpStackLocation(Irp);

    switch (stack->Parameters.DeviceIoControl.IoControlCode) {
        case IOCTL_CHECK_DEBUGGER:
            BOOLEAN debugged = IsProcessBeingDebugged(PsGetCurrentProcess());
            // Return result to user mode
            break;
    }
}
```

#### Steps:

1. **Set Up Kernel Debugging**
   ```
   # On target machine (debuggee):
   bcdedit /debug on
   bcdedit /dbgsettings serial debugport:1 baudrate:115200

   # Reboot

   # On host machine (debugger):
   windbg -k com:port=<com_port>,baud=115200
   ```

2. **Load and Analyze Driver**
   ```windbg
   # In kernel debugger
   lm m AntiDebugDriver

   # List driver functions
   x AntiDebugDriver!*

   # Disassemble IOCTL handler
   uf AntiDebugDriver!DeviceControl
   ```

3. **Bypass Kernel Detection**
   ```windbg
   # Method 1: Patch driver's detection function
   bp AntiDebugDriver!IsProcessBeingDebugged
   g
   # Return FALSE
   r rax=0

   # Method 2: Modify debug port in EPROCESS
   !process 0 0 target.exe
   # Get EPROCESS address
   dt _EPROCESS <address>
   # Find DebugPort offset
   # Set it to NULL
   eq <eprocess_addr>+<debugport_offset> 0

   # Method 3: Unload the driver
   # From admin command prompt:
   sc stop AntiDebugDriver
   sc delete AntiDebugDriver
   ```

4. **User-Mode Bypass (If Kernel Modification Not Possible)**
   ```windbg
   # Hook DeviceIoControl
   bp kernelbase!DeviceIoControl "j (dwo(@esp+8) == 0x<IOCTL_CHECK_DEBUGGER>) '.echo Faking kernel response; r eax=1; .echo Modifying output buffer; eb <buffer_addr> 0; gc' 'gc'"
   ```

#### Deliverables:
- Kernel debugging session log
- Analysis of kernel-mode detection techniques
- Bypass method documentation
- Comparison of kernel vs. user-mode bypass effectiveness
- Flag capture
- Notes on EPROCESS structure

## Comprehensive Final Challenge: The Nexus

**Duration:** 180 minutes (3 hours)

### Objective:
Defeat a multi-layered protection system combining ALL techniques from this lab:
- Exception-based anti-debugging
- Heaven's Gate 64-bit transitions
- VM/Hypervisor detection
- Kernel-mode protection
- Self-modifying code
- Code integrity checks

### Challenge Binary: nexus.exe

### Protection Layers:

1. **Layer 1: VM Detection**
   - Must pass CPUID, timing, registry, and file checks
   - If detected, program exits immediately

2. **Layer 2: Exception-Based Anti-Debug**
   - Multiple VEH handlers
   - SEH manipulation checks
   - Single-step detection

3. **Layer 3: Heaven's Gate**
   - Critical code runs in 64-bit mode
   - Accesses PEB64 directly
   - Performs integrity checks in 64-bit space

4. **Layer 4: Kernel-Mode Verification**
   - Communicates with kernel driver
   - Verifies no user-mode debuggers attached
   - Checks for kernel debuggers

5. **Layer 5: Code Integrity**
   - CRC checks on critical sections
   - Detects breakpoint patches (INT3)
   - Self-healing code

6. **Final Vault:**
   - Multi-stage password
   - Each stage protected differently
   - Final flag revealed only when all layers bypassed

### Success Criteria:
- Extract all 5 intermediate flags (one per layer)
- Extract final master flag
- Document complete bypass methodology
- Create automated bypass scripts

### Hints:
1. Start with VM detection - easiest layer
2. Use hardware breakpoints to avoid INT3 detection
3. 64-bit code holds encryption key for next layer
4. Kernel driver can be bypassed via IOCTL hooking
5. Code integrity uses CRC32 - calculate expected values
6. Master password is SHA256 hash of all 5 layer flags

### Deliverables:
- **Technical Report** (minimum 10 pages):
  - Executive summary
  - Detailed analysis of each layer
  - Bypass methodology for each protection
  - Tools and techniques used
  - Challenges encountered and solutions
  - Lessons learned

- **Bypass Toolkit**:
  - WinDbg scripts for automated bypass
  - Python tools for decryption/unpacking
  - Patched binary (optional)
  - Documentation for each tool

- **Flags Document**:
  - All 5 layer flags with extraction proof
  - Master flag with derivation explanation
  - Screenshots of successful bypasses

## Assessment Criteria

### Excellent (90-100%):
- All exercises completed successfully
- Comprehensive documentation
- Working automation scripts for all techniques
- All flags captured
- Comprehensive challenge completed with full report
- Deep understanding demonstrated

### Good (80-89%):
- Most exercises completed (3-4 of 4)
- Good documentation
- Some automation scripts
- Most flags captured
- Comprehensive challenge attempted, multiple layers defeated
- Solid understanding

### Satisfactory (70-79%):
- Half of exercises completed (2 of 4)
- Adequate documentation
- Manual analysis, minimal scripting
- Some flags captured
- Comprehensive challenge attempted, at least 2 layers defeated

### Needs Improvement (<70%):
- Minimal exercises completed (0-1)
- Poor documentation
- No flags captured
- Comprehensive challenge not seriously attempted

## Lab Deliverables

### 1. Comprehensive Technical Report
- Executive summary of all techniques
- Detailed methodology for each exercise
- Tool documentation
- Challenges and solutions
- Advanced topics explored

### 2. Bypass Toolkit
- All WinDbg scripts
- Python utilities
- Automation tools
- Usage documentation

### 3. Flags and Proof of Completion
- All individual flags
- Master flag from final challenge
- Screenshots and proof
- Derivation/calculation explanations

### 4. Reflection Document
- What you learned
- Most challenging aspects
- Practical applications
- Future study areas

## Troubleshooting

### Common Issues:

1. **Kernel Debugging Won't Connect**
   - Verify COM port settings on both machines
   - Check firewall settings for network debugging
   - Ensure bcdedit settings are correct
   - Try network debugging instead of serial

2. **Heaven's Gate Code Not Visible**
   - Use 64-bit WinDbg, not 32-bit
   - Switch effective machine: `.effmach amd64`
   - Disassemble with `u` command at correct addresses

3. **VM Detection Can't Be Bypassed**
   - Some checks may require registry/file modifications on host
   - Consider using paravirtualization tools
   - Test on physical hardware if available

4. **Kernel Driver Won't Load**
   - Disable driver signature enforcement: `bcdedit /set testsigning on`
   - Check if driver is properly signed
   - Verify compatibility with Windows version

5. **Exception Handlers Interfering**
   - Use `sxd` to disable first-chance exception handling
   - Set exception handling: `sxe -c "gc" <exception>`
   - Clear vectored exception handlers if possible

## Next Steps

After completing this lab:
1. **Practice on Real Malware**
   - Analyze real-world packed samples (in isolated environment)
   - Study APT malware protection techniques
   - Contribute to malware analysis communities

2. **Advanced Topics**
   - Code virtualization (VMProtect, Themida)
   - Hardware-based protection (Intel SGX)
   - Hypervisor-based debugging
   - Advanced ROP chain analysis

3. **Tool Development**
   - Create your own anti-anti-debug plugins
   - Develop automated unpacking tools
   - Build custom debugger extensions

4. **Certification Prep**
   - Continue OSED course material
   - Practice on Crackmes and CTF challenges
   - Review all sections 2.1-2.8

## Additional Resources

### Tools:
- **ScyllaHide**: Anti-anti-debug plugin
- **HyperDbg**: Hypervisor-based debugger
- **Pafish**: VM/Sandbox detection tool (for testing)
- **Al-Khaser**: Anti-debugging/VM detection suite (for testing)
- **TitanHide**: Advanced anti-anti-debug

### Reading:
- "Rootkits and Bootkits" by Matrosov et al.
- "Windows Kernel Programming" by Pavel Yosifovich
- "The Rootkit Arsenal" by Bill Blunden
- Anti-debugging research papers from security conferences

### Courses:
- Windows Kernel Exploitation (Advanced)
- Modern Binary Exploitation
- Malware Analysis and Reverse Engineering

### Communities:
- /r/ReverseEngineering
- /r/Malware
- OpenRCE Forums
- Reverse Engineering Stack Exchange

### Practice:
- Flare-On Challenge (annual RE CTF)
- crackmes.one
- root-me.org RE challenges
- HackTheBox RE boxes
