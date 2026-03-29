# OSED Section 2.1 Lab Structure Guide

## Overview

This directory contains comprehensive lab materials for **Section 2.1: Introduction to x86 Architecture**. The labs are organized by difficulty level and provide detailed step-by-step instructions for hands-on learning.

---

## Lab Organization

### Lab Difficulty Levels

1. **Beginner Lab** (`lab_guide.md`)
   - **Target Audience:** Students new to x86 architecture and WinDbg
   - **Duration:** 3.5 hours
   - **Focus:** Basic memory layout analysis, register examination
   - **Prerequisites:** Basic understanding of Windows processes

2. **Assembly Beginner Lab** (`assembly_beginner_lab.md`)
   - **Target Audience:** Students learning x86 assembly language
   - **Duration:** 4-5 hours
   - **Focus:** Assembly basics, register operations, memory operations, control flow
   - **Prerequisites:** Basic understanding of x86 architecture

3. **Intermediate Lab** (`intermediate/lab_guide.md`)
   - **Target Audience:** Students with basic x86 knowledge
   - **Duration:** 4-5 hours
   - **Focus:** Multi-threaded analysis, complex data structures
   - **Prerequisites:** Completion of beginner lab

4. **Assembly Intermediate Lab** (`assembly_intermediate_lab.md`)
   - **Target Audience:** Students with basic assembly knowledge
   - **Duration:** 5-6 hours
   - **Focus:** Advanced instructions, string operations, calling conventions
   - **Prerequisites:** Completion of assembly beginner lab

5. **Consolidated Advanced/Expert Lab** (`consolidated_advanced_lab.md`)
   - **Target Audience:** Students ready for exploit development
   - **Duration:** 8-10 hours
   - **Focus:** Exploit development, mitigation bypass, multi-vector exploitation
   - **Prerequisites:** Completion of beginner and intermediate labs

---

## Recommended Learning Path

### Path 1: Complete Beginner Path
1. Start with **Beginner Lab** (`lab_guide.md`)
2. Complete **Assembly Beginner Lab** (`assembly_beginner_lab.md`)
3. Complete all exercises thoroughly
4. Review theory materials
5. Move to Intermediate Lab when comfortable

### Path 2: Accelerated Path (For Experienced Students)
1. Review Beginner Lab concepts quickly
2. Complete Assembly Beginner Lab
3. Complete Intermediate Lab
4. Complete Assembly Intermediate Lab
5. Focus on Consolidated Advanced/Expert Lab
6. Practice with real-world scenarios

### Path 3: Expert Path (For Advanced Students)
1. Review Beginner/Intermediate concepts
2. Review Assembly labs for reference
3. Focus entirely on Consolidated Advanced/Expert Lab
4. Extend exercises with custom challenges
5. Research real-world vulnerabilities

### Path 4: Assembly-Focused Path (For Assembly Learners)
1. Complete **Assembly Beginner Lab** first
2. Complete **Assembly Intermediate Lab**
3. Complete **Beginner Lab** (applies assembly knowledge)
4. Complete **Intermediate Lab**
5. Move to advanced topics

---

## Lab Files Structure

```
osed/2/2.1/lab/
├── README.md                          # This file
├── lab_guide.md                       # Beginner lab (detailed step-by-step)
├── assembly_beginner_lab.md           # Assembly beginner lab
├── assembly_intermediate_lab.md        # Assembly intermediate lab
├── assembly_labs_README.md            # Assembly labs guide
├── intermediate/
│   └── lab_guide.md                   # Intermediate lab
├── advanced/
│   └── lab_guide.md                   # Original advanced lab (reference)
├── expert/
│   └── lab_guide.md                   # Original expert lab (reference)
└── consolidated_advanced_lab.md       # Combined advanced/expert lab
```

---

## How to Use These Labs

### Step 1: Preparation
1. **Read the Theory:** Review `../theory/theory.md` before starting labs
2. **Set Up Environment:** Ensure WinDbg, compiler, and tools are installed
3. **Create Workspace:** Set up a dedicated directory for lab work

