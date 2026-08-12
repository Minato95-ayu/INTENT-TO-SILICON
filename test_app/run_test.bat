@echo off
echo ==========================================
echo AAYU Ecosystem Integration Test
echo ==========================================

echo [1] Compiling Ecosystem Tester to Web UI...
python -m aayu.cli build test_app\ecosystem_tester.aayu
if %errorlevel% neq 0 (
    echo Error during build!
    exit /b %errorlevel%
)

echo [2] Running CLI/Native Entry Point...
python -m aayu.cli run test_app\ecosystem_tester.aayu
if %errorlevel% neq 0 (
    echo Error during runtime execution!
    exit /b %errorlevel%
)

echo.
echo All Subsystems Executed Successfully!
