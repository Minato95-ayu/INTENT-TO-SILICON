from ir import Opcode
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
            from errors import UndefinedVariableError
            vm._raise_runtime_error(f"Variable '{name}' not found.", cls=UndefinedVariableError)
        current_frame.stack.append(val)
    elif opcode == Opcode.STORE_VAR:
        name = current_frame.bytecode.names[operand]
        val = current_frame.stack.pop()
        vm.memory.store(name, val)
    elif opcode == Opcode.POP:
        current_frame.stack.pop()
