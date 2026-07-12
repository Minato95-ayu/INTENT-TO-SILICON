"""
=============================================================================
FILE: test_chat_auto.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import subprocess
import os
import sys

def main():
    cli_path = os.path.join(os.path.dirname(__file__), "prototype", "cli.py")
    inputs = "hospital\nSingle\nY\nY\nY\n"
    
    result = subprocess.run(
        [sys.executable, cli_path, "chat"], 
        input=inputs.encode('utf-8'),
        capture_output=True
    )
    
    print("STDOUT:")
    print(result.stdout.decode('utf-8'))
    print("\nSTDERR:")
    print(result.stderr.decode('utf-8'))
    
if __name__ == "__main__":
    main()
