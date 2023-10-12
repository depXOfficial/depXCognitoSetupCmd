#!/bin/bash

# Define variables
APP_NAME="DepXCognitoSetup"
SCRIPT_NAME="src/run.py"
ARCH=$(uname -m)

# Function to check if a command is available
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install pip if not already installed
install_pip() {
    if ! command_exists pip; then
        echo "Installing pip..."
        if command_exists apt-get; then
            sudo apt-get update >/dev/null 
            sudo apt-get install -y python3-pip >/dev/null  
        elif command_exists yum; then
            sudo yum install -y python3-pip >/dev/null
        elif command_exists dnf; then
            sudo dnf install -y python3-pip >/dev/null
        else
            echo "Unsupported package manager. Please install pip manually and rerun this script."
            exit 1
        fi
        echo "pip installation complete."
    fi
}

# Function to install PyInstaller if not already installed
install_packages() {
    echo "Installing dependencies.."
    pip install -r requirements.txt
}

# Install dependencies
install_pip

# Install PyInstaller
install_packages

# Run PyInstaller to create the executable
echo "Building $APP_NAME..."
pyinstaller --name "$APP_NAME" --onefile "$SCRIPT_NAME" --path=.

# Optional: Clean up temporary files generated by PyInstaller
rm -rf __pycache__ build "$APP_NAME".spec

echo
echo "Build completed successfully."
echo "You can find the executable in the 'dist' directory."
echo "You can run ./dist/$APP_NAME"
echo

exit 0
