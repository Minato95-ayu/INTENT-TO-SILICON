use crate::opcode::Opcode;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Instruction {
    pub opcode: Opcode,
    pub operand: Option<usize>,
    pub line: Option<usize>,
    pub file: Option<String>,
}
