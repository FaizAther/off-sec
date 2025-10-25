# OSED Section 2.5: Additional WinDbg Features

## Learning Objectives
By the end of this section, students will be able to:
- List modules and symbols in WinDbg
- Use WinDbg as a calculator for address arithmetic
- Format data output in various formats
- Work with pseudo registers effectively
- Apply advanced WinDbg features to exploit development
- Utilize WinDbg's built-in utilities for analysis

## Prerequisites
- Completion of Section 2.1 (x86 Architecture)
- Completion of Section 2.2 (Windows Debugger)
- Completion of Section 2.3 (Memory Manipulation)
- Completion of Section 2.4 (Execution Control)
- Basic understanding of WinDbg commands

## Duration
- **Theory:** 2 hours
- **Lab:** 1.5 hours
- **Total:** 3.5 hours

## Theory Components

### 2.5.1 Listing Modules and Symbols in WinDbg
**Duration:** 45 minutes

#### Key Topics:
1. **Module Concepts**
   - What are modules
   - Module types
   - Module loading
   - Module information

2. **WinDbg Module Commands**
   - `lm` command (list modules)
   - `lm v` command (verbose module listing)
   - `lm m` command (module-specific listing)
   - `lm k` command (kernel modules)

3. **Symbol Commands**
   - `x` command (examine symbols)
   - `x <module>!*` command (all symbols)
   - `x <module>!<pattern>` command (pattern matching)
   - `x <address>` command (symbol at address)

4. **Module Analysis**
   - Module enumeration
   - Symbol resolution
   - Address calculation
   - Module relationships

#### Learning Activities:
- Module listing exercises
- Symbol examination tasks
- Module analysis practice

### 2.5.2 Using WinDbg as a Calculator
**Duration:** 30 minutes

#### Key Topics:
1. **Calculator Concepts**
   - Address arithmetic
   - Expression evaluation
   - Data type conversion
   - Mathematical operations

2. **WinDbg Calculator Commands**
   - `?` command (evaluate expression)
   - `? <expression>` command (calculate)
   - `? <address>` command (address analysis)
   - `? <register>` command (register analysis)

3. **Calculator Applications**
   - Address calculation
   - Offset determination
   - Size calculation
   - Memory layout analysis

#### Learning Activities:
- Calculator practice exercises
- Address arithmetic tasks
- Expression evaluation practice

### 2.5.3 Data Output Format
**Duration:** 30 minutes

#### Key Topics:
1. **Output Format Concepts**
   - Data representation
   - Format specifications
   - Output customization
   - Display options

2. **WinDbg Format Commands**
   - `d` command (dump)
   - `d <format>` command (specific format)
   - `d <address> L<length>` command (length specification)
   - `d <address> <address>` command (range specification)

3. **Format Applications**
   - Data analysis
   - Memory inspection
   - Structure examination
   - Exploit development

#### Learning Activities:
- Format specification exercises
- Data output practice
- Format analysis tasks

### 2.5.4 Pseudo Registers
**Duration:** 35 minutes

#### Key Topics:
1. **Pseudo Register Concepts**
   - What are pseudo registers
   - Pseudo register types
   - Pseudo register usage
   - Pseudo register benefits

2. **WinDbg Pseudo Registers**
   - `$exentry` (exception entry point)
   - `$exreturn` (exception return)
   - `$ra` (return address)
   - `$retreg` (return register)

3. **Pseudo Register Applications**
   - Exception handling
   - Function analysis
   - Return address tracking
   - Exploit development

#### Learning Activities:
- Pseudo register exercises
- Exception handling practice
- Function analysis tasks

## Lab Components

### Lab 2.5.1: Module and Symbol Analysis
**Duration:** 45 minutes

#### Objectives:
- List and analyze modules
- Examine symbols effectively
- Use module information for analysis

#### Tasks:
1. **Module Listing**
   - List all loaded modules
   - Analyze module information
   - Examine module relationships

2. **Symbol Examination**
   - List symbols for specific modules
   - Search for specific symbols
   - Analyze symbol information

3. **Module Analysis**
   - Calculate module sizes
   - Determine module offsets
   - Analyze module layout

#### Deliverables:
- Module analysis report
- Symbol examination worksheet
- Module relationship documentation

### Lab 2.5.2: Calculator and Format Features
**Duration:** 45 minutes

#### Objectives:
- Use WinDbg calculator effectively
- Format data output appropriately
- Work with pseudo registers

#### Tasks:
1. **Calculator Usage**
   - Perform address arithmetic
   - Calculate offsets and sizes
   - Evaluate expressions

2. **Data Formatting**
   - Format data in different ways
   - Customize output display
   - Analyze formatted data

3. **Pseudo Register Usage**
   - Use pseudo registers for analysis
   - Track exception handling
   - Analyze function returns

#### Deliverables:
- Calculator usage log
- Data formatting examples
- Pseudo register analysis

## Assessment

### Theory Assessment (30 minutes)
- Multiple choice questions on WinDbg features
- Practical exercises on module analysis
- Calculator and formatting tasks

### Lab Assessment (30 minutes)
- Module and symbol analysis
- Calculator usage and data formatting
- Pseudo register utilization

## Resources

### Required Reading:
- WinDbg Advanced Commands Reference
- WinDbg Calculator Documentation
- OSED Course Materials Section 2.5

### Recommended Tools:
- WinDbg Preview
- Module analysis utilities
- Symbol analysis tools

### Additional Resources:
- WinDbg feature tutorials
- Advanced debugging guides
- Exploit development references

## Next Steps
Upon completion of this section, students will proceed to:
- **Section 2.6:** Wrapping Up
- **Section 3:** Exploiting Stack Overflows

## Notes for Instructors
- Emphasize practical application of advanced features
- Provide real-world analysis scenarios
- Encourage exploration of WinDbg capabilities
- Connect advanced features to exploit development
- Use progressive complexity levels
