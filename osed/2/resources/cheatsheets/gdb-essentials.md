# GDB Essentials Cheat Sheet

## Quick Reference for OSED Section 2

---

## 🚀 Getting Started

### Launch & Exit
```bash
gdb <program>                  # Debug program
gdb <program> <core>           # Debug core dump
gdb -p <pid>                   # Attach to process
gdb --args <program> <args>    # Debug with arguments

quit                           # Exit GDB
q                              # Exit GDB (short)
Ctrl+d                         # Exit GDB
```

### Help & Information
```gdb
help                           # General help
help <command>                 # Help for specific command
info                           # Show information
show                           # Show GDB settings
set                            # Set GDB settings
```

---

## 🎯 Breakpoints

### Setting Breakpoints
```gdb
break <function>               # Break at function
break <file>:<line>            # Break at line in file
break <address>                # Break at address
break *<address>               # Break at address (explicit)
break <line>                   # Break at line number
break +<offset>                # Break at offset from current
break -<offset>                # Break at offset before current
```

### Breakpoint Management
```gdb
info breakpoints               # List breakpoints
info break                     # List breakpoints (short)
delete <num>                   # Delete breakpoint
delete                         # Delete all breakpoints
disable <num>                  # Disable breakpoint
enable <num>                   # Enable breakpoint
clear <function>               # Clear breakpoint at function
clear <file>:<line>            # Clear breakpoint at line
```

### Conditional Breakpoints
```gdb
break <location> if <condition> # Conditional breakpoint
condition <num> <condition>     # Add condition to breakpoint
condition <num>                 # Remove condition from breakpoint
```

### Watchpoints
```gdb
watch <variable>               # Watch variable
watch *<address>               # Watch memory address
rwatch <variable>              # Watch for read access
awatch <variable>              # Watch for read/write access
info watchpoints               # List watchpoints
```

---

## 🏃 Execution Control

### Basic Execution
```gdb
run                            # Start program
run <args>                     # Start with arguments
start                          # Start and stop at main
continue                       # Continue execution
c                              # Continue (short)
step                           # Step into (next line)
s                              # Step into (short)
next                           # Step over (next line)
n                              # Step over (short)
finish                         # Step out of function
```

### Advanced Stepping
```gdb
stepi                          # Step one instruction
si                             # Step one instruction (short)
nexti                          # Next instruction
ni                             # Next instruction (short)
until                          # Continue until current function returns
until <line>                   # Continue until line
advance <line>                 # Advance to line
advance <function>             # Advance to function
```

### Execution Control
```gdb
kill                           # Kill program
interrupt                      # Interrupt program
Ctrl+c                         # Interrupt program
signal <signal>                # Send signal to program
```

---

## 🔍 Examining Data

### Variables & Memory
```gdb
print <variable>               # Print variable
p <variable>                   # Print variable (short)
print <expression>             # Print expression
x/<format> <address>           # Examine memory
x/<count><format> <address>    # Examine memory (count)
x/<count><format><size> <address> # Examine memory (size)
```

### Memory Formats
```gdb
x/10x <address>                # 10 hex values
x/10d <address>                # 10 decimal values
x/10u <address>                # 10 unsigned values
x/10o <address>                # 10 octal values
x/10t <address>                # 10 binary values
x/10c <address>                # 10 characters
x/10s <address>                # 10 strings
x/10i <address>                # 10 instructions
```

### Data Types
```gdb
print/x <variable>             # Print in hex
print/d <variable>             # Print in decimal
print/o <variable>             # Print in octal
print/t <variable>             # Print in binary
print/c <variable>             # Print as character
print/s <variable>             # Print as string
```

### Arrays & Structures
```gdb
print <array>[<index>]         # Print array element
print <array>[<start>:<end>]   # Print array range
print *<pointer>               # Print pointed value
print <struct>.<field>         # Print struct field
print <struct>-><field>        # Print struct field via pointer
```

---

## 📚 Stack & Functions

### Stack Operations
```gdb
backtrace                      # Show call stack
bt                             # Show call stack (short)
bt <num>                       # Show <num> frames
frame <num>                    # Switch to frame
up                             # Move up stack
down                           # Move down stack
info frame                     # Show current frame info
info registers                 # Show registers
```

### Function Information
```gdb
info functions                 # List functions
info functions <pattern>       # List functions matching pattern
info variables                 # List variables
info variables <pattern>       # List variables matching pattern
info locals                    # Show local variables
info args                      # Show function arguments
```

### Function Calls
```gdb
call <function>(<args>)        # Call function
print <function>(<args>)       # Call function and print result
```

---

## 🔧 Disassembly

### Disassembly Commands
```gdb
disassemble                    # Disassemble current function
disassemble <function>         # Disassemble function
disassemble <start>,<end>      # Disassemble range
disassemble <start> <end>      # Disassemble range
x/<count>i <address>           # Disassemble instructions
```

### Assembly Control
```gdb
set disassembly-flavor intel   # Intel syntax
set disassembly-flavor att     # AT&T syntax
show disassembly-flavor        # Show current syntax
```

