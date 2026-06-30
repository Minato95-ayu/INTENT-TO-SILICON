from typing import List, Dict, Any, Optional
from .models import Breakpoint, ExecutionMode
from .host import DebuggerHost
from runtime.values.base import RuntimeValue

class BreakpointManager:
    def __init__(self):
        self.breakpoints: Dict[int, Breakpoint] = {}
        self._next_id = 1
        
    def add_breakpoint(self, module: str, instruction_pointer: Optional[int] = None, span=None) -> Breakpoint:
        bp = Breakpoint(
            id=self._next_id,
            module=module,
            instruction_pointer=instruction_pointer,
            span=span
        )
        self.breakpoints[bp.id] = bp
        self._next_id += 1
        return bp
        
    def remove_breakpoint(self, bp_id: int) -> bool:
        if bp_id in self.breakpoints:
            del self.breakpoints[bp_id]
            return True
        return False
        
    def enable_breakpoint(self, bp_id: int, enabled: bool):
        if bp_id in self.breakpoints:
            self.breakpoints[bp_id].enabled = enabled
            
    def should_pause(self, module: str, ip: int) -> Optional[Breakpoint]:
        for bp in self.breakpoints.values():
            if not bp.enabled:
                continue
            if bp.module == module:
                if bp.instruction_pointer == ip:
                    return bp
                # Advanced SourceSpan matching can be added here
        return None


class ExecutionController:
    def __init__(self, host: DebuggerHost):
        self.host = host
        self.mode = ExecutionMode.RUN
        
        # Step Over/Out state
        self.target_depth = -1
        
    def pause(self):
        self.mode = ExecutionMode.PAUSED
        
    def resume(self):
        self.mode = ExecutionMode.RUN
        self.target_depth = -1
        
    def step_into(self):
        self.mode = ExecutionMode.STEP_INTO
        
    def step_over(self, current_depth: int):
        self.mode = ExecutionMode.STEP_OVER
        self.target_depth = current_depth
        
    def step_out(self, current_depth: int):
        self.mode = ExecutionMode.STEP_OUT
        self.target_depth = current_depth - 1

    def evaluate_pause(self, current_depth: int) -> bool:
        if self.mode == ExecutionMode.PAUSED:
            return True
        elif self.mode == ExecutionMode.STEP_INTO:
            return True
        elif self.mode == ExecutionMode.STEP_OVER:
            if current_depth <= self.target_depth:
                return True
        elif self.mode == ExecutionMode.STEP_OUT:
            if current_depth <= self.target_depth:
                return True
        return False


class VariableInspector:
    def __init__(self, vm):
        self.vm = vm
        
    def inspect_locals(self) -> Dict[str, Any]:
        """Resolves local variables for the current frame."""
        if not self.vm.frames:
            return {}
            
        current_frame = self.vm.frames[-1]
        
        # We need to map stack offsets to local names.
        # This requires the compiler to emit a local variables table in DebugInfo.
        # For now, if we don't have that metadata, we might not be able to name them.
        # But we return what we can. 
        # A full VariableInspector would read frame.stack and map using DebugInfo.
        # In this phase, we just expose the current stack or empty if no metadata.
        locals_dict = {}
        for k, v in self.vm.memory.get_locals().items():
            locals_dict[k] = v.to_python() if isinstance(v, RuntimeValue) else str(v)
            
        return locals_dict


class StackInspector:
    def __init__(self, vm):
        self.vm = vm
        
    def get_stack_trace(self) -> List['StackFrame']:
        """Returns the current stack trace using the VM's built-in mechanism."""
        # Using the VM's existing _build_frame_info
        trace = []
        for frame in self.vm.frames:
            trace.append(self.vm._build_frame_info(frame))
        return trace


class DebuggerRuntime:
    def __init__(self, host: DebuggerHost):
        self.host = host
        self.breakpoint_manager = BreakpointManager()
        self.execution_controller = ExecutionController(host)
        self.vm = None
        self.variable_inspector = None
        self.stack_inspector = None
        
    def attach(self, vm):
        """Attaches the debugger to a VirtualMachine."""
        self.vm = vm
        self.variable_inspector = VariableInspector(vm)
        self.stack_inspector = StackInspector(vm)
        
    def before_instruction(self, vm, current_frame, opcode, operand):
        """Called by the VM before executing an instruction."""
        module_name = current_frame.bytecode.name or 'main'
        if hasattr(current_frame.bytecode, 'debug_info') and current_frame.bytecode.debug_info:
            if current_frame.bytecode.debug_info.module_table:
                module_name = current_frame.bytecode.debug_info.module_table[0]
                
        ip = current_frame.ip
        current_depth = len(vm.frames)
        
        # 1. Check Breakpoints
        bp = self.breakpoint_manager.should_pause(module_name, ip)
        if bp:
            self.execution_controller.pause()
            self.host.on_breakpoint(self, vm, bp)
            
        # 2. Check Execution Controller Step logic
        if self.execution_controller.evaluate_pause(current_depth):
            self.execution_controller.pause()
            self.host.on_pause(self, vm)
