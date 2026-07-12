from .base import RuntimeValue
import heapq

class HeapValue(RuntimeValue):
    def __init__(self, elements=None):
        self.elements = elements if elements else []
        heapq.heapify(self.elements)
        
    def type_name(self) -> str:
        return "Heap"
        
    def truthy(self) -> bool:
        return len(self.elements) > 0
        
    def equals(self, other: 'RuntimeValue') -> bool:
        if not isinstance(other, HeapValue): return False
        return self.elements == other.elements
        
    def clone(self) -> 'RuntimeValue':
        return HeapValue(list(self.elements))
        
    def stringify(self) -> str:
        return f"Heap({self.elements})"
        
    def to_python(self):
        return self.elements
