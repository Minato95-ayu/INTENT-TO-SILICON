from aayu.runtime.vm.exceptions import InvalidBytecodeError
from aayu.runtime.vm.instructions import Opcode

class Validator:
    """Pre-flight verifier for bytecode."""
    
    @staticmethod
    def validate(bytecode, constant_pool):
        ip = 0
        length = len(bytecode)
        
        while ip < length:
            opcode = bytecode[ip]
            
            # Check Unknown Opcode
            if not any(v == opcode for k,v in Opcode.__dict__.items() if not k.startswith('__')):
                raise InvalidBytecodeError(f"Unknown opcode 0x{opcode:02X}", ip)
                
            if opcode == Opcode.PUSH_CONST:
                if ip + 2 >= length:
                    raise InvalidBytecodeError("PUSH_CONST missing operand", ip)
                idx = (bytecode[ip+1] << 8) | bytecode[ip+2]
                if idx >= len(constant_pool):
                    raise InvalidBytecodeError(f"Constant pool index out of bounds: {idx}", ip)
                ip += 3
            elif opcode in (Opcode.JMP, Opcode.JMP_IF_FALSE, Opcode.CALL):
                if ip + 2 >= length:
                    raise InvalidBytecodeError("Jump instruction missing operand", ip)
                target = (bytecode[ip+1] << 8) | bytecode[ip+2]
                if target >= length and target != 0xFFFF: # 0xFFFF might be native call
                    raise InvalidBytecodeError(f"Jump target out of bounds: {target}", ip)
                ip += 3
            elif opcode in (Opcode.STORE_STATE, Opcode.LOAD_STATE):
                if ip + 2 >= length:
                    raise InvalidBytecodeError("State instruction missing operand", ip)
                idx = (bytecode[ip+1] << 8) | bytecode[ip+2]
                if idx >= len(constant_pool):
                    raise InvalidBytecodeError(f"Constant pool index out of bounds: {idx}", ip)
                ip += 3
            elif opcode in (Opcode.BUILD_WIDGET, Opcode.PRINT):
                if ip + 2 >= length:
                    raise InvalidBytecodeError("Instruction missing operand", ip)
                ip += 3
            else:
                ip += 3
                
        return True
