from .collection import CollectionValue
from .base import RuntimeValue
from .number import NumberValue
from .boolean import BooleanValue
from .null import NullValue
from ..memory.heap import Heap

class StringValue(CollectionValue):
    def __init__(self, heap_id: int, heap: Heap):
        super().__init__(heap_id, "string", heap)

    def _get_payload(self) -> str:
        return self.heap.get(self.heap_id).payload

    def length(self) -> RuntimeValue:
        return NumberValue(len(self._get_payload()))
        
    def get(self, key: RuntimeValue) -> RuntimeValue:
        if not isinstance(key, NumberValue):
            raise Exception("String index must be a number")
        idx = int(key.value)
        s = self._get_payload()
        if 0 <= idx < len(s):
            # Need to allocate a new string on the heap for the single char
            new_heap_obj = self.heap.allocate("string", s[idx])
            return StringValue(new_heap_obj.id, self.heap)
        return NullValue()
        
    def set(self, key: RuntimeValue, value: RuntimeValue):
        raise Exception("Strings are immutable")
            
    def append(self, value: RuntimeValue):
        raise Exception("Strings are immutable")
        
    def remove(self, key: RuntimeValue):
        raise Exception("Strings are immutable")
            
    def contains(self, value: RuntimeValue) -> RuntimeValue:
        if not isinstance(value, StringValue):
            return BooleanValue(False)
        # Check if substring
        s = self._get_payload()
        val_s = value._get_payload()
        return BooleanValue(val_s in s)
        
    def iterate(self):
        return list(self._get_payload())

    def stringify(self) -> str:
        return self._get_payload()
        
    def to_python(self):
        return self._get_payload()
        
    def equals(self, other: 'RuntimeValue') -> bool:
        if not isinstance(other, StringValue):
            return False
        # Strings are equal if their payload is equal (value semantics, not reference semantics)
        # Though since it's a reference, we might compare heap_id first
        if self.heap_id == other.heap_id:
            return True
        return self._get_payload() == other._get_payload()

    def compare(self, other: 'RuntimeValue') -> int:
        if not isinstance(other, StringValue):
            raise Exception("Cannot compare string with other type")
        s1 = self._get_payload()
        s2 = other._get_payload()
        if s1 < s2: return -1
        if s1 > s2: return 1
        return 0

    def add(self, other: 'RuntimeValue') -> 'RuntimeValue':
        if isinstance(other, StringValue):
            new_str = self._get_payload() + other._get_payload()
            new_obj = self.heap.allocate("string", new_str)
            return StringValue(new_obj.id, self.heap)
        return super().add(other)

    def truthy(self) -> bool:
        return len(self._get_payload()) > 0
        
    def clone(self) -> 'RuntimeValue':
        return StringValue(self.heap_id, self.heap)
