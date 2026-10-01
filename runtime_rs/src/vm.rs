use std::fs;
// Ureq for native web requests
use ureq;

#[derive(Clone, Copy)]
pub struct NanVal(u64);

const TAG_INT: u64 = 0x7FF8_0000_0000_0000;
const TAG_FLOAT: u64 = 0x7FF9_0000_0000_0000;
const TAG_BOOL: u64 = 0x7FFA_0000_0000_0000;
const TAG_NULL: u64 = 0x7FFB_0000_0000_0000;
const TAG_STR: u64  = 0x7FFC_0000_0000_0000; // Pointer/Index to String Heap

impl NanVal {
    #[inline(always)] pub fn int(v: i64) -> Self { NanVal(TAG_INT | (v as u64 & 0x0000_FFFF_FFFF_FFFF)) }
    #[inline(always)] pub fn float(v: f64) -> Self { NanVal(v.to_bits()) }
    #[inline(always)] pub fn bool(v: bool) -> Self { NanVal(TAG_BOOL | (if v { 1 } else { 0 })) }
    #[inline(always)] pub fn null() -> Self { NanVal(TAG_NULL) }
    #[inline(always)] pub fn string(idx: usize) -> Self { NanVal(TAG_STR | (idx as u64 & 0x0000_FFFF_FFFF_FFFF)) }

    #[inline(always)] pub fn is_int(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_INT }
    #[inline(always)] pub fn is_float(self) -> bool { self.0 < 0x7FF8_0000_0000_0000 }
    #[inline(always)] pub fn is_bool(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_BOOL }
    #[inline(always)] pub fn is_null(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_NULL }
    #[inline(always)] pub fn is_string(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_STR }

    #[inline(always)] pub fn as_int(self) -> i64 { (self.0 & 0x0000_FFFF_FFFF_FFFF) as i64 }
    #[inline(always)] pub fn as_float(self) -> f64 { f64::from_bits(self.0) }
    #[inline(always)] pub fn as_bool(self) -> bool { (self.0 & 1) == 1 }
    #[inline(always)] pub fn as_string_idx(self) -> usize { (self.0 & 0x0000_FFFF_FFFF_FFFF) as usize }
}

impl std::fmt::Display for NanVal {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        if self.is_int() { write!(f, "{}", self.as_int()) }
        else if self.is_float() { write!(f, "{}", self.as_float()) }
        else if self.is_bool() { write!(f, "{}", self.as_bool()) }
        else if self.is_null() { write!(f, "null") }
        else if self.is_string() { write!(f, "<String at {}>", self.as_string_idx()) }
        else { write!(f, "Unknown") }
    }
}

pub struct AayuVM {
    stack: [NanVal; 4096],
    sp: usize,
    ip: usize,
    bytecode: Vec<u8>,
    constants: Vec<NanVal>,
    string_heap: Vec<String>, // Arena for strings
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
        }
    }

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
                    
                    0x10 => { // ADD (Math)
                        self.sp -= 1;
                        let b = *stack.add(self.sp);
                        self.sp -= 1;
                        let a = *stack.add(self.sp);
                        if a.is_int() && b.is_int() {
                            *stack.add(self.sp) = NanVal::int(a.as_int() + b.as_int());
                        } else {
                            *stack.add(self.sp) = NanVal::null();
                        }
                        self.sp += 1;
                    }

                    0x51 => { // PRINT
                        self.sp -= 1;
                        let val = *stack.add(self.sp);
                        if val.is_string() {
                            let s = &self.string_heap[val.as_string_idx()];
                            println!("{}", s);
                        } else {
                            println!("{}", val);
                        }
                    }

                    0x60 => { // FILE_READ (Pops filename string, pushes content string)
                        self.sp -= 1;
                        let val = *stack.add(self.sp);
                        if val.is_string() {
                            let filename = &self.string_heap[val.as_string_idx()];
                            match fs::read_to_string(filename) {
                                Ok(content) => {
                                    self.string_heap.push(content);
                                    *stack.add(self.sp) = NanVal::string(self.string_heap.len() - 1);
                                },
                                Err(_) => {
                                    *stack.add(self.sp) = NanVal::null();
                                }
                            }
                        } else {
                            *stack.add(self.sp) = NanVal::null();
                        }
                        self.sp += 1;
                    }

                    0x61 => { // FILE_WRITE (Pops content, pops filename, pushes bool)
                        self.sp -= 1;
                        let content_val = *stack.add(self.sp);
                        self.sp -= 1;
                        let filename_val = *stack.add(self.sp);
                        
                        if filename_val.is_string() && content_val.is_string() {
                            let filename = &self.string_heap[filename_val.as_string_idx()];
                            let content = &self.string_heap[content_val.as_string_idx()];
                            match fs::write(filename, content) {
                                Ok(_) => *stack.add(self.sp) = NanVal::bool(true),
                                Err(_) => *stack.add(self.sp) = NanVal::bool(false),
                            }
                        } else {
                            *stack.add(self.sp) = NanVal::bool(false);
                        }
                        self.sp += 1;
                    }

                    0x70 => { // HTTP_GET (Pops URL string, fetches, pushes response string)
                        self.sp -= 1;
                        let val = *stack.add(self.sp);
                        if val.is_string() {
                            let url = &self.string_heap[val.as_string_idx()];
                            // Perform blocking HTTP GET using ureq
                            match ureq::get(url).call() {
                                Ok(response) => {
                                    if let Ok(text) = response.into_string() {
                                        self.string_heap.push(text);
                                        *stack.add(self.sp) = NanVal::string(self.string_heap.len() - 1);
                                    } else {
                                        *stack.add(self.sp) = NanVal::null();
                                    }
                                },
                                Err(_) => {
                                    *stack.add(self.sp) = NanVal::null();
                                }
                            }
                        } else {
                            *stack.add(self.sp) = NanVal::null();
                        }
                        self.sp += 1;
                    }

                    _ => {} // skip unknown
                }
            }
        }
    }
}
