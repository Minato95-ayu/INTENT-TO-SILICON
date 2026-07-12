"""
=============================================================================
FILE: __init__.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from .base import MemoryBackend
from .json_memory import JSONMemory
from .sqlite_memory import SQLiteMemory

__all__ = [
    'MemoryBackend',
    'JSONMemory',
    'SQLiteMemory'
]
