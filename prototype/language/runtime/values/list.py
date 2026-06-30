from .collection import CollectionValue
from .base import RuntimeValue
from .number import NumberValue
from .boolean import BooleanValue
from .null import NullValue
from ..memory.heap import Heap

class ListValue(CollectionValue):
    def __init__(self, heap_id: int, heap: Heap):
        super().__init__(heap_id, "list", heap)

    def _get_payload(self) -> list:
        return self.heap.get(self.heap_id).payload

    def length(self) -> RuntimeValue:
        return NumberValue(len(self._get_payload()))
        
    def get(self, key: RuntimeValue) -> RuntimeValue:
        if not isinstance(key, NumberValue):
            raise Exception("List index must be a number")
        idx = int(key.value)
        lst = self._get_payload()
        if 0 <= idx < len(lst):
            return lst[idx]
        import errors
        raise errors.IndexOutOfBoundsError(f"List index out of range: {idx}.", 0)
        
    def set(self, key: RuntimeValue, value: RuntimeValue):
        if not isinstance(key, NumberValue):
            raise Exception("List index must be a number")
        idx = int(key.value)
        lst = self._get_payload()
        if 0 <= idx < len(lst):
            lst[idx] = value
        else:
            raise Exception("List index out of bounds")
            
    def append(self, value: RuntimeValue):
        self._get_payload().append(value)
        
    def remove(self, key: RuntimeValue):
        if not isinstance(key, NumberValue):
            raise Exception("List index must be a number")
        idx = int(key.value)
        lst = self._get_payload()
        if 0 <= idx < len(lst):
            lst.pop(idx)
            
    def contains(self, value: RuntimeValue) -> RuntimeValue:
        for item in self._get_payload():
            if item.equals(value):
                return BooleanValue(True)
        return BooleanValue(False)
        
    def iterate(self):
        return self._get_payload()

    # Delegate base operations
    def stringify(self) -> str:
        return str(self.to_python())
        
    def to_python(self):
        return [val.to_python() for val in self._get_payload()]
        
    def equals(self, other: 'RuntimeValue') -> bool:
        if not isinstance(other, ListValue):
            return False
        return self.heap_id == other.heap_id

    def truthy(self) -> bool:
        return len(self._get_payload()) > 0
        
    def clone(self) -> 'RuntimeValue':
        return ListValue(self.heap_id, self.heap)
