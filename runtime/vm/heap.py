from runtime.vm.allocator import Allocator
from runtime.vm.gc import GarbageCollector

class Heap:
    """
    Central memory manager exposing a reference table.
    Bridges Allocator and GarbageCollector.
    """
    def __init__(self):
        self.allocator = Allocator()
        self.gc = GarbageCollector(self.allocator)
        
    def allocate(self, type_name: str, value: any) -> int:
        return self.allocator.pool.allocate(type_name, value)
        
    def read(self, ptr: int):
        return self.allocator.pool.get(ptr)
        
    def write(self, ptr: int, value: any):
        obj = self.allocator.pool.get(ptr)
        if obj:
            obj['value'] = value
            
    def retain(self, ptr: int):
        self.gc.incref(ptr)
        
    def release(self, ptr: int):
        self.gc.decref(ptr)
        
    def get_metrics(self):
        return {
            'active_objects': len(self.allocator.pool.pool),
            'allocated_bytes': len(self.allocator.pool.pool) * 64 # Approximation
        }
