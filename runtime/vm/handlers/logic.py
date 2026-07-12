"""
=============================================================================
FILE: logic.py
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
from ...values.boolean import BooleanValue

def handle_logic(opcode, current_frame, vm):
    if opcode == Opcode.EQ:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        current_frame.stack.append(BooleanValue(left.equals(right)))
    elif opcode == Opcode.NE:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        current_frame.stack.append(BooleanValue(not left.equals(right)))
    elif opcode == Opcode.LT:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        try:
            current_frame.stack.append(BooleanValue(left.compare(right) < 0))
        except Exception as ex:
            vm._raise_runtime_error(str(ex))
    elif opcode == Opcode.LE:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        try:
            current_frame.stack.append(BooleanValue(left.compare(right) <= 0))
        except Exception as ex:
            vm._raise_runtime_error(str(ex))
    elif opcode == Opcode.GT:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        try:
            current_frame.stack.append(BooleanValue(left.compare(right) > 0))
        except Exception as ex:
            vm._raise_runtime_error(str(ex))
    elif opcode == Opcode.GE:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        try:
            current_frame.stack.append(BooleanValue(left.compare(right) >= 0))
        except Exception as ex:
            vm._raise_runtime_error(str(ex))
    elif opcode == Opcode.NOT:
        val = current_frame.stack.pop()
        current_frame.stack.append(BooleanValue(not val.truthy()))
