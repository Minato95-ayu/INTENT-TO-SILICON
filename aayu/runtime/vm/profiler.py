class Profiler:
    """Collects execution telemetry for benchmarking."""
    def __init__(self):
        self.instruction_count = 0
        self.peak_memory_bytes = 0
        self.allocations = 0
        self.start_time = 0
        self.end_time = 0
        
    def tick(self, heap_active_bytes=0):
        self.instruction_count += 1
        if heap_active_bytes > self.peak_memory_bytes:
            self.peak_memory_bytes = heap_active_bytes
            
    def record_allocation(self):
        self.allocations += 1
        
    def summary(self):
        return {
            'instructions': self.instruction_count,
            'peak_memory': self.peak_memory_bytes,
            'allocations': self.allocations,
            'time': self.end_time - self.start_time
        }
