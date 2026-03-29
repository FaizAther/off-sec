# OSED Section 2.1: Assembly Language Labs Guide

## Overview

This directory contains comprehensive assembly language labs designed to teach x86 assembly from basics to advanced topics. These labs complement the x86 architecture theory and provide hands-on practice essential for exploit development.

---

## Lab Structure

### Assembly Beginner Lab (`assembly_beginner_lab.md`)
- **Duration:** 4-5 hours
- **Difficulty:** Beginner
- **Prerequisites:** Basic understanding of x86 architecture
- **Topics Covered:**
  - Understanding assembly basics
  - Register operations
  - Memory operations
  - Arithmetic operations
  - Control flow (jumps, loops)
  - Function calls

### Assembly Intermediate Lab (`assembly_intermediate_lab.md`)
- **Duration:** 5-6 hours
- **Difficulty:** Intermediate
- **Prerequisites:** Completion of Assembly Beginner Lab
- **Topics Covered:**
  - Advanced instructions (LEA, XCHG, etc.)
  - String operations
  - Stack manipulation
  - Calling conventions (__cdecl, __stdcall, __fastcall)
  - Bitwise operations
  - Advanced control flow

---

## Learning Path

### Recommended Sequence

1. **Start Here:** Assembly Beginner Lab
   - Complete all 6 exercises
   - Understand each concept before moving on
   - Practice with variations

2. **Next:** Assembly Intermediate Lab
   - Build on beginner knowledge
   - Focus on calling conventions (critical for exploit dev)
   - Master stack operations

3. **Practice:** Analyze real code
   - Use WinDbg to disassemble C programs
   - Compare your understanding with compiler output
   - Study vulnerable code

4. **Apply:** Use in exploit development
   - Understand shellcode
   - Analyze ROP gadgets
   - Write custom assembly payloads

---

## How to Use These Labs

### Step 1: Preparation
1. **Read Theory:** Review x86 architecture theory first
2. **Set Up Environment:** Install WinDbg, compiler, text editor
3. **Create Workspace:** Set up directory for assembly programs

### Step 2: Follow Step-by-Step Instructions
- **Don't skip steps** - each builds on previous
- **Type commands yourself** - don't copy-paste blindly
- **Understand before moving on** - if confused, review

### Step 3: Practice and Experiment
- **Modify examples** - change values, try variations
- **Break things** - see what happens with wrong code
- **Ask why** - understand the reasoning behind each instruction

### Step 4: Document Your Learning
- **Take notes** - record key concepts
- **Screenshot WinDbg** - capture important outputs
- **Create cheat sheets** - build your own reference

---

## Lab Environment Setup

### Required Software

1. **Windows 10/11** (64-bit)
   - Tested on Windows 10
   - Can use Windows 11

2. **WinDbg Preview**
   - Download from Microsoft Store
   - Latest version recommended

3. **C Compiler**
   - **Option 1:** MinGW-w64 (recommended)
     ```bash
     gcc -m32 -g -o program.exe program.c
     ```
   - **Option 2:** Visual Studio
     ```bash
     cl /Zi /GS- program.c
     ```

4. **Text Editor**
   - Notepad++
   - VS Code
   - Any editor you prefer

### Compilation Settings

**For 32-bit (x86) Assembly:**
```bash
gcc -m32 -g -fno-stack-protector -z execstack -o program.exe program.c
```

**Flags Explained:**
- `-m32`: Compile for 32-bit architecture
- `-g`: Include debugging information
- `-fno-stack-protector`: Disable stack canary (for learning)
- `-z execstack`: Allow executable stack (for learning)

---

## Key Concepts by Lab

### Beginner Lab Concepts

#### Exercise 1: Assembly Basics
- **MOV instruction:** Data movement
- **Immediate values:** Constants in instructions
- **Register usage:** EAX, EBX, ECX, EDX

#### Exercise 2: Register Operations
- **Register-to-register:** Copying between registers
- **Immediate values:** Loading constants
- **Register arithmetic:** ADD, SUB operations

#### Exercise 3: Memory Operations
- **Reading from memory:** Loading variables
- **Writing to memory:** Storing values
- **Addressing modes:** Direct, indirect, indexed

#### Exercise 4: Arithmetic Operations
- **ADD/SUB:** Addition and subtraction
- **MUL/DIV:** Multiplication and division
- **INC/DEC:** Increment and decrement

#### Exercise 5: Control Flow
- **Conditional jumps:** JE, JNE, JG, JL
- **CMP instruction:** Comparison
- **Loops:** LOOP instruction

#### Exercise 6: Function Calls
- **Stack frames:** EBP, ESP usage
- **Parameters:** Accessing function arguments
- **Return values:** EAX register

### Intermediate Lab Concepts

#### Exercise 1: Advanced Instructions
- **LEA:** Load effective address
- **XCHG:** Exchange values
- **NOT/NEG:** Bitwise and arithmetic negation

#### Exercise 2: String Operations
- **MOVS:** Move string
- **CMPS:** Compare strings
- **REP prefix:** Repeat instructions

#### Exercise 3: Stack Operations
- **PUSH/POP:** Stack manipulation
- **Stack frames:** Function prologue/epilogue
- **Stack layout:** Parameter and local variable access

#### Exercise 4: Calling Conventions
- **__cdecl:** Caller cleans stack
- **__stdcall:** Callee cleans stack
- **__fastcall:** Parameters in registers

#### Exercise 5: Bitwise Operations
- **AND/OR/XOR:** Logical operations
- **SHL/SHR:** Logical shifts
- **SAL/SAR:** Arithmetic shifts

