"""
=============================================================================
FILE: patch_vm_imports.py
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

vm_dir = r"prototype\language\runtime\vm"
for filepath in glob.glob(os.path.join(vm_dir, "*.py")):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # replace 'from vm.' with 'from .'
    # wait, it might be 'from vm import'
    content = content.replace("from vm.", "from .")
    content = content.replace("from vm import", "from . import")
    # Also fix 'from aayu_language.' since it was renamed to 'language.' or '..'
    content = content.replace("from aayu_language.", "from ...")
    content = content.replace("import aayu_language.", "import language.")
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
print("Fixed imports in vm directory.")
