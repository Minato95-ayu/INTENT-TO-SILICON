from runtime.vm.instructions import Opcode
from runtime.vm.exceptions import InvalidBytecodeError

# Opcodes that take a constant pool index as operand
_POOL_OPCODES = {Opcode.PUSH_CONST, Opcode.STORE_STATE, Opcode.LOAD_STATE}

# Opcodes that take a jump/call target as operand
_JUMP_OPCODES = {Opcode.JMP, Opcode.JMP_IF_FALSE, Opcode.CALL}

# All valid opcodes
_ALL_OPCODES = {v for k, v in Opcode.__dict__.items() if not k.startswith('__') and isinstance(v, int)}

INSTRUCTION_WIDTH = 3

class Validator:
    """Pre-flight verifier for fixed-width bytecode.
    
    Validates:
    - All opcodes are recognized
    - Constant pool indices are in bounds
    - Jump/call targets are valid instruction boundaries
    - Bytecode length is a multiple of INSTRUCTION_WIDTH
    - Stack underflow/overflow detection (basic)
    """
    
    @staticmethod
    def validate(bytecode, constant_pool):
        length = len(bytecode)
        
        # Check fixed-width alignment
        if length % INSTRUCTION_WIDTH != 0:
            raise InvalidBytecodeError(
                f"Bytecode length {length} is not a multiple of {INSTRUCTION_WIDTH}",
                0
            )
        
        ip = 0
        stack_depth = 0
        max_stack = 256  # configurable stack limit
        
        while ip < length:
            opcode = bytecode[ip]
            operand = (bytecode[ip + 1] << 8) | bytecode[ip + 2]
            
            # Check unknown opcode
            if opcode not in _ALL_OPCODES:
                raise InvalidBytecodeError(f"Unknown opcode 0x{opcode:02X}", ip)
            
            # Check constant pool bounds
            if opcode in _POOL_OPCODES:
                pool_len = len(constant_pool) if isinstance(constant_pool, list) else constant_pool
                if operand >= pool_len:
                    raise InvalidBytecodeError(
                        f"Constant pool index {operand} out of bounds (pool size: {pool_len})",
                        ip
                    )
            
            # Check jump target bounds and alignment
            if opcode in _JUMP_OPCODES:
                if operand != 0xFFFF:  # 0xFFFF = unresolved relocation placeholder
                    if operand >= length:
                        raise InvalidBytecodeError(
                            f"Jump target {operand} out of bounds (bytecode length: {length})",
                            ip
                        )
                    if operand % INSTRUCTION_WIDTH != 0:
                        raise InvalidBytecodeError(
                            f"Jump target {operand} is not aligned to instruction boundary",
                            ip
                        )
            
            # Basic stack depth tracking
            if opcode == Opcode.PUSH_CONST:
                stack_depth += 1
            elif opcode == Opcode.LOAD_STATE:
                stack_depth += 1
            elif opcode in (Opcode.POP, Opcode.PRINT):
                if stack_depth <= 0:
                    raise InvalidBytecodeError("Potential stack underflow", ip)
                stack_depth -= 1
            elif opcode in (Opcode.ADD, Opcode.SUB, Opcode.MUL, Opcode.DIV):
                if stack_depth < 2:
                    raise InvalidBytecodeError("Potential stack underflow (binary op)", ip)
                stack_depth -= 1  # pops 2, pushes 1
            elif opcode == Opcode.STORE_STATE:
                if stack_depth <= 0:
                    raise InvalidBytecodeError("Potential stack underflow (store)", ip)
                stack_depth -= 1
            elif opcode == Opcode.BUILD_WIDGET:
                if stack_depth <= 0:
                    raise InvalidBytecodeError("Potential stack underflow (build_widget)", ip)
                stack_depth -= 1
            elif opcode == Opcode.DUP:
                stack_depth += 1
            
            if stack_depth > max_stack:
                raise InvalidBytecodeError(
                    f"Potential stack overflow (depth: {stack_depth})",
                    ip
                )
            
            ip += INSTRUCTION_WIDTH
                
        return True
