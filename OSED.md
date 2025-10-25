# OSED Course Table of Contents

## 1. Windows User Mode Exploit Development: General Course Information
- **Page:** 1

### 1.1 About the EXP-301 Course
- **Page:** 1

### 1.2 Provided Materials
- **Page:** 1
- **1.2.1** EXP-301 Course Materials *(Page 1)*
- **1.2.2** Access to the Internal VPN Lab Network *(Page 1)*
- **1.2.3** The Offensive Security Student Forum *(Page 1)*
- **1.2.4** Live Support and RocketChat *(Page 1)*
- **1.2.5** OSED Exam Attempt *(Page 1)*

### 1.3 Overall Strategies for Approaching the Course
- **Page:** 1
- **1.3.1** Welcome and Course Information Emails *(Page 1)*
- **1.3.2** Course Materials *(Page 1)*
- **1.3.3** Course Exercises *(Page 1)*

### 1.4 About the EXP-301 VPN Labs
- **Page:** 1
- **1.4.1** Control Panel *(Page 1)*
- **1.4.2** Reverts *(Page 1)*
- **1.4.3** Kali Virtual Machine *(Page 1)*
- **1.4.4** Lab Behavior and Lab Restrictions *(Page 1)*

### 1.5 About the OSED Exam
- **Page:** 1

### 1.6 Wrapping Up
- **Page:** 1

## 2. WinDbg and x86 Architecture
- **Page:** 2

### 2.1 Introduction to x86 Architecture
- **Page:** 2
- **2.1.1** Program Memory *(Page 2)*
- **2.1.2** CPU Registers *(Page 2)*

### 2.2 Introduction to Windows Debugger
- **Page:** 2
- **2.2.1** What is a Debugger? *(Page 2)*
- **2.2.2** WinDbg Interface *(Page 2)*
- **2.2.3** Understanding the Workspace *(Page 2)*
- **2.2.4** Debugging Symbols *(Page 2)*

### 2.3 Accessing and Manipulating Memory from WinDbg
- **Page:** 2
- **2.3.1** Unassemble from Memory *(Page 2)*
- **2.3.2** Reading from Memory *(Page 2)*
- **2.3.3** Dumping Structures from Memory *(Page 2)*
- **2.3.4** Writing to Memory *(Page 2)*
- **2.3.5** Searching the Memory Space *(Page 2)*
- **2.3.6** Inspecting and Editing CPU Registers in WinDbg *(Page 2)*

### 2.4 Controlling the Program Execution in WinDbg
- **Page:** 2
- **2.4.1** Software Breakpoints *(Page 2)*
- **2.4.2** Unresolved Function Breakpoint *(Page 2)*
- **2.4.3** Breakpoint-Based Actions *(Page 2)*
- **2.4.4** Hardware Breakpoints *(Page 2)*
- **2.4.5** Stepping Through the Code *(Page 2)*

### 2.5 Additional WinDbg Features
- **Page:** 2
- **2.5.1** Listing Modules and Symbols in WinDbg *(Page 2)*
- **2.5.2** Using WinDbg as a Calculator *(Page 2)*
- **2.5.3** Data Output Format *(Page 2)*
- **2.5.4** Pseudo Registers *(Page 2)*

### 2.6 Wrapping Up
- **Page:** 2

## 3. Exploiting Stack Overflows
- **Page:** 3

### 3.1 Stack Overflows Introduction
- **Page:** 3

### 3.2 Installing the Sync Breeze Application
- **Page:** 3

### 3.3 Crashing the Sync Breeze Application
- **Page:** 3

