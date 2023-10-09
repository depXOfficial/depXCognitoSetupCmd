#!/bin/bash

# Define variables
APP_NAME="DepXCogntioSetup"

# Path to the executable file
EXECUTABLE_PATH="./dist/$APP_NAME"

# Check if the executable file exists
if [ -e "$EXECUTABLE_PATH" ]; then
    echo "Uninstalling $APP_NAME..."
    
    # Remove the executable file
    rm -f "$EXECUTABLE_PATH" DepXCogntioSetup.spec
    
    echo "$APP_NAME has been uninstalled."
else
    echo "$APP_NAME is not installed or the executable file does not exist."
fi

exit 0
