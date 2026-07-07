"""
=============================================================================
FILE: reference.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from .base import RuntimeValue

class ReferenceValue(RuntimeValue):
    def __init__(self, heap_id: int, ref_type: str, heap):
        self.heap_id = heap_id
        self.ref_type = ref_type
        self.heap = heap

    def type_name(self) -> str:
        return self.ref_type
        
    def clone(self) -> 'RuntimeValue':
        # Stack only carries references, clone just duplicates the reference, not the heap object!
        return ReferenceValue(self.heap_id, self.ref_type, self.heap)
