from .base import RuntimeValue

class ReferenceValue(RuntimeValue):
    def __init__(self, heap_id: int, ref_type: str, heap):
        self.heap_id = heap_id
        self.ref_type = ref_type
        self.heap = heap

    def type_name(self) -> str:
        return self.ref_type
        
    def clone(self) -> 'RuntimeValue':
        # Stack only carries references, clone just duplicates the reference, not the heap object!
        return ReferenceValue(self.heap_id, self.ref_type, self.heap)
