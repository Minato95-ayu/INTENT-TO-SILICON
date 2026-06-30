import os

vm_path = r"prototype\aayu_language\vm.py"
with open(vm_path, "r", encoding="utf-8") as f:
    vm_content = f.read()

# Replace imports
imports = """import sqlite3
from ir import Opcode, Bytecode
from errors import (
    AAYUError,
    AAYURuntimeError,
    UndefinedVariableError,
    DivisionByZeroError,
    IndexOutOfBoundsError,
    InvalidCallError,
    DatabaseError
)

from dataclasses import dataclass
from runtime.memory import MemoryManager
from runtime.values import RuntimeValue, NumberValue, StringValue, BooleanValue, NullValue, FunctionValue, ListValue, MapValue, NativeFunctionValue
"""
vm_content = vm_content.split("@dataclass")[1]
vm_content = imports + "\n@dataclass" + vm_content

# Update CallFrame
old_callframe = """class CallFrame:
    def __init__(self, bytecode: Bytecode, locals_dict: dict, frame_name: str = "main"):
        self.bytecode = bytecode
        self.locals = locals_dict
        self.ip = 0
        self.stack = []
        self.frame_name = frame_name
        self.source_file = getattr(bytecode, 'file', '')"""

new_callframe = """class CallFrame:
    def __init__(self, bytecode: Bytecode, frame_name: str = "main"):
        self.bytecode = bytecode
        self.ip = 0
        self.stack = []
        self.frame_name = frame_name
        self.source_file = getattr(bytecode, 'file', '')"""
vm_content = vm_content.replace(old_callframe, new_callframe)

# Update VirtualMachine.__init__
vm_content = vm_content.replace("self.globals = {}", "self.memory = MemoryManager()\n        self.globals = {} # Kept for legacy compatibility if needed")

# Replace dispatch
old_dispatch = """        sub_vm.globals = dict(self.globals)
        sub_vm._register_stdlib()
        sub_vm.routes = self.routes
        
        req_map = {
            "path": path,
            "method": method,
            "_form_data": form_data or {},
            "dispatch_context": True
        }
        sub_vm.current_request = req_map
        
        param_name = handler_bc.parameters[0] if handler_bc.parameters else "req"
        
        sub_vm.run(handler_bc, initial_locals={param_name: req_map})"""

