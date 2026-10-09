use std::collections::HashMap;

use crate::math::Tensor;
use crate::db::DbEngine;
use crate::net::HttpServer;
use crate::ui::{UiNode, Style};

#[derive(Clone, Copy, Debug)]
pub struct NanVal(u64);

const TAG_INT: u64 = 0x7FF8_0000_0000_0000;

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
    locals: [NanVal; 256],
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
            locals: [NanVal::null(); 256],
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
                0x05 => { // LOAD_VAR
                    let idx = self.bytecode[self.ip] as usize;
                    self.ip += 1;
                    self.stack[self.sp] = self.locals[idx];
                    self.sp += 1;
                }
                0x06 => { // STORE_VAR
                    let idx = self.bytecode[self.ip] as usize;
                    self.ip += 1;
                    self.locals[idx] = self.stack[self.sp - 1];
                    self.sp -= 1;
                }
                0x10 => { // ADD
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::int(a + b);
                    self.sp -= 1;
                }
                41 => { // LT
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a < b);
                    self.sp -= 1;
                }
                0x20 => { // JUMP
                    let offset = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip = offset;
                }
                0x21 => { // JUMP_IF_FALSE
                    let offset = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    let cond = self.stack[self.sp - 1].as_bool();
                    self.sp -= 1;
                    if !cond {
                        self.ip = offset;
                    }
                }
                145 => { // PUSH_STRING_SAFE
                    let idx = (self.bytecode[self.ip] as usize) | ((self.bytecode[self.ip+1] as usize) << 8);
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
                
                160 => { // TensorCreate
                    println!("[Native] Creating PyTorch-style Tensor in Rust...");
                    let t = Tensor::new(vec![2, 2], vec![1.0, 2.0, 3.0, 4.0]);
                    self.tensor_heap.push(t);
                    println!("[Native] Tensor generated and stored in RAM.");
                }
                
                170 => { // DbSet
                    let val_ref = self.stack[self.sp - 1];
                    let key_ref = self.stack[self.sp - 2];
                    self.sp -= 2;
                    
                    if key_ref.is_string() && val_ref.is_string() {
                        let k = &self.string_heap[key_ref.as_string_idx()];
                        let v = &self.string_heap[val_ref.as_string_idx()];
                        println!("[Native] Executing DB Set: '{}' = '{}' (RAM -> SSD WAL)...", k, v);
                        self.db_engine.set(k, v);
                    }
                }
                
                171 => { // DbGet
                    let key_ref = self.stack[self.sp - 1];
                    self.sp -= 1;
                    
                    if key_ref.is_string() {
                        let k = &self.string_heap[key_ref.as_string_idx()];
                        println!("[Native] Executing DB Get for '{}' (RAM Cache Hit)...", k);
                        let val = self.db_engine.get(k);
                        // Push result as string back to stack for printing
                        if let Some(s) = val {
                            let idx = self.string_heap.len();
                            self.string_heap.push(s);
                            self.stack[self.sp] = NanVal::string(idx);
                        } else {
                            self.stack[self.sp] = NanVal::null();
                        }
                        self.sp += 1;
                    }
                }
                
                180 => { // ServerStart
                    println!("[Native] Initializing HTTP/HTTPS Server...");
                    let _server = HttpServer::new(3000);
                    println!("[Native] Listening on port 3000 (Mock Mode).");
                }
                
                190 => { // UIRender
                    let val_ref = self.stack[self.sp - 1];
                    self.sp -= 1;
                    if val_ref.is_string() {
                        let component_name = &self.string_heap[val_ref.as_string_idx()];
                        println!("[Native] Compiling Declarative UI Component '{}' into DOM Tree...", component_name);
                        
                        let mut root = UiNode::new("div");
                        let mut style = Style::default();
                        style.display = "flex".to_string();
                        style.background_color = "#111".to_string();
                        root = root.with_style(style);
                        
                        let text_node = UiNode::new("h1").with_text(&format!("Welcome to {}", component_name));
                        let btn_node = UiNode::new("button").with_text("Click Me");
                        
                        root = root.add_child(text_node).add_child(btn_node);
                        
                        println!("[Native] Rendered HTML Output:");
                        println!("{}", root.render());
                    }
                }                17 => { // SUB
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::int(a - b);
                    self.sp -= 1;
                }
                18 => { // MUL
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::int(a * b);
                    self.sp -= 1;
                }
                19 => { // DIV
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    if b == 0 { panic!("Division by zero"); }
                    self.stack[self.sp - 2] = NanVal::int(a / b);
                    self.sp -= 1;
                }
                20 => { // MOD
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    if b == 0 { panic!("Modulo by zero"); }
                    self.stack[self.sp - 2] = NanVal::int(a % b);
                    self.sp -= 1;
                }
                38 => { // CmpEq
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a == b);
                    self.sp -= 1;
                }
                39 => { // CmpNeq
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a != b);
                    self.sp -= 1;
                }
                42 => { // CmpGt
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a > b);
                    self.sp -= 1;
                }
                43 => { // CmpLte
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a <= b);
                    self.sp -= 1;
                }
                44 => { // CmpGte
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a >= b);
                    self.sp -= 1;
                }
                0x03 => { // DUP
                    self.stack[self.sp] = self.stack[self.sp - 1];
                    self.sp += 1;
                }
                _ => {
                    panic!("[Runtime Error] Unknown instruction opcode: 0x{:02X} at IP: {}", op, self.ip - 1);
                }
            }
        }
    }
}


