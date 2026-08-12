from .base import RuntimeValue
from .list import ListValue
from .string import StringValue
from .number import NumberValue
from .boolean import BooleanValue
from .null import NullValue

class SetValue(RuntimeValue):
    def __init__(self, elements: set):
        self.elements = elements
        
    def type_name(self) -> str:
        return "Set"
        
    def truthy(self) -> bool:
        return len(self.elements) > 0
        
    def equals(self, other: 'RuntimeValue') -> bool:
        if not isinstance(other, SetValue):
            return False
        return self.elements == other.elements
        
    def clone(self) -> 'RuntimeValue':
        return SetValue(set(self.elements))
        
    def stringify(self) -> str:
        items = ", ".join([str(item) for item in self.elements])
        return f"set({{{items}}})"
        
    def to_python(self):
        return set(self.elements)