---

## 📝 Source Code

### Source Operations
```gdb
list                           # List source code
list <line>                    # List around line
list <function>                # List function
list <start>,<end>             # List range
list +<offset>                 # List from current + offset
list -<offset>                 # List from current - offset
```

### Source Information
```gdb
info source                    # Show source file info
info sources                   # List source files
info line <line>               # Show line info
info line <function>           # Show function line info
```

---

## 🎯 Threads & Processes

### Thread Operations
```gdb
info threads                   # List threads
thread <num>                   # Switch to thread
thread apply <num> <command>   # Apply command to thread
thread apply all <command>     # Apply command to all threads
```

### Process Operations
```gdb
info proc                      # Show process info
info proc mappings            # Show memory mappings
attach <pid>                   # Attach to process
detach                         # Detach from process
```

---

## ⚙️ Configuration

### Essential Settings
```gdb
set print pretty on            # Pretty print structures
set print array on             # Print arrays nicely
set print array-indexes on     # Show array indexes
set print null-stop on         # Stop at null characters
set print repeats 0            # Don't print repeated values
set print elements 0           # Print all elements
set print max-depth 0          # Print all structure depth
```

### History & Completion
```gdb
set history save on            # Save command history
set history size <num>         # Set history size
set history filename <file>     # Set history file
set auto-solib-add on          # Auto-load shared libraries
set confirm off                # Don't confirm dangerous operations
```

### Display Settings
```gdb
set disassembly-flavor intel   # Intel assembly syntax
set architecture i386           # Set architecture
set endian little              # Set endianness
set endian big                 # Set endianness
```

---

## 🎬 Advanced Features

### Commands & Macros
```gdb
define <name>                  # Define command macro
  <commands>
end                            # End macro definition
document <name>                # Document macro
  <help text>
end                            # End documentation
```

### Logging
```gdb
set logging on                 # Enable logging
set logging file <file>        # Set log file
set logging off                # Disable logging
```

### Remote Debugging
```gdb
target remote <host>:<port>    # Connect to remote target
target extended-remote <host>:<port> # Extended remote
monitor <command>              # Send monitor command
```

---

## 🎯 Practical Examples

### Basic Debugging Session
```gdb
# Start debugging
gdb ./program

# Set breakpoint
(gdb) break main

# Run program
(gdb) run

# Step through code
(gdb) next
(gdb) step

# Examine variables
(gdb) print variable
(gdb) print/x variable

# Continue execution
(gdb) continue
```

### Memory Analysis
```gdb
# Examine memory
(gdb) x/10x 0x8048000
(gdb) x/10s 0x8048000
(gdb) x/10i 0x8048000

# Watch memory
(gdb) watch *0x8048000
(gdb) rwatch *0x8048000
```

### Function Analysis
```gdb
# List functions
(gdb) info functions
(gdb) info functions main

# Disassemble function
(gdb) disassemble main
(gdb) disassemble 0x8048000,0x8048100

# Call function
(gdb) call function(1, 2, 3)
(gdb) print function(1, 2, 3)
```

---

## 🔑 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Enter | Repeat last command |
| Ctrl+c | Interrupt program |
| Ctrl+d | Exit GDB |
| Tab | Command completion |
| Up/Down | Command history |
| Ctrl+r | Reverse search |
| Ctrl+s | Forward search |

---

## 💡 Pro Tips

1. **Use command completion**: Tab for completion
2. **Use command history**: Up/Down arrows
3. **Use abbreviations**: `p` for `print`, `c` for `continue`
4. **Use expressions**: `print variable + 1`
5. **Use convenience variables**: `set $var = expression`
6. **Use display**: `display variable` for automatic display
7. **Use conditional breakpoints**: `break if condition`
8. **Use watchpoints**: `watch variable`
9. **Use reverse debugging**: `reverse-step`, `reverse-next`
10. **Use Python scripting**: `python` for advanced scripting

---

## 🔧 Troubleshooting

### Common Issues
- **Program not found**: Check path and permissions
- **No debugging symbols**: Compile with `-g`
- **Can't set breakpoint**: Check if function exists
- **Program crashes**: Use `run` to restart

### Debugging Tips
```gdb
# Check if symbols are loaded
(gdb) info functions

# Check if source is available
(gdb) info source

# Check if program is running
(gdb) info proc

# Check if threads exist
(gdb) info threads
```

---

## 📚 Additional Resources

- **GDB Manual**: https://www.gnu.org/software/gdb/documentation/
- **GDB Tutorial**: https://www.gnu.org/software/gdb/documentation/gdb.html
- **GDB Cheat Sheet**: https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf
- **GDB Python API**: https://sourceware.org/gdb/onlinedocs/gdb/Python-API.html

---

**Version**: 1.0 | **Last Updated**: December 2024
**For**: OSED Section 2 - Linux Debugging and Analysis

*Print this cheat sheet for quick reference during labs!*
