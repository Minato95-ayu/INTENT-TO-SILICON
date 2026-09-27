#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpCode {
    Halt = 0x00,
    
    // Stack Operations
    PushConst = 0x01,
    Pop = 0x02,
    Dup = 0x03,
    
    // Math Operations
    Add = 0x10,
    Sub = 0x11,
    Mul = 0x12,
    Div = 0x13,
    
    // Control Flow
    Jmp = 0x20,
    JmpIfFalse = 0x21,
    Call = 0x22,
    Ret = 0x23,
    GetIter = 0x24,
    ForIter = 0x25,
    
    // Comparisons
    CmpEq = 0x26,
    CmpNeq = 0x27,
    CallComponent = 0x28,
    CmpLt = 0x29,
    CmpGt = 0x2A,
    CmpLte = 0x2B,
    CmpGte = 0x2C,
    PrepareCall = 0x2D,
    
    // State & Memory
    StoreState = 0x30,
    LoadState = 0x31,
    InitState = 0x32,
    EnterScope = 0x33,
    ExitScope = 0x34,
    
    // Kernel & External
    Dispatch = 0x40,
    BuildWidget = 0x50,
    Print = 0x51,
    MarkBlockStart = 0x52,
    
    // Backend Engine
    CreateModel = 0x60,
    RegisterRoute = 0x61,
}

impl From<u8> for OpCode {
    #[inline(always)]
    fn from(byte: u8) -> Self {
        unsafe { std::mem::transmute(byte) }
    }
}
