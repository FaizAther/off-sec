# OSED Section 2.2 Lab: Introduction to Windows Debugger

## Lab Overview
This lab provides hands-on experience with WinDbg interface, workspace management, and symbol loading. Students will learn to navigate WinDbg effectively and configure debugging environments.

## Prerequisites
- WinDbg Preview installed
- Basic understanding of Windows processes
- Sample executable for debugging

## Lab Environment Setup

### Required Software:
- Windows 10/11 (64-bit)
- WinDbg Preview
- Visual Studio or MinGW for C compilation
- Sample C program

### Sample C Program:
```c
#include <stdio.h>
#include <stdlib.h>
#include <windows.h>

int add_numbers(int a, int b) {
    return a + b;
}

int multiply_numbers(int a, int b) {
    return a * b;
}

int main() {
    int x = 10;
    int y = 20;
    int sum, product;
    
    printf("Starting calculation...\n");
    
    sum = add_numbers(x, y);
    product = multiply_numbers(x, y);
    
    printf("Sum: %d, Product: %d\n", sum, product);
    
    Sleep(5000); // Keep process alive for debugging
    
    return 0;
}
```

## Lab Exercises

### Exercise 1: WinDbg Interface Exploration
**Duration:** 30 minutes

#### Objective:
Explore WinDbg interface components and practice basic navigation.

#### Steps:

1. **Launch WinDbg**
   - Start WinDbg Preview
   - Observe interface layout
   - Identify main components

2. **Interface Components**
   - Command window (bottom)
   - Output window (top)
   - Source window (optional)
   - Memory window (optional)
   - Register window (optional)

3. **Basic Commands**
   ```windbg
   .help
   .version
   .time
   ```

4. **Command History**
   - Use up/down arrows
   - Access command history
   - Practice command completion

5. **Interface Customization**
   - Resize windows
   - Dock/undock panels
   - Change font settings

#### Expected Output:
```
Microsoft (R) Windows Debugger Version 10.0.25200.1003 X86
Copyright (c) Microsoft Corporation. All rights reserved.

CommandLine: 
Symbol search path is: srv*
Executable search path is: 
ModLoad: 00400000 00401000   sample.exe
ModLoad: 77c00000 77d00000   ntdll.dll
ModLoad: 77a00000 77b00000   kernel32.dll
```

### Exercise 2: Workspace Configuration
**Duration:** 30 minutes

#### Objective:
Configure WinDbg workspace and save settings for future use.

#### Steps:

1. **Create New Workspace**
   - File → New Workspace
   - Configure workspace name
   - Set workspace options

2. **Configure Preferences**
   - Tools → Options
   - Set debugging options
   - Configure display settings
   - Set command options

3. **Save Workspace**
   - File → Save Workspace
   - Choose workspace location
   - Verify workspace creation

4. **Load Workspace**
   - File → Open Workspace
   - Select saved workspace
   - Verify configuration

#### Configuration Options:
```
Workspace Settings:
- Auto-save workspace: Yes
- Save command history: Yes
- Save breakpoints: Yes
- Save watch expressions: Yes
```

### Exercise 3: Symbol Loading and Management
**Duration:** 60 minutes

#### Objective:
Load debugging symbols and configure symbol paths for effective debugging.

#### Steps:

1. **Compile with Debug Information**
   ```bash
   gcc -g -o sample.exe sample.c
   ```

2. **Launch Program and Attach WinDbg**
   - Start sample.exe
   - Attach WinDbg to process
   - Observe initial state

3. **Configure Symbol Path**
   ```windbg
   .sympath
   .sympath srv*C:\Symbols*https://msdl.microsoft.com/download/symbols
   .reload
   ```

4. **Load Symbols for Modules**
   ```windbg
   .reload sample.exe
   .reload kernel32.dll
   .reload ntdll.dll
   ```

5. **Verify Symbol Loading**
   ```windbg
   x sample!*
   x kernel32!*
   ```

6. **Analyze Symbol Information**
   ```windbg
   !lmi sample
   !lmi kernel32
   ```

#### Expected Output:
```
Symbol search path is: srv*C:\Symbols*https://msdl.microsoft.com/download/symbols
ModLoad: 00400000 00401000   sample.exe
Symbols loaded for sample
ModLoad: 77c00000 77d00000   ntdll.dll
Symbols loaded for ntdll
```

### Exercise 4: Process Information Analysis
**Duration:** 30 minutes

#### Objective:
Analyze process information and understand debugging context.

#### Steps:

1. **Process Information**
   ```windbg
   !process
   !process 0 0
   ```

2. **Module Information**
   ```windbg
   lm
   lm v
   ```

3. **Thread Information**
   ```windbg
   !threads
   ~
   ```

4. **Memory Information**
   ```windbg
   !address
   !vadump
   ```

5. **Symbol Information**
   ```windbg
   x sample!add_numbers
   x sample!multiply_numbers
   ```

#### Expected Output:
```
PROCESS 856a1234  SessionId: 1  Cid: 1234    Peb: 7ffdf000  ParentCid: 1234
    DirBase: 12345678  ObjectTable: 856a1234  HandleCount: 123.
    Image: sample.exe

MODULE_NAME: sample
IMAGE_NAME: sample.exe
BASE: 00400000
SIZE: 00001000
ENTRY_POINT: 00401000
```

## Lab Deliverables

### 1. Interface Configuration Report
Create a document containing:
- Screenshots of WinDbg interface
- Workspace configuration details
- Command reference sheet
- Interface customization notes

### 2. Symbol Management Worksheet
Complete the following:
- Symbol path configuration
- Symbol loading verification
- Symbol analysis results
- Troubleshooting notes

### 3. Process Analysis Summary
Document the following:
- Process information
- Module details
- Thread information
- Memory layout analysis

## Troubleshooting

### Common Issues:

1. **Symbols Not Loading**
   - Check symbol path configuration
   - Verify internet connectivity
   - Use local symbol files
   - Check file permissions

2. **Process Not Attaching**
   - Verify process is running
   - Check user permissions
   - Ensure correct architecture
   - Use appropriate attachment method

3. **Interface Issues**
   - Reset workspace to default
   - Check display settings
   - Verify WinDbg installation
   - Update WinDbg version

## Assessment Criteria

### Excellent (90-100%):
- Complete interface exploration
- Proper workspace configuration
- Successful symbol loading
- Clear documentation

### Good (80-89%):
- Most interface components identified
- Basic workspace setup
- Some symbols loaded
- Adequate documentation

### Satisfactory (70-79%):
- Limited interface exploration
- Minimal workspace configuration
- Few symbols loaded
- Basic documentation

### Needs Improvement (<70%):
- Incomplete interface exploration
- No workspace configuration
- No symbols loaded
- Inadequate documentation

## Next Steps
After completing this lab:
1. Review theory materials
2. Practice with additional programs
3. Prepare for Section 2.3: Accessing and Manipulating Memory
4. Experiment with different debugging scenarios

## Additional Resources
- WinDbg Help Documentation
- Microsoft Symbol Server
- Windows Debugging Tools
- Debugging Tutorials
