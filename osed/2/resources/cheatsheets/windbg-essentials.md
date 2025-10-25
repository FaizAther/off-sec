# WinDbg Essentials Cheat Sheet

## Quick Reference for OSED Section 2

---

## 🚀 Getting Started

### Launch & Attach
```windbg
windbg.exe <program.exe>          # Launch program
windbg.exe -p <PID>                # Attach to running process
.attach <PID>                      # Attach from within WinDbg
.detach                            # Detach from process
q                                  # Quit WinDbg
```

### Help & Information
```windbg
.hh                                # Open help documentation
.help                              # List all commands
.help <command>                    # Help for specific command
?                                  # Evaluate expression
.time                              # Display system time
.version                           # WinDbg version
```

---

## 📊 Process & Module Information

### Process Commands
```windbg
|                                  # List all processes
|<n>s                              # Switch to process n
!process                           # Current process info
!process 0 0                       # All processes (kernel mode)
!peb                               # Display PEB
dt _PEB @$peb                      # Detailed PEB structure
```

### Module Commands
```windbg
lm                                 # List modules
lm m <pattern>                     # List modules matching pattern
lm v m <module>                    # Verbose module info
!lmi <module>                      # Detailed module info
!dlls                              # List all DLLs
```

### Thread Commands
```windbg
~                                  # List all threads
~<n>s                              # Switch to thread n
~*                                 # All threads
!threads                           # Detailed thread info
~~[TID]s                          # Switch by thread ID
```

---

## 🔍 Memory Operations

### Reading Memory
```windbg
d <address>                        # Display memory (default type)
db <address>                       # Display bytes
dw <address>                       # Display words (2 bytes)
dd <address>                       # Display dwords (4 bytes)
dq <address>                       # Display qwords (8 bytes)
da <address>                       # Display ASCII string
du <address>                       # Display Unicode string
dps <address>                      # Display symbols + pointers
```

### Writing Memory
```windbg
e <address> <values>               # Edit memory
eb <address> <bytes>               # Edit bytes
ed <address> <dwords>              # Edit dwords
ea <address> "<string>"            # Edit ASCII string
eu <address> "<string>"            # Edit Unicode string
```

### Searching Memory
```windbg
s -<type> <range> <pattern>        # Search memory
s -b <start> L<length> <bytes>     # Search bytes
s -a <start> L<length> "<string>"  # Search ASCII
s -u <start> L<length> "<string>"  # Search Unicode
```

### Memory Information
```windbg
!address                           # Display memory layout
!address -summary                  # Summary of memory usage
!address <address>                 # Info about specific address
!vadump                            # Virtual address dump
!vprot <address>                   # Virtual protection info
```

---

## 🎯 Breakpoints

### Software Breakpoints
```windbg
bp <address>                       # Set breakpoint
bp <module>!<function>             # Set on function
bp <address> "<command>"           # BP with command
bl                                 # List breakpoints
bc <n>                             # Clear breakpoint n
bc *                               # Clear all breakpoints
bd <n>                             # Disable breakpoint n
be <n>                             # Enable breakpoint n
```

### Hardware Breakpoints
```windbg
ba <access> <size> <address>       # Hardware breakpoint
ba e 1 <address>                   # Execute (1 byte)
ba r 4 <address>                   # Read (4 bytes)
ba w 4 <address>                   # Write (4 bytes)
```

Access types:
- `e` = execute
- `r` = read
- `w` = write
- `i` = I/O (not usermode)

### Conditional Breakpoints
```windbg
bp <addr> ".if (poi(esp+4) == 0x42) {} .else {gc}"
bp <addr> "j (eax == 0) 'gc' ''"
```

---

## 🏃 Execution Control

### Basic Execution
```windbg
g                                  # Go (continue)
g <address>                        # Go to address
p                                  # Step over
t                                  # Step into (trace)
pa <address>                       # Step to address
ta <address>                       # Trace to address
```

### Advanced Stepping
```windbg
pc                                 # Step to next call
pt                                 # Step to next return
ph                                 # Step to next branch
gu                                 # Go up (step out)
```

### Execution Control
```windbg
.kill                              # Terminate debugged process
.restart                           # Restart debugging session
```

---

## 📝 Registers

### Display Registers
```windbg
r                                  # Display all registers
r <reg>                            # Display specific register
r <reg>=<value>                    # Set register value
rm                                 # Display register mask
```

