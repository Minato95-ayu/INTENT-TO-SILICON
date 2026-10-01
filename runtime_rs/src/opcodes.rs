#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpCode {
    Halt = 0x00,
    
    // Stack Operations
    PushConst = 0x01,
    Pop = 0x02,
    Dup = 0x03,
    
    // Math Operations (Self-Hosted Compiler Emits these)
    Add = 16,        // 0x10
    Sub = 17,        // 0x11
    Mul = 18,        // 0x12
    Div = 19,        // 0x13
    Mod = 20,
    
    // Type Casting
    CastInt = 21,
    CastStr = 22,
    
    // Control Flow
    Jmp = 32,        // 0x20
    JmpIfFalse = 33, // 0x21
    Call = 34,       // 0x22
    Ret = 35,        // 0x23
    
    // Comparisons
    CmpEq = 38,      // 0x26
    CmpNeq = 39,     // 0x27
    CmpLt = 41,      // 0x29
    CmpGt = 42,      // 0x2A
    CmpLte = 43,     // 0x2B
    CmpGte = 44,     // 0x2C
    
    // State & Memory
    StoreState = 48, // 0x30
    LoadState = 49,  // 0x31
    InitState = 50,  // 0x32
    
    // Kernel & External
    Print = 81,      // 0x51
    ReturnValue = 98, // 0x62
    
    // ----------------------------------------------------
    // ADVANCED COLLECTIONS (Array & Dict Heaps)
    // ----------------------------------------------------
    BuildDict = 128,  // OP_BUILD_DICT (from compiler.aayu)
    CreateArray = 134, // OP_CREATE_ARRAY (from compiler.aayu)
    LoadSubscr = 136,  // OP_LOAD_SUBSCR (from compiler.aayu)
    StoreSubscr = 137, // OP_STORE_SUBSCR (from compiler.aayu)
    
    // String Core (Python-like manipulation)
    StringConcat = 140,
    StringSlice = 141,
    StringLen = 142,
    
    // IO Core
    ConsoleRead = 150,
}

impl From<u8> for OpCode {
    #[inline(always)]
    fn from(byte: u8) -> Self {
        unsafe { std::mem::transmute(byte) }
    }
}