### 3.4 Win32 Buffer Overflow Exploitation
- **Page:** 3
- **3.4.1** A Word About DEP, ASLR, and CFG *(Page 3)*
- **3.4.2** Controlling EIP *(Page 3)*
- **3.4.3** Locating Space for Our Shellcode *(Page 3)*
- **3.4.4** Checking for Bad Characters *(Page 3)*
- **3.4.5** Redirecting the Execution Flow *(Page 3)*
- **3.4.6** Finding a Return Address *(Page 3)*
- **3.4.7** Generating Shellcode with Metasploit *(Page 3)*
- **3.4.8** Getting a Shell *(Page 3)*
- **3.4.9** Improving the Exploit *(Page 3)*

### 3.5 Wrapping Up
- **Page:** 3

## 4. Exploiting SEH Overflows
- **Page:** 4

### 4.1 Installing the Sync Breeze Application
- **Page:** 4

### 4.2 Crashing Sync Breeze
- **Page:** 4

### 4.3 Analyzing the Crash in WinDbg
- **Page:** 4

### 4.4 Introduction to Structured Exception Handling
- **Page:** 4
- **4.4.1** Understanding SEH *(Page 4)*
- **4.4.2** SEH Validation *(Page 4)*

### 4.5 Structured Exception Handler Overflows
- **Page:** 4
- **4.5.1** Gaining Code Execution *(Page 4)*
- **4.5.2** Detecting Bad Characters *(Page 4)*
- **4.5.3** Finding a P/P/R Instruction Sequence *(Page 4)*
- **4.5.4** Island-Hopping in Assembly *(Page 4)*
- **4.5.5** Obtaining a Shell *(Page 4)*

### 4.6 Wrapping Up
- **Page:** 4

## 5. Introduction to IDA Pro
- **Page:** 5

### 5.1 IDA Pro 101
- **Page:** 5
- **5.1.1** Installing IDA Pro *(Page 5)*
- **5.1.2** The IDA Pro User Interface *(Page 5)*
- **5.1.3** Basic Functionality *(Page 5)*
- **5.1.4** Search Functionality *(Page 5)*

### 5.2 Working with IDA Pro
- **Page:** 5
- **5.2.1** Static-Dynamic Analysis Synchronization *(Page 5)*
- **5.2.2** Tracing Notepad *(Page 5)*

### 5.3 Wrapping Up
- **Page:** 5

## 6. Overcoming Space Restrictions: Egghunters
- **Page:** 6

### 6.1 Crashing the Savant Web Server
- **Page:** 6

### 6.2 Analyzing the Crash in WinDbg
- **Page:** 6

### 6.3 Detecting Bad Characters
- **Page:** 6

### 6.4 Gaining Code Execution
- **Page:** 6
- **6.4.1** Partial EIP Overwrite *(Page 6)*
- **6.4.2** Changing the HTTP Method *(Page 6)*
- **6.4.3** Conditional Jumps *(Page 6)*

### 6.5 Finding Alternative Places to Store Large Buffers
- **Page:** 6
- **6.5.1** The Windows Heap Memory Manager *(Page 6)*

### 6.6 Finding our Buffer - The Egghunter Approach
- **Page:** 6
- **6.6.1** Keystone Engine *(Page 6)*
- **6.6.2** System Calls and Egghunters *(Page 6)*
- **6.6.3** Identifying and Addressing the Egghunter Issue *(Page 6)*
- **6.6.4** Obtaining a Shell *(Page 6)*

### 6.7 Improving the Egghunter Portability Using SEH
- **Page:** 6
- **6.7.1** Identifying the SEH-Based Egghunter Issue *(Page 6)*
- **6.7.2** Porting the SEH Egghunter to Windows 10 *(Page 6)*

### 6.8 Wrapping Up
- **Page:** 6

## 7. Creating Custom Shellcode
- **Page:** 7

### 7.1 Calling Conventions on x86
- **Page:** 7

### 7.2 The System Call Problem
- **Page:** 7

### 7.3 Finding kernel32.dll
- **Page:** 7
- **7.3.1** PEB Method *(Page 7)*
- **7.3.2** Assembling the Shellcode *(Page 7)*

