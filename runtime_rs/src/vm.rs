use std::collections::HashMap;
use crate::opcodes::OpCode;
use crate::math::tensor::Tensor;
use crate::db::DbEngine;
use crate::net::HttpServer;

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
        else { write!(f, "<Unknown>") }
    }
}

pub struct AayuVM {
    stack: [NanVal; 4096],
    sp: usize,
    ip: usize,
    bytecode: Vec<u8>,
    constants: Vec<NanVal>,
    pub string_heap: Vec<String>,
    pub array_heap: Vec<Vec<NanVal>>,
    pub dict_heap: Vec<HashMap<String, NanVal>>,
    
    pub tensor_heap: Vec<Tensor>,
    pub db_engine: DbEngine,
}

impl AayuVM {
    pub fn new(bytecode: Vec<u8>, constants: Vec<NanVal>, strings: Vec<String>) -> Self {
        Self {
            stack: [NanVal::null(); 4096],
            sp: 0,
            ip: 0,
            bytecode,
            constants,
            string_heap: strings,
            array_heap: Vec::new(),
            dict_heap: Vec::new(),
            tensor_heap: Vec::new(),
            db_engine: DbEngine::new("aayu_db.rsdb"),
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
                0x10 => { // PUSH_STRING
                    let idx = ((self.bytecode[self.ip] as usize) | ((self.bytecode[self.ip+1] as usize) << 8));
                    self.ip += 2;
                    self.stack[self.sp] = NanVal::string(idx);
                    self.sp += 1;
                }
                0x02 => { self.sp -= 1; } // POP
                
                81 => { // PRINT
                    let val = self.stack[self.sp - 1];
                    self.sp -= 1;
                    if val.is_string() {
                        let s = &self.string_heap[val.as_string_idx()];
                        println!("{}", s);
                    } else {
                        println!("{}", val);
                    }
                }
                
                // --- NEW OPCODES FOR AI / DATA / SERVER ---
                
                160 => { // TensorCreate (Mock)
                    println!("[Native] Creating PyTorch-style Tensor in Rust...");
                    let t = Tensor::new(vec![2, 2], vec![1.0, 2.0, 3.0, 4.0]);
                    self.tensor_heap.push(t);
                    println!("[Native] Tensor generated and stored in RAM.");
                }
                
                170 => { // DbSet (Mock)
                    println!("[Native] Executing DB Set (RAM -> SSD WAL)...");
                    self.db_engine.set("key", "value");
                    println!("[Native] Key saved securely.");
                }
                
                171 => { // DbGet (Mock)
                    println!("[Native] Executing DB Get (RAM Cache Hit)...");
                    let val = self.db_engine.get("key");
                    println!("[Native] Retrieved: {:?}", val);
                }
                
                180 => { // ServerStart (Mock)
                    println!("[Native] Initializing HTTP/HTTPS Server...");
                    let _server = HttpServer::new(3000);
                    println!("[Native] Listening on port 3000 (Mock Mode).");
                }
                
                _ => {
                    // Skip
                }
            }
        }
    }
}
