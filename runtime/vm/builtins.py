"""
=============================================================================
FILE: builtins.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

def builtin_print(vm, args):
    text = " ".join(map(str, args))
    print(text)
    vm.output.append(text)
    return None

def builtin_len(vm, args):
    if not args:
        return 0
    return len(args[0])

BUILTINS = {
    "print": builtin_print,
    "len": builtin_len,
}
