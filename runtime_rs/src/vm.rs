
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
    pub memory: crate::memory::MemoryManager,
    
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
            memory: crate::memory::MemoryManager::new(),
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
                        let style = Style { display: "flex".to_string(), background_color: "#111".to_string(), ..Default::default() };
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
                134 => { // CreateArray
                    let len = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    let mut arr = Vec::with_capacity(len);
                    for _ in 0..len {
                        arr.push(self.stack[self.sp - 1]);
                        self.sp -= 1;
                    }
                    arr.reverse();
                    
                    let idx = self.memory.allocate(crate::memory::HeapObject::AArray(arr));
                    self.stack[self.sp] = NanVal::array(idx);
                    self.sp += 1;
                }
                
                136 => { // LoadSubscr
                    let index_val = self.stack[self.sp - 1].as_int() as usize;
                    let arr_ref = self.stack[self.sp - 2];
                    self.sp -= 2;
                    
                    if arr_ref.is_array() {
                        let idx = arr_ref.as_array_idx();
                        if let crate::memory::HeapObject::AArray(arr) = self.memory.get(idx) {
                            if index_val < arr.len() {
                                self.stack[self.sp] = arr[index_val];
                            } else {
                                panic!("Array Index Out of Bounds!");
                            }
                        }
                    } else {
                        panic!("LoadSubscr on non-array!");
                    }
                    self.sp += 1;
                }

                137 => { // StoreSubscr
                    let val = self.stack[self.sp - 1];
                    let index_val = self.stack[self.sp - 2].as_int() as usize;
                    let arr_ref = self.stack[self.sp - 3];
                    self.sp -= 3;
                    
                    if arr_ref.is_array() {
                        let idx = arr_ref.as_array_idx();
                        if let crate::memory::HeapObject::AArray(arr) = self.memory.get_mut(idx) {
                            if index_val < arr.len() {
                                arr[index_val] = val;
                            } else {
                                panic!("Array Index Out of Bounds!");
                            }
                        }
                    } else {
                        panic!("StoreSubscr on non-array!");
                    }
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
        assert!(vm.stack[0].as_bool());
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
        assert!(vm.stack[0].as_bool());

        // Test CmpGt (True)
        let mut vm2 = AayuVM::new(vec![0x01, 0x00, 0x00, 0x01, 0x00, 0x01, 42, 0x00], vec![NanVal::int(10), NanVal::int(5)], vec![]);
        vm2.run();
        assert!(vm2.stack[0].as_bool());
    }
    
    #[test]
    fn test_dup() {
        let mut vm = AayuVM::new(vec![0x01, 0x00, 0x00, 0x03, 0x00], vec![NanVal::int(77)], vec![]);
        vm.run();
        assert_eq!(vm.stack[0].as_int(), 77);
        assert_eq!(vm.stack[1].as_int(), 77);
    }
    #[test]
    fn test_gc_array_allocation() {
        // [10, 20, 30] -> CreateArray(3) -> ArrayRef
        let mut vm = AayuVM::new(
            vec![
                0x01, 0x00, 0x00, // push 10
                0x01, 0x00, 0x01, // push 20
                0x01, 0x00, 0x02, // push 30
                134, 0x00, 0x03,  // CreateArray len 3
                0x01, 0x00, 0x03, // push index 1 (to read)
                136,              // LoadSubscr (reads array[1])
                0x00              // HALT
            ], 
            vec![NanVal::int(10), NanVal::int(20), NanVal::int(30), NanVal::int(1)], 
            vec![]
        );
        vm.run();
        
        // Stack top should be array[1], which is 20
        assert_eq!(vm.stack[0].as_int(), 20);
        
        // Memory should have 1 allocated object (the array)
        assert_eq!(vm.memory.total_allocated, 1);
        
        // Let's trigger a mock GC Mark & Sweep
        // We push the array ref back to stack manually to act as a root
        vm.stack[0] = NanVal::array(0); // The array is at index 0
        vm.memory.mark_roots(&vm.stack[0..1]); // Mark
        let freed = vm.memory.sweep(); // Sweep
        
        assert_eq!(freed, 0); // Array should survive because it's on stack!
        assert_eq!(vm.memory.total_allocated, 1);
        
        // Now kill the root and sweep again
        vm.stack[0] = NanVal::null();
        vm.memory.mark_roots(&vm.stack[0..1]);
        let freed_after = vm.memory.sweep();
        
        assert_eq!(freed_after, 1); // Array is dead! GC cleans it up!
        assert_eq!(vm.memory.total_allocated, 0); // RAM is completely free!
    }
}


