"""
=============================================================================
FILE: patch_vm2.py
PURPOSE: Fixes or patches existing code
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles fixes or patches existing code.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import re
import os

vm_path = r"prototype\aayu_language\vm\vm.py"
with open(vm_path, "r", encoding="utf-8") as f:
    vm_content = f.read()

# Replace arithmetic ops in vm.py
# ADD
old_add = """                elif opcode == Opcode.ADD:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(NumberValue(left.value + right.value))
                    elif isinstance(left, StringValue) or isinstance(right, StringValue):
                        current_frame.stack.append(StringValue(left.to_string() + right.to_string()))
                    else:
                        self._raise_runtime_error(f"Cannot add {left.type_name()} and {right.type_name()}")"""
new_add = """                elif opcode == Opcode.ADD:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    try:
                        current_frame.stack.append(left.add(right))
                    except Exception as ex:
                        self._raise_runtime_error(str(ex))"""
vm_content = vm_content.replace(old_add, new_add)

# SUB
old_sub = """                elif opcode == Opcode.SUB:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(NumberValue(left.value - right.value))
                    else:
                        self._raise_runtime_error("Subtraction requires numbers")"""
new_sub = """                elif opcode == Opcode.SUB:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    try:
                        current_frame.stack.append(left.sub(right))
                    except Exception as ex:
                        self._raise_runtime_error(str(ex))"""
vm_content = vm_content.replace(old_sub, new_sub)

# MUL
old_mul = """                elif opcode == Opcode.MUL:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(NumberValue(left.value * right.value))
                    else:
                        self._raise_runtime_error("Multiplication requires numbers")"""
new_mul = """                elif opcode == Opcode.MUL:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    try:
                        current_frame.stack.append(left.mul(right))
                    except Exception as ex:
                        self._raise_runtime_error(str(ex))"""
vm_content = vm_content.replace(old_mul, new_mul)

# DIV
old_div = """                elif opcode == Opcode.DIV:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        if right.value == 0:
                            raise DivisionByZeroError("Division by zero", 0)
                        current_frame.stack.append(NumberValue(left.value / right.value))
                    else:
                        self._raise_runtime_error("Division requires numbers")"""
new_div = """                elif opcode == Opcode.DIV:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    try:
                        current_frame.stack.append(left.div(right))
                    except Exception as ex:
                        if "zero" in str(ex).lower():
                            raise DivisionByZeroError(str(ex), 0)
                        self._raise_runtime_error(str(ex))"""
vm_content = vm_content.replace(old_div, new_div)

# MOD
old_mod = """                elif opcode == Opcode.MOD:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        if right.value == 0:
                            raise DivisionByZeroError("Modulo by zero", 0)
                        current_frame.stack.append(NumberValue(left.value % right.value))
                    else:
                        self._raise_runtime_error("Modulo requires numbers")"""
new_mod = """                elif opcode == Opcode.MOD:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    try:
                        current_frame.stack.append(left.mod(right))
                    except Exception as ex:
                        if "zero" in str(ex).lower():
                            raise DivisionByZeroError(str(ex), 0)
                        self._raise_runtime_error(str(ex))"""
vm_content = vm_content.replace(old_mod, new_mod)


# Compare ops
# EQ is already there
new_eq = """                elif opcode == Opcode.EQ:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(BooleanValue(left.equals(right)))
                elif opcode == Opcode.NE:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(BooleanValue(not left.equals(right)))"""
vm_content = vm_content.replace("""                elif opcode == Opcode.EQ:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    current_frame.stack.append(BooleanValue(left.equals(right)))""", new_eq)

old_lt = """                elif opcode == Opcode.LT:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(BooleanValue(left.value < right.value))
                    else:
                        self._raise_runtime_error("Less-than requires numbers")"""
new_lt = """                elif opcode == Opcode.LT:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    try:
                        current_frame.stack.append(left.less_than(right))
                    except Exception as ex:
                        self._raise_runtime_error(str(ex))
                elif opcode == Opcode.LE:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    try:
                        current_frame.stack.append(left.less_than_or_equal(right))
                    except Exception as ex:
                        self._raise_runtime_error(str(ex))"""
vm_content = vm_content.replace(old_lt, new_lt)

old_gt = """                elif opcode == Opcode.GT:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    if isinstance(left, NumberValue) and isinstance(right, NumberValue):
                        current_frame.stack.append(BooleanValue(left.value > right.value))
                    else:
                        self._raise_runtime_error("Greater-than requires numbers")"""
new_gt = """                elif opcode == Opcode.GT:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    try:
                        current_frame.stack.append(left.greater_than(right))
                    except Exception as ex:
                        self._raise_runtime_error(str(ex))
                elif opcode == Opcode.GE:
                    right = current_frame.stack.pop()
                    left = current_frame.stack.pop()
                    try:
                        current_frame.stack.append(left.greater_than_or_equal(right))
                    except Exception as ex:
                        self._raise_runtime_error(str(ex))
                elif opcode == Opcode.NOT:
                    val = current_frame.stack.pop()
                    current_frame.stack.append(BooleanValue(not val.truthy()))
                elif opcode == Opcode.JUMP_IF_TRUE:
                    condition = current_frame.stack.pop()
                    if condition.truthy():
                        current_frame.ip += operand
                        continue"""
vm_content = vm_content.replace(old_gt, new_gt)

with open(vm_path, "w", encoding="utf-8") as f:
    f.write(vm_content)
print("Updated vm.py successfully")
