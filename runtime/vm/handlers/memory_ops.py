"""
=============================================================================
FILE: memory_ops.py
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
from ...values.null import NullValue
from ...values.list import ListValue
from ...values.map import MapValue

def handle_memory(opcode, operand, current_frame, vm):
    if opcode == Opcode.LOAD_CONST:
        val = vm.memory.load_constant(operand)
        current_frame.stack.append(val)
    elif opcode == Opcode.LOAD_VAR:
        name = current_frame.bytecode.names[operand]
        val = vm.memory.load(name)
        if isinstance(val, NullValue):
            from compiler.frontend.errors import UndefinedVariableError
            vm._raise_runtime_error(f"Variable '{name}' not found.", cls=UndefinedVariableError)
        current_frame.stack.append(val)
    elif opcode == Opcode.STORE_VAR:
        name = current_frame.bytecode.names[operand]
        val = current_frame.stack.pop()
        vm.memory.store(name, val)
    elif opcode == Opcode.POP:
        current_frame.stack.pop()