#[cfg(test)]
mod tests {
    use super::*;
    use crate::NanVal;

    #[test]
    fn test_push_and_add() {
        let bytecode = vec![
            0x01, 0x00, 0x00, // PUSH_CONST 0
            0x01, 0x00, 0x01, // PUSH_CONST 1
            0x10,             // ADD
            0x00              // HALT
        ];
        let constants = vec![NanVal::int(10), NanVal::int(20)];
        let strings = vec![];
        let mut vm = AayuVM::new(bytecode, constants, strings);
        vm.run();
        assert_eq!(vm.stack[0].as_int(), 30);
    }
    #[test]
    fn test_lt() {
        let bytecode = vec![
            0x01, 0x00, 0x00, // PUSH_CONST 10
            0x01, 0x00, 0x01, // PUSH_CONST 20
            41,             // LT (10 < 20 -> true)
            0x00              // HALT
        ];
        let constants = vec![NanVal::int(10), NanVal::int(20)];
        let strings = vec![];
        let mut vm = AayuVM::new(bytecode, constants, strings);
        vm.run();
        assert_eq!(vm.stack[0].as_bool(), true);
    }

    #[test]
    fn test_jump() {
        let bytecode = vec![
            0x20, 0x00, 0x05, // JUMP to index 5
            0x00, 0x00,       // Skip these (would be index 3, 4)
            0x01, 0x00, 0x00, // PUSH_CONST 42 (index 5, 6, 7)
            0x00              // HALT (index 8)
        ];
        let constants = vec![NanVal::int(42)];
        let strings = vec![];
        let mut vm = AayuVM::new(bytecode, constants, strings);
        vm.run();
        assert_eq!(vm.stack[0].as_int(), 42);
    }
    #[test]
    fn test_math_extended() {
        // Test MUL
        let mut vm = AayuVM::new(vec![0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 18, 0x00], vec![NanVal::int(10), NanVal::int(5)], vec![]);
        vm.run();
        assert_eq!(vm.stack[0].as_int(), 50);

        // Test SUB
        let mut vm2 = AayuVM::new(vec![0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 17, 0x00], vec![NanVal::int(20), NanVal::int(8)], vec![]);
        vm2.run();
        assert_eq!(vm2.stack[0].as_int(), 12);

        // Test DIV
        let mut vm3 = AayuVM::new(vec![0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 19, 0x00], vec![NanVal::int(100), NanVal::int(4)], vec![]);
        vm3.run();
        assert_eq!(vm3.stack[0].as_int(), 25);
    }

    #[test]
    fn test_cmp_extended() {
        // Test CmpEq (True)
        let mut vm = AayuVM::new(vec![0x01, 0x00, 0x00, 0x01, 0x00, 0x00, 38, 0x00], vec![NanVal::int(42)], vec![]);
        vm.run();
        assert_eq!(vm.stack[0].as_bool(), true);

        // Test CmpGt (True)
        let mut vm2 = AayuVM::new(vec![0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 42, 0x00], vec![NanVal::int(10), NanVal::int(5)], vec![]);
        vm2.run();
        assert_eq!(vm2.stack[0].as_bool(), true);
    }
    
    #[test]
    fn test_dup() {
        let mut vm = AayuVM::new(vec![0x01, 0x00, 0x00, 0x03, 0x00], vec![NanVal::int(77)], vec![]);
        vm.run();
        assert_eq!(vm.stack[0].as_int(), 77);
        assert_eq!(vm.stack[1].as_int(), 77);
    }
}



