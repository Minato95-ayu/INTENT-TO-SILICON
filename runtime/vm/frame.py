"""
=============================================================================
FILE: frame.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from compiler.frontend.ir import Bytecode
from typing import List, Dict, Any

class CallFrame:
    def __init__(self, bytecode: Bytecode, locals_dict: dict, frame_name: str = "main"):
        self.bytecode = bytecode
        self.locals = locals_dict
        self.ip = 0
        self.stack = []
        self.return_ip = -1
        self.function = None
        self.frame_name = frame_name
        self.source_file = getattr(bytecode, 'file', '')

class CallStackEntry:
    def __init__(self, task: str, file: str, line: int):
        self.task = task
        self.file = file
        self.line = line
