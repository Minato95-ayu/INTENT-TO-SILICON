"""
=============================================================================
FILE: patch_stdlib.py
PURPOSE: Patches standard library
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles patches standard library.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os

stdlib_path = r"prototype\language\runtime\stdlib\stdlib.py"
with open(stdlib_path, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(".to_string()", ".stringify()")

with open(stdlib_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Updated stdlib.py stringify")
