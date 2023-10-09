@echo off

:: Define variables
set APP_NAME=your_app_name

:: Path to the executable file
set EXECUTABLE_PATH=.\dist\%APP_NAME%.exe

:: Check if the executable file exists
if exist %EXECUTABLE_PATH% (
    echo Uninstalling %APP_NAME%...
    
    :: Remove the executable file
    del %EXECUTABLE_PATH%
    
    echo %APP_NAME% has been uninstalled.
) else (
    echo %APP_NAME% is not installed or the executable file does not exist.
)

exit /b 0
