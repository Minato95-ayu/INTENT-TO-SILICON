class Debugger:
    """Basic debugging utilities for the VM."""
    def __init__(self, vm):
        self.vm = vm
        self.breakpoints = set()
        
    def add_breakpoint(self, ip: int):
        self.breakpoints.add(ip)
        
    def check_breakpoint(self):
        if self.vm.registers.ip in self.breakpoints:
            print(f"[DEBUG] Breakpoint hit at IP: {self.vm.registers.ip}")
            # Pause execution, wait for resume (not implemented in this mock)
