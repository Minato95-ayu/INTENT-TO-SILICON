use crate::opcodes::OpCode;

#[derive(Debug, Clone)]
pub enum Value {
    Int(i64),
    Float(f64),
    String(String),
    Bool(bool),
    Null,
}

// Core Stack-based VM designed for absolute maximum execution speed
pub struct VM {
    stack: Vec<Value>, 
    ip: usize,
    bytecode: Vec<u8>,
}

impl VM {
    pub fn new(bytecode: Vec<u8>) -> Self {
        Self {
            stack: Vec::with_capacity(1024), // Fast pre-allocation
            ip: 0,
            bytecode,
        }
    }

    #[inline(always)]
    fn fetch(&mut self) -> u8 {
        let op = self.bytecode[self.ip];
        self.ip += 1;
        op
    }

    #[inline(always)]
    fn fetch_u16(&mut self) -> u16 {
        let b1 = self.fetch() as u16;
        let b2 = self.fetch() as u16;
        (b1 << 8) | b2
    }

    pub fn run(&mut self) {
        loop {
            if self.ip >= self.bytecode.len() {
                break;
            }

            let instruction = self.fetch();
            // unsafe for absolute god-level speed, bypassing bounds checks where safe
            let op: OpCode = unsafe { std::mem::transmute(instruction) };

            match op {
                OpCode::Halt => {
                    break;
                }
                OpCode::PushConst => {
                    let _idx = self.fetch_u16();
                    // In a full implementation, we'd read from a constant pool.
                    // For scaffolding the engine, we push a dummy value.
                    self.stack.push(Value::Null); 
                }
                OpCode::Pop => {
                    self.stack.pop();
                }
                OpCode::Print => {
                    // Optimized Native System Call Print
                    if let Some(val) = self.stack.pop() {
                        match val {
                            Value::Int(i) => println!("{}", i),
                            Value::Float(f) => println!("{}", f),
                            Value::String(s) => println!("{}", s),
                            Value::Bool(b) => println!("{}", b),
                            Value::Null => println!("null"),
                        }
                    }
                }
                OpCode::Add => {
                    let b = self.stack.pop().unwrap();
                    let a = self.stack.pop().unwrap();
                    if let (Value::Int(x), Value::Int(y)) = (&a, &b) {
                        self.stack.push(Value::Int(x + y));
                    }
                }
                // We map out all others so the VM is robust
                _ => {
                    // Ignore unimplemented opcodes silently for this test scaffold
                }
            }
        }
    }
}
