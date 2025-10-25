# OSEE Course Table of Contents

## 1. Introduction
- **Page:** 8

## 2. Microsoft Edge Type Confusion
- **Page:** 9

### 2.1 Exploitation Introduction
- **Page:** 9
- **2.1.1** 64-bit Architecture *(Page 12)*
- **2.1.2** Vulnerability Classes *(Page 13)*
- **2.1.3** Basic Security Mitigations *(Page 17)*

### 2.2 Edge Internals
- **Page:** 18
- **2.2.1** JavaScript Engine *(Page 19)*
- **2.2.2** Chakra Internals *(Page 23)*
- **2.2.3** JIT and Type Confusion *(Page 24)*

### 2.3 Type Confusion Case Study
- **Page:** 25
- **2.3.1** Triggering the Vulnerability *(Page 26)*
- **2.3.2** Root Cause Analysis *(Page 31)*

### 2.4 Exploiting Type Confusion
- **Page:** 31
- **2.4.1** Controlling the auxSlots Pointer *(Page 34)*
- **2.4.2** Abuse AuxSlots Pointer *(Page 39)*
- **2.4.3** Create Read and Write Primitive *(Page 43)*
- **2.4.4** Going for RIP *(Page 44)*

### 2.5 Vanilla Attack
- **Page:** 44
- **2.5.1** CFG Internals *(Page 45)*
- **2.5.2** CFG Bypass *(Page 49)*

### 2.6 CFG Bypass
- **Page:** 49
- **2.6.1** Return Address Overwrite *(Page 49)*
- **2.6.2** Intel CET *(Page 53)*
- **2.6.3** Out-of-Context Calls *(Page 54)*

### 2.7 Data Only Attack
- **Page:** 57
- **2.7.1** Parallel DLL Loading *(Page 57)*
- **2.7.2** Injecting Fake Work *(Page 58)*
- **2.7.3** Faking the Work *(Page 63)*
- **2.7.4** Hot Patching DLLs *(Page 69)*

### 2.8 Arbitrary Code Guard (ACG)
- **Page:** 72
- **2.8.1** ACG Theory *(Page 72)*
- **2.8.2** ACG Bypasses *(Page 74)*

### 2.9 Advanced Out-of-Context Calls
- **Page:** 75
- **2.9.1** Faking it to Make it *(Page 75)*
- **2.9.2** Fixing the Crash *(Page 83)*

### 2.10 Remote Procedure Calls
- **Page:** 88
- **2.10.1** RPC Theory *(Page 88)*
- **2.10.2** Is That My Structure *(Page 91)*
- **2.10.3** Analyzing the Buffers *(Page 95)*
- **2.10.4** Calling an API *(Page 106)*
- **2.10.5** Return of Mitigations *(Page 111)*

### 2.11 Perfecting Out-of-Context Calls
- **Page:** 116
- **2.11.1** Come Back to JavaScript *(Page 116)*
- **2.11.2** Return Value Alignment *(Page 119)*
- **2.11.3** Call Me Again *(Page 125)*

### 2.12 Combining the Work
- **Page:** 129
- **2.12.1** NOP'ing CFG *(Page 129)*
- **2.12.2** Call Arbitrary API *(Page 131)*

### 2.13 Browser Sandbox
- **Page:** 133
- **2.13.1** Sandbox Theory Introduction *(Page 133)*
- **2.13.2** Sandbox Escape Theory *(Page 135)*
- **2.13.3** The Glue That Binds *(Page 136)*

### 2.14 Sandbox Escape Practice
- **Page:** 139
- **2.14.1** Insecure Access *(Page 139)*
- **2.14.2** The Problem of Languages *(Page 142)*

### 2.15 The Great Escape
- **Page:** 143
- **2.15.1** Activation Factory *(Page 143)*
- **2.15.2** GetTemplateContent *(Page 150)*
- **2.15.3** What Is As? *(Page 152)*
- **2.15.4** Loading the XML *(Page 155)*
- **2.15.5** Allowing Scripts *(Page 159)*
- **2.15.6** Pop That Notepad *(Page 161)*
- **2.15.7** Getting a Shell *(Page 163)*

### 2.16 Upping The Game - Making the Exploit Version Independent
- **Page:** 165
- **2.16.1** Locating the Base *(Page 165)*
- **2.16.2** Locating Internal Functions and Imports *(Page 167)*
- **2.16.3** Locating Exported Functions *(Page 171)*

### 2.17 Wrapping Up
- **Page:** 175

## 3. Kernel Exploitation and Payloads
- **Page:** 176

### 3.1 The Windows Kernel
- **Page:** 176
- **3.1.1** Privilege Levels *(Page 176)*
- **3.1.2** Interrupt Request Level (IRQL) *(Page 177)*
- **3.1.3** Windows Kernel Driver Signing *(Page 179)*

### 3.2 Kernel-Mode Debugging on Windows
- **Page:** 180
- **3.2.1** Remote Kernel Debugging Over TCP/IP *(Page 183)*

### 3.3 Communicating with the Kernel
- **Page:** 184
- **3.3.1** Native System Calls *(Page 193)*
- **3.3.2** Device Drivers *(Page 209)*

### 3.4 Kernel Vulnerability Classes
- **Page:** 211