### Common Registers (x86)
```
General Purpose:
  eax, ebx, ecx, edx               # General purpose
  esi, edi                         # Source/Destination index
  esp, ebp                         # Stack/Base pointer
  eip                              # Instruction pointer

Segment:
  cs, ds, ss, es, fs, gs           # Segment registers

Flags:
  efl                              # EFLAGS register
```

### Pseudo-Registers
```windbg
@$ip                               # Instruction pointer
@$sp                               # Stack pointer
@$peb                              # PEB address
@$teb                              # TEB address
@$retreg                           # Return value register
@$retreg64                         # 64-bit return register
```

---

## 🔧 Disassembly

### Disassemble Commands
```windbg
u <address>                        # Disassemble
u <address> L<lines>               # Disassemble N lines
ub <address>                       # Disassemble backwards
uf <function>                      # Unassemble function
up <address>                       # Disassemble with source
```

### Assembly Control
```windbg
a <address>                        # Assemble at address
```

---

## 📚 Stack Operations

### Stack Display
```windbg
k                                  # Stack trace
kb                                 # Stack with first 3 params
kv                                 # Stack verbose
kp                                 # Stack with all params
kn                                 # Stack with frame numbers
dps esp                            # Display stack with symbols
```

### Stack Frame
```windbg
.frame <n>                         # Switch to frame n
dv                                 # Display local variables
dt <type> <address>                # Display structure
```

---

## 🔗 Symbols

### Symbol Management
```windbg
.sympath                           # Show symbol path
.sympath+ <path>                   # Append to symbol path
.symfix                            # Set default symbol path
.reload                            # Reload symbols
.reload /f                         # Force reload
.reload /i <module>                # Reload specific module
```

### Symbol Operations
```windbg
x <module>!<pattern>               # Examine symbols
x /t /v <module>!*                 # List with types
ln <address>                       # List nearest symbol
!sym noisy                         # Verbose symbol loading
```

### Microsoft Symbol Server
```windbg
.sympath srv*C:\Symbols*https://msdl.microsoft.com/download/symbols
```

---

## 🧮 Expressions & Calculator

### Evaluate Expressions
```windbg
? <expression>                     # Evaluate expression
?? <C++ expression>                # Evaluate C++ expression
.formats <value>                   # Show value in all formats
```

### Common Operators
```
+  -  *  /                         # Arithmetic
&  |  ^  ~                         # Bitwise
<<  >>                             # Shift
==  !=  <  >  <=  >=               # Comparison
poi(<address>)                     # Dereference pointer
```

---

## 📄 Output & Logging

### Output Control
```windbg
.echo <text>                       # Echo text
.printf "format", <args>           # Printf-style output
.logopen <file>                    # Start logging
.logclose                          # Stop logging
.logappend <file>                  # Append to log
```

### Output Format
```windbg
.ocommand <command>                # Send output to command window
.cls                               # Clear screen
```

---

## 🎬 Scripts & Automation

### Script Execution
```windbg
$$                                 # Comment
$$< <scriptfile>                   # Run script file
$><scriptfile>                     # Run and redirect output
```

### Loops & Conditionals
```windbg
.for (init; condition; increment) { commands }
.foreach (variable {command}) { commands }
.if (condition) { commands } .else { commands }
.while (condition) { commands }
```

### Example Script
```windbg
$$ Analyze all modules
.foreach (mod {lm1m}) {
    .echo "Analyzing: ${mod}"
    !lmi ${mod}
}
```

---

## 🔍 Common Extension Commands

### Process/Memory
```windbg
!peb                               # Process Environment Block
!teb                               # Thread Environment Block
!heap                              # Heap information
!heap -s                           # Heap summary
!address                           # Memory regions
```

### Handles
```windbg
!handle                            # List handles
!handle <handle> f                 # Handle info
```

### Error Information
```windbg
!gle                               # Get last error
!error <code>                      # Decode error code
```

---

## 🐛 Exception Handling

### Exception Control
```windbg
sx                                 # List exception handling
sxe <exception>                    # Break on exception (first chance)
sxd <exception>                    # Disable break on exception
sxn <exception>                    # Notify on exception
sxi <exception>                    # Ignore exception
```

### Common Exceptions
```
av      # Access violation
bpe     # Breakpoint exception
cpr     # Process creation
dz      # Divide by zero
ld      # Load module
ud      # Unload module
```

