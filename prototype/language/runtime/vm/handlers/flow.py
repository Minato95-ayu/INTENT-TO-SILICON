from ir import Opcode

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
