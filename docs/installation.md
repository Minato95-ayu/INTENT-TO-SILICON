# Installation Guide

Welcome to AAYU! AAYU provides pre-compiled binaries for Windows, macOS, and Linux.

## Quick Install (Windows)
Download the ayu-v1.0.0-windows-x64.zip release and add the extracted folder to your System PATH.
Alternatively, use the AAYU Installer:
`powershell
Invoke-WebRequest -Uri "https://aayu.dev/install.ps1" -OutFile "install.ps1"; .\install.ps1
`

## Quick Install (macOS / Linux)
`ash
curl -fsSL https://aayu.dev/install.sh | bash
`

## Verify Installation
`ash
aayu --version
# Expected: AAYU Language CLI (v1.0.0 Stable)
`\n