### 7.4 Resolving Symbols
- **Page:** 7
- **7.4.1** Export Directory Table *(Page 7)*
- **7.4.2** Working with the Export Names Array *(Page 7)*
- **7.4.3** Computing Function Name Hashes *(Page 7)*
- **7.4.4** Fetching the VMA of a Function *(Page 7)*

### 7.5 NULL-Free Position-Independent Shellcode (PIC)
- **Page:** 7
- **7.5.1** Avoiding NULL Bytes *(Page 7)*
- **7.5.2** Position-Independent Shellcode *(Page 7)*

### 7.6 Reverse Shell
- **Page:** 7
- **7.6.1** Loading ws2_32.dll and Resolving Symbols *(Page 7)*
- **7.6.2** Calling WSAStartup *(Page 7)*
- **7.6.3** Calling WSASocket *(Page 7)*
- **7.6.4** Calling WSAConnect *(Page 7)*
- **7.6.5** Calling CreateProcessA *(Page 7)*

### 7.7 Wrapping Up
- **Page:** 7

## 8. Reverse Engineering for Bugs
- **Page:** 8

### 8.1 Installation and Enumeration
- **Page:** 8
- **8.1.1** Installing Tivoli Storage Manager *(Page 8)*
- **8.1.2** Enumerating an Application *(Page 8)*

### 8.2 Interacting with Tivoli Storage Manager
- **Page:** 8
- **8.2.1** Hooking the recv API *(Page 8)*
- **8.2.2** Synchronizing WinDbg and IDA Pro *(Page 8)*
- **8.2.3** Tracing the Input *(Page 8)*
- **8.2.4** Checksum, Please *(Page 8)*

### 8.3 Reverse Engineering the Protocol
- **Page:** 8
- **8.3.1** Header-Data Separation *(Page 8)*
- **8.3.2** Reversing the Header *(Page 8)*
- **8.3.3** Exploiting Memcpy *(Page 8)*
- **8.3.4** Getting EIP Control *(Page 8)*

### 8.4 Digging Deeper to Find More Bugs
- **Page:** 8
- **8.4.1** Switching Execution *(Page 8)*
- **8.4.2** Going Down 0x534 *(Page 8)*

### 8.5 Wrapping Up
- **Page:** 8

## 9. Stack Overflows and DEP Bypass
- **Page:** 9

### 9.1 Data Execution Prevention
- **Page:** 9
- **9.1.1** DEP Theory *(Page 9)*
- **9.1.2** Windows Defender Exploit Guard *(Page 9)*

### 9.2 Return Oriented Programming
- **Page:** 9
- **9.2.1** Origins of Return Oriented Programming Exploitation *(Page 9)*
- **9.2.2** Return Oriented Programming Evolution *(Page 9)*

### 9.3 Gadget Selection
- **Page:** 9
- **9.3.1** Debugger Automation: Pykd *(Page 9)*
- **9.3.2** Optimized Gadget Discovery: RP++ *(Page 9)*

### 9.4 Bypassing DEP
- **Page:** 9
- **9.4.1** Getting The Offset *(Page 9)*
- **9.4.2** Locating Gadgets *(Page 9)*
- **9.4.3** Preparing the Battlefield *(Page 9)*
- **9.4.4** Making ROP's Acquaintance *(Page 9)*
- **9.4.5** Obtaining VirtualAlloc Address *(Page 9)*
- **9.4.6** Patching the Return Address *(Page 9)*
- **9.4.7** Patching Arguments *(Page 9)*
- **9.4.8** Executing VirtualAlloc *(Page 9)*
- **9.4.9** Getting a Reverse Shell *(Page 9)*

### 9.5 Wrapping Up
- **Page:** 9

## 10. Stack Overflows and ASLR Bypass
- **Page:** 10

### 10.1 ASLR Introduction
- **Page:** 10
- **10.1.1** ASLR Implementation *(Page 10)*
- **10.1.2** ASLR Bypass Theory *(Page 10)*
- **10.1.3** Windows Defender Exploit Guard and ASLR *(Page 10)*

