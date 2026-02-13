@echo off
echo ========================================
echo Checking Python Installation
echo ========================================
echo.

echo [1] Checking python command...
python --version 2>nul
if %errorlevel% == 0 (
    echo ✓ Python found!
    python --version
    echo.
    echo [2] Checking pip...
    python -m pip --version 2>nul
    if %errorlevel% == 0 (
        echo ✓ pip found!
        echo.
        echo [3] Installing dependencies...
        python -m pip install -r requirements.txt
    ) else (
        echo ✗ pip not found
        echo Try: python -m ensurepip --upgrade
    )
) else (
    echo ✗ Python not found
    echo.
    echo [2] Checking py launcher...
    py --version 2>nul
    if %errorlevel% == 0 (
        echo ✓ Python launcher found!
        py --version
        echo.
        echo [3] Installing dependencies...
        py -m pip install -r requirements.txt
    ) else (
        echo ✗ Python launcher not found
        echo.
        echo ========================================
        echo Python belum terinstall!
        echo Silakan install Python dari:
        echo https://www.python.org/downloads/
        echo.
        echo PENTING: Centang "Add Python to PATH" saat instalasi
        echo ========================================
    )
)

echo.
pause
