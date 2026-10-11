# Installation Guide

## Global Installation (Recommended)
To install AAYU globally on your system, run:

```bash
pip install aayu-lang
```

This will automatically add the `aayu` command to your system's PATH.

## Development Installation
If you want to contribute to AAYU or test the bleeding edge:

```bash
git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git
cd INTENT-TO-SILICON
pip install -e .
```

## VS Code Extension
AAYU provides a first-class VS Code extension offering syntax highlighting, autocompletion, diagnostics, hover, and debugging.

1. Install the `vscode-aayu` extension from the VS Code Marketplace (or load it locally).
2. Ensure you have installed the `aayu-lang` CLI globally.
3. Open an `.aayu` file and the language server will start automatically!