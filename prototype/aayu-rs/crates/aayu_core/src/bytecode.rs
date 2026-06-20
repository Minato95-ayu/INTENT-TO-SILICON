use crate::instruction::Instruction;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(tag = "__type__", content = "value")]
pub enum BytecodeWrapper {
    Bytecode(Bytecode),
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
#[serde(untagged)]
pub enum Constant {
    Bytecode(BytecodeWrapper),
    String(String),
    Number(f64),
    Boolean(bool),
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct Bytecode {
    #[serde(default)]
    pub name: String,
    #[serde(default)]
    pub file: String,
    #[serde(default)]
    pub constants: Vec<Constant>,
    #[serde(default)]
    pub names: Vec<String>,
    #[serde(default)]
    pub parameters: Vec<String>,
    #[serde(default)]
    pub instructions: Vec<Instruction>,
    #[serde(default)]
    pub tasks: HashMap<String, Bytecode>,
}