# We'll just patch the run method directly, which is simpler
run_start = vm_content.find("    def run(self")
run_end = vm_content.find("        except Exception as e:")
new_run = """    def run(self, bytecode: Bytecode, initial_globals: dict = None, initial_locals: dict = None):
        if initial_globals is not None:
            # Not fully supported with MemoryManager MVP but we'll try
            pass
        elif not self.globals:
            self._register_stdlib()
            
        self.output = []
        self.instruction_count = 0
        self.return_value = NullValue()
        
        main_frame = CallFrame(bytecode, "main")
        self.frames = [main_frame]
        
        # Initialize memory for this run
        self.memory.set_constants(bytecode.constants)
        
        # Convert initial_locals to RuntimeValues
        init_locs = {}
        if initial_locals:
            for k, v in initial_locals.items():
                if isinstance(v, dict):
                    # Simple conversion for request map
                    map_val = MapValue()
                    for dk, dv in v.items():
                        map_val.set(dk, StringValue(str(dv)))
                    init_locs[k] = map_val
                elif isinstance(v, RuntimeValue):
                    init_locs[k] = v
                else:
                    init_locs[k] = StringValue(str(v))
                    
        self.memory.push_frame(init_locs)
        
        import time
        t_start = time.perf_counter()
        try:
            while self.frames:
                self.instruction_count += 1
                current_frame = self.frames[-1]
                
                if current_frame.ip >= len(current_frame.bytecode.instructions):
                    self.frames.pop()
                    self.memory.pop_frame()
                    continue
                    
                instruction = current_frame.bytecode.instructions[current_frame.ip]
                opcode = instruction.opcode
                operand = instruction.operand
                
                if opcode == Opcode.LOAD_CONST:
                    raw_val = current_frame.bytecode.constants[operand]
                    if isinstance(raw_val, (int, float)):
                        val = NumberValue(raw_val)
                    elif isinstance(raw_val, str):
                        val = StringValue(raw_val)
                    elif isinstance(raw_val, bool):
                        val = BooleanValue(raw_val)
                    elif raw_val is None:
                        val = NullValue()
                    elif isinstance(raw_val, Bytecode):
                        val = FunctionValue(raw_val.name, raw_val)
                    else:
                        val = NullValue()
                    current_frame.stack.append(val)
                    
                elif opcode == Opcode.STORE_VAR:
                    val = current_frame.stack.pop()
                    name = current_frame.bytecode.names[operand]
                    self.memory.store(name, val)
                        
                elif opcode == Opcode.LOAD_VAR:
                    name = current_frame.bytecode.names[operand]
                    val = self.memory.load(name)
                    current_frame.stack.append(val)
                    
                elif opcode == Opcode.ADD:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(NumberValue(left.value + right.value))
                    elif isinstance(left, StringValue) or isinstance(right, StringValue):
                        current_frame.stack.append(StringValue(left.to_string() + right.to_string()))
                    else:
                        self._raise_runtime_error(f"Cannot add {left.type_name()} and {right.type_name()}")
                        
                elif opcode == Opcode.SUB:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(NumberValue(left.value - right.value))
                    else:
                        self._raise_runtime_error("Subtraction requires numbers")
                        
                elif opcode == Opcode.MUL:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(NumberValue(left.value * right.value))
                    else:
                        self._raise_runtime_error("Multiplication requires numbers")
                        
                elif opcode == Opcode.DIV:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        if right.value == 0:
                            raise DivisionByZeroError("Division by zero", 0)
                        current_frame.stack.append(NumberValue(left.value / right.value))
                    else:
                        self._raise_runtime_error("Division requires numbers")
                        
                elif opcode == Opcode.MOD:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        if right.value == 0:
                            raise DivisionByZeroError("Modulo by zero", 0)
                        current_frame.stack.append(NumberValue(left.value % right.value))
                    else:
                        self._raise_runtime_error("Modulo requires numbers")
                        
                elif opcode == Opcode.NEG:
                    val = current_frame.stack.pop()
                    if isinstance(val, NumberValue):
                        current_frame.stack.append(NumberValue(-val.value))
                    else:
                        self._raise_runtime_error("Negation requires number")
                    
                elif opcode == Opcode.EQ:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(BooleanValue(left.equals(right)))
                    
                elif opcode == Opcode.LT:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(BooleanValue(left.value < right.value))
                    else:
                        self._raise_runtime_error("Less-than requires numbers")
                        
                elif opcode == Opcode.GT:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(BooleanValue(left.value > right.value))
                    else:
                        self._raise_runtime_error("Greater-than requires numbers")
                    
                elif opcode == Opcode.JUMP:
                    current_frame.ip += operand
                    continue
                    
                elif opcode == Opcode.JUMP_IF_FALSE:
                    condition = current_frame.stack.pop()
                    if not condition.truthy():
                        current_frame.ip += operand
                        continue
                        
                elif opcode == Opcode.JUMP_BACKWARD:
                    current_frame.ip -= operand
                    continue
                        
                elif opcode == Opcode.CALL or opcode == Opcode.CALL_TASK:
                    n_args = operand
                    args = []
                    for _ in range(n_args):
                        args.append(current_frame.stack.pop())
                    args.reverse()
                    
                    fn_obj = current_frame.stack.pop()
                    
                    # Native functions / stdlib
                    if isinstance(fn_obj, NativeFunctionValue):
                        ret = fn_obj.call_fn(args)
                        current_frame.stack.append(ret if ret is not None else NullValue())
                    elif getattr(fn_obj, 'name', None) == "print":
                        val = args[0].to_string() if args else ""
                        print(val)
                        self.output.append(val)
                        current_frame.stack.append(NullValue())
                    elif isinstance(fn_obj, FunctionValue):
                        # Create new frame for function
                        func_bc = fn_obj.bytecode
                        func_frame = CallFrame(func_bc, func_bc.name)
                        
                        # Bind parameters
                        locals_dict = {}
                        for i, param in enumerate(func_bc.parameters):
                            locals_dict[param] = args[i] if i < len(args) else NullValue()
                            
                        self.frames.append(func_frame)
                        self.memory.push_frame(locals_dict)
                        # Switch constants pool
                        # Wait, we need to save the old constants pool or bind constants to bytecode.
                        # For MVP, assuming constants are flattened or we can fetch from bytecode directly:
                        self.memory.set_constants(func_bc.constants)
                        continue # Start executing the new frame
                    else:
                        # Legacy support for python functions in globals
                        if callable(fn_obj):
                            # Convert args to python
                            py_args = [a.value if hasattr(a, 'value') else a for a in args]
                            ret = fn_obj(*py_args)
                            current_frame.stack.append(StringValue(str(ret)) if ret is not None else NullValue())
                        else:
                            self._raise_runtime_error(f"Not callable: {fn_obj.type_name()}")
                        
                elif opcode == Opcode.RETURN:
                    if current_frame.stack:
                        ret_val = current_frame.stack.pop()
                    else:
                        ret_val = NullValue()
                        
                    self.frames.pop()
                    self.memory.pop_frame()
                    
                    if self.frames:
                        # Restore previous frame's constants
                        self.memory.set_constants(self.frames[-1].bytecode.constants)
                        self.frames[-1].stack.append(ret_val)
                    else:
                        self.return_value = ret_val
                    continue
                    
                elif opcode == Opcode.POP:
                    if current_frame.stack:
                        current_frame.stack.pop()
                        
                else:
                    self._raise_runtime_error(f"VM Error: Unimplemented opcode {opcode}")
                    
                current_frame.ip += 1

"""

vm_content = vm_content[:run_start] + new_run + vm_content[run_end:]

with open(vm_path, "w", encoding="utf-8") as f:
    f.write(vm_content)
print("Updated vm.py successfully")
