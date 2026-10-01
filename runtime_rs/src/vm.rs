use crate::opcodes::OpCode;

// =====================================================
//  NaN-boxed Value — EVERYTHING fits in 8 bytes
//  No enum discriminant, no heap allocation
//  Inspired by LuaJIT, V8, SpiderMonkey
// =====================================================

#[derive(Clone, Copy)]
pub struct NanVal(u64);

// IEEE 754 NaN has exponent bits all 1 and non-zero mantissa
// We use the quiet NaN space to tag our types:
const QNAN: u64     = 0x7FF8_0000_0000_0000; // quiet NaN
const TAG_INT: u64   = QNAN | 0x0001_0000_0000_0000; // int tag
const TAG_TRUE: u64  = QNAN | 0x0002_0000_0000_0000;
const TAG_FALSE: u64 = QNAN | 0x0003_0000_0000_0000;
const TAG_NULL: u64  = QNAN | 0x0004_0000_0000_0000;

const INT_MASK: u64 = 0x0000_FFFF_FFFF_FFFF; // 48-bit payload

impl NanVal {
    #[inline(always)]
    pub fn int(v: i64) -> Self {
        // Store i64 in lower 48 bits with sign extension
        NanVal(TAG_INT | (v as u64 & INT_MASK))
    }
    #[inline(always)]
    pub fn float(v: f64) -> Self { NanVal(v.to_bits()) }
    #[inline(always)]
    pub fn bool(v: bool) -> Self { if v { NanVal(TAG_TRUE) } else { NanVal(TAG_FALSE) } }
    #[inline(always)]
    pub fn null() -> Self { NanVal(TAG_NULL) }

    #[inline(always)]
    pub fn is_float(self) -> bool { (self.0 & QNAN) != QNAN }
    #[inline(always)]
    pub fn is_int(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_INT }
    #[inline(always)]
    pub fn is_true(self) -> bool { self.0 == TAG_TRUE }
    #[inline(always)]
    pub fn is_null(self) -> bool { self.0 == TAG_NULL }

    #[inline(always)]
    pub fn as_int(self) -> i64 {
        let raw = (self.0 & INT_MASK) as i64;
        // Sign extend from 48 bits
        (raw << 16) >> 16
    }
    #[inline(always)]
    pub fn as_float(self) -> f64 { f64::from_bits(self.0) }
}

impl std::fmt::Display for NanVal {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.is_float() {
            write!(f, "{}", self.as_float())
        } else if self.is_int() {
            write!(f, "{}", self.as_int())
        } else if self.0 == TAG_TRUE {
            write!(f, "true")
        } else if self.0 == TAG_FALSE {
            write!(f, "false")
        } else {
            write!(f, "null")
        }
    }
}

// =====================================================
//  AAYU VM v0.3 — NaN-boxed, unsafe, maximum speed
// =====================================================

const STACK_SIZE: usize = 8192;

pub struct AayuVM {
    stack: [NanVal; STACK_SIZE],
    sp: usize,
    ip: usize,
    bytecode: Vec<u8>,
    constants: Vec<NanVal>,
}

impl AayuVM {
    pub fn new(bytecode: Vec<u8>, constants: Vec<NanVal>) -> Self {
        Self {
            stack: [NanVal::null(); STACK_SIZE],
            sp: 0,
            ip: 0,
            bytecode,
            constants,
        }
    }

    /// Maximum speed execution — all unsafe, no bounds checks
    pub fn run(&mut self) {
        let len = self.bytecode.len();
        let bc = self.bytecode.as_ptr();
        let consts = self.constants.as_ptr();
        let stack = self.stack.as_mut_ptr();

        unsafe {
            loop {
                if self.ip >= len { break; }
                let op = *bc.add(self.ip);
                self.ip += 1;

                match op {
                    0x00 => break, // HALT

                    0x01 => { // PUSH_CONST
                        let idx = ((*bc.add(self.ip) as usize) << 8) | *bc.add(self.ip + 1) as usize;
                        self.ip += 2;
                        *stack.add(self.sp) = *consts.add(idx);
                        self.sp += 1;
                    }

                    0x02 => { self.sp -= 1; } // POP

                    0x03 => { // DUP
                        *stack.add(self.sp) = *stack.add(self.sp - 1);
                        self.sp += 1;
                    }

                    0x10 => { // ADD
                        self.sp -= 1;
                        let b = *stack.add(self.sp);
                        self.sp -= 1;
                        let a = *stack.add(self.sp);
                        if a.is_int() && b.is_int() {
                            *stack.add(self.sp) = NanVal::int(a.as_int() + b.as_int());
                        } else if a.is_float() && b.is_float() {
                            *stack.add(self.sp) = NanVal::float(a.as_float() + b.as_float());
                        } else {
                            *stack.add(self.sp) = NanVal::null();
                        }
                        self.sp += 1;
                    }

                    0x11 => { // SUB
                        self.sp -= 1;
                        let b = *stack.add(self.sp);
                        self.sp -= 1;
                        let a = *stack.add(self.sp);
                        if a.is_int() && b.is_int() {
                            *stack.add(self.sp) = NanVal::int(a.as_int() - b.as_int());
                        } else if a.is_float() && b.is_float() {
                            *stack.add(self.sp) = NanVal::float(a.as_float() - b.as_float());
                        } else {
                            *stack.add(self.sp) = NanVal::null();
                        }
                        self.sp += 1;
                    }

                    0x12 => { // MUL
                        self.sp -= 1;
                        let b = *stack.add(self.sp);
                        self.sp -= 1;
                        let a = *stack.add(self.sp);
                        if a.is_int() && b.is_int() {
                            *stack.add(self.sp) = NanVal::int(a.as_int() * b.as_int());
                        } else if a.is_float() && b.is_float() {
                            *stack.add(self.sp) = NanVal::float(a.as_float() * b.as_float());
                        } else {
                            *stack.add(self.sp) = NanVal::null();
                        }
                        self.sp += 1;
                    }

                    0x13 => { // DIV
                        self.sp -= 1;
                        let b = *stack.add(self.sp);
                        self.sp -= 1;
                        let a = *stack.add(self.sp);
                        if a.is_int() && b.is_int() && b.as_int() != 0 {
                            *stack.add(self.sp) = NanVal::int(a.as_int() / b.as_int());
                        } else if a.is_float() && b.is_float() && b.as_float() != 0.0 {
                            *stack.add(self.sp) = NanVal::float(a.as_float() / b.as_float());
                        } else {
                            *stack.add(self.sp) = NanVal::null();
                        }
                        self.sp += 1;
                    }

                    0x51 => { // PRINT
                        self.sp -= 1;
                        let val = *stack.add(self.sp);
                        println!("{}", val);
                    }

                    _ => {} // skip unknown
                }
            }
        }
    }
}