### Exception with Commands
```windbg
sxe -c "gc" av                     # Continue on access violation
sxe -c ".echo AV!; g" av           # Echo and continue
```

---

## 💾 Data Structures

### Display Type
```windbg
dt <type>                          # Display type definition
dt <type> <address>                # Display at address
dt -r <type> <address>             # Recursive display
dt -v <type> <address>             # Verbose display
```

### Common Windows Structures
```windbg
dt ntdll!_PEB                      # Process Environment Block
dt ntdll!_TEB                      # Thread Environment Block
dt ntdll!_EPROCESS                 # Process object (kernel)
dt kernel32!_EXCEPTION_RECORD      # Exception record
```

---

## 🎓 Practical Examples

### Find String in Memory
```windbg
s -a 0 L?7fffffff "password"
```

### Trace Function Calls
```windbg
bp kernel32!CreateFileW ".echo Creating: ${@$arg1}; gc"
```

### Dump Process Memory
```windbg
.writemem dump.bin <start> <end>
```

### Analyze Crash
```windbg
.lastevent                         # Last event info
!analyze -v                        # Analyze crash
.ecxr                              # Set exception context
```

### Find RET Instructions
```windbg
s -[1]b <start> <end> c3           # Search for 0xC3 (ret)
```

---

## 🔑 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| F5 | Go (continue execution) |
| F10 | Step over |
| F11 | Step into |
| Shift+F11 | Step out |
| F9 | Toggle breakpoint |
| Ctrl+Break | Break execution |
| Alt+1 | Command window |
| Alt+2 | Watch window |
| Alt+3 | Locals window |
| Alt+4 | Registers window |
| Alt+5 | Memory window |
| Alt+6 | Callstack window |
| Alt+7 | Disassembly window |

---

## 📋 Common Workflows

### Basic Debugging Session
```windbg
# 1. Attach to process
windbg.exe -p <PID>

# 2. Set symbol path
.symfix
.reload

# 3. Set breakpoint
bp main

# 4. Run
g

# 5. Examine state
r
k
dv
```

### Memory Analysis
```windbg
# 1. Find memory region
!address <address>

# 2. Search for pattern
s -a 0 L?7fffffff "pattern"

# 3. Dump interesting memory
db <found_address>
```

### Function Analysis
```windbg
# 1. Find function
x *!*FunctionName*

# 2. Disassemble
uf <function_address>

# 3. Set breakpoint at entry
bp <function_address>

# 4. Run and trace
g
p
```

---

## 💡 Pro Tips

1. **Use Tab Completion**: Type partial commands and press Tab
2. **Command History**: Up/Down arrows for command history
3. **Copy Commands**: Right-click to copy from output
4. **Save Workspace**: File → Save Workspace for persistent settings
5. **Symbol Noise**: Use `!sym noisy` when symbols won't load
6. **Quick Registers**: `r eax` faster than `r` then search
7. **Address Math**: Use `?` for address calculations
8. **Auto-Commands**: Use `.logopen` to save all output
9. **Conditional BPs**: Save time with command-based breakpoints
10. **Pseudo-Registers**: Use `@$` for dynamic values

---

## 🔧 Troubleshooting

### Symbols Not Loading
```windbg
.symfix
.reload /f
!sym noisy
.reload /f
```

### Process Won't Attach
- Check if 32-bit vs 64-bit mismatch
- Run WinDbg as administrator
- Verify process is not protected

### Commands Not Working
- Check command syntax: `.hh <command>`
- Ensure symbols are loaded
- Verify correct module name

---

## 📖 Quick Reference Legend

| Symbol | Meaning |
|--------|---------|
| `<address>` | Memory address (hex) |
| `<module>` | Module name (e.g., kernel32) |
| `<function>` | Function name |
| `<n>` | Number |
| `<pattern>` | Search pattern or wildcard |
| `<type>` | Data type name |
| `*` | Wildcard |
| `!` | Extension command |
| `.` | Meta-command |

---

## 📚 Additional Resources

- **Official Docs**: https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/
- **WinDbg Commands**: `.hh debugger`
- **Symbol Server**: https://msdl.microsoft.com/download/symbols
- **Debugging Tools**: Windows SDK

---

**Version**: 1.0 | **Last Updated**: December 2024
**For**: OSED Section 2 - WinDbg and x86 Architecture

*Print this cheat sheet for quick reference during labs!*
