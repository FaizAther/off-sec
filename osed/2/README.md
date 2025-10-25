# OSED Section 2: WinDbg and x86 Architecture

## Overview
This section provides comprehensive coverage of Windows debugging fundamentals and x86 architecture concepts essential for exploit development. Students will learn to use WinDbg effectively for analyzing programs, manipulating memory, and controlling execution flow.

## Learning Objectives
By the end of this section, students will be able to:
- Understand x86 architecture fundamentals
- Navigate and use WinDbg effectively
- Manipulate memory and analyze data structures
- Control program execution with breakpoints
- Utilize advanced WinDbg features
- Apply debugging skills to exploit development

## Prerequisites
- Basic understanding of computer architecture
- Familiarity with binary and hexadecimal numbering systems
- Basic knowledge of assembly language concepts
- Windows operating system experience

## Section Structure

### [2.1 Introduction to x86 Architecture](2.1/)
**Duration:** 3.5 hours (Theory: 2h, Lab: 1.5h)

**Topics:**
- Program Memory Layout
- CPU Registers
- Memory Addressing
- Memory Protection

**Lab Focus:**
- Memory Layout Analysis
- Register Analysis
- Address Calculations

[📖 Theory Guide](./2.1/theory/lesson_plan.md) | [🔬 Lab Guide](./2.1/lab/lab_guide.md)

---

### [2.2 Introduction to Windows Debugger](2.2/)
**Duration:** 4.5 hours (Theory: 2.5h, Lab: 2h)

**Topics:**
- What is a Debugger?
- WinDbg Interface
- Understanding the Workspace
- Debugging Symbols

**Lab Focus:**
- Interface Exploration
- Symbol Management
- Process Analysis

[📖 Theory Guide](./2.2/theory/lesson_plan.md) | [🔬 Lab Guide](./2.2/lab/lab_guide.md)

---

### [2.3 Accessing and Manipulating Memory from WinDbg](2.3/)
**Duration:** 5.5 hours (Theory: 3h, Lab: 2.5h)

**Topics:**
- Unassemble from Memory
- Reading from Memory
- Dumping Structures from Memory
- Writing to Memory
- Searching the Memory Space
- Inspecting and Editing CPU Registers

**Lab Focus:**
- Memory Analysis and Disassembly
- Structure Analysis
- Memory Manipulation and Search
- Register Manipulation

[📖 Theory Guide](./2.3/theory/lesson_plan.md) | [🔬 Lab Guide](./2.3/lab/lab_guide.md)

---

### [2.4 Controlling the Program Execution in WinDbg](2.4/)
**Duration:** 4.5 hours (Theory: 2.5h, Lab: 2h)

**Topics:**
- Software Breakpoints
- Unresolved Function Breakpoint
- Breakpoint-Based Actions
- Hardware Breakpoints
- Stepping Through the Code

**Lab Focus:**
- Breakpoint Management and Control
- Hardware Breakpoints and Code Stepping
- Execution Control

[📖 Theory Guide](./2.4/theory/lesson_plan.md) | [🔬 Lab Guide](./2.4/lab/lab_guide.md)

---

### [2.5 Additional WinDbg Features](2.5/)
**Duration:** 3.5 hours (Theory: 2h, Lab: 1.5h)

**Topics:**
- Listing Modules and Symbols in WinDbg
- Using WinDbg as a Calculator
- Data Output Format
- Pseudo Registers

**Lab Focus:**
- Module and Symbol Analysis
- Calculator and Format Features
- Advanced WinDbg Utilities

[📖 Theory Guide](./2.5/theory/lesson_plan.md) | [🔬 Lab Guide](./2.5/lab/lab_guide.md)

---

### [2.6 Wrapping Up](2.6/)
**Duration:** 2 hours (Theory: 1h, Lab: 1h)

**Topics:**
- Section 2 Review and Consolidation
- Skill Integration
- Preparation for Advanced Topics

**Lab Focus:**
- Comprehensive Debugging Challenge
- Skill Demonstration
- Practical Application Assessment

[📖 Theory Guide](./2.6/theory/lesson_plan.md) | [🔬 Lab Guide](./2.6/lab/lab_guide.md)

---

## Total Section Duration
**23 hours** (Theory: 13h, Lab: 10h)

## Required Tools and Software
- Windows 10/11 (64-bit)
- WinDbg Preview
- Visual Studio or MinGW for C compilation
- Sample C programs for analysis

## Assessment Overview
Each subsection includes:
- **Theory Assessment:** Multiple choice questions, practical exercises, and analysis tasks
- **Lab Assessment:** Hands-on debugging challenges and skill demonstrations
- **Deliverables:** Reports, worksheets, and documentation

## Learning Path
1. **Start with 2.1** - Build foundational x86 architecture knowledge
2. **Progress through 2.2-2.5** - Develop WinDbg proficiency
3. **Complete with 2.6** - Integrate all skills through comprehensive challenges

## Next Steps
Upon completion of Section 2, students will proceed to:
- **Section 3:** Exploiting Stack Overflows
- **Advanced exploit development topics**

## Additional Resources
- [WinDbg Documentation](https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/)
- [Intel x86 Architecture Manual](https://software.intel.com/content/www/us/en/develop/articles/intel-sdm.html)
- [Windows Internals Book](https://docs.microsoft.com/en-us/sysinternals/resources/windows-internals)
- [OSED Course Materials](../../OSED.md)

## Support and Help
- Review theory materials before attempting labs
- Practice with additional programs beyond provided samples
- Use troubleshooting guides for common issues
- Seek help when encountering difficulties

---

*This section forms the foundation for all subsequent exploit development topics in the OSED course.*
