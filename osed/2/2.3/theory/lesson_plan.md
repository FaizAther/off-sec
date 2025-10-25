# OSED Section 2.3: Accessing and Manipulating Memory from WinDbg

## Learning Objectives
By the end of this section, students will be able to:
- Unassemble code from memory locations
- Read and interpret memory contents
- Dump structures from memory
- Write data to memory locations
- Search memory space effectively
- Inspect and edit CPU registers
- Apply memory manipulation techniques to exploit development

## Prerequisites
- Completion of Section 2.1 (x86 Architecture)
- Completion of Section 2.2 (Windows Debugger)
- Basic understanding of assembly language
- Familiarity with memory addressing

## Duration
- **Theory:** 3 hours
- **Lab:** 2.5 hours
- **Total:** 5.5 hours

## Theory Components

### 2.3.1 Unassemble from Memory
**Duration:** 45 minutes

#### Key Topics:
1. **Disassembly Concepts**
   - What is disassembly
   - Machine code to assembly translation
   - Instruction decoding
   - Address resolution

2. **WinDbg Disassembly Commands**
   - `u` command (unassemble)
   - `uf` command (unassemble function)
   - `ub` command (unassemble backward)
   - `uu` command (unassemble with symbols)

3. **Disassembly Options**
   - Address specification
   - Length parameters
   - Symbol resolution
   - Output formatting

4. **Practical Applications**
   - Code analysis
   - Exploit development
   - Reverse engineering
   - Vulnerability research

#### Learning Activities:
- Disassembly practice exercises
- Code analysis tasks
- Instruction identification

### 2.3.2 Reading from Memory
**Duration:** 45 minutes

#### Key Topics:
1. **Memory Reading Concepts**
   - Memory access methods
   - Data interpretation
   - Endianness considerations
   - Memory alignment

2. **WinDbg Memory Commands**
   - `d` command (dump)
   - `db` command (dump bytes)
   - `dw` command (dump words)
   - `dd` command (dump dwords)
   - `dq` command (dump qwords)

3. **Memory Formats**
   - Hexadecimal display
   - ASCII representation
   - Unicode display
   - Custom formats

4. **Memory Analysis**
   - Pattern recognition
   - Data structure identification
   - Memory corruption detection
   - Exploit payload analysis

#### Learning Activities:
- Memory reading exercises
- Data interpretation practice
- Format analysis tasks

### 2.3.3 Dumping Structures from Memory
**Duration:** 45 minutes

#### Key Topics:
1. **Structure Concepts**
   - Data structure layout
   - Memory organization
   - Field alignment
   - Padding considerations

2. **Structure Dumping Commands**
   - `dt` command (dump type)
   - `dps` command (dump pointers)
   - `dpp` command (dump process pointers)
   - `dppp` command (dump process pointers with symbols)

3. **Structure Analysis**
   - Field identification
   - Size calculation
   - Offset determination
   - Type information

4. **Practical Applications**
   - Vulnerability analysis
   - Exploit development
   - Memory corruption research
   - Reverse engineering

#### Learning Activities:
- Structure analysis exercises
- Field identification tasks
- Memory layout analysis

### 2.3.4 Writing to Memory
**Duration:** 45 minutes

#### Key Topics:
1. **Memory Writing Concepts**
   - Memory modification
   - Data validation
   - Permission requirements
   - Safety considerations

2. **WinDbg Memory Commands**
   - `e` command (edit)
   - `eb` command (edit bytes)
   - `ew` command (edit words)
   - `ed` command (edit dwords)
   - `eq` command (edit qwords)

3. **Memory Writing Techniques**
   - Direct memory modification
   - Register-based writing
   - Pointer manipulation
   - Buffer overflow simulation

4. **Exploit Development Applications**
   - Payload injection
   - Return address modification
   - Function pointer manipulation
   - Memory corruption exploitation

#### Learning Activities:
- Memory writing exercises
- Payload injection practice
- Exploit simulation tasks

### 2.3.5 Searching the Memory Space
**Duration:** 30 minutes

#### Key Topics:
1. **Memory Search Concepts**
   - Pattern matching
   - Search algorithms
   - Memory scanning
   - Data location

2. **WinDbg Search Commands**
   - `s` command (search)
   - `s-` command (search backward)
   - `s+` command (search forward)
   - `s-a` command (search ASCII)

3. **Search Applications**
   - Exploit payload location
   - Shellcode detection
   - Pattern identification
   - Memory analysis

#### Learning Activities:
- Memory search exercises
- Pattern matching practice
- Data location tasks

### 2.3.6 Inspecting and Editing CPU Registers
**Duration:** 30 minutes

#### Key Topics:
1. **Register Concepts**
   - Register purposes
   - Register relationships
   - Register modification
   - Register analysis

2. **WinDbg Register Commands**
   - `r` command (registers)
   - `r <register>=<value>` (register modification)
   - `r <register>` (single register)
   - `r <register>=<value>` (register assignment)

3. **Register Applications**
   - Exploit development
   - Code execution control
   - Memory manipulation
   - Debugging techniques

#### Learning Activities:
- Register inspection exercises
- Register modification practice
- Execution control tasks

## Lab Components

### Lab 2.3.1: Memory Analysis and Disassembly
**Duration:** 60 minutes

#### Objectives:
- Practice memory reading and disassembly
- Analyze code structures
- Understand memory layout

#### Tasks:
1. **Memory Reading**
   - Read different memory regions
   - Interpret memory contents
   - Analyze data patterns

2. **Code Disassembly**
   - Disassemble functions
   - Analyze instruction sequences
   - Identify control flow

3. **Structure Analysis**
   - Dump data structures
   - Analyze field layouts
   - Calculate offsets

#### Deliverables:
- Memory analysis report
- Disassembly documentation
- Structure analysis worksheet

### Lab 2.3.2: Memory Manipulation and Search
**Duration:** 90 minutes

#### Objectives:
- Practice memory writing techniques
- Search memory space
- Manipulate registers

#### Tasks:
1. **Memory Writing**
   - Modify memory contents
   - Inject payloads
   - Simulate exploits

2. **Memory Search**
   - Search for patterns
   - Locate data structures
   - Find exploit payloads

3. **Register Manipulation**
   - Inspect register states
   - Modify register values
   - Control execution flow

#### Deliverables:
- Memory manipulation log
- Search results documentation
- Register analysis report

## Assessment

### Theory Assessment (60 minutes)
- Multiple choice questions on memory operations
- Practical exercises on disassembly
- Memory analysis tasks

### Lab Assessment (60 minutes)
- Memory reading and analysis
- Disassembly and structure analysis
- Memory manipulation and search

## Resources

### Required Reading:
- WinDbg Memory Commands Reference
- x86 Assembly Language Guide
- OSED Course Materials Section 2.3

### Recommended Tools:
- WinDbg Preview
- Hex editors
- Memory analysis tools

### Additional Resources:
- Assembly language tutorials
- Memory management guides
- Exploit development references

## Next Steps
Upon completion of this section, students will proceed to:
- **Section 2.4:** Controlling the Program Execution in WinDbg
- **Section 2.5:** Additional WinDbg Features

## Notes for Instructors
- Emphasize practical memory manipulation
- Provide real-world exploit scenarios
- Encourage hands-on experimentation
- Connect memory operations to exploit development
- Use progressive difficulty levels
