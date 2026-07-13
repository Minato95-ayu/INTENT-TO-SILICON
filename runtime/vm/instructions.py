class Opcode:
    """AAYU Bytecode Instruction Set"""
    # Stack Operations
    PUSH_CONST = 0x01
    POP = 0x02
    DUP = 0x03
    
    # Math Operations
    ADD = 0x10
    SUB = 0x11
    MUL = 0x12
    DIV = 0x13
    
    # Control Flow
    JMP = 0x20
    JMP_IF_FALSE = 0x21
    CALL = 0x22
    RET = 0x23
    
    # State & Memory
    STORE_STATE = 0x30
    LOAD_STATE = 0x31
    
    # Kernel & External
    DISPATCH = 0x40
    BUILD_WIDGET = 0x50
    PRINT = 0x51
    
    # System
    HALT = 0xFF

def opcode_to_str(opcode):
    for k, v in Opcode.__dict__.items():
        if v == opcode:
            return k
    return "UNKNOWN"
