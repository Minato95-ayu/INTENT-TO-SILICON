use std::fmt;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum VMError {
    StackUnderflow,
    DivisionByZero,
    UnknownOpcode(u8),
    UnknownVariable(String),
    TypeMismatch(String),
    InvalidJump { current_ip: usize, target_ip: usize },
    InvalidConstantIndex,
    InvalidNameIndex,
    IndexOutOfBounds(String),
    KeyNotFound(String),
    InvalidCollectionAccess(String),
    InvalidIndexType(String),
}

impl fmt::Display for VMError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            VMError::StackUnderflow => write!(f, "Stack underflow error"),
            VMError::DivisionByZero => write!(f, "Division by zero"),
            VMError::UnknownOpcode(op) => write!(f, "Unknown opcode: {}", op),
            VMError::UnknownVariable(var) => write!(f, "Variable '{}' not found", var),
            VMError::TypeMismatch(msg) => write!(f, "Type mismatch: {}", msg),
            VMError::InvalidJump { current_ip, target_ip } => {
                write!(f, "Invalid jump: current_ip={}, target_ip={}", current_ip, target_ip)
            }
            VMError::InvalidConstantIndex => write!(f, "Invalid constant pool index"),
            VMError::InvalidNameIndex => write!(f, "Invalid name pool index"),
            VMError::IndexOutOfBounds(msg) => write!(f, "Index out of bounds: {}", msg),
            VMError::KeyNotFound(msg) => write!(f, "Key not found: {}", msg),
            VMError::InvalidCollectionAccess(msg) => write!(f, "Invalid collection access: {}", msg),
            VMError::InvalidIndexType(msg) => write!(f, "Invalid index type: {}", msg),
        }
    }
}

impl std::error::Error for VMError {}
