use aayu_core::bytecode::{Bytecode, Constant, BytecodeWrapper};
use std::collections::HashMap;
use std::fmt;
use std::rc::Rc;
use std::cell::RefCell;

#[derive(Debug, Clone)]
pub enum RuntimeKey {
    String(String),
    Number(f64),
    Boolean(bool),
}

impl PartialEq for RuntimeKey {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (RuntimeKey::String(s1), RuntimeKey::String(s2)) => s1 == s2,
            (RuntimeKey::Number(n1), RuntimeKey::Number(n2)) => {
                if n1.is_nan() && n2.is_nan() {
                    true
                } else {
                    n1.to_bits() == n2.to_bits()
                }
            }
            (RuntimeKey::Boolean(b1), RuntimeKey::Boolean(b2)) => b1 == b2,
            _ => false,
        }
    }
}

impl Eq for RuntimeKey {}

impl std::hash::Hash for RuntimeKey {
    fn hash<H: std::hash::Hasher>(&self, state: &mut H) {
        match self {
            RuntimeKey::String(s) => s.hash(state),
            RuntimeKey::Number(n) => {
                let bits = if n.is_nan() {
                    f64::NAN.to_bits()
                } else {
                    n.to_bits()
                };
                bits.hash(state);
            }
            RuntimeKey::Boolean(b) => b.hash(state),
        }
    }
}

impl fmt::Display for RuntimeKey {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RuntimeKey::String(s) => write!(f, "{}", s),
            RuntimeKey::Number(n) => {
                if n.fract() == 0.0 {
                    write!(f, "{:.1}", n)
                } else {
                    write!(f, "{}", n)
                }
            }
            RuntimeKey::Boolean(b) => write!(f, "{}", b),
        }
    }
}

#[derive(Debug, Clone)]
pub enum RuntimeValue {
    Number(f64),
    Boolean(bool),
    String(String),
    List(Rc<RefCell<Vec<RuntimeValue>>>),
    Map(Rc<RefCell<HashMap<RuntimeKey, RuntimeValue>>>),
    Task(Box<Bytecode>),
    Native(String),
    Null,
}

impl PartialEq for RuntimeValue {
    fn eq(&self, other: &Self) -> bool {
        match (self, other) {
            (RuntimeValue::Number(l), RuntimeValue::Number(r)) => {
                if l.is_nan() && r.is_nan() {
                    true
                } else {
                    l == r
                }
            }
            (RuntimeValue::Boolean(l), RuntimeValue::Boolean(r)) => l == r,
            (RuntimeValue::String(l), RuntimeValue::String(r)) => l == r,
            (RuntimeValue::List(l), RuntimeValue::List(r)) => l == r,
            (RuntimeValue::Map(l), RuntimeValue::Map(r)) => l == r,
            (RuntimeValue::Task(l), RuntimeValue::Task(r)) => l.name == r.name && l.file == r.file,
            (RuntimeValue::Native(l), RuntimeValue::Native(r)) => l == r,
            (RuntimeValue::Null, RuntimeValue::Null) => true,
            _ => false,
        }
    }
}

impl From<&Constant> for RuntimeValue {
    fn from(const_val: &Constant) -> Self {
        match const_val {
            Constant::String(s) => RuntimeValue::String(s.clone()),
            Constant::Number(n) => RuntimeValue::Number(*n),
            Constant::Boolean(b) => RuntimeValue::Boolean(*b),
            Constant::Bytecode(wrapper) => {
                let BytecodeWrapper::Bytecode(bc) = wrapper;
                RuntimeValue::Task(Box::new(bc.clone()))
            }
        }
    }
}

impl fmt::Display for RuntimeValue {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            RuntimeValue::Number(n) => {
                if n.fract() == 0.0 {
                    write!(f, "{:.1}", n)
                } else {
                    write!(f, "{}", n)
                }
            }
            RuntimeValue::Boolean(b) => write!(f, "{}", b),
            RuntimeValue::String(s) => write!(f, "{}", s),
            RuntimeValue::List(l) => {
                let borrowed = l.borrow();
                let items: Vec<String> = borrowed.iter().map(|item| item.to_string()).collect();
                write!(f, "[{}]", items.join(", "))
            }
            RuntimeValue::Map(m) => {
                let borrowed = m.borrow();
                let items: Vec<String> = borrowed.iter().map(|(k, v)| format!("{}: {}", k, v)).collect();
                write!(f, "{{{}}}", items.join(", "))
            }
            RuntimeValue::Task(t) => write!(f, "<task {}>", t.name),
            RuntimeValue::Native(n) => write!(f, "<native function {}>", n),
            RuntimeValue::Null => write!(f, "null"),
        }
    }
}
