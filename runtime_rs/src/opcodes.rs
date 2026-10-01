#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpCode {
    Halt = 0x00,
    PushConst = 0x01,
    Pop = 0x02,
    Dup = 0x03,
    
    Add = 16,        
    Sub = 17,        
    Mul = 18,        
    Div = 19,        
    Mod = 20,
    
    CastInt = 21,
    CastStr = 22,
    
    Jmp = 32,        
    JmpIfFalse = 33, 
    Call = 34,       
    Ret = 35,        
    
    CmpEq = 38,      
    CmpNeq = 39,     
    CmpLt = 41,      
    CmpGt = 42,      
    CmpLte = 43,     
    CmpGte = 44,     
    
    StoreState = 48, 
    LoadState = 49,  
    InitState = 50,  
    
    Print = 81,      
    ReturnValue = 98, 
    
    BuildDict = 128,  
    CreateArray = 134, 
    LoadSubscr = 136,  
    StoreSubscr = 137, 
    
    StringConcat = 140,
    StringSlice = 141,
    StringLen = 142,
    
    ConsoleRead = 150,

    // AI & TENSOR ENGINES
    TensorCreate = 160,
    TensorAdd = 161,
    TensorMatMul = 162,
    
    // DB (RAM+SSD) ENGINE
    DbSet = 170,
    DbGet = 171,
    DbFlush = 172,
    
    // HTTP/S SERVER ENGINE
    ServerStart = 180,
    ServerRoute = 181,
    
    // UI ENGINE
    UiCreateNode = 190,
    UiRender = 191,
}

impl From<u8> for OpCode {
    #[inline(always)]
    fn from(byte: u8) -> Self {
        unsafe { std::mem::transmute(byte) }
    }
}
