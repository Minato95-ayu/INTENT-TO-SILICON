#!/bin/bash
set -e
echo "=========================================="
echo "  Installing AAYU (Intent-to-Silicon)     "
echo "=========================================="

OS="$(uname -s)"
if [ "$OS" = "Linux" ]; then
    ASSET="aayu-linux.tar.gz"
elif [ "$OS" = "Darwin" ]; then
    ASSET="aayu-macos.zip"
else
    echo "Unsupported OS: $OS"
    exit 1
fi

URL="https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases/download/v1.3.0/$ASSET"
INSTALL_DIR="$HOME/.aayu/bin"
mkdir -p "$INSTALL_DIR"
TMP_FILE="$INSTALL_DIR/aayu_tmp_download"

echo "[1/3] Downloading Native Rust Binary for $OS..."
curl -fsSL -o "$TMP_FILE" "$URL"

echo "[2/3] Extracting Engine..."
if [ "$OS" = "Linux" ]; then
    tar -xzf "$TMP_FILE" -C "$INSTALL_DIR"
else
    unzip -qo "$TMP_FILE" -d "$INSTALL_DIR"
fi
rm -f "$TMP_FILE"

echo "[3/3] Setting up PATH..."
echo "AAYU installed successfully to $INSTALL_DIR!"
echo ""
echo "=> To get started, add AAYU to your PATH:"
echo "   export PATH=\"$INSTALL_DIR:\\""
echo "=========================================="
