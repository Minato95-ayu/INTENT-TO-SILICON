use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum VMError {
    StackUnderflow,
    DivisionByZero,
    UnknownOpcode(u8),
    UnknownVariable(String),
    TypeMismatch(String),
}

impl fmt::Display for VMError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            VMError::StackUnderflow => write!(f, "Stack underflow error"),
            VMError::DivisionByZero => write!(f, "Division by zero"),
            VMError::UnknownOpcode(op) => write!(f, "Unknown opcode: {}", op),
            VMError::UnknownVariable(var) => write!(f, "Variable '{}' not found", var),
            VMError::TypeMismatch(msg) => write!(f, "Type mismatch: {}", msg),
        }
    }
}

impl std::error::Error for VMError {}
