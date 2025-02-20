#!/bin/bash

# Configuration
REPO_URL="https://github.com/MFRealG/binance-speedtest.git"
PROJECT_DIR="$HOME/binance-speedtest"
PYTHON_VERSION="python3"

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

# Create and activate virtualenv
echo "[INFO] Creating virtual environment..."
virtualenv .venv
source .venv/bin/activate

# Install dependencies
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt

# Run the script
echo "[INFO] Running the script..."
python binance.py

# Deactivate virtualenv after completion
deactivate
echo "[INFO] Script completed. Virtualenv deactivated."