### Step 2: Choose Your Lab
- **New to x86?** → Start with `lab_guide.md`
- **Have some experience?** → Start with `intermediate/lab_guide.md`
- **Ready for exploitation?** → Start with `consolidated_advanced_lab.md`

### Step 3: Follow Step-by-Step Instructions
- Each lab provides **detailed step-by-step instructions**
- **Don't skip steps** - each builds on the previous
- **Document everything** - take notes, screenshots, save outputs
- **Experiment** - try variations and modifications

### Step 4: Complete Deliverables
- Each lab has specific deliverables
- Create reports documenting your findings
- Save exploit code and scripts
- Build a portfolio of your work

### Step 5: Review and Practice
- Review concepts you found difficult
- Practice with variations of the exercises
- Research related topics
- Prepare for next section

---

## Lab Features

### Beginner Lab Features
- ✅ **Extremely detailed step-by-step instructions**
- ✅ **Clear explanations of each command**
- ✅ **Expected outputs for verification**
- ✅ **Troubleshooting section**
- ✅ **Assessment criteria**

### Intermediate Lab Features
- ✅ **Multi-threaded analysis**
- ✅ **Complex data structure analysis**
- ✅ **Advanced register manipulation**
- ✅ **Real-world application scenarios**

### Consolidated Advanced/Expert Lab Features
- ✅ **Topic-based organization** (5 major topics)
- ✅ **Complete exploit development workflow**
- ✅ **Multi-vector exploitation techniques**
- ✅ **Mitigation bypass introduction**
- ✅ **Real-world vulnerability patterns**

---

## Key Learning Objectives

### Beginner Level
- [ ] Understand x86 memory layout
- [ ] Identify memory segments (text, data, heap, stack)
- [ ] Examine CPU registers
- [ ] Use basic WinDbg commands
- [ ] Calculate memory addresses

### Intermediate Level
- [ ] Analyze multi-threaded applications
- [ ] Understand complex data structures
- [ ] Trace execution flow
- [ ] Manipulate registers during execution
- [ ] Analyze stack frames

### Advanced/Expert Level
- [ ] Perform comprehensive memory analysis
- [ ] Develop buffer overflow exploits
- [ ] Implement multiple exploitation vectors
- [ ] Understand mitigation techniques
- [ ] Create working exploit payloads

---

## Lab Environment Requirements

### Software Requirements
- **Windows 10/11** (64-bit) - Tested on Windows 10
- **WinDbg Preview** (latest version)
- **Visual Studio 2019+** or **MinGW-w64** for compilation
- **Python 3.8+** (for exploit scripts)
- **Hex Editor** (HxD recommended)
- **IDA Free** or **Ghidra** (optional, for reverse engineering)

### Hardware Requirements
- **Minimum:** 4GB RAM, 20GB free disk space
- **Recommended:** 8GB+ RAM, 50GB+ free disk space
- **Virtual Machine:** Optional but recommended for safety

### Compilation Settings
```bash
# 32-bit compilation (x86)
gcc -m32 -g -fno-stack-protector -z execstack -o program.exe program.c

# For Visual Studio
cl /Zi /GS- /DYNAMICBASE:NO /NXCOMPAT:NO program.c
```

---

## Common Issues and Solutions

### Issue: WinDbg Won't Attach
**Solution:**
- Run WinDbg as Administrator
- Check if process is already being debugged
- Verify architecture match (32-bit vs 64-bit)

### Issue: Symbols Not Loading
**Solution:**
```windbg
.sympath+ C:\Symbols
.reload /f
```

### Issue: Program Exits Too Quickly
**Solution:**
- Add `getchar();` or `Sleep(30000);` before `return 0;`
- Use WinDbg to launch program: `windbg program.exe`

### Issue: Exploit Doesn't Work
**Solution:**
- Verify function addresses are correct
- Check payload alignment (4-byte boundaries)
- Verify buffer offset calculations
- Check for bad characters in payload

