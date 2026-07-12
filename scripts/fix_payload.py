"""
=============================================================================
FILE: fix_payload.py
PURPOSE: Fixes payload handling
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes payload handling.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

﻿import sys

def fix_list_lib():
    with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\list_lib.py', 'r') as f:
        content = f.read()
    content = content.replace('args[0].elements', 'args[0]._get_payload()')
    with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\list_lib.py', 'w') as f:
        f.write(content)

def fix_map_lib():
    with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\map_lib.py', 'r') as f:
        content = f.read()
    content = content.replace('args[0].elements', 'args[0]._get_payload()')
    with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\map_lib.py', 'w') as f:
        f.write(content)

def fix_string_lib():
    with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\string_lib.py', 'r') as f:
        content = f.read()
    if 'string::length' not in content:
        code = '''
    def fn_length(args, vm):
        if not args: return NullValue()
        return NumberValue(len(args[0].to_python()))
    registry.register("string::length", fn_length)
'''
        content = content + code
    with open(r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules\string_lib.py', 'w') as f:
        f.write(content)

fix_list_lib()
fix_map_lib()
fix_string_lib()
