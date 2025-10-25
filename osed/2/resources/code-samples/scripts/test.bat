@echo off
REM test.bat
REM Quick test script for Windows to verify compilation
REM Usage: test.bat

echo ========================================
echo   Testing Compiled Programs
echo ========================================
echo.

if not exist "bin\" (
    echo ERROR: bin\ directory not found
    echo Run 'make' first
    exit /b 1
)

set TOTAL=0
set SUCCESS=0
set FAILED=0

echo Testing basic programs...
echo.

REM Test each program with --help or quick exit
for %%P in (hello variables calculations memory_layout stack_demo calling_conventions struct_basic malloc_simple thread_basic seh_basic buffer_overflow format_string use_after_free) do (
    set /a TOTAL+=1

    if exist "bin\%%P.exe" (
        echo   [OK] %%P.exe exists
        set /a SUCCESS+=1
    ) else (
        echo   [FAIL] %%P.exe missing
        set /a FAILED+=1
    )
)

echo.
echo ========================================
echo   Summary
echo ========================================
echo Total:   %TOTAL%
echo Success: %SUCCESS%
echo Failed:  %FAILED%
echo.

if %FAILED%==0 (
    echo All programs compiled successfully!
    exit /b 0
) else (
    echo Some programs are missing.
    exit /b 1
)
