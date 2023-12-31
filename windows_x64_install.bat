@echo off
setlocal enabledelayedexpansion

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python and rerun this script.
    exit /b 1
)

rem Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. Installing pip...
    python -m ensurepip --default-pip
    python -m pip install --upgrade pip
)

rem Define variables
set APP_NAME=DepXCognitoSetup
set SCRIPT_NAME=.\src\run.py

rem Installing dependencies
pip install -r requirements.txt

rem Run PyInstaller to create the executable
pyinstaller --name %APP_NAME% --path . %SCRIPT_NAME%

rem Optional: Clean up temporary files generated by PyInstaller
rd /s /q build 

rem Cleanup the spec file
del %APP_NAME%.spec

echo.
echo %APP_NAME% has been successfully built.
echo You can run the executable with .\dist\%APP_NAME%\%APP_NAME%
echo.

pause
