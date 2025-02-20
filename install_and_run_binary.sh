#!/bin/bash

# Configuration
BIN_DIR="/binance-speedtest"
BIN_URL="https://github.com/MFRealG/binance-speedtest/releases/download/1.0.0/binance.bin"
BIN_FILE="binance.bin"

# Create directory if it doesn't exist
if [ ! -d "$BIN_DIR" ]; then
    echo "[INFO] Creating directory: $BIN_DIR"
    sudo mkdir -p "$BIN_DIR"
    sudo chown $USER:$USER "$BIN_DIR"
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
./"$BIN_FILE"
