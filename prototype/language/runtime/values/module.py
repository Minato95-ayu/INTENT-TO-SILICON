from .base import RuntimeValue
from typing import Any, Dict

class ModuleValue(RuntimeValue):
    def __init__(self, name: str, exports: Dict[str, RuntimeValue] = None, reflection_info: Any = None):
        self.name = name; self.exports = exports if exports is not None else {}
        self.reflection_info = reflection_info
    def type_name(self) -> str: return "Module"
    def truthy(self) -> bool: return True
    def equals(self, other: RuntimeValue) -> bool: return self is other
    def compare(self, other: RuntimeValue) -> int: raise Exception("Cannot compare module")
    def add(self, other: RuntimeValue) -> RuntimeValue: return super().add(other)
    def sub(self, other: RuntimeValue) -> RuntimeValue: return super().sub(other)
    def mul(self, other: RuntimeValue) -> RuntimeValue: return super().mul(other)
    def div(self, other: RuntimeValue) -> RuntimeValue: return super().div(other)
    def clone(self) -> RuntimeValue: return self
    def stringify(self) -> str: return f"<module {self.name}>"
    def to_python(self) -> Any: return self
