from .base import RuntimeValue
from .boolean import BooleanValue
from typing import Any

class NumberValue(RuntimeValue):
    def __init__(self, value: float): self.value = float(value)
    def type_name(self) -> str: return "Number"
    def truthy(self) -> bool: return self.value != 0.0
    def equals(self, other: RuntimeValue) -> bool: return isinstance(other, NumberValue) and self.value == other.value
    def compare(self, other: RuntimeValue) -> int:
        if not isinstance(other, NumberValue): raise Exception("Cannot compare")
        if self.value < other.value: return -1
        if self.value > other.value: return 1
        return 0
    def add(self, other: RuntimeValue) -> RuntimeValue:
        if isinstance(other, NumberValue): return NumberValue(self.value + other.value)
        return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue:
        if isinstance(other, NumberValue): return NumberValue(self.value - other.value)
        return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue:
        if isinstance(other, NumberValue): return NumberValue(self.value * other.value)
        return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue:
        if isinstance(other, NumberValue):
            if other.value == 0: raise Exception("Division by zero")
            return NumberValue(self.value / other.value)
        return super().div(other)
    def clone(self) -> RuntimeValue: return NumberValue(self.value)
    def stringify(self) -> str: return str(self.value)
    def to_python(self) -> Any: return self.value
