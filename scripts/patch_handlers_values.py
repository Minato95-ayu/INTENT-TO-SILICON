"""
=============================================================================
FILE: patch_handlers_values.py
PURPOSE: Fixes or patches existing code
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes or patches existing code.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import glob

handlers_dir = r"prototype\language\runtime\vm\handlers"
for filepath in glob.glob(os.path.join(handlers_dir, "*.py")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("from ..values", "from ...values")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Fixed values imports in handlers")