### 10.2 Finding Hidden Gems
- **Page:** 10
- **10.2.1** FXCLI_DebugDispatch *(Page 10)*
- **10.2.2** Arbitrary Symbol Resolution *(Page 10)*
- **10.2.3** Returning the Goods *(Page 10)*

### 10.3 Expanding our Exploit (ASLR Bypass)
- **Page:** 10
- **10.3.1** Leaking an IBM Module *(Page 10)*
- **10.3.2** Is That a Bad Character? *(Page 10)*

### 10.4 Bypassing DEP with WriteProcessMemory
- **Page:** 10
- **10.4.1** WriteProcessMemory *(Page 10)*
- **10.4.2** Getting Our Shell *(Page 10)*
- **10.4.3** Handmade ROP Decoder *(Page 10)*
- **10.4.4** Automating the Shellcode Encoding *(Page 10)*
- **10.4.5** Automating the ROP Decoder *(Page 10)*

### 10.5 Wrapping Up
- **Page:** 10

## 11. Format String Specifier Attack Part I
- **Page:** 11

### 11.1 Format String Attacks
- **Page:** 11
- **11.1.1** Format String Theory *(Page 11)*
- **11.1.2** Exploiting Format String Specifiers *(Page 11)*

### 11.2 Attacking IBM Tivoli FastBackServer
- **Page:** 11
- **11.2.1** Investigating the EventLog Function *(Page 11)*
- **11.2.2** Reverse Engineering a Path *(Page 11)*
- **11.2.3** Invoke the Specifiers *(Page 11)*

### 11.3 Reading the Event Log
- **Page:** 11
- **11.3.1** The Tivoli Event Log *(Page 11)*
- **11.3.2** Remote Event Log Service *(Page 11)*
- **11.3.3** Read From an Index *(Page 11)*
- **11.3.4** Read From the Log *(Page 11)*
- **11.3.5** Return the Log Content *(Page 11)*

### 11.4 Bypassing ASLR with Format Strings
- **Page:** 11
- **11.4.1** Parsing the Event Log *(Page 11)*
- **11.4.2** Leak Stack Address Remotely *(Page 11)*
- **11.4.3** Saving the Stack *(Page 11)*
- **11.4.4** Bypassing ASLR *(Page 11)*

### 11.5 Wrapping Up
- **Page:** 11

## 12. Format String Specifier Attack Part II
- **Page:** 12

### 12.1 Write Primitive with Format Strings
- **Page:** 12
- **12.1.1** Format String Specifiers Revisited *(Page 12)*
- **12.1.2** Overcoming Limitations *(Page 12)*
- **12.1.3** Write to the Stack *(Page 12)*
- **12.1.4** Going for a DWORD *(Page 12)*

### 12.2 Overwriting EIP with Format Strings
- **Page:** 12
- **12.2.1** Locating a Target *(Page 12)*
- **12.2.2** Obtaining EIP Control *(Page 12)*

### 12.3 Locating Storage Space
- **Page:** 12
- **12.3.1** Finding Buffers *(Page 12)*
- **12.3.2** Stack Pivot *(Page 12)*

### 12.4 Getting Code Execution
- **Page:** 12
- **12.4.1** ROP Limitations *(Page 12)*
- **12.4.2** Getting a Shell *(Page 12)*

### 12.5 Wrapping Up
- **Page:** 12

## 13. Trying Harder: The Labs
- **Page:** 13

### 13.1 Challenge 1
- **Page:** 13

### 13.2 Challenge 2
- **Page:** 13

### 13.3 Challenge 3
- **Page:** 13

### 13.4 Wrapping Up
- **Page:** 13

---

*This table of contents covers the Offensive Security Exploit Developer (OSED) course material focusing on Windows user-mode exploit development techniques including stack overflows, SEH exploitation, shellcode development, and modern mitigation bypasses.*
