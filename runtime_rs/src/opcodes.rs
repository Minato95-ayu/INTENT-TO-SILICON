#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OpCode {
    Halt = 0x00,
    PushConst = 0x01,
    Pop = 0x02,
    StoreState = 0x03,
    LoadState = 0x04,
    Add = 0x05,
    Sub = 0x06,
    Mul = 0x07,
    Div = 0x08,
    Jump = 0x20,
    JumpIfFalse = 0x21,
    Call = 0x30,
    Return = 0x31,
    Syscall = 0xFF,
}