### 3.5 Kernel-Mode Payloads
- **Page:** 212
- **3.5.1** Token Stealing *(Page 212)*
- **3.5.2** ACL Editing *(Page 217)*
- **3.5.3** Kernel Mode Rootkits *(Page 221)*

### 3.6 Vulnerability Overview and Exploitation
- **Page:** 222
- **3.6.1** Triggering the Vulnerability *(Page 222)*
- **3.6.2** Bypassing DSE *(Page 234)*

### 3.7 Redirecting Execution to Usermode
- **Page:** 236
- **3.7.1** Stack Pivoting *(Page 236)*
- **3.7.2** Kernel Read/Write Primitive *(Page 242)*
- **3.7.3** Restoring the I/O Ring Object *(Page 254)*

### 3.8 Elevate Privileges
- **Page:** 255
- **3.8.1** Data Only Attack *(Page 255)*

### 3.9 Developing a Rootkit
- **Page:** 258
- **3.9.1** Elevating Permissions *(Page 258)*
- **3.9.2** Evading Detection *(Page 263)*
- **3.9.3** Version Independence *(Page 272)*

### 3.10 Dynamic Gadget Location
- **Page:** 276

### 3.11 Extra Mile Exercise
- **Page:** 278

### 3.12 Wrapping Up
- **Page:** 278

## 4. Untrusted Pointer Dereference
- **Page:** 280

### 4.1 Vulnerability Overview and Exploit Types
- **Page:** 280
- **4.1.1** Identifying the Vulnerability through Patch-Diffing *(Page 281)*

### 4.2 Introduction to Memory Paging and Structures
- **Page:** 291
- **4.2.1** Memory Descriptor Lists (MDLs) *(Page 299)*
- **4.2.2** The PML4 Self-Reference Entry *(Page 301)*
- **4.2.3** PML4 Self-Reference Entry Randomization *(Page 306)*

### 4.3 Virtualization-Based Security
- **Page:** 307
- **4.3.1** Hyper-V - The Windows Hypervisor *(Page 308)*
- **4.3.2** Windows Hypervisor Debugging *(Page 312)*

### 4.4 Interacting With the Device Driver
- **Page:** 317

### 4.5 Extra Mile Exercise
- **Page:** 339

### 4.6 Reaching the Vulnerable Code Block
- **Page:** 339
- **4.6.1** Joy: From Happiness to Insight *(Page 348)*
- **4.6.2** Contentment: Unveiling Inner Peace *(Page 394)*
- **4.6.3** Uncertainty: Navigating the Unknown *(Page 407)*
- **4.6.4** Doubt: Understanding Self-Doubt *(Page 435)*
- **4.6.5** Fear: Facing Our Deepest Anxieties *(Page 442)*
- **4.6.6** Despair: The Path to Hope *(Page 462)*

### 4.7 A Wild Blue Screen Appears
- **Page:** 474

### 4.8 Mapping Physical Memory to User-Mode
- **Page:** 530

### 4.9 Exploiting the Vulnerability
- **Page:** 556

### 4.10 Wrapping Up
- **Page:** 566

## 5. Unsanitized User-Mode Callback
- **Page:** 567

### 5.1 Windows Desktop Applications
- **Page:** 567
- **5.1.1** Windows Kernel Pool Memory *(Page 567)*
- **5.1.2** Creating Windows Desktop Applications *(Page 580)*
- **5.1.3** Reversing the TagWND Object *(Page 591)*
- **5.1.4** Kernel User-mode Callbacks *(Page 598)*
- **5.1.5** Leaking pWND User-Mode Objects *(Page 611)*

### 5.2 Triggering the Vulnerability
- **Page:** 619
- **5.2.1** Spraying the Desktop Heap *(Page 620)*
- **5.2.2** Hooking the Callback *(Page 625)*
- **5.2.3** Arbitrary WndExtra Overwrite *(Page 628)*

### 5.3 TagWND Write Primitive
- **Page:** 638
- **5.3.1** Overwrite pWND[0].cbWndExtra *(Page 639)*
- **5.3.2** Overwrite pWND[1].WndExtra *(Page 647)*

### 5.4 TagWND Leak and Read Primitive
- **Page:** 653
- **5.4.1** Changing pWND[1].dwStyle *(Page 654)*
- **5.4.2** Setting The TagWND[1].spmenu *(Page 657)*
- **5.4.3** Creating a fake TagWND[1].spmenu *(Page 664)*
- **5.4.4** GetMenuBarInfo Read Primitive *(Page 686)*

### 5.5 Privilege Escalation
- **Page:** 688
- **5.5.1** Low integrity *(Page 688)*
- **5.5.2** Data Only Attack *(Page 692)*
- **5.5.3** Restoring The Execution Flow *(Page 701)*

### 5.6 Executing Code in Kernel-Mode
- **Page:** 704
- **5.6.1** Leaking Nt and Win32k Base *(Page 706)*
- **5.6.2** NOP-ing KCFG *(Page 711)*
- **5.6.3** Hijacking a Kernel-Mode Routine *(Page 716)*
- **5.6.4** Wrapping Up *(Page 721)*

---

*This table of contents covers the Offensive Security Exploitation Expert (OSEE) course material focusing on advanced exploitation techniques including browser exploitation, kernel exploitation, and Windows security mechanisms.*
