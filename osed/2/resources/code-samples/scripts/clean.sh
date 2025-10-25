#!/bin/bash

# clean.sh
# Removes all compiled binaries and build artifacts
# Usage: ./clean.sh

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Cleaning Build Artifacts${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Count files before deletion
if [ -d "bin" ]; then
    FILE_COUNT=$(find bin -name "*.exe" 2>/dev/null | wc -l)
    echo "Found $FILE_COUNT executable(s) in bin/"

    if [ $FILE_COUNT -gt 0 ]; then
        echo ""
        echo "Files to be removed:"
        ls -lh bin/*.exe 2>/dev/null || true
        echo ""

        read -p "Delete these files? (y/N): " -n 1 -r
        echo ""

        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -f bin/*.exe
            echo -e "${GREEN}Deleted $FILE_COUNT file(s)${NC}"

            # Remove bin directory if empty
            if [ -z "$(ls -A bin 2>/dev/null)" ]; then
                rmdir bin
                echo -e "${GREEN}Removed empty bin/ directory${NC}"
            fi
        else
            echo -e "${YELLOW}Cancelled - no files deleted${NC}"
        fi
    else
        echo "No .exe files found in bin/"

        # Remove empty bin directory
        if [ -z "$(ls -A bin 2>/dev/null)" ]; then
            rmdir bin
            echo -e "${GREEN}Removed empty bin/ directory${NC}"
        fi
    fi
else
    echo "No bin/ directory found - nothing to clean"
fi

echo ""
echo -e "${GREEN}Cleanup complete${NC}"
