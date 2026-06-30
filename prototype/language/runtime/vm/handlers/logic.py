from ir import Opcode
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
