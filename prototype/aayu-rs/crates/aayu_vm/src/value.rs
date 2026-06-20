use aayu_core::bytecode::Constant;
use std::fmt;

#[derive(Debug, Clone, PartialEq)]
pub enum RuntimeValue {
    Number(f64),
    Boolean(bool),
    String(String),
    Null,
}

impl From<&Constant> for RuntimeValue {
    fn from(const_val: &Constant) -> Self {
        match const_val {
            Constant::String(s) => RuntimeValue::String(s.clone()),
            Constant::Number(n) => RuntimeValue::Number(*n),
            Constant::Boolean(b) => RuntimeValue::Boolean(*b),
        }
    }
}

impl fmt::Display for RuntimeValue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RuntimeValue::Number(n) => write!(f, "{}", n),
            RuntimeValue::Boolean(b) => write!(f, "{}", b),
            RuntimeValue::String(s) => write!(f, "{}", s),
            RuntimeValue::Null => write!(f, "null"),
        }
    }
}
