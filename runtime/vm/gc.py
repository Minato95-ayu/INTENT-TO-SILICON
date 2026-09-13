class GarbageCollector:
    __slots__ = ['allocator', 'vm']
    
    def __init__(self, allocator, vm=None):
        self.allocator = allocator
        self.vm = vm

    def incref(self, ptr: int):
        obj = self.allocator.pool.get(ptr)
        if obj:
            obj['ref_count'] += 1

    def decref(self, ptr: int):
        obj = self.allocator.pool.get(ptr)
        if obj:
            obj['ref_count'] -= 1
            if obj['ref_count'] <= 0:
                self.allocator.pool.free(ptr)
                
    def _mark(self, ptr: int, visited: set):
        if ptr in visited:
            return
        obj = self.allocator.pool.get(ptr)
        if not obj:
            return
        visited.add(ptr)
        
        # If the object holds references to other objects (like a list/dict of pointers), mark them too.
        val = obj.get('value')
        if isinstance(val, int):
            self._mark(val, visited)
        elif isinstance(val, list):
            for item in val:
                if isinstance(item, int):
                    self._mark(item, visited)
        elif isinstance(val, dict):
            for k, v in val.items():
                if isinstance(k, int):
                    self._mark(k, visited)
                if isinstance(v, int):
                    self._mark(v, visited)

    def collect(self):
        if not self.vm:
            return
            
        visited = set()
        
        # Trace from Global State
        for var_name, ptr in self.vm.state.items():
            if isinstance(ptr, int):
                self._mark(ptr, visited)
                
        # Trace from Call Stack (Frames)
        for frame in self.vm.frames:
            for ptr in frame.locals.values():
                if isinstance(ptr, int):
                    self._mark(ptr, visited)
            for ptr in frame.stack:
                if isinstance(ptr, int):
                    self._mark(ptr, visited)
                    
        # Trace from current VM value stack
        for ptr in self.vm.interpreter.stack:
            if isinstance(ptr, int):
                self._mark(ptr, visited)
                
        # Sweep
        all_ptrs = list(self.allocator.pool.pool.keys())
        swept = 0
        for ptr in all_ptrs:
            if ptr not in visited:
                self.allocator.pool.free(ptr)
                swept += 1
                
        return swept