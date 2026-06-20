use crate::value::RuntimeValue;
use aayu_core::bytecode::Bytecode;
use std::collections::HashMap;

pub struct RuntimeFrame {
    pub bytecode: Bytecode,
    pub ip: usize,
    pub locals: HashMap<String, RuntimeValue>,
    pub stack: crate::stack::RuntimeStack,
}

impl RuntimeFrame {
    pub fn new(bytecode: Bytecode) -> Self {
        Self {
            bytecode,
            ip: 0,
            locals: HashMap::new(),
            stack: crate::stack::RuntimeStack::new(),
        }
    }
}
