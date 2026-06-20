use serde_repr::{Deserialize_repr, Serialize_repr};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize_repr, Deserialize_repr)]
#[repr(u8)]
pub enum Opcode {
    LoadConst = 1,
    LoadName = 2,
    StoreName = 3,
    Pop = 4,
    Add = 5,
    Sub = 6,
    Mul = 7,
    Div = 8,
    Equal = 9,
    Greater = 10,
    Less = 11,
    Not = 12,
    JumpForward = 13,
    JumpIfFalse = 14,
    JumpBackward = 15,
    Print = 16,
    BuildList = 17,
    BuildMap = 18,
    AddToList = 19,
    MapSet = 20,
    GetItem = 21,
    CallTask = 22,
    Return = 23,
}
