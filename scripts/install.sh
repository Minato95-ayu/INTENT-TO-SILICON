#!/bin/bash
# AAYU Language macOS/Linux Installer (Development Version)

set -e

echo "Installing AAYU Compiler..."

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 is required to run the AAYU VM."
    exit 1
fi

AAYU_HOME="$HOME/.aayu"
BIN_DIR="$AAYU_HOME/bin"

mkdir -p "$BIN_DIR"

# For development, we assume the user is inside the INTENT-TO-SILICON directory
# In production, this would download a release binary.
CLI_PATH="$(pwd)/prototype/cli.py"

cat << EOF > "$BIN_DIR/aayu"
#!/bin/bash
python3 "$CLI_PATH" "\$@"
EOF

chmod +x "$BIN_DIR/aayu"
echo "Created aayu executable at $BIN_DIR/aayu"

# Check if BIN_DIR is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "Adding $BIN_DIR to your PATH..."
    
    # Try to determine the shell profile
    if [ -n "$ZSH_VERSION" ]; then
        PROFILE_FILE="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        PROFILE_FILE="$HOME/.bashrc"
    else
        PROFILE_FILE="$HOME/.profile"
    fi
    
    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$PROFILE_FILE"
    echo "PATH updated in $PROFILE_FILE. Please restart your terminal or run: source $PROFILE_FILE"
fi

echo ""
echo "AAYU Installation Complete!"
echo "Try running: aayu new myapp"
