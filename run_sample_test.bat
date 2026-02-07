@echo off
REM Sample test run script for Windows
REM This script demonstrates how to run the policy gap analysis system

echo ============================================================
echo Local LLM Policy Gap Analysis - Sample Test Run
echo ============================================================
echo.

echo Step 1: Verifying system setup...
python test_system.py --verify-offline
echo.

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: System verification failed. Please complete installation.
    echo See docs/INSTALLATION.md for setup instructions.
    pause
    exit /b 1
)

echo Step 2: Analyzing ISMS Policy (sample test)...
echo This will take approximately 5-8 minutes...
echo.
python src/main.py --policy data/test_policies/isms_policy.txt --output output/sample_run
echo.

if %ERRORLEVEL% EQU 0 (
    echo ============================================================
    echo SUCCESS! Sample analysis complete.
    echo ============================================================
    echo.
    echo Output files saved to: output/sample_run/
    echo.
    echo Generated reports:
    echo   - Gap Analysis Report
    echo   - Revised Policy Document
    echo   - Implementation Roadmap
    echo   - Executive Summary
    echo   - Comprehensive Report
    echo.
    echo To analyze all test policies, run:
    echo   python src/main.py --batch data/test_policies/
    echo.
) else (
    echo ERROR: Analysis failed. Check error messages above.
    echo.
)

pause
