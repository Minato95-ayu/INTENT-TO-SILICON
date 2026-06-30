from .collection import CollectionValue
from .base import RuntimeValue
from .number import NumberValue
from .string import StringValue
from .boolean import BooleanValue
from .null import NullValue
from ..memory.heap import Heap

class MapValue(CollectionValue):
    def __init__(self, heap_id: int, heap: Heap):
        super().__init__(heap_id, "map", heap)

    def _get_payload(self) -> dict:
        obj = self.heap.get(self.heap_id)
        if obj is None:
            print(f'[FATAL] MapValue heap_id={self.heap_id} not found in heap with keys: {list(self.heap.objects.keys())}')
            raise Exception("Heap object not found!")
        return obj.payload

    def length(self) -> RuntimeValue:
        return NumberValue(len(self._get_payload()))
        
    def get(self, key: RuntimeValue) -> RuntimeValue:
        if not isinstance(key, StringValue):
            raise Exception("Map key must be a string")
        dct = self._get_payload()
        k_str = key.stringify()
        if k_str not in dct:
            import errors
            raise errors.IndexOutOfBoundsError(f"Key '{k_str}' not found in map.", 0)
        return dct[k_str]
        
    def set(self, key: RuntimeValue, value: RuntimeValue):
        if not isinstance(key, StringValue):
            raise Exception("Map key must be a string")
        self._get_payload()[key.stringify()] = value
            
    def append(self, value: RuntimeValue):
        raise Exception("Cannot append to a map. Use set(key, value) instead.")
        
    def remove(self, key: RuntimeValue):
        if not isinstance(key, StringValue):
            raise Exception("Map key must be a string")
        dct = self._get_payload()
        if key.stringify() in dct:
            del dct[key.stringify()]
            
    def contains(self, value: RuntimeValue) -> RuntimeValue:
        if not isinstance(value, StringValue):
            return BooleanValue(False)
        return BooleanValue(value.stringify() in self._get_payload())
        
    def iterate(self):
        # Could return list of keys or entries, for now just keys
        return self._get_payload().keys()

    def stringify(self) -> str:
        return str(self.to_python())
        
    def to_python(self):
        return {k: v.to_python() for k, v in self._get_payload().items()}
        
    def equals(self, other: 'RuntimeValue') -> bool:
        if not isinstance(other, MapValue):
            return False
        return self.heap_id == other.heap_id

    def truthy(self) -> bool:
        return len(self._get_payload()) > 0
        
    def clone(self) -> 'RuntimeValue':
        return MapValue(self.heap_id, self.heap)
