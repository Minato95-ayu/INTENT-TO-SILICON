use std::fs;
use std::io::{self, Write};
use std::collections::HashMap;
use crate::opcodes::OpCode;

#[derive(Clone, Copy, Debug)]
pub struct NanVal(u64);

const TAG_INT: u64 = 0x7FF8_0000_0000_0000;
const TAG_FLOAT: u64 = 0x7FF9_0000_0000_0000;
const TAG_BOOL: u64 = 0x7FFA_0000_0000_0000;
const TAG_NULL: u64 = 0x7FFB_0000_0000_0000;
const TAG_STR: u64  = 0x7FFC_0000_0000_0000;
const TAG_ARR: u64  = 0x7FFD_0000_0000_0000;
const TAG_DICT: u64 = 0x7FFE_0000_0000_0000;

impl NanVal {
    #[inline(always)] pub fn int(v: i64) -> Self { NanVal(TAG_INT | (v as u64 & 0x0000_FFFF_FFFF_FFFF)) }
    #[inline(always)] pub fn float(v: f64) -> Self { NanVal(v.to_bits()) }
    #[inline(always)] pub fn bool(v: bool) -> Self { NanVal(TAG_BOOL | (if v { 1 } else { 0 })) }
    #[inline(always)] pub fn null() -> Self { NanVal(TAG_NULL) }
    #[inline(always)] pub fn string(idx: usize) -> Self { NanVal(TAG_STR | (idx as u64 & 0x0000_FFFF_FFFF_FFFF)) }
    #[inline(always)] pub fn array(idx: usize) -> Self { NanVal(TAG_ARR | (idx as u64 & 0x0000_FFFF_FFFF_FFFF)) }
    #[inline(always)] pub fn dict(idx: usize) -> Self { NanVal(TAG_DICT | (idx as u64 & 0x0000_FFFF_FFFF_FFFF)) }

    #[inline(always)] pub fn is_int(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_INT }
    #[inline(always)] pub fn is_float(self) -> bool { self.0 < 0x7FF8_0000_0000_0000 }
    #[inline(always)] pub fn is_bool(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_BOOL }
    #[inline(always)] pub fn is_null(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_NULL }
    #[inline(always)] pub fn is_string(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_STR }
    #[inline(always)] pub fn is_array(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_ARR }
    #[inline(always)] pub fn is_dict(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_DICT }

    #[inline(always)] pub fn as_int(self) -> i64 { (self.0 & 0x0000_FFFF_FFFF_FFFF) as i64 }
    #[inline(always)] pub fn as_float(self) -> f64 { f64::from_bits(self.0) }
    #[inline(always)] pub fn as_bool(self) -> bool { (self.0 & 1) == 1 }
    #[inline(always)] pub fn as_string_idx(self) -> usize { (self.0 & 0x0000_FFFF_FFFF_FFFF) as usize }
    #[inline(always)] pub fn as_array_idx(self) -> usize { (self.0 & 0x0000_FFFF_FFFF_FFFF) as usize }
    #[inline(always)] pub fn as_dict_idx(self) -> usize { (self.0 & 0x0000_FFFF_FFFF_FFFF) as usize }
}

impl std::fmt::Display for NanVal {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.is_int() { write!(f, "{}", self.as_int()) }
        else if self.is_float() { write!(f, "{}", self.as_float()) }
        else if self.is_bool() { write!(f, "{}", self.as_bool()) }
        else if self.is_null() { write!(f, "null") }
        else if self.is_string() { write!(f, "<String at {}>", self.as_string_idx()) }
        else if self.is_array() { write!(f, "<Array at {}>", self.as_array_idx()) }
        else if self.is_dict() { write!(f, "<Dict at {}>", self.as_dict_idx()) }
        else { write!(f, "Unknown") }
    }
}

pub struct AayuVM {
    stack: [NanVal; 4096],
    locals: [NanVal; 256],
    sp: usize,
    ip: usize,
    bytecode: Vec<u8>,
    constants: Vec<NanVal>,
    pub string_heap: Vec<String>,
    pub array_heap: Vec<Vec<NanVal>>,
    pub dict_heap: Vec<HashMap<String, NanVal>>,
}

impl AayuVM {
    pub fn new(bytecode: Vec<u8>, constants: Vec<NanVal>, strings: Vec<String>) -> Self {
        Self {
            stack: [NanVal::null(); 4096],
            locals: [NanVal::null(); 256],
            sp: 0,
            ip: 0,
            bytecode,
            constants,
            string_heap: strings,
            array_heap: Vec::new(),
            dict_heap: Vec::new(),
        }
    }

