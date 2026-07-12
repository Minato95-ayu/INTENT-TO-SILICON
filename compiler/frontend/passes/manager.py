"""
=============================================================================
FILE: manager.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import List
from compiler.frontend.compiler_context import CompilerContext
from .base import BasePass

class PassManager:
    def __init__(self):
        self.passes: List[BasePass] = []
        
    def add_pass(self, p: BasePass):
        self.passes.append(p)
        
    def run(self, context: CompilerContext) -> bool:
        for p in self.passes:
            success = p.run(context)
            if context.diagnostics.has_errors() or not success:
                context.diagnostics.error(f"Compilation stopped due to errors in pass: {p.name}", context.current_module)
                return False
        return True
