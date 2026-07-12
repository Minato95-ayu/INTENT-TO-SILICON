"""
=============================================================================
FILE: location.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from dataclasses import dataclass

@dataclass
class SourceFile:
    id: int
    path: str
    module: str

@dataclass
class SourceSpan:
    file_id: int
    start_line: int
    start_column: int
    end_line: int
    end_column: int
    
    def __str__(self):
        return f"file_id={self.file_id}:{self.start_line}:{self.start_column}-{self.end_line}:{self.end_column}"
