"""
=============================================================================
FILE: null.py
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
from typing import Any

class NullValue(RuntimeValue):
    def type_name(self) -> str: return "Null"
    def truthy(self) -> bool: return False
    def equals(self, other: RuntimeValue) -> bool: return isinstance(other, NullValue)
    def compare(self, other: RuntimeValue) -> int: return 0 if isinstance(other, NullValue) else -1
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return NullValue()
    def stringify(self) -> str: return "null"
    def to_python(self) -> Any: return None
