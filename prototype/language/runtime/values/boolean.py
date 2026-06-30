from .base import RuntimeValue
from typing import Any

class BooleanValue(RuntimeValue):
    def __init__(self, value: bool): self.value = bool(value)
    def type_name(self) -> str: return "Boolean"
    def truthy(self) -> bool: return self.value
    def equals(self, other: RuntimeValue) -> bool: return isinstance(other, BooleanValue) and self.value == other.value
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare boolean")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return BooleanValue(self.value)
    def stringify(self) -> str: return "true" if self.value else "false"
    def to_python(self) -> Any: return self.value
