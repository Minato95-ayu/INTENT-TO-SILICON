#!/bin/bash
echo "====================================="
echo "   AAYU Installer for Android (Termux) "
echo "====================================="
echo "Installing prerequisites..."
pkg update -y
pkg install python git rust clang -y

echo "Cloning AAYU Repository..."
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON

echo "Installing AAYU Python Compiler..."
pip install -e .

echo "Building AAYU Rust VM (Silicon Engine)..."
cd runtime_rs
cargo build --release

echo "Installation Complete!"
echo "Run 'aayu run hello.aayu' to get started."
