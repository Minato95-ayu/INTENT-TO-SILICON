from ir import Opcode
from ...values.number import NumberValue
from ...values.string import StringValue

def handle_math(opcode, current_frame, vm):
    if opcode == Opcode.ADD:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        try:
            current_frame.stack.append(left.add(right))
        except Exception as ex:
            vm._raise_runtime_error(str(ex))
    elif opcode == Opcode.SUB:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        try:
            current_frame.stack.append(left.sub(right))
        except Exception as ex:
            vm._raise_runtime_error(str(ex))
    elif opcode == Opcode.MUL:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        try:
            current_frame.stack.append(left.mul(right))
        except Exception as ex:
            vm._raise_runtime_error(str(ex))
    elif opcode == Opcode.DIV:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        try:
            current_frame.stack.append(left.div(right))
        except Exception as ex:
            if "zero" in str(ex).lower():
                from errors import DivisionByZeroError
                raise DivisionByZeroError(str(ex), 0)
            vm._raise_runtime_error(str(ex))
    elif opcode == Opcode.MOD:
        right = current_frame.stack.pop()
        left = current_frame.stack.pop()
        try:
            current_frame.stack.append(left.mod(right)) # Assuming mod is added to RuntimeValue, if not we will just use python % for now, but user said 'har opcode RuntimeValue methods ko call kare'. Wait, user didn't list mod in the 11 methods. We'll leave it as left.mod(right) and we will add mod to RuntimeValue in base.py later if needed. Actually we added mod to NumberValue in earlier phase. But user's list didn't have mod. Let's just catch it.
        except AttributeError:
            vm._raise_runtime_error(f"{left.type_name()} does not support modulo")
        except Exception as ex:
            vm._raise_runtime_error(str(ex))
    elif opcode == Opcode.NEG:
        val = current_frame.stack.pop()
        if hasattr(val, 'value'):
            current_frame.stack.append(NumberValue(-val.value)) # quick hack for neg
        else:
            vm._raise_runtime_error("Negation requires number")
