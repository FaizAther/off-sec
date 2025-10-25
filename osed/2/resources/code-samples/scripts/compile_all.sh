#!/bin/bash

# compile_all.sh
# Compiles all OSED Section 2 code samples
# Usage: ./compile_all.sh [category]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
OUTDIR="bin"
CC="gcc"
CFLAGS="-g -O0 -Wall"
VULN_CFLAGS="-g -O0 -fno-stack-protector -Wall"

# Statistics
TOTAL=0
SUCCESS=0
FAILED=0

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  OSED Section 2 - Compilation Script${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Create output directory
mkdir -p "$OUTDIR"

# Function to compile a single file
compile_file() {
    local src_file=$1
    local category=$2
    local use_vuln_flags=${3:-0}

    local basename=$(basename "$src_file" .c)
    local output="$OUTDIR/${basename}.exe"

    echo -n "  Compiling $(basename $src_file)... "

    if [ "$use_vuln_flags" = "1" ]; then
        if $CC $VULN_CFLAGS -o "$output" "$src_file" 2>/dev/null; then
            echo -e "${GREEN}OK${NC}"
            ((SUCCESS++))
        else
            echo -e "${RED}FAILED${NC}"
            ((FAILED++))
        fi
    else
        if $CC $CFLAGS -o "$output" "$src_file" 2>/dev/null; then
            echo -e "${GREEN}OK${NC}"
            ((SUCCESS++))
        else
            echo -e "${RED}FAILED${NC}"
            ((FAILED++))
        fi
    fi

    ((TOTAL++))
}

# Function to compile a category
compile_category() {
    local category=$1
    local use_vuln_flags=${2:-0}

    echo -e "${YELLOW}[$category]${NC}"

    if [ -d "$category" ]; then
        for src_file in $category/*.c; do
            if [ -f "$src_file" ]; then
                compile_file "$src_file" "$category" "$use_vuln_flags"
            fi
        done
    else
        echo -e "  ${RED}Directory not found${NC}"
    fi

    echo ""
}

# Main compilation logic
if [ $# -eq 0 ]; then
    # Compile all categories
    echo "Compiling all categories..."
    echo ""

    compile_category "01-basic"
    compile_category "02-memory"
    compile_category "03-functions"
    compile_category "04-structures"
    compile_category "05-heap"
    compile_category "06-threads"
    compile_category "07-exceptions"
    compile_category "08-vulnerable" 1  # Use vulnerable flags
else
    # Compile specific category
    case "$1" in
        basic)
            compile_category "01-basic"
            ;;
        memory)
            compile_category "02-memory"
            ;;
        functions|func)
            compile_category "03-functions"
            ;;
        structures|struct)
            compile_category "04-structures"
            ;;
        heap)
            compile_category "05-heap"
            ;;
        threads)
            compile_category "06-threads"
            ;;
        exceptions|except)
            compile_category "07-exceptions"
            ;;
        vulnerable|vuln)
            compile_category "08-vulnerable" 1
            ;;
        *)
            echo -e "${RED}Unknown category: $1${NC}"
            echo ""
            echo "Available categories:"
            echo "  basic, memory, functions, structures, heap, threads, exceptions, vulnerable"
            exit 1
            ;;
    esac
fi

# Summary
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Compilation Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "Total:   $TOTAL"
echo -e "${GREEN}Success: $SUCCESS${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}Failed:  $FAILED${NC}"
else
    echo -e "Failed:  $FAILED"
fi
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All compilations successful!${NC}"
    echo ""
    echo "Executables in: $OUTDIR/"
    ls -lh "$OUTDIR"/*.exe 2>/dev/null || true
else
    echo -e "${YELLOW}Some compilations failed. Check errors above.${NC}"
    exit 1
fi
