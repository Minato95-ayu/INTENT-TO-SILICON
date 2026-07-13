import copy

class VMSnapshot:
    """Immutable snapshot of the VM state when paused."""
    def __init__(self, vm):
        # We deeply copy or extract primitive state to prevent live mutation
        self.ip = vm.registers.ip
        self.registers = copy.deepcopy(vm.registers.__dict__)
        
        # Snapshot the call stack (just frames)
        self.call_stack = []
        for frame in vm.call_stack.frames:
            self.call_stack.append({
                "function": frame.function_name,
                "ip": frame.return_address,
                "locals": copy.deepcopy(frame.locals)
            })
            
        # Optional: Heap snapshot summary
        self.heap_summary = {
            "allocated": len(vm.heap.allocator.pool.pool)
        }
