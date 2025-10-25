#!/bin/bash

# verify.sh
# Verifies that all programs compiled successfully and are executable
# Usage: ./verify.sh

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Verification Report${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Expected programs
EXPECTED_PROGRAMS=(
    "hello"
    "variables"
    "calculations"
    "memory_layout"
    "stack_demo"
    "calling_conventions"
    "struct_basic"
    "malloc_simple"
    "thread_basic"
    "seh_basic"
    "buffer_overflow"
    "format_string"
    "use_after_free"
)

TOTAL=${#EXPECTED_PROGRAMS[@]}
FOUND=0
MISSING=0
EXECUTABLE=0
NOT_EXECUTABLE=0

echo "Expected programs: $TOTAL"
echo ""

# Check bin directory exists
if [ ! -d "bin" ]; then
    echo -e "${RED}ERROR: bin/ directory not found${NC}"
    echo "Run 'make' or './compile_all.sh' first"
    exit 1
fi

echo "Checking each program..."
echo ""

for program in "${EXPECTED_PROGRAMS[@]}"; do
    exe_file="bin/${program}.exe"

    printf "  %-25s " "$program.exe"

    if [ -f "$exe_file" ]; then
        ((FOUND++))

        # Check if executable
        if [ -x "$exe_file" ]; then
            ((EXECUTABLE++))

            # Get file size
            SIZE=$(stat -f%z "$exe_file" 2>/dev/null || stat -c%s "$exe_file" 2>/dev/null)
            SIZE_KB=$((SIZE / 1024))

            echo -e "${GREEN}OK${NC} (${SIZE_KB}KB)"
        else
            ((NOT_EXECUTABLE++))
            echo -e "${YELLOW}NOT EXECUTABLE${NC}"
        fi
    else
        ((MISSING++))
        echo -e "${RED}MISSING${NC}"
    fi
done

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Total expected:     $TOTAL"
echo -e "${GREEN}Found:              $FOUND${NC}"

if [ $MISSING -gt 0 ]; then
    echo -e "${RED}Missing:            $MISSING${NC}"
else
    echo -e "Missing:            $MISSING"
fi

echo -e "${GREEN}Executable:         $EXECUTABLE${NC}"

if [ $NOT_EXECUTABLE -gt 0 ]; then
    echo -e "${YELLOW}Not executable:     $NOT_EXECUTABLE${NC}"
else
    echo -e "Not executable:     $NOT_EXECUTABLE"
fi

echo ""

# Overall status
if [ $MISSING -eq 0 ] && [ $NOT_EXECUTABLE -eq 0 ]; then
    echo -e "${GREEN}✓ All programs compiled successfully!${NC}"
    echo ""

    # Disk usage
    TOTAL_SIZE=$(du -sh bin/ 2>/dev/null | cut -f1)
    echo "Total size: $TOTAL_SIZE"
    echo ""

    echo "Ready for debugging with WinDbg!"
    exit 0
elif [ $MISSING -gt 0 ]; then
    echo -e "${RED}✗ Some programs are missing${NC}"
    echo ""
    echo "Run: make"
    echo " or: ./scripts/compile_all.sh"
    exit 1
else
    echo -e "${YELLOW}⚠ Some programs exist but are not executable${NC}"
    echo ""
    echo "This might be a permission issue."
    exit 1
fi
