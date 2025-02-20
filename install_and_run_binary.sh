#!/bin/bash

# Configuration
BIN_DIR="$HOME/binance-speedtest"
BIN_URL="https://github.com/MFRealG/binance-speedtest/releases/download/1.0.0/binance.bin"
BIN_FILE="binance.bin"
SCRIPT_NAME="install_and_run_binary.sh"

# Create directory in HOME if it doesn't exist
if [ ! -d "$BIN_DIR" ]; then
    echo "[INFO] Creating directory: $BIN_DIR"
    mkdir -p "$BIN_DIR"
fi

# Navigate to the directory
cd "$BIN_DIR"

# Download the binary
echo "[INFO] Downloading $BIN_FILE from $BIN_URL"
wget -q --show-progress "$BIN_URL" -O "$BIN_FILE"

# Make the binary executable
echo "[INFO] Making the binary executable"
chmod +x "$BIN_FILE"

# Clearing
clear

# Run the binary
echo "[INFO] Running the binary"
echo " "
echo " "
./"$BIN_FILE"

# Delete this script from the home directory
if [ -f "$HOME/$SCRIPT_NAME" ]; then
    echo "[INFO] Deleting the installation script..."
    rm "$HOME/$SCRIPT_NAME"
fi

echo "[INFO] Setup completed. You can now run the binary from $BIN_DIR"
