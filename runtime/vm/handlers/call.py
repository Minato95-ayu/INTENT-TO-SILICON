"""
=============================================================================
FILE: call.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from compiler.frontend.ir import Opcode
from ...values.function import FunctionValue, NativeFunctionValue
from ..frame import CallFrame

def handle_call(opcode, operand, current_frame, vm):
    if opcode in (Opcode.CALL, Opcode.CALL_TASK):
        args = []
        for _ in range(operand):
            args.insert(0, current_frame.stack.pop())
            
        func_val = current_frame.stack.pop()
        
        if isinstance(func_val, NativeFunctionValue):
            import inspect
            sig = inspect.signature(func_val.call_fn)
            if len(sig.parameters) >= 2:
                res = func_val.call_fn(args, vm)
            else:
                res = func_val.call_fn(args)
            from ...values.null import NullValue
            if res is None:
                current_frame.stack.append(NullValue())
            else:
                current_frame.stack.append(res)
        elif isinstance(func_val, FunctionValue):
            current_frame.ip += 1 # Advance caller IP before suspending
            
            func_bc = func_val.bytecode
            func_frame = CallFrame(func_bc, func_bc.name)
            
            locals_dict = {}
            for i, param in enumerate(func_bc.parameters):
                param_name = param[0] if isinstance(param, tuple) else param
                locals_dict[param_name] = args[i] if i < len(args) else NullValue()
                
            vm.frames.append(func_frame)
            vm.memory.push_frame(locals_dict)
            vm.memory.set_constants(func_bc.constants)
            
            return True # Tell VM not to advance IP (we already advanced caller, and new frame starts at 0)
        else:
            vm._raise_runtime_error(f"Not callable: {func_val.type_name()}")
            
    return False
