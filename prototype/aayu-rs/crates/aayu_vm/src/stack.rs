use crate::value::RuntimeValue;
use aayu_diagnostics::VMError;

#[derive(Debug, Default)]
pub struct RuntimeStack {
    values: Vec<RuntimeValue>,
}

impl RuntimeStack {
    pub fn new() -> Self {
        Self { values: Vec::new() }
    }

    pub fn push(&mut self, val: RuntimeValue) {
        self.values.push(val);
    }

    pub fn pop(&mut self) -> Result<RuntimeValue, VMError> {
        self.values.pop().ok_or(VMError::StackUnderflow)
    }

    pub fn peek(&self) -> Result<&RuntimeValue, VMError> {
        self.values.last().ok_or(VMError::StackUnderflow)
    }

    pub fn len(&self) -> usize {
        self.values.len()
    }

    pub fn is_empty(&self) -> bool {
        self.values.is_empty()
    }
}
