#!/bin/bash
set -e
echo "========================================="
echo "      AAYU Compiler Setup (Linux)        "
echo "========================================="
echo "This script will install AAYU on your system."
sleep 1

# Check dependencies
for req in git python3 cargo; do
    if ! command -v $req &> /dev/null; then
        echo "Error: $req is required but not installed."
        echo "Please install it first (e.g., sudo apt install $req)"
        exit 1
    fi
done

INSTALL_DIR="$HOME/.aayu"
echo "[*] Cloning repository to $INSTALL_DIR..."
rm -rf "$INSTALL_DIR"
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git "$INSTALL_DIR"

echo "[*] Setting up Python CLI..."
cd "$INSTALL_DIR"
python3 -m pip install -e . --break-system-packages 2>/dev/null || python3 -m pip install -e .

echo "[*] Compiling Native Silicon Engine (Rust VM)..."
cd runtime_rs
cargo build --release

echo "[*] Configuring PATH..."
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"
ln -sf "$INSTALL_DIR/runtime_rs/target/release/aayu-vm" "$BIN_DIR/aayu-vm"

SHELL_RC="$HOME/.bashrc"
if [[ "$SHELL" == *"zsh"* ]]; then SHELL_RC="$HOME/.zshrc"; fi

if ! grep -q "$BIN_DIR" "$SHELL_RC"; then
    echo "export PATH=\"$BIN_DIR:$PATH\"" >> "$SHELL_RC"
    export PATH="$BIN_DIR:$PATH"
fi

echo "========================================="
echo " AAYU installed successfully! 🚀"
echo " Please restart your terminal or run:"
echo " source $SHELL_RC"
echo " Then type 'aayu run <file.aayu>'"
echo "========================================="