    pub fn run(&mut self) {
        let len = self.bytecode.len();
        
        loop {
            if self.ip >= len { break; }
            let op = self.bytecode[self.ip];
            self.ip += 1;

            match op {
                0x00 => break, // HALT
                0x01 => { // PUSH_CONST
                    let idx = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    self.stack[self.sp] = self.constants[idx];
                    self.sp += 1;
                }
                0x02 => { self.sp -= 1; } // POP
                
                // Math
                16 => { // ADD
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.sp -= 1;
                    if a.is_int() && b.is_int() {
                        self.stack[self.sp - 1] = NanVal::int(a.as_int() + b.as_int());
                    } else if a.is_float() && b.is_float() {
                        self.stack[self.sp - 1] = NanVal::float(a.as_float() + b.as_float());
                    }
                }
                17 => { // SUB
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.sp -= 1;
                    if a.is_int() && b.is_int() {
                        self.stack[self.sp - 1] = NanVal::int(a.as_int() - b.as_int());
                    }
                }
                18 => { // MUL
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.sp -= 1;
                    if a.is_int() && b.is_int() {
                        self.stack[self.sp - 1] = NanVal::int(a.as_int() * b.as_int());
                    }
                }
                19 => { // DIV
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.sp -= 1;
                    if a.is_int() && b.is_int() {
                        self.stack[self.sp - 1] = NanVal::int(a.as_int() / b.as_int());
                    }
                }
                
                // Control Flow & Memory
                32 => { // JMP
                    let tgt = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip = tgt;
                }
                33 => { // JMP_IF_FALSE
                    let tgt = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    let cond = self.stack[self.sp - 1];
                    self.sp -= 1;
                    if cond.is_int() && cond.as_int() == 0 {
                        self.ip = tgt;
                    } else if cond.is_bool() && !cond.as_bool() {
                        self.ip = tgt;
                    }
                }
                41 => { // CMP_LT
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.sp -= 1;
                    if a.is_int() && b.is_int() {
                        self.stack[self.sp - 1] = NanVal::bool(a.as_int() < b.as_int());
                    }
                }
                48 => { // STORE_STATE (Store Local/Global)
                    let slot = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    let val = self.stack[self.sp - 1];
                    self.sp -= 1;
                    if slot < 256 {
                        self.locals[slot] = val;
                    }
                }
                49 => { // LOAD_STATE
                    let slot = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    if slot < 256 {
                        self.stack[self.sp] = self.locals[slot];
                        self.sp += 1;
                    }
                }
                81 => { // PRINT
                    let val = self.stack[self.sp - 1];
                    self.sp -= 1;
                    if val.is_string() {
                        println!("{}", self.string_heap[val.as_string_idx()]);
                    } else {
                        println!("{}", val);
                    }
                }
                
                // NEW: Arrays, Dicts, Subscripts
                134 => { // CREATE_ARRAY (len in next byte or from stack)
                    let count = self.bytecode[self.ip] as usize; // Simplified
                    self.ip += 2; // + padding byte
                    let mut arr = Vec::with_capacity(count);
                    for _ in 0..count {
                        self.sp -= 1;
                        arr.push(self.stack[self.sp]); // Reversing not handled here for simplicity
                    }
                    arr.reverse();
                    let idx = self.array_heap.len();
                    self.array_heap.push(arr);
                    self.stack[self.sp] = NanVal::array(idx);
                    self.sp += 1;
                }
                136 => { // LOAD_SUBSCR
                    let index_val = self.stack[self.sp - 1];
                    let target = self.stack[self.sp - 2];
                    self.sp -= 2;
                    
                    if target.is_array() && index_val.is_int() {
                        let arr = &self.array_heap[target.as_array_idx()];
                        let idx = index_val.as_int() as usize;
                        if idx < arr.len() {
                            self.stack[self.sp] = arr[idx];
                        } else {
                            self.stack[self.sp] = NanVal::null();
                        }
                        self.sp += 1;
                    } else if target.is_string() && index_val.is_int() {
                        let s = &self.string_heap[target.as_string_idx()];
                        let idx = index_val.as_int() as usize;
                        if let Some(c) = s.chars().nth(idx) {
                            let s_idx = self.string_heap.len();
                            self.string_heap.push(c.to_string());
                            self.stack[self.sp] = NanVal::string(s_idx);
                        } else {
                            self.stack[self.sp] = NanVal::null();
                        }
                        self.sp += 1;
                    }
                }
                
                // Native String and Console functions
                142 => { // StringLen (len)
                    let target = self.stack[self.sp - 1];
                    if target.is_string() {
                        let len = self.string_heap[target.as_string_idx()].len();
                        self.stack[self.sp - 1] = NanVal::int(len as i64);
                    } else if target.is_array() {
                        let len = self.array_heap[target.as_array_idx()].len();
                        self.stack[self.sp - 1] = NanVal::int(len as i64);
                    }
                }
                150 => { // ConsoleRead (input)
                    let mut input = String::new();
                    io::stdin().read_line(&mut input).unwrap();
                    let s_idx = self.string_heap.len();
                    self.string_heap.push(input.trim().to_string());
                    self.stack[self.sp] = NanVal::string(s_idx);
                    self.sp += 1;
                }
                21 => { // CastInt
                    let target = self.stack[self.sp - 1];
                    if target.is_string() {
                        let s = &self.string_heap[target.as_string_idx()];
                        if let Ok(v) = s.parse::<i64>() {
                            self.stack[self.sp - 1] = NanVal::int(v);
                        }
                    }
                }
                
                _ => {
                    println!("Unknown OpCode: {}", op);
                }
            }
        }
    }
}
