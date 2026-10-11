#!/usr/bin/env bash
set -e

echo "===================================="
echo ">> Installing AAYU Language Compiler <<"
echo "===================================="

OS="$(uname -s)"
if [ "$OS" = "Linux" ]; then
    URL="https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases/latest/download/aayu-linux.tar.gz"
    echo ">> Downloading Native Linux Compiler..."
    curl -sL "$URL" -o aayu.tar.gz
    tar -xzf aayu.tar.gz
    rm aayu.tar.gz
elif [ "$OS" = "Darwin" ]; then
    URL="https://github.com/Minato95-ayu/INTENT-TO-SILICON/releases/latest/download/aayu-macos.zip"
    echo ">> Downloading Native macOS Compiler..."
    curl -sL "$URL" -o aayu.zip
    unzip -q aayu.zip
    rm aayu.zip
else
    echo "Unsupported OS: $OS"
    exit 1
fi

chmod +x aayu
echo ">> Installing to /usr/local/bin..."
sudo mv aayu /usr/local/bin/aayu

echo "===================================="
echo ">> AAYU INSTALLATION SUCCESSFUL! <<"
echo "===================================="
echo "You can now run AAYU from ANY folder by typing:"
echo "$ aayu run yourfile.aayu"