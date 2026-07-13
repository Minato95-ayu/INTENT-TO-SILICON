class Opcode:
    """AAYU Bytecode Instruction Set
    
    All instructions are fixed-width: 3 bytes.
        [OPCODE: 1 byte] [OPERAND: 2 bytes big-endian]
    """
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
    
    # I/O
    PRINT = 0x50
    
    # UI
    BUILD_WIDGET = 0x60
    
    # System
    HALT = 0xFF

def opcode_to_str(opcode):
    for k, v in Opcode.__dict__.items():
        if not k.startswith('__') and v == opcode:
            return k
    return "UNKNOWN"
