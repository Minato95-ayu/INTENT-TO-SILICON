import threading
from .breakpoint import BreakpointManager
from .stepping import SteppingController
from .timeline import Timeline
from .snapshot import VMSnapshot

class Debugger:
    """The central orchestrator sitting above the VM."""
    
    def __init__(self, vm):
        self.vm = vm
        self.breakpoints = BreakpointManager()
        self.timeline = Timeline()
        
        # Set by compiler payload
        self.debug_map = {} 
        self.stepping = SteppingController(self.debug_map)
        
        self.is_paused = False
        self.pause_event = threading.Event()
        self.pause_event.set() # Initially running
        
        self.snapshot = None
        
    def load_debug_symbols(self, debug_symbols: dict):
        """Loads the .debug symbols from the compiler."""
        self.debug_map = debug_symbols.get("map", {})
        self.stepping.debug_map = self.debug_map
        
    def check_hook(self, ip: int):
        """Called by the VM's interpreter loop on every instruction."""
        if not self.debug_map:
            return
            
        current_line = None
        if ip in self.debug_map:
            current_line = self.debug_map[ip]["line"]
            
        should_pause = False
        
        # 1. Check Breakpoints
        if current_line is not None:
            if self.breakpoints.should_break(current_line):
                should_pause = True
                self.timeline.record("breakpoint", f"Hit at line {current_line}")
                
        # 2. Check Stepping
        if not should_pause and self.stepping.mode:
            current_depth = len(self.vm.call_stack.frames)
            # We assume target depth was saved during step request, mocked here
            if self.stepping.should_break(ip, current_depth, current_depth):
                should_pause = True
                
        if should_pause or self.is_paused:
            self._halt(ip)
            
    def pause(self):
        self.is_paused = True
        
    def resume(self):
        self.is_paused = False
        self.stepping.mode = None
        self.snapshot = None
        self.pause_event.set()
        
    def step_into(self):
        self.stepping.step_into()
        self.pause_event.set()
        
    def step_over(self):
        if self.vm.registers.ip in self.debug_map:
            self.stepping.step_over(self.debug_map[self.vm.registers.ip]["line"])
            self.pause_event.set()
            
    def step_out(self):
        self.stepping.step_out()
        self.pause_event.set()
        
    def _halt(self, ip):
        self.is_paused = True
        self.snapshot = VMSnapshot(self.vm)
        self.pause_event.clear()
        
        # Block the VM thread until pause_event is set by DAP server
        self.pause_event.wait()
