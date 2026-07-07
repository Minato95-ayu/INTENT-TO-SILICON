"""
=============================================================================
FILE: freeze.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

class FreezeGuard:
    def check(self, component: str) -> bool:
        """
        Check if a component is frozen.
        Returns True if ALLOWED to modify, False if FROZEN.
        """
        # MVP: Stub based on PROJECT_SNAPSHOT.md
        frozen_components = ["Lexer", "Parser", "AST", "Compiler", "ISA", "Modules"]
        if component in frozen_components:
            return False
        return True
