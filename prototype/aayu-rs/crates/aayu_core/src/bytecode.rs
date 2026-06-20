use crate::instruction::Instruction;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum Constant {
    String(String),
    Number(f64),
    Boolean(bool),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Bytecode {
    pub name: String,
    pub file: String,
    pub constants: Vec<Constant>,
    pub names: Vec<String>,
    pub parameters: Vec<String>,
    pub instructions: Vec<Instruction>,
    #[serde(default)]
    pub tasks: HashMap<String, Bytecode>,
}