---

## Assessment and Progress Tracking

### Self-Assessment Checklist

**Beginner Lab:**
- [ ] Can identify all memory segments
- [ ] Can examine and modify registers
- [ ] Can calculate memory addresses
- [ ] Can use basic WinDbg commands
- [ ] Understands stack frame structure

**Intermediate Lab:**
- [ ] Can analyze multi-threaded applications
- [ ] Can trace complex data structures
- [ ] Can manipulate execution flow
- [ ] Understands calling conventions
- [ ] Can analyze heap structures

**Advanced/Expert Lab:**
- [ ] Can develop buffer overflow exploits
- [ ] Can implement multiple exploitation vectors
- [ ] Understands mitigation techniques
- [ ] Can create working exploit payloads
- [ ] Can analyze real-world vulnerabilities

---

## Additional Resources

### Documentation
- **WinDbg Documentation:** https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/
- **x86 Assembly Reference:** Intel Architecture Manuals
- **Windows Internals:** Mark Russinovich's Windows Internals

### Tutorials
- **Corelan Exploit Writing:** https://www.corelan.be/index.php/2009/07/19/exploit-writing-tutorial-part-1-stack-based-overflows/
- **Smashing the Stack:** Aleph One's classic paper
- **ROP Techniques:** Return-Oriented Programming Explained

### Practice Platforms
- **Exploit Exercises:** https://exploit-exercises.com/
- **Hack The Box:** https://www.hackthebox.com/
- **TryHackMe:** https://tryhackme.com/

---

## Lab Completion Criteria

### Minimum Requirements
- Complete all exercises in chosen lab
- Document findings in lab report
- Create working code/exploits
- Understand key concepts

### Excellent Completion
- Complete all exercises thoroughly
- Extend exercises with custom challenges
- Research related topics
- Create comprehensive documentation
- Help others learn (teaching reinforces learning)

---

## Next Steps After Section 2.1

After completing Section 2.1 labs:
1. **Review:** Ensure you understand all concepts
2. **Practice:** Work with variations and custom programs
3. **Prepare:** Review Section 2.2 materials
4. **Document:** Build your portfolio of work
5. **Share:** Discuss findings with peers or mentors

---

## Support and Feedback

### Getting Help
- Review troubleshooting sections in each lab
- Check WinDbg documentation
- Search for error messages online
- Ask questions in OSED student forums

### Providing Feedback
- Report issues with lab instructions
- Suggest improvements
- Share additional resources
- Contribute your own exercises

---

## Lab Schedule Recommendation

### Full-Time Study (40 hours/week)
- **Week 1:** Beginner Lab (3.5 hours) + Theory Review (2 hours)
- **Week 1:** Intermediate Lab (5 hours) + Practice (2 hours)
- **Week 2:** Consolidated Advanced/Expert Lab (10 hours) + Practice (5 hours)

### Part-Time Study (10 hours/week)
- **Week 1:** Beginner Lab (3.5 hours)
- **Week 2:** Theory Review + Intermediate Lab Start (5 hours)
- **Week 3:** Intermediate Lab Complete (5 hours)
- **Week 4-5:** Consolidated Advanced/Expert Lab (10 hours)

### Intensive Study (60 hours/week)
- **Day 1:** Beginner Lab + Theory (6 hours)
- **Day 2:** Intermediate Lab (6 hours)
- **Day 3-4:** Consolidated Advanced/Expert Lab (12 hours)

---

## Tips for Success

1. **Don't Rush:** Take time to understand each concept
2. **Experiment:** Try variations and modifications
3. **Document:** Keep detailed notes and screenshots
4. **Practice:** Repetition builds understanding
5. **Ask Questions:** Don't hesitate to seek help
6. **Teach Others:** Explaining concepts reinforces learning
7. **Stay Curious:** Research topics that interest you
8. **Build Portfolio:** Document your work for future reference

---

**Good luck with your OSED journey! Remember: "Try Harder" - but also work smarter by following these detailed step-by-step instructions.**

