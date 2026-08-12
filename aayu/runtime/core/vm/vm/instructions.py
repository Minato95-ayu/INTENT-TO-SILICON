class Opcode:
    """AAYU Bytecode Instruction Set"""
    # Stack Operations
    PUSH_CONST = 0x01
    POP = 0x02
    DUP = 0x03
    
    # Locals & Globals
    LOAD_LOCAL = 0x04
    STORE_LOCAL = 0x05
    LOAD_GLOBAL = 0x06
    STORE_GLOBAL = 0x07
    LOAD_UPVALUE = 0x08
    STORE_UPVALUE = 0x09
    
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
    GET_ITER = 0x24
    FOR_ITER = 0x25
    
    # Comparisons
    CMP_EQ = 0x26
    CMP_NEQ = 0x27
    CMP_LT = 0x29
    CMP_GT = 0x2A
    CMP_LTE = 0x2B
    CMP_GTE = 0x2C
    
    # Components
    CALL_COMPONENT = 0x28
    
    # State & Memory
    STORE_STATE = 0x30
    LOAD_STATE = 0x31
    INIT_STATE = 0x32
    
    # Kernel & External
    DISPATCH = 0x40
    BUILD_WIDGET = 0x50
    PRINT = 0x51
    MARK_BLOCK_START = 0x52
    
    # Backend Engine
    CREATE_MODEL = 0x60
    REGISTER_ROUTE = 0x61
    RETURN_VALUE = 0x62
    CHECK_AUTH = 0x63
    
    # UI Engine
    SET_THEME = 0x70
    DECLARE_THEME = 0x72
    NAVIGATE = 0x71
    
    # Phase 1.5 Features
    BUILD_DICT = 0x80
    OP_ASYNC_CALL = 0x81
    SET_BINDING = 0x82
    DECLARE_VALIDATION = 0x83
    SET_ANIMATION = 0x84
    
    # Exception Handling
    SETUP_EXCEPT = 0x90
    POP_EXCEPT = 0x91
    THROW = 0x92
    RETHROW = 0x93
    SETUP_FINALLY = 0x94
    EXEC_FINALLY = 0x95
    DECLARE_LIFECYCLE = 0x85
    CREATE_CLOSURE = 0x8A
    CREATE_ARRAY = 0x86
    GET_LENGTH = 0x87
    LOAD_SUBSCR = 0x88
    STORE_SUBSCR = 0x89
    
    # System
    HALT = 0xFF

def opcode_to_str(opcode):
    for k, v in Opcode.__dict__.items():
        if v == opcode:
            return k
    return "UNKNOWN"
