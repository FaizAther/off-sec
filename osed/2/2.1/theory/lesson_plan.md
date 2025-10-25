# OSED Section 2.1: Introduction to x86 Architecture

## Learning Objectives
By the end of this section, students will be able to:
- Understand the fundamental concepts of x86 architecture
- Explain program memory layout and organization
- Identify and describe CPU registers and their purposes
- Apply knowledge of x86 architecture to exploit development

## Prerequisites
- Basic understanding of computer architecture
- Familiarity with binary and hexadecimal numbering systems
- Basic knowledge of assembly language concepts

## Duration
- **Theory:** 2 hours
- **Lab:** 1.5 hours
- **Total:** 3.5 hours

## Theory Components

### 2.1.1 Program Memory
**Duration:** 60 minutes

#### Key Topics:
1. **Memory Layout Overview**
   - Virtual memory concepts
   - Memory segmentation
   - Memory pages and frames

2. **Process Memory Structure**
   - Text segment (code)
   - Data segment
   - BSS segment
   - Heap
   - Stack

3. **Memory Addressing**
   - Linear addressing
   - Segmented addressing
   - Physical vs Virtual addresses

4. **Memory Protection**
   - Read/Write/Execute permissions
   - Memory protection mechanisms
   - Segmentation faults

#### Learning Activities:
- Interactive diagrams of memory layout
- Memory mapping exercises
- Address calculation practice

### 2.1.2 CPU Registers
**Duration:** 60 minutes

#### Key Topics:
1. **General Purpose Registers**
   - EAX, EBX, ECX, EDX
   - ESI, EDI, EBP, ESP
   - Register usage conventions

2. **Segment Registers**
   - CS (Code Segment)
   - DS (Data Segment)
   - SS (Stack Segment)
   - ES, FS, GS (Extra Segments)

3. **Control Registers**
   - EIP (Instruction Pointer)
   - EFLAGS (Flags Register)
   - Control register functions

4. **Register Operations**
   - Register-to-register operations
   - Memory-to-register operations
   - Register-to-memory operations

#### Learning Activities:
- Register identification exercises
- Assembly code analysis
- Register manipulation practice

## Lab Components

### Lab 2.1.1: Memory Layout Analysis
**Duration:** 45 minutes

#### Objectives:
- Analyze process memory layout using WinDbg
- Identify different memory segments
- Understand memory organization

#### Tasks:
1. **Setup Environment**
   - Launch a simple C program
   - Attach WinDbg to the process
   - Load debugging symbols

2. **Memory Analysis**
   - Use `!address` command to view memory layout
   - Identify text, data, heap, and stack segments
   - Analyze memory permissions

3. **Address Calculation**
   - Calculate offsets between segments
   - Identify base addresses
   - Document memory layout

#### Deliverables:
- Screenshots of memory layout
- Address calculations worksheet
- Memory segment analysis report

### Lab 2.1.2: Register Analysis
**Duration:** 45 minutes

#### Objectives:
- Examine CPU registers in WinDbg
- Understand register contents and purposes
- Practice register manipulation

#### Tasks:
1. **Register Inspection**
   - Use `r` command to view all registers
   - Analyze register contents
   - Identify register purposes

2. **Register Manipulation**
   - Modify register values
   - Execute instructions step-by-step
   - Observe register changes

3. **Register Analysis**
   - Document register states
   - Analyze register relationships
   - Create register usage map

#### Deliverables:
- Register analysis worksheet
- Register manipulation log
- Step-by-step execution trace

## Assessment

### Theory Assessment (30 minutes)
- Multiple choice questions on memory layout
- Short answer questions on register purposes
- Diagram labeling exercises

### Lab Assessment (30 minutes)
- Practical memory analysis task
- Register identification and manipulation
- Problem-solving scenarios

## Resources

### Required Reading:
- Intel x86 Architecture Manual
- Windows Internals (Memory Management chapter)
- OSED Course Materials Section 2.1

### Recommended Tools:
- WinDbg (Windows Debugger)
- Process Monitor
- Memory analysis tools

### Additional Resources:
- x86 Assembly tutorials
- Memory management documentation
- CPU architecture references

## Next Steps
Upon completion of this section, students will proceed to:
- **Section 2.2:** Introduction to Windows Debugger
- **Section 2.3:** Accessing and Manipulating Memory from WinDbg

## Notes for Instructors
- Emphasize practical application of theoretical concepts
- Use visual aids for memory layout explanations
- Provide hands-on exercises for register manipulation
- Encourage students to experiment with different scenarios
- Connect concepts to exploit development applications