// String-capable Value for full-featured VM (kept for compatibility)
#[derive(Debug, Clone)]
pub enum Value {
    Int(i64),
    Float(f64),
    String(String),
    Bool(bool),
    Null,
}

impl std::fmt::Display for Value {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Value::Int(i) => write!(f, "{}", i),
            Value::Float(v) => write!(f, "{}", v),
            Value::String(s) => write!(f, "{}", s),
            Value::Bool(b) => write!(f, "{}", b),
            Value::Null => write!(f, "null"),
        }
    }
}

pub struct VM {
    stack: Vec<Value>,
    ip: usize,
    bytecode: Vec<u8>,
    constants: Vec<Value>,
}

impl VM {
    pub fn new(bytecode: Vec<u8>) -> Self {
        Self { stack: Vec::with_capacity(1024), ip: 0, bytecode, constants: Vec::new() }
    }
    pub fn new_with_constants(bytecode: Vec<u8>, constants: Vec<Value>) -> Self {
        Self { stack: Vec::with_capacity(1024), ip: 0, bytecode, constants }
    }
    #[inline(always)]
    fn fetch(&mut self) -> u8 { let op = self.bytecode[self.ip]; self.ip += 1; op }
    #[inline(always)]
    fn fetch_u16(&mut self) -> u16 { let b1 = self.fetch() as u16; let b2 = self.fetch() as u16; (b1<<8)|b2 }

    pub fn run(&mut self) {
        loop {
            if self.ip >= self.bytecode.len() { break; }
            let instruction = self.fetch();
            match instruction {
                0x00 => break,
                0x01 => {
                    let idx = self.fetch_u16() as usize;
                    if idx < self.constants.len() { self.stack.push(self.constants[idx].clone()); }
                    else { self.stack.push(Value::Null); }
                }
                0x02 => { self.stack.pop(); }
                0x10 => {
                    let b = self.stack.pop().unwrap_or(Value::Null);
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    match (&a, &b) {
                        (Value::Int(x), Value::Int(y)) => self.stack.push(Value::Int(x+y)),
                        (Value::Float(x), Value::Float(y)) => self.stack.push(Value::Float(x+y)),
                        (Value::String(x), Value::String(y)) => self.stack.push(Value::String(format!("{}{}",x,y))),
                        _ => self.stack.push(Value::Null),
                    }
                }
                0x11 => {
                    let b = self.stack.pop().unwrap_or(Value::Null);
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    match (&a, &b) {
                        (Value::Int(x), Value::Int(y)) => self.stack.push(Value::Int(x-y)),
                        _ => self.stack.push(Value::Null),
                    }
                }
                0x12 => {
                    let b = self.stack.pop().unwrap_or(Value::Null);
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    match (&a, &b) {
                        (Value::Int(x), Value::Int(y)) => self.stack.push(Value::Int(x*y)),
                        _ => self.stack.push(Value::Null),
                    }
                }
                0x13 => {
                    let b = self.stack.pop().unwrap_or(Value::Null);
                    let a = self.stack.pop().unwrap_or(Value::Null);
                    match (&a, &b) {
                        (Value::Int(x), Value::Int(y)) if *y != 0 => self.stack.push(Value::Int(x/y)),
                        _ => self.stack.push(Value::Null),
                    }
                }
                0x51 => {
                    if let Some(val) = self.stack.pop() { println!("{}", val); }
                }
                _ => {}
            }
        }
    }
}
