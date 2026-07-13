class ObjectPool:
    """Manages the raw memory allocation for VM objects."""
    def __init__(self):
        self.pool = {}
        self.next_ptr = 1

    def allocate(self, obj_type, value):
        ptr = self.next_ptr
        self.next_ptr += 1
        # Each object has a type, value, and a reference count (initially 0)
        self.pool[ptr] = {'type': obj_type, 'value': value, 'ref_count': 0}
        return ptr
        
    def free(self, ptr):
        if ptr in self.pool:
            del self.pool[ptr]

    def get(self, ptr):
        return self.pool.get(ptr)
        
class Allocator:
    def __init__(self):
        self.pool = ObjectPool()
        
    def alloc_string(self, val: str) -> int:
        return self.pool.allocate('string', val)
        
    def alloc_int(self, val: int) -> int:
        return self.pool.allocate('int', val)
        
    def alloc_widget(self, w_type: str, props: dict) -> int:
        return self.pool.allocate('widget', {'type': w_type, 'props': props, 'children': []})
