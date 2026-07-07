"""
=============================================================================
FILE: flow.py
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

def handle_flow(opcode, operand, current_frame, vm):
    if opcode == Opcode.JUMP:
        current_frame.ip += operand
        return True # Handled PC change
    elif opcode == Opcode.JUMP_IF_FALSE:
        condition = current_frame.stack[-1]
        if not condition.truthy():
            current_frame.ip += operand
            return True
    elif opcode == Opcode.JUMP_IF_TRUE:
        condition = current_frame.stack[-1]
        if condition.truthy():
            current_frame.ip += operand
            return True
    elif opcode == Opcode.JUMP_BACKWARD:
        current_frame.ip -= operand
        return True
    return False
