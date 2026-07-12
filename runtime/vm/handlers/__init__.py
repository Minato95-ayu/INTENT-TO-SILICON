"""
=============================================================================
FILE: __init__.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from .math import handle_math
from .logic import handle_logic
from .memory_ops import handle_memory
from .flow import handle_flow
from .call import handle_call
from compiler.frontend.ir import Opcode

def dispatch(opcode, operand, current_frame, vm):
    if opcode in (Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV, Opcode.MOD, Opcode.NEG):
        handle_math(opcode, current_frame, vm)
    elif opcode in (Opcode.EQ, Opcode.NE, Opcode.LT, Opcode.LE, Opcode.GT, Opcode.GE, Opcode.NOT):
        handle_logic(opcode, current_frame, vm)
    elif opcode in (Opcode.LOAD_CONST, Opcode.LOAD_VAR, Opcode.STORE_VAR, Opcode.POP):
        handle_memory(opcode, operand, current_frame, vm)
    elif opcode in (Opcode.JUMP, Opcode.JUMP_IF_FALSE, Opcode.JUMP_IF_TRUE, Opcode.JUMP_BACKWARD):
        return handle_flow(opcode, operand, current_frame, vm)
    elif opcode in (Opcode.CALL, Opcode.CALL_TASK):
        return handle_call(opcode, operand, current_frame, vm)
    elif opcode == Opcode.MAKE_LIST:
        from .collections_ops import handle_make_list
        handle_make_list(vm, current_frame, operand)
    elif opcode == Opcode.MAKE_MAP:
        from .collections_ops import handle_make_map
        handle_make_map(vm, current_frame, operand)
    elif opcode == Opcode.RETURN:
        pass # Handle in VM loop directly for now
    elif opcode in (Opcode.TRY_BEGIN, Opcode.TRY_END, Opcode.THROW, Opcode.PANIC,
                    Opcode.FINALLY_BEGIN, Opcode.FINALLY_END):
        pass # Handled directly in VM loop (Phase 4.1)
    else:
        vm._raise_runtime_error(f"Unknown opcode: {opcode}")
    return False
