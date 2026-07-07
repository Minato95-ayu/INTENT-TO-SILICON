"""
=============================================================================
FILE: fix_lib.py
PURPOSE: Fixes library issues
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes library issues.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import os
import re

dir_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules'

for filename in os.listdir(dir_path):
    if not filename.endswith('.py'): continue
    filepath = os.path.join(dir_path, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add imports if not present
    if 'make_string' not in content and ('StringValue(' in content or 'ListValue(' in content or 'MapValue(' in content):
        content = 'from ..helpers import make_string, make_list, make_map\n' + content
        
    content = re.sub(r'StringValue\(([^)]+)\)', r'make_string(vm, \1)', content)
    content = re.sub(r'ListValue\(([^)]+)\)', r'make_list(vm, \1)', content)
    content = re.sub(r'MapValue\(([^)]+)\)', r'make_map(vm, \1)', content)
    
    with open(filepath, 'w') as f:
        f.write(content)