#### Exercise 6: Advanced Control Flow
- **Switch statements:** Jump tables
- **Complex conditionals:** Multiple comparisons

---

## Common Patterns and Techniques

### Pattern 1: Function Prologue
```assembly
push ebp        ; Save old base pointer
mov ebp, esp    ; Set new base pointer
sub esp, N      ; Allocate space for locals
```

### Pattern 2: Function Epilogue
```assembly
mov esp, ebp    ; Restore stack pointer
pop ebp         ; Restore old base pointer
ret             ; Return
```

### Pattern 3: Parameter Access
```assembly
mov eax, [ebp+8]   ; First parameter
mov ebx, [ebp+12]  ; Second parameter
```

### Pattern 4: Local Variable Access
```assembly
mov [ebp-4], eax   ; Store in local variable
mov eax, [ebp-4]   ; Load from local variable
```

### Pattern 5: Loop Structure
```assembly
mov ecx, N         ; Loop counter
loop_start:
    ; Loop body
    loop loop_start ; Decrement ECX, jump if not zero
```

---

## Troubleshooting Guide

### Issue 1: Compilation Errors

**Error:** "undefined reference to `__main'"
- **Solution:** Ensure you're using `-m32` flag for 32-bit compilation

**Error:** Inline assembly syntax errors
- **Solution:** Check compiler documentation for inline assembly syntax
- **Solution:** Try using `__asm__` instead of `__asm` (GCC)

### Issue 2: Program Crashes

**Symptom:** Access violation
- **Solution:** Check memory addresses are valid
- **Solution:** Verify stack is balanced (push/pop match)

**Symptom:** Wrong results
- **Solution:** Verify register values in WinDbg
- **Solution:** Check addressing modes are correct

### Issue 3: WinDbg Issues

**Issue:** Can't see assembly code
- **Solution:** Load symbols with `.reload`
- **Solution:** Use `u` command to disassemble

**Issue:** Breakpoints not working
- **Solution:** Ensure symbols are loaded
- **Solution:** Use full function name: `bp program!function_name`

---

## Practice Exercises

### Beginner Practice

1. **Modify Examples:**
   - Change values in arithmetic operations
   - Try different register combinations
   - Experiment with addressing modes

2. **Create Your Own:**
   - Write a program that swaps two variables
   - Implement a simple loop that counts to 10
   - Create a function that multiplies two numbers

3. **Analyze Real Code:**
   - Compile simple C programs
   - Disassemble in WinDbg
   - Compare with your understanding

### Intermediate Practice

1. **Calling Conventions:**
   - Write functions using each calling convention
   - Compare stack layouts
   - Understand when each is used

2. **String Operations:**
   - Implement string copy function
   - Write string comparison function
   - Create string length function

3. **Stack Manipulation:**
   - Practice function prologue/epilogue
   - Understand parameter passing
   - Master local variable access

---

## Assessment Checklist

### Beginner Level
- [ ] Can read basic assembly instructions
- [ ] Understands register operations
- [ ] Can perform memory operations
- [ ] Understands arithmetic operations
- [ ] Can follow control flow
- [ ] Understands basic function calls

### Intermediate Level
- [ ] Masters advanced instructions
- [ ] Can perform string operations
- [ ] Understands stack manipulation
- [ ] Knows different calling conventions
- [ ] Can perform bitwise operations
- [ ] Understands advanced control flow

---

## Additional Resources

### Documentation
- **Intel x86 Manual:** https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
- **x86 Assembly Cheat Sheet:** `../resources/cheatsheets/x86-assembly.md`
- **WinDbg Documentation:** https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/

### Online Tools
- **Online Assembler:** https://defuse.ca/online-x86-assembler.htm
- **Compiler Explorer:** https://godbolt.org/ (see C code compiled to assembly)

### Books
- **"The Art of Assembly Language"** by Randall Hyde
- **"Programming from the Ground Up"** by Jonathan Bartlett
- **"Assembly Language Step-by-Step"** by Jeff Duntemann

---

## Integration with OSED Course

### Section 2.1: x86 Architecture
- **Theory:** Learn architecture concepts
- **Assembly Labs:** Practice with assembly code
- **WinDbg Labs:** Analyze programs in debugger

### Section 2.2: Windows Debugger
- **Use assembly knowledge** to understand disassembly
- **Analyze stack frames** in WinDbg
- **Trace execution** through assembly code

### Section 3+: Exploit Development
- **Understand shellcode** (assembly code)
- **Analyze ROP gadgets** (assembly snippets)
- **Write custom exploits** using assembly knowledge

---

## Tips for Success

1. **Start Simple:** Don't try to learn everything at once
2. **Practice Regularly:** Daily practice beats cramming
3. **Use WinDbg:** Visual learning helps understanding
4. **Experiment:** Break things to learn how they work
5. **Document:** Take notes and create cheat sheets
6. **Ask Questions:** Don't hesitate to seek help
7. **Review:** Regularly review previous concepts
8. **Apply:** Use knowledge in real scenarios

---

## Next Steps

After completing assembly labs:
1. **Review:** Ensure you understand all concepts
2. **Practice:** Work with real-world code
3. **Extend:** Learn more advanced topics
4. **Apply:** Use in exploit development
5. **Teach:** Explain to others (reinforces learning)

---

**Remember:** Assembly language is the foundation of exploit development. Master these concepts, and you'll have a solid foundation for the rest of the OSED course!

---

**Good luck with your assembly learning journey!**


