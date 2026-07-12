"""
=============================================================================
FILE: function.py
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

class FunctionValue(RuntimeValue):
    def __init__(self, name: str, bytecode: Any, env: Any = None):
        self.name = name; self.bytecode = bytecode; self.closure_env = env
        self.reflection_info = getattr(bytecode, 'reflection_info', None)
    def type_name(self) -> str: return "Function"
    def truthy(self) -> bool: return True
    def equals(self, other: RuntimeValue) -> bool: return self is other
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare function")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return self
    def stringify(self) -> str: return f"<function {self.name}>"
    def to_python(self) -> Any: return self

class NativeFunctionValue(RuntimeValue):
    def __init__(self, name: str, call_fn: callable):
        self.name = name; self.call_fn = call_fn
    def type_name(self) -> str: return "NativeFunction"
    def truthy(self) -> bool: return True
    def equals(self, other: RuntimeValue) -> bool: return self is other
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare native function")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return self
    def stringify(self) -> str: return f"<native function {self.name}>"
    def to_python(self) -> Any: return self
