#!/bin/bash

# Clearing the screen
clear

# Configuration
REPO_URL="https://github.com/MFRealG/binance-speedtest.git"
PROJECT_DIR="$HOME/binance-speedtest"
PYTHON_VERSION="python3"
SCRIPT_NAME="install_and_run.sh"

# Check if Python is installed
if ! command -v $PYTHON_VERSION &> /dev/null
then
    echo "[ERROR] $PYTHON_VERSION is not installed. Please install Python 3 and run the script again."
    exit 1
fi

# Install virtualenv if not already installed
if ! command -v virtualenv &> /dev/null
then
    echo "[INFO] Installing virtualenv..."
    $PYTHON_VERSION -m pip install --upgrade pip
    $PYTHON_VERSION -m pip install virtualenv
fi

# Clone the repository
echo "[INFO] Cloning the repository..."
if [ -d "$PROJECT_DIR" ]; then
    echo "[INFO] Repository already exists. Updating..."
    cd "$PROJECT_DIR"
    git pull
else
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# Make this script executable for future use
chmod +x "$PROJECT_DIR/$SCRIPT_NAME"

# Create and activate virtualenv
echo "[INFO] Creating virtual environment..."
virtualenv .venv
source .venv/bin/activate

# Install dependencies
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt

# Clearing the screen
clear

# Run the script
echo "[INFO] Running the script..."
echo " "
echo " "
python binance.py

# Deactivate virtualenv after completion
deactivate
echo "[INFO] Script completed. Virtualenv deactivated."

# Delete this script from the home directory
if [ -f "$HOME/$SCRIPT_NAME" ]; then
    rm "$HOME/$SCRIPT_NAME"
fi

echo "[INFO] Setup completed. You can now run the script from $PROJECT_DIR/install_and_run.sh"
