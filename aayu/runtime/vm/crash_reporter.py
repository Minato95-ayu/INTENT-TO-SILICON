import json

class CrashReporter:
    """Generates structured post-mortem crash reports."""
    
    @staticmethod
    def generate(exception, vm):
        report = {
            "error_type": type(exception).__name__,
            "message": str(exception),
            "ip": vm.registers.ip,
            "sp": vm.registers.sp,
            "call_depth": vm.call_stack.depth(),
            "value_stack_depth": vm.value_stack.depth(),
            "heap_objects": len(vm.heap.allocator.pool.pool),
            "instructions_executed": vm.profiler.instruction_count
        }
        
        # In a real system, this would write to a log file or stderr
        return "\n=== VM CRASH REPORT ===\n" + json.dumps(report, indent=2) + "\n=======================\n"
