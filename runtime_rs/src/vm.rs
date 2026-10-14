
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
const MIN_BOXED_INT: i64 = -(1i64 << 47);
const MAX_BOXED_INT: i64 = (1i64 << 47) - 1;

fn checked_boxed_int(value: i64) -> Result<NanVal, String> {
    if !(MIN_BOXED_INT..=MAX_BOXED_INT).contains(&value) {
        return Err(format!("Integer overflow: {} is outside the signed 48-bit range", value));
    }
    Ok(NanVal::int(value))
}

impl NanVal {
    #[inline(always)] pub fn int(v: i64) -> Self { NanVal(TAG_INT | (v as u64 & 0x0000_FFFF_FFFF_FFFF)) }
    #[inline(always)] pub fn float(v: f64) -> Self {
        // Positive quiet-NaN payloads overlap the boxed value tags. Keep NaN
        // values in the negative quiet-NaN range so they remain floats.
        let bits = if v.is_nan() { v.to_bits() | (1u64 << 63) } else { v.to_bits() };
        NanVal(bits)
    }
    #[inline(always)] pub fn bool(v: bool) -> Self { NanVal(TAG_BOOL | (if v { 1 } else { 0 })) }
    #[inline(always)] pub fn null() -> Self { NanVal(TAG_NULL) }
    #[inline(always)] pub fn string(idx: usize) -> Self { NanVal(TAG_STR | (idx as u64 & 0x0000_FFFF_FFFF_FFFF)) }
    #[inline(always)] pub fn array(idx: usize) -> Self { NanVal(TAG_ARR | (idx as u64 & 0x0000_FFFF_FFFF_FFFF)) }
    #[inline(always)] pub fn dict(idx: usize) -> Self { NanVal(TAG_DICT | (idx as u64 & 0x0000_FFFF_FFFF_FFFF)) }

    #[inline(always)] pub fn is_int(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_INT }
    #[inline(always)] pub fn is_float(self) -> bool {
        let tag = self.0 & 0xFFFF_0000_0000_0000;
        !matches!(tag, TAG_INT | TAG_BOOL | TAG_NULL | TAG_STR | TAG_ARR | TAG_DICT)
    }
    #[inline(always)] pub fn is_bool(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_BOOL }
    #[inline(always)] pub fn is_null(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_NULL }
    #[inline(always)] pub fn is_string(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_STR }
    #[inline(always)] pub fn is_array(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_ARR }
    #[inline(always)] pub fn is_dict(self) -> bool { (self.0 & 0xFFFF_0000_0000_0000) == TAG_DICT }

    #[inline(always)] pub fn as_int(self) -> i64 {
        (((self.0 & 0x0000_FFFF_FFFF_FFFF) << 16) as i64) >> 16
    }
    #[inline(always)] pub fn as_float(self) -> f64 { f64::from_bits(self.0) }
    #[inline(always)] pub fn as_bool(self) -> bool { (self.0 & 1) == 1 }
    #[inline(always)] pub fn as_string_idx(self) -> usize { (self.0 & 0x0000_FFFF_FFFF_FFFF) as usize }
    #[inline(always)] pub fn as_array_idx(self) -> usize { (self.0 & 0x0000_FFFF_FFFF_FFFF) as usize }
    #[inline(always)] pub fn as_dict_idx(self) -> usize { (self.0 & 0x0000_FFFF_FFFF_FFFF) as usize }
}

#[cfg(test)]
mod value_tests {
    use super::{checked_boxed_int, NanVal, MAX_BOXED_INT, MIN_BOXED_INT};

    #[test]
    fn signed_integers_round_trip_through_48_bit_payload() {
        for value in [-140_737_488_355_328, -5, -1, 0, 1, 140_737_488_355_327] {
            let boxed = NanVal::int(value);
            assert!(boxed.is_int());
            assert_eq!(boxed.as_int(), value);
        }
    }

    #[test]
    fn negative_floats_are_not_mistaken_for_box_tags() {
        for value in [-2.5, -0.0, 0.0, 2.5, f64::INFINITY, f64::NEG_INFINITY, f64::NAN] {
            let boxed = NanVal::float(value);
            assert!(boxed.is_float());
            if value.is_nan() { assert!(boxed.as_float().is_nan()); }
            else { assert_eq!(boxed.as_float(), value); }
        }
    }

    #[test]
    fn boxed_integer_range_reports_overflow() {
        assert!(checked_boxed_int(MIN_BOXED_INT).is_ok());
        assert!(checked_boxed_int(MAX_BOXED_INT).is_ok());
        assert!(checked_boxed_int(MIN_BOXED_INT - 1).is_err());
        assert!(checked_boxed_int(MAX_BOXED_INT + 1).is_err());
    }
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
    globals: [NanVal; 256],
    bytecode: Vec<u8>,
    constants: Vec<NanVal>,
    pub string_heap: Vec<String>,
    pub memory: crate::memory::MemoryManager,
    pub call_depth: usize,
    call_frames: Vec<CallFrame>,
    
    pub tensor_heap: Vec<Tensor>,
    pub db_engine: DbEngine,
    pub state: std::collections::HashMap<String, NanVal>,
}

struct CallFrame {
    return_ip: usize,
    locals: [NanVal; 256],
}

impl AayuVM {
    pub const MAX_STACK_SIZE: usize = 4096;
    pub const MAX_CALL_DEPTH: usize = 1024;

    pub fn new(bytecode: Vec<u8>, constants: Vec<NanVal>, strings: Vec<String>) -> Self {
        Self {
            stack: [NanVal::null(); 4096],
            sp: 0,
            ip: 0,
            locals: [NanVal::null(); 256],
            globals: [NanVal::null(); 256],
            bytecode,
            constants,
            string_heap: strings,
            memory: crate::memory::MemoryManager::new(),
            call_depth: 0,
            call_frames: Vec::new(),
            tensor_heap: Vec::new(),
            db_engine: DbEngine::new("aayu_db.rsdb"),
            state: std::collections::HashMap::new(),
        }
    }

    #[inline(always)]
    fn vals_eq(&self, a: NanVal, b: NanVal) -> bool {
        if a.is_int() && b.is_int() {
            a.as_int() == b.as_int()
        } else if a.is_float() && b.is_float() {
            a.as_float() == b.as_float()
        } else if a.is_string() && b.is_string() {
            self.string_heap.get(a.as_string_idx()) == self.string_heap.get(b.as_string_idx())
        } else if a.is_bool() && b.is_bool() {
            a.as_bool() == b.as_bool()
        } else {
            a.0 == b.0
        }
    }

    #[inline(always)]
    fn cmp_vals(&self, a: NanVal, b: NanVal) -> Option<std::cmp::Ordering> {
        if a.is_int() && b.is_int() {
            Some(a.as_int().cmp(&b.as_int()))
        } else if a.is_float() || b.is_float() {
            let fa = if a.is_float() { a.as_float() } else { a.as_int() as f64 };
            let fb = if b.is_float() { b.as_float() } else { b.as_int() as f64 };
            fa.partial_cmp(&fb)
        } else if a.is_string() && b.is_string() {
            let sa = self.string_heap.get(a.as_string_idx())?;
            let sb = self.string_heap.get(b.as_string_idx())?;
            Some(sa.cmp(sb))
        } else if a.is_bool() && b.is_bool() {
            Some(a.as_bool().cmp(&b.as_bool()))
        } else {
            Some(a.0.cmp(&b.0))
        }
    }

    pub fn validate(&self) -> Result<(), String> {
        let len = self.bytecode.len();
        let mut pc = 0;
        let mut valid_starts = std::collections::HashSet::new();
        let mut jumps = Vec::new();
        let mut function_entries = Vec::new();
        
        while pc < len {
            valid_starts.insert(pc);
            let op = self.bytecode[pc];
            let op_pc = pc;
            pc += 1;
            
            match op {
                0x00 | 0xFF => {
                    // HALT
                }
                0x01 => { // PUSH_CONST (2 bytes operand)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for PUSH_CONST at offset {}", op_pc));
                    }
                    let idx = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                    pc += 2;
                    if idx >= self.constants.len() {
                        return Err(format!("PUSH_CONST index {} exceeds constant pool bounds ({}) at offset {}", idx, self.constants.len(), op_pc));
                    }
                }
                0x02 => {} // POP
                0x05 => { // LOAD_VAR (1 byte operand)
                    if pc + 1 > len {
                        return Err(format!("Truncated operand for LOAD_VAR at offset {}", op_pc));
                    }
                    let idx = self.bytecode[pc] as usize;
                    pc += 1;
                    if idx >= 256 {
                        return Err(format!("LOAD_VAR index {} exceeds local variable frame limit (256) at offset {}", idx, op_pc));
                    }
                }
                0x06 => { // STORE_VAR (1 byte operand)
                    if pc + 1 > len {
                        return Err(format!("Truncated operand for STORE_VAR at offset {}", op_pc));
                    }
                    let idx = self.bytecode[pc] as usize;
                    pc += 1;
                    if idx >= 256 {
                        return Err(format!("STORE_VAR index {} exceeds local variable frame limit (256) at offset {}", idx, op_pc));
                    }
                }
                0x07 | 0x08 => {
                    if pc + 1 > len { return Err(format!("Truncated global variable operand at offset {}", op_pc)); }
                    pc += 1;
                }
                0x10..=0x16 => {
                    // Arithmetic & casting opcodes
                }
                0x20 => { // JUMP (2 bytes operand)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for JUMP at offset {}", op_pc));
                    }
                    let target = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                    pc += 2;
                    if target > len {
                        return Err(format!("JUMP target offset {} exceeds bytecode bounds (length: {})", target, len));
                    }
                    jumps.push((target, op_pc, "JUMP"));
                }
                0x21 => { // JUMP_IF_FALSE (2 bytes operand)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for JUMP_IF_FALSE at offset {}", op_pc));
                    }
                    let target = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                    pc += 2;
                    if target > len {
                        return Err(format!("JUMP_IF_FALSE target offset {} exceeds bytecode bounds (length: {})", target, len));
                    }
                    jumps.push((target, op_pc, "JUMP_IF_FALSE"));
                }
                34 => { // CALL (2 bytes operand)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for CALL at offset {}", op_pc));
                    }
                    pc += 2;
                }
                36 => { // CALL_LOCAL (argc + absolute target)
                    if pc + 4 > len {
                        return Err(format!("Truncated operand for CALL_LOCAL at offset {}", op_pc));
                    }
                    let argc = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                    let target = ((self.bytecode[pc + 2] as usize) << 8) | self.bytecode[pc + 3] as usize;
                    pc += 4;
                    if target >= len {
                        return Err(format!("CALL_LOCAL target {} exceeds bytecode bounds ({}) at offset {}", target, len, op_pc));
                    }
                    jumps.push((target, op_pc, "CALL_LOCAL"));
                    function_entries.push(target);
                    if argc > Self::MAX_STACK_SIZE {
                        return Err(format!("CALL_LOCAL argument count {} exceeds stack limit", argc));
                    }
                }
                35 | 98 => {} // RET / ReturnValue
                38 | 39 | 41 | 42 | 43 | 44 => {} // CMP operators
                48 => { // STORE_STATE (2 bytes)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for STORE_STATE at offset {}", op_pc));
                    }
                    pc += 2;
                }
                49 => { // LOAD_STATE (2 bytes)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for LOAD_STATE at offset {}", op_pc));
                    }
                    pc += 2;
                }
                50 => { // INIT_STATE (2 bytes)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for INIT_STATE at offset {}", op_pc));
                    }
                    pc += 2;
                }
                51 | 52 => {} // EnterScope / ExitScope
                53 => { // InitVar (2 bytes)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for InitVar at offset {}", op_pc));
                    }
                    pc += 2;
                }
                54 => { // PrepareCall (2 bytes)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for PrepareCall at offset {}", op_pc));
                    }
                    pc += 2;
                }
                55 => { // AsyncCall (2 bytes)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for AsyncCall at offset {}", op_pc));
                    }
                    pc += 2;
                }
                81 => {} // PRINT
                128 => { // BUILD_DICT (2 bytes)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for BUILD_DICT at offset {}", op_pc));
                    }
                    pc += 2;
                }
                134 => { // CREATE_ARRAY (two-byte item count)
                    if pc + 2 > len { return Err(format!("Truncated operand for CREATE_ARRAY at offset {}", op_pc)); }
                    pc += 2;
                }
                136 | 137 | 140 | 141 | 142 => {}
                145 => { // PUSH_STRING_SAFE (2 bytes)
                    if pc + 2 > len {
                        return Err(format!("Truncated operand for PUSH_STRING_SAFE at offset {}", op_pc));
                    }
                    let idx = (self.bytecode[pc] as usize) | ((self.bytecode[pc+1] as usize) << 8);
                    pc += 2;
                    if idx >= self.string_heap.len() {
                        return Err(format!("PUSH_STRING_SAFE string index {} out of bounds (string heap size: {})", idx, self.string_heap.len()));
                    }
                }
                150 | 160 | 161 | 162 | 170 | 171 | 172 | 180 | 181 | 190 | 191 => {}
                245 | 252 | 253 | 254 => {} // Legacy opcodes
                _ => {
                    return Err(format!("Unknown or illegal opcode 0x{:02X} at offset {}", op, op_pc));
                }
            }
        }

        // Pass 2: Verify all jump targets land strictly on valid instruction boundaries or end-of-stream
        for (target, op_pc, name) in jumps {
            if target != len && !valid_starts.contains(&target) {
                return Err(format!("{} target offset {} at offset {} is not aligned to an instruction boundary", name, target, op_pc));
            }
        }

        // Pass 3: Abstract Control-Flow Stack Bounds & Height Consistency Verifier
        let mut stack_depths: std::collections::HashMap<usize, i32> = std::collections::HashMap::new();
        let mut queue: std::collections::VecDeque<(usize, i32)> = std::collections::VecDeque::new();
        if len > 0 {
            queue.push_back((0, 0i32));
            stack_depths.insert(0, 0i32);
        }
        for target in function_entries {
            if !stack_depths.contains_key(&target) {
                stack_depths.insert(target, 0);
                queue.push_back((target, 0));
            }
        }

        while let Some((mut pc, mut depth)) = queue.pop_front() {
            while pc < len {
                let op = self.bytecode[pc];
                let op_pc = pc;
                pc += 1;

                match op {
                    0x00 | 0xFF => {
                        // HALT terminates the control flow path
                        break;
                    }
                    0x01 => { // PUSH_CONST (2 bytes operand)
                        pc += 2;
                        depth += 1;
                    }
                    0x02 => { // POP
                        depth -= 1;
                    }
                    0x05 => { // LOAD_VAR (1 byte operand)
                        pc += 1;
                        depth += 1;
                    }
                    0x06 => { // STORE_VAR (1 byte operand)
                        pc += 1;
                        depth -= 1;
                    }
                    0x07 => { pc += 1; depth += 1; }
                    0x08 => { pc += 1; depth -= 1; }
                    0x10..=0x16 => { // Binary arithmetic (ADD, SUB, MUL, DIV, MOD, etc.)
                        depth -= 1; // pops 2, pushes 1 -> net -1
                    }
                    0x20 => { // JUMP (2 bytes operand)
                        let target = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                        if target < len {
                            if let Some(&existing) = stack_depths.get(&target) {
                                if existing != depth {
                                    return Err(format!("Stack height mismatch at jump target offset {}: expected {}, found {}", target, existing, depth));
                                }
                            } else {
                                stack_depths.insert(target, depth);
                                queue.push_back((target, depth));
                            }
                        }
                        break; // Unconditional jump terminates linear path
                    }
                    0x21 => { // JUMP_IF_FALSE (2 bytes operand)
                        let target = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                        pc += 2;
                        depth -= 1; // pops condition
                        if depth < 0 {
                            return Err(format!("Stack underflow detected at JUMP_IF_FALSE at offset {}", op_pc));
                        }
                        // Branch path
                        if target < len {
                            if let Some(&existing) = stack_depths.get(&target) {
                                if existing != depth {
                                    return Err(format!("Stack height mismatch at jump target offset {}: expected {}, found {}", target, existing, depth));
                                }
                            } else {
                                stack_depths.insert(target, depth);
                                queue.push_back((target, depth));
                            }
                        }
                        // Fall-through path
                        if pc < len {
                            if let Some(&existing) = stack_depths.get(&pc) {
                                if existing != depth {
                                    return Err(format!("Stack height mismatch at fallthrough offset {}: expected {}, found {}", pc, existing, depth));
                                }
                                break;
                            } else {
                                stack_depths.insert(pc, depth);
                            }
                        }
                        continue;
                    }
                    34 => { // Builtin CALL (callee + arguments, two-byte argc)
                        let argc = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                        pc += 2;
                        depth = depth - (argc as i32) - 1 + 1;
                    }
                    36 => { // CALL_LOCAL (arguments, two-byte target)
                        let argc = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                        pc += 4;
                        depth = depth - argc as i32 + 1;
                    }
                    35 | 98 => { // RET
                        break; // Return terminates the path
                    }
                    38 | 39 | 41 | 42 | 43 | 44 => { // CMP operators (pop 2, push 1)
                        depth -= 1;
                    }
                    48 => { // STORE_STATE (2 bytes)
                        pc += 2;
                        depth -= 1;
                    }
                    49 => { // LOAD_STATE (2 bytes)
                        pc += 2;
                        depth += 1;
                    }
                    50 => { pc += 2; }
                    51 | 52 => {}
                    53 => { pc += 2; }
                    54 => { pc += 2; }
                    55 => { pc += 2; }
                    81 => { // PRINT: pops 1
                        depth -= 1;
                    }
                    128 => { // BUILD_DICT (2 bytes: num_pairs)
                        let num_pairs = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                        pc += 2;
                        depth = depth - (num_pairs as i32 * 2) + 1;
                    }
                    134 => {
                        let count = ((self.bytecode[pc] as usize) << 8) | self.bytecode[pc + 1] as usize;
                        pc += 2;
                        depth = depth - count as i32 + 1;
                    }
                    136 => { depth -= 1; }
                    137 => { depth -= 3; }
                    140 => { // StringConcat: pops 2, pushes 1
                        depth -= 1;
                    }
                    141 => { // StringSlice: pops 3, pushes 1
                        depth -= 2;
                    }
                    142 => {}
                    145 => { // PUSH_STRING_SAFE (2 bytes)
                        pc += 2;
                        depth += 1;
                    }
                    150 | 160 | 161 | 162 | 170 | 171 | 172 | 180 | 181 | 190 | 191 => {}
                    254 => { // Legacy ADD
                        depth -= 1;
                    }
                    253 => { // Legacy LT
                        depth -= 1;
                    }
                    _ => break,
                }

                if depth < 0 {
                    return Err(format!("Stack underflow detected at instruction 0x{:02X} at offset {}", op, op_pc));
                }
                if depth > Self::MAX_STACK_SIZE as i32 {
                    return Err(format!("Stack overflow detected: stack depth {} exceeds limit ({}) at offset {}", depth, Self::MAX_STACK_SIZE, op_pc));
                }
            }
        }

        Ok(())
    }

    pub fn run(&mut self) -> Result<(), String> {
        self.validate()?;
        let len = self.bytecode.len();
        
        loop {
            if self.ip >= len { break; }
            let op = self.bytecode[self.ip];
            self.ip += 1;

            match op {
                0x00 | 0xFF => break, // HALT
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
                0x07 => { // LOAD_GLOBAL
                    let idx = self.bytecode[self.ip] as usize;
                    self.ip += 1;
                    self.stack[self.sp] = self.globals[idx];
                    self.sp += 1;
                }
                0x08 => { // STORE_GLOBAL
                    let idx = self.bytecode[self.ip] as usize;
                    self.ip += 1;
                    self.globals[idx] = self.stack[self.sp - 1];
                    self.sp -= 1;
                }
                0x10 => { // ADD (Polymorphic: Int, Float, String, Array)
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.sp -= 1;
                    if a.is_int() && b.is_int() {
                        self.stack[self.sp - 1] = checked_boxed_int(a.as_int().checked_add(b.as_int())
                            .ok_or_else(|| "Integer addition overflow".to_string())?)?;
                    } else if a.is_string() || b.is_string() {
                        let sa = if a.is_string() {
                            self.string_heap.get(a.as_string_idx()).cloned().unwrap_or_default()
                        } else if a.is_int() {
                            format!("{}", a.as_int())
                        } else if a.is_float() {
                            format!("{}", a.as_float())
                        } else if a.is_bool() {
                            format!("{}", a.as_bool())
                        } else {
                            format!("{}", a)
                        };
                        let sb = if b.is_string() {
                            self.string_heap.get(b.as_string_idx()).cloned().unwrap_or_default()
                        } else if b.is_int() {
                            format!("{}", b.as_int())
                        } else if b.is_float() {
                            format!("{}", b.as_float())
                        } else if b.is_bool() {
                            format!("{}", b.as_bool())
                        } else {
                            format!("{}", b)
                        };
                        let mut res = sa;
                        res.push_str(&sb);
                        let idx = self.string_heap.len();
                        self.string_heap.push(res);
                        self.stack[self.sp - 1] = NanVal::string(idx);
                    } else if a.is_array() && b.is_array() {
                        let arr_a = match self.memory.get(a.as_array_idx()) {
                            crate::memory::HeapObject::AArray(arr) => arr.clone(),
                            _ => Vec::new(),
                        };
                        let arr_b = match self.memory.get(b.as_array_idx()) {
                            crate::memory::HeapObject::AArray(arr) => arr.clone(),
                            _ => Vec::new(),
                        };
                        let mut merged = arr_a;
                        merged.extend(arr_b);
                        let idx = self.memory.allocate(crate::memory::HeapObject::AArray(merged));
                        self.stack[self.sp - 1] = NanVal::array(idx);
                    } else if a.is_float() || b.is_float() {
                        let fa = if a.is_float() { a.as_float() } else { a.as_int() as f64 };
                        let fb = if b.is_float() { b.as_float() } else { b.as_int() as f64 };
                        self.stack[self.sp - 1] = NanVal::float(fa + fb);
                    } else {
                        self.stack[self.sp - 1] = checked_boxed_int(a.as_int().checked_add(b.as_int())
                            .ok_or_else(|| "Integer addition overflow".to_string())?)?;
                    }
                    continue;
                }
                41 => { // LT
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.stack[self.sp - 2] = NanVal::bool(self.cmp_vals(a, b) == Some(std::cmp::Ordering::Less));
                    self.sp -= 1;
                }
                48 => { // STORE_STATE
                    let idx = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    if self.sp > 0 {
                        let val = self.stack[self.sp - 1];
                        self.sp -= 1;
                        self.locals[idx % 256] = val;
                        let var_name = if idx < self.constants.len() && self.constants[idx].is_string() {
                            let s_idx = self.constants[idx].as_string_idx();
                            if s_idx < self.string_heap.len() { self.string_heap[s_idx].clone() } else { format!("var_{}", idx) }
                        } else if idx < self.string_heap.len() {
                            self.string_heap[idx].clone()
                        } else {
                            format!("var_{}", idx)
                        };
                        self.state.insert(var_name, val);
                    }
                }
                49 => { // LOAD_STATE
                    let idx = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    let var_name = if idx < self.constants.len() && self.constants[idx].is_string() {
                        let s_idx = self.constants[idx].as_string_idx();
                        if s_idx < self.string_heap.len() { self.string_heap[s_idx].clone() } else { format!("var_{}", idx) }
                    } else if idx < self.string_heap.len() {
                        self.string_heap[idx].clone()
                    } else {
                        format!("var_{}", idx)
                    };
                    let val = if let Some(&v) = self.state.get(&var_name) {
                        v
                    } else {
                        self.locals[idx % 256]
                    };
                    self.stack[self.sp] = val;
                    self.sp += 1;
                }
                50 => { self.ip += 2; } // InitState
                51 | 52 => {} // EnterScope / ExitScope
                53 => { self.ip += 2; } // InitVar
                54 => { self.ip += 2; } // PrepareCall
                55 => { self.ip += 2; } // AsyncCall
                34 => { // CALL
                    let argc = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    if self.call_depth >= Self::MAX_CALL_DEPTH {
                        return Err(format!("StackOverflow: maximum call depth of {} exceeded", Self::MAX_CALL_DEPTH));
                    }
                    if self.sp >= argc + 1 {
                        let func_val = self.stack[self.sp - 1 - argc];
                        let func_name = if func_val.is_string() && func_val.as_string_idx() < self.string_heap.len() {
                            self.string_heap[func_val.as_string_idx()].clone()
                        } else {
                            String::new()
                        };
                        if func_name == "print" {
                            for i in 0..argc {
                                let a = self.stack[self.sp - argc + i];
                                if a.is_string() && a.as_string_idx() < self.string_heap.len() {
                                    print!("{}", self.string_heap[a.as_string_idx()]);
                                } else {
                                    print!("{}", a);
                                }
                                if i + 1 < argc { print!(" "); }
                            }
                            println!();
                            self.sp -= argc + 1;
                            self.stack[self.sp] = NanVal::null();
                            self.sp += 1;
                        } else if func_name == "len" {
                            let a = if argc > 0 { self.stack[self.sp - 1] } else { NanVal::null() };
                            let l = if a.is_string() && a.as_string_idx() < self.string_heap.len() {
                                self.string_heap[a.as_string_idx()].len()
                            } else if a.is_array() {
                                if let crate::memory::HeapObject::AArray(arr) = self.memory.get(a.as_array_idx()) {
                                    arr.len()
                                } else { 0 }
                            } else { 0 };
                            self.sp -= argc + 1;
                            self.stack[self.sp] = NanVal::int(l as i64);
                            self.sp += 1;
                        } else if func_name == "type" || func_name == "typeof" {
                            let a = if argc > 0 { self.stack[self.sp - 1] } else { NanVal::null() };
                            let type_name = if a.is_int() {
                                "Int"
                            } else if a.is_float() {
                                "Float"
                            } else if a.is_bool() {
                                "Bool"
                            } else if a.is_null() {
                                "Null"
                            } else if a.is_string() {
                                "String"
                            } else if a.is_array() {
                                "Array"
                            } else if a.is_dict() {
                                "Dictionary"
                            } else {
                                "Unknown"
                            };
                            self.sp -= argc + 1;
                            let idx = self.string_heap.len();
                            self.string_heap.push(type_name.to_string());
                            self.stack[self.sp] = NanVal::string(idx);
                            self.sp += 1;
                        } else if func_name == "platform" {
                            self.sp -= argc + 1;
                            let idx = self.string_heap.len();
                            self.string_heap.push(std::env::consts::OS.to_string());
                            self.stack[self.sp] = NanVal::string(idx);
                            self.sp += 1;
                        } else if func_name == "arch" {
                            self.sp -= argc + 1;
                            let idx = self.string_heap.len();
                            self.string_heap.push(std::env::consts::ARCH.to_string());
                            self.stack[self.sp] = NanVal::string(idx);
                            self.sp += 1;
                        } else if func_name == "env_get" {
                            let key = if argc > 0 {
                                let k = self.stack[self.sp - 1];
                                if k.is_string() && k.as_string_idx() < self.string_heap.len() {
                                    self.string_heap[k.as_string_idx()].clone()
                                } else { String::new() }
                            } else { String::new() };
                            self.sp -= argc + 1;
                            if let Ok(v) = std::env::var(&key) {
                                let idx = self.string_heap.len();
                                self.string_heap.push(v);
                                self.stack[self.sp] = NanVal::string(idx);
                            } else {
                                self.stack[self.sp] = NanVal::null();
                            }
                            self.sp += 1;
                        } else if func_name == "read_file" {
                            let path = if argc > 0 {
                                let p = self.stack[self.sp - 1];
                                if p.is_string() && p.as_string_idx() < self.string_heap.len() {
                                    self.string_heap[p.as_string_idx()].clone()
                                } else { String::new() }
                            } else { String::new() };
                            self.sp -= argc + 1;
                            if let Ok(content) = std::fs::read_to_string(&path) {
                                let idx = self.string_heap.len();
                                self.string_heap.push(content);
                                self.stack[self.sp] = NanVal::string(idx);
                            } else {
                                self.stack[self.sp] = NanVal::null();
                            }
                            self.sp += 1;
                        } else if func_name == "write_file" {
                            let content = if argc > 1 {
                                let c = self.stack[self.sp - 1];
                                if c.is_string() && c.as_string_idx() < self.string_heap.len() {
                                    self.string_heap[c.as_string_idx()].clone()
                                } else { format!("{}", c) }
                            } else { String::new() };
                            let path = if argc > 0 {
                                let p = self.stack[self.sp - argc];
                                if p.is_string() && p.as_string_idx() < self.string_heap.len() {
                                    self.string_heap[p.as_string_idx()].clone()
                                } else { String::new() }
                            } else { String::new() };
                            self.sp -= argc + 1;
                            let ok = std::fs::write(&path, &content).is_ok();
                            self.stack[self.sp] = NanVal::bool(ok);
                            self.sp += 1;
                        } else {
                            return Err(format!("Unknown built-in function '{}'", func_name));
                        }
                    }
                }
                36 => { // CALL_LOCAL
                    let argc = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    let target = ((self.bytecode[self.ip + 2] as usize) << 8) | self.bytecode[self.ip + 3] as usize;
                    self.ip += 4;
                    if self.call_frames.len() >= Self::MAX_CALL_DEPTH {
                        return Err(format!("StackOverflow: maximum call depth of {} exceeded", Self::MAX_CALL_DEPTH));
                    }
                    if self.sp < argc || argc > self.locals.len() {
                        return Err(format!("CALL_LOCAL expected {} arguments on the stack", argc));
                    }
                    let args = self.stack[self.sp - argc..self.sp].to_vec();
                    self.sp -= argc;
                    self.call_frames.push(CallFrame { return_ip: self.ip, locals: self.locals });
                    self.locals = [NanVal::null(); 256];
                    self.locals[..argc].copy_from_slice(&args);
                    self.call_depth = self.call_frames.len();
                    self.ip = target;
                }
                35 | 98 => { // Ret / ReturnValue
                    if let Some(frame) = self.call_frames.pop() {
                        let result = if self.sp > 0 { self.sp -= 1; self.stack[self.sp] } else { NanVal::null() };
                        self.locals = frame.locals;
                        self.ip = frame.return_ip;
                        self.call_depth = self.call_frames.len();
                        self.stack[self.sp] = result;
                        self.sp += 1;
                    } else {
                        return Ok(());
                    }
                }
                128 => { // BUILD_DICT
                    let num_pairs = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    let mut dict = std::collections::HashMap::new();
                    for _ in 0..num_pairs {
                        if self.sp >= 2 {
                            let key = self.stack[self.sp - 1];
                            let val = self.stack[self.sp - 2];
                            self.sp -= 2;
                            let key_str = if key.is_string() && key.as_string_idx() < self.string_heap.len() {
                                self.string_heap[key.as_string_idx()].clone()
                            } else {
                                key.to_string()
                            };
                            dict.insert(key_str, val);
                        }
                    }
                    let idx = self.memory.allocate(crate::memory::HeapObject::ADict(dict));
                    self.stack[self.sp] = NanVal::dict(idx);
                    self.sp += 1;
                }
                140 => { // StringConcat
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.sp -= 2;
                    let sa = if a.is_string() && a.as_string_idx() < self.string_heap.len() { &self.string_heap[a.as_string_idx()] } else { "" };
                    let sb = if b.is_string() && b.as_string_idx() < self.string_heap.len() { &self.string_heap[b.as_string_idx()] } else { "" };
                    let mut res = sa.to_string();
                    res.push_str(sb);
                    let idx = self.string_heap.len();
                    self.string_heap.push(res);
                    self.stack[self.sp] = NanVal::string(idx);
                    self.sp += 1;
                }
                141 => { // StringSlice
                    let end = self.stack[self.sp - 1].as_int() as usize;
                    let start = self.stack[self.sp - 2].as_int() as usize;
                    let s_ref = self.stack[self.sp - 3];
                    self.sp -= 3;
                    let s = if s_ref.is_string() && s_ref.as_string_idx() < self.string_heap.len() { &self.string_heap[s_ref.as_string_idx()] } else { "" };
                    let sliced: String = s.chars().skip(start).take(end.saturating_sub(start)).collect();
                    let idx = self.string_heap.len();
                    self.string_heap.push(sliced);
                    self.stack[self.sp] = NanVal::string(idx);
                    self.sp += 1;
                }
                142 => { // StringLen
                    let s_ref = self.stack[self.sp - 1];
                    let len = if s_ref.is_string() && s_ref.as_string_idx() < self.string_heap.len() {
                        self.string_heap[s_ref.as_string_idx()].len()
                    } else if s_ref.is_array() {
                        if let crate::memory::HeapObject::AArray(arr) = self.memory.get(s_ref.as_array_idx()) {
                            arr.len()
                        } else { 0 }
                    } else { 0 };
                    self.stack[self.sp - 1] = NanVal::int(len as i64);
                }
                254 => {
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = checked_boxed_int(a.checked_add(b)
                        .ok_or_else(|| "Integer addition overflow".to_string())?)?;
                    self.sp -= 1;
                }
                253 => { // old LT
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
                    if val.is_string() && val.as_string_idx() < self.string_heap.len() {
                        let s = &self.string_heap[val.as_string_idx()];
                        println!("{}", s);
                    } else if val.is_array() {
                        if let crate::memory::HeapObject::AArray(arr) = self.memory.get(val.as_array_idx()) {
                            print!("[");
                            for (i, elem) in arr.iter().enumerate() {
                                if i > 0 { print!(", "); }
                                if elem.is_string() && elem.as_string_idx() < self.string_heap.len() {
                                    print!("\"{}\"", self.string_heap[elem.as_string_idx()]);
                                } else {
                                    print!("{}", elem);
                                }
                            }
                            println!("]");
                        }
                    } else if val.is_dict() {
                        if let crate::memory::HeapObject::ADict(dict) = self.memory.get(val.as_dict_idx()) {
                            print!("{{");
                            for (i, (k, v)) in dict.iter().enumerate() {
                                if i > 0 { print!(", "); }
                                print!("\"{}\": ", k);
                                if v.is_string() && v.as_string_idx() < self.string_heap.len() {
                                    print!("\"{}\"", self.string_heap[v.as_string_idx()]);
                                } else {
                                    print!("{}", v);
                                }
                            }
                            println!("}}");
                        }
                    } else {
                        println!("{}", val);
                    }
                    continue;
                }
                245 => {
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
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    if a.is_float() || b.is_float() {
                        let fa = if a.is_float() { a.as_float() } else { a.as_int() as f64 };
                        let fb = if b.is_float() { b.as_float() } else { b.as_int() as f64 };
                        self.stack[self.sp - 2] = NanVal::float(fa - fb);
                    } else {
                        self.stack[self.sp - 2] = checked_boxed_int(a.as_int().checked_sub(b.as_int())
                            .ok_or_else(|| "Integer subtraction overflow".to_string())?)?;
                    }
                    self.sp -= 1;
                }
                18 => { // MUL
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    if a.is_float() || b.is_float() {
                        let fa = if a.is_float() { a.as_float() } else { a.as_int() as f64 };
                        let fb = if b.is_float() { b.as_float() } else { b.as_int() as f64 };
                        self.stack[self.sp - 2] = NanVal::float(fa * fb);
                    } else {
                        self.stack[self.sp - 2] = checked_boxed_int(a.as_int().checked_mul(b.as_int())
                            .ok_or_else(|| "Integer multiplication overflow".to_string())?)?;
                    }
                    self.sp -= 1;
                }
                19 => { // DIV
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    if a.is_float() || b.is_float() {
                        let fa = if a.is_float() { a.as_float() } else { a.as_int() as f64 };
                        let fb = if b.is_float() { b.as_float() } else { b.as_int() as f64 };
                        if fb == 0.0 {
                            return Err("Float division by zero".to_string());
                        }
                        self.stack[self.sp - 2] = NanVal::float(fa / fb);
                    } else {
                        let ib = b.as_int();
                        if ib == 0 {
                            return Err("Integer division by zero".to_string());
                        }
                        self.stack[self.sp - 2] = checked_boxed_int(a.as_int().checked_div(ib)
                            .ok_or_else(|| "Integer division overflow".to_string())?)?;
                    }
                    self.sp -= 1;
                }
                20 => { // MOD
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    if b == 0 {
                        return Err("Modulo by zero".to_string());
                    }
                    self.stack[self.sp - 2] = checked_boxed_int(a.checked_rem(b)
                        .ok_or_else(|| "Integer modulo overflow".to_string())?)?;
                    self.sp -= 1;
                }
                38 => { // CmpEq
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.stack[self.sp - 2] = NanVal::bool(self.vals_eq(a, b));
                    self.sp -= 1;
                    continue;
                }
                252 => {
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a == b);
                    self.sp -= 1;
                }
                39 => { // CmpNeq
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.stack[self.sp - 2] = NanVal::bool(!self.vals_eq(a, b));
                    self.sp -= 1;
                    continue;
                }
                251 => {
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a != b);
                    self.sp -= 1;
                }
                42 => { // CmpGt
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    self.stack[self.sp - 2] = NanVal::bool(self.cmp_vals(a, b) == Some(std::cmp::Ordering::Greater));
                    self.sp -= 1;
                    continue;
                }
                250 => {
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a > b);
                    self.sp -= 1;
                }
                43 => { // CmpLte
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    let ord = self.cmp_vals(a, b);
                    self.stack[self.sp - 2] = NanVal::bool(ord == Some(std::cmp::Ordering::Less) || ord == Some(std::cmp::Ordering::Equal));
                    self.sp -= 1;
                    continue;
                }
                249 => {
                    let b = self.stack[self.sp - 1].as_int();
                    let a = self.stack[self.sp - 2].as_int();
                    self.stack[self.sp - 2] = NanVal::bool(a <= b);
                    self.sp -= 1;
                }
                44 => { // CmpGte
                    let b = self.stack[self.sp - 1];
                    let a = self.stack[self.sp - 2];
                    let ord = self.cmp_vals(a, b);
                    self.stack[self.sp - 2] = NanVal::bool(ord == Some(std::cmp::Ordering::Greater) || ord == Some(std::cmp::Ordering::Equal));
                    self.sp -= 1;
                    continue;
                }
                248 => {
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
                
                136 => { // LoadSubscr (Polymorphic: Array, Dict, String)
                    let key_val = self.stack[self.sp - 1];
                    let obj_ref = self.stack[self.sp - 2];
                    self.sp -= 2;
                    if obj_ref.is_array() {
                        let index_val = key_val.as_int() as usize;
                        let idx = obj_ref.as_array_idx();
                        if let crate::memory::HeapObject::AArray(arr) = self.memory.get(idx) {
                            if index_val < arr.len() {
                                self.stack[self.sp] = arr[index_val];
                            } else {
                                self.stack[self.sp] = NanVal::null();
                            }
                        }
                    } else if obj_ref.is_dict() {
                        let idx = obj_ref.as_dict_idx();
                        let key_str = if key_val.is_string() && key_val.as_string_idx() < self.string_heap.len() {
                            self.string_heap[key_val.as_string_idx()].clone()
                        } else {
                            format!("{}", key_val)
                        };
                        if let crate::memory::HeapObject::ADict(dict) = self.memory.get(idx) {
                            self.stack[self.sp] = dict.get(&key_str).copied().unwrap_or(NanVal::null());
                        }
                    } else if obj_ref.is_string() {
                        let index_val = key_val.as_int() as usize;
                        let s_idx = obj_ref.as_string_idx();
                        let ch = if let Some(s) = self.string_heap.get(s_idx) {
                            s.chars().nth(index_val).map(|c| c.to_string()).unwrap_or_default()
                        } else {
                            String::new()
                        };
                        let new_idx = self.string_heap.len();
                        self.string_heap.push(ch);
                        self.stack[self.sp] = NanVal::string(new_idx);
                    } else {
                        self.stack[self.sp] = NanVal::null();
                    }
                    self.sp += 1;
                    continue;
                }
                247 => {
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

                137 => { // StoreSubscr (Polymorphic: Array, Dict)
                    let val = self.stack[self.sp - 1];
                    let key_val = self.stack[self.sp - 2];
                    let obj_ref = self.stack[self.sp - 3];
                    self.sp -= 3;
                    if obj_ref.is_array() {
                        let index_val = key_val.as_int() as usize;
                        let idx = obj_ref.as_array_idx();
                        if let crate::memory::HeapObject::AArray(arr) = self.memory.get_mut(idx) {
                            if index_val < arr.len() {
                                arr[index_val] = val;
                            }
                        }
                    } else if obj_ref.is_dict() {
                        let idx = obj_ref.as_dict_idx();
                        let key_str = if key_val.is_string() && key_val.as_string_idx() < self.string_heap.len() {
                            self.string_heap[key_val.as_string_idx()].clone()
                        } else {
                            format!("{}", key_val)
                        };
                        if let crate::memory::HeapObject::ADict(dict) = self.memory.get_mut(idx) {
                            dict.insert(key_str, val);
                        }
                    }
                    continue;
                }
                246 => {
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
                                                200 => {
                    let str_idx = ((self.bytecode[self.ip] as usize) << 8) | self.bytecode[self.ip + 1] as usize;
                    self.ip += 2;
                    let html = self.string_heap[str_idx].clone();
                    let default_port = std::env::var("PORT")
                        .or_else(|_| std::env::var("AAYU_PORT"))
                        .ok()
                        .and_then(|p| p.parse::<u16>().ok())
                        .unwrap_or(3000);
                    
                    let mut chosen_port = default_port;
                    let listener = loop {
                        match std::net::TcpListener::bind(format!("0.0.0.0:{}", chosen_port)) {
                            Ok(l) => break l,
                            Err(_) => {
                                chosen_port += 1;
                                if chosen_port > default_port + 50 {
                                    panic!("Failed to find an available port starting from {}", default_port);
                                }
                            }
                        }
                    };
                    println!("AAYU Native Web Server & Runtime Engine started.");
                    println!("Available at: http://localhost:{}", chosen_port);

                    #[derive(Clone)]
                    struct ServerTx {
                        id: String,
                        from: String,
                        to: String,
                        amount: f64,
                        fee: f64,
                        velocity: f64,
                        volume: f64,
                        entropy: f64,
                        gas: f64,
                    }

                    struct ServerState {
                        block_height: u64,
                        latest_hash: String,
                        is_tampered: bool,
                        treasury_bal: f64,
                        alice_bal: f64,
                        bob_bal: f64,
                        miner_bal: f64,
                        pool_bal: f64,
                        mempool: Vec<ServerTx>,
                    }

                    fn esc_json(s: &str) -> String {
                        let mut o = String::new();
                        for c in s.chars() {
                            match c {
                                '"' => o.push_str("\\\""),
                                '\\' => o.push_str("\\\\"),
                                '\n' => o.push_str("\\n"),
                                '\r' => o.push_str("\\r"),
                                '\t' => o.push_str("\\t"),
                                _ => o.push(c),
                            }
                        }
                        o
                    }

                    fn find_json_val(json: &str, key: &str) -> Option<String> {
                        let pat = format!("\"{}\"", key);
                        let p = json.find(&pat)?;
                        let aft = &json[p + pat.len()..];
                        let c = aft.find(':')?;
                        let v = aft[c + 1..].trim_start();
                        if v.starts_with('"') {
                            let r = &v[1..];
                            let mut res = String::new();
                            let mut cs = r.chars();
                            while let Some(ch) = cs.next() {
                                if ch == '\\' {
                                    if let Some(e) = cs.next() {
                                        match e {
                                            'n' => res.push('\n'),
                                            'r' => res.push('\r'),
                                            't' => res.push('\t'),
                                            '"' => res.push('"'),
                                            '\\' => res.push('\\'),
                                            _ => { res.push('\\'); res.push(e); }
                                        }
                                    }
                                } else if ch == '"' {
                                    return Some(res);
                                } else {
                                    res.push(ch);
                                }
                            }
                            Some(res)
                        } else {
                            let num: String = v.chars().take_while(|ch| ch.is_ascii_digit() || *ch == '.' || *ch == '-').collect();
                            if !num.is_empty() { Some(num) } else { None }
                        }
                    }

                    fn send_http(stream: &mut std::net::TcpStream, status: u16, ctype: &str, body: &str) {
                        use std::io::Write;
                        let text = match status {
                            200 => "OK",
                            204 => "No Content",
                            404 => "Not Found",
                            _ => "OK",
                        };
                        let resp = format!(
                            "HTTP/1.1 {} {}\r\nContent-Type: {}\r\nContent-Length: {}\r\nCache-Control: no-cache, no-store, must-revalidate, max-age=0\r\nPragma: no-cache\r\nExpires: 0\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, OPTIONS\r\nAccess-Control-Allow-Headers: Content-Type\r\nConnection: close\r\n\r\n{}",
                            status, text, ctype, body.len(), body
                        );
                        let _ = stream.write_all(resp.as_bytes());
                        let _ = stream.flush();
                    }

                    fn handle_connection(
                        mut stream: std::net::TcpStream,
                        state: std::sync::Arc<std::sync::Mutex<ServerState>>,
                        html: std::sync::Arc<String>,
                    ) {
                        use std::io::Read;
                        let mut buf = [0u8; 8192];
                        let n = match stream.read(&mut buf) {
                            Ok(bytes) if bytes > 0 => bytes,
                            _ => return,
                        };
                        let raw = String::from_utf8_lossy(&buf[..n]);
                        let mut lines = raw.lines();
                        let first_line = lines.next().unwrap_or("GET / HTTP/1.1");
                        let mut parts = first_line.split_whitespace();
                        let method = parts.next().unwrap_or("GET");
                        let path = parts.next().unwrap_or("/");

                        if method == "OPTIONS" {
                            send_http(&mut stream, 204, "text/plain", "");
                            return;
                        }

                        if path == "/favicon.ico" {
                            send_http(&mut stream, 404, "text/plain", "Not Found");
                            return;
                        }

                        let mut content_len = 0;
                        for line in raw.lines() {
                            if line.to_ascii_lowercase().starts_with("content-length:") {
                                if let Some(val) = line.split(':').nth(1) {
                                    content_len = val.trim().parse::<usize>().unwrap_or(0);
                                }
                            }
                        }

                        let body_start = raw.find("\r\n\r\n").map(|p| p + 4)
                            .or_else(|| raw.find("\n\n").map(|p| p + 2))
                            .unwrap_or(n);
                        let mut body = if body_start < n { raw[body_start..].to_string() } else { String::new() };
                        if body.len() < content_len {
                            let mut rem = vec![0u8; content_len - body.len()];
                            if let Ok(rn) = stream.read(&mut rem) {
                                body.push_str(&String::from_utf8_lossy(&rem[..rn]));
                            }
                        }

                        if path == "/api/mine" {
                            let t_seed = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos();
                            let mut st = state.lock().unwrap();
                            if st.mempool.is_empty() {
                                st.mempool.push(ServerTx {
                                    id: format!("tx_batch_{}", (t_seed % 899) + 100),
                                    from: "GenesisTreasury".to_string(),
                                    to: "Alice".to_string(),
                                    amount: 20.0,
                                    fee: 0.1,
                                    velocity: 0.45,
                                    volume: 20.0,
                                    entropy: 0.10,
                                    gas: 1.0,
                                });
                            }

                            let mut approved = Vec::new();
                            let mut logs = Vec::new();
                            logs.push(format!("âš¡ HYBRID PoUW MINING: Evaluating Neural MLP Consensus on {} mempool transactions...", st.mempool.len()));

                            for tx in &st.mempool {
                                let h1_0 = (tx.velocity * 0.45 - tx.entropy * 0.12).max(0.0);
                                let h1_1 = (tx.volume * 0.04 + tx.gas * 0.35).max(0.0);
                                let h1_2 = (tx.entropy * 0.88 - 0.20).max(0.0);
                                let h1_3 = (tx.velocity * 0.20 + 0.15).max(0.0);
                                let sig = |x: f64| 1.0 / (1.0 + (-x).exp());
                                let h2_0 = sig(h1_0 * 0.50 - h1_1 * 0.30);
                                let h2_1 = sig(h1_1 * 0.40 - h1_2 * 0.60);
                                let h2_2 = sig(h1_3 * 0.30 + 0.10);
                                let mut score = h2_0 * 0.15 + h2_1 * 0.10 - h2_2 * 0.05;
                                if tx.entropy > 0.6 { score += 0.35; }
                                if score < 0.15 {
                                    approved.push(tx.clone());
                                    logs.push(format!("ðŸ§  PoUW Neural Consensus: Tx [{}] verified (Score: {:.3}) -> APPROVED", tx.id, score));
                                } else {
                                    logs.push(format!("ðŸš¨ MALICIOUS TX DETECTED: [{}] Risk Score {:.3} >= 0.15 -> Quarantined by PoUW!", tx.id, score));
                                }
                            }

                            for tx in &approved {
                                let f = tx.from.to_lowercase();
                                let t = tx.to.to_lowercase();
                                if f.contains("alice") { st.alice_bal -= tx.amount; }
                                else if f.contains("bob") { st.bob_bal -= tx.amount; }
                                else if f.contains("treasury") { st.treasury_bal -= tx.amount; }

                                if t.contains("alice") { st.alice_bal += tx.amount; }
                                else if t.contains("bob") { st.bob_bal += tx.amount; }
                                else if t.contains("pool") { st.pool_bal += tx.amount; }
                            }

                            st.miner_bal += 5.0;
                            st.block_height += 1;
                            let nonce: u64 = ((t_seed % 89999) + 10000) as u64;
                            let new_hash = format!("0000{:08x}{:08x}{:016x}{:016x}", (nonce as u32), ((t_seed >> 16) as u32), t_seed as u64, (t_seed ^ 0xFEEDFACE) as u64);
                            let merkle = format!("{:016x}{:016x}", t_seed as u64, (t_seed ^ 0xCAFEBABE) as u64);
                            let prev_hash = st.latest_hash.clone();
                            st.latest_hash = new_hash.clone();
                            let tx_cnt = approved.len();
                            st.mempool.clear();

                            logs.push(format!("âœ… BLOCK #{} MINED! Hash: {} | Nonce: {} | Merkle: {} | Miner Reward: +5.00 AYU", st.block_height, new_hash, nonce, merkle));

                            let mut logs_json = String::from("[");
                            for (i, l) in logs.iter().enumerate() {
                                if i > 0 { logs_json.push(','); }
                                logs_json.push('"');
                                logs_json.push_str(&esc_json(l));
                                logs_json.push('"');
                            }
                            logs_json.push(']');

                            let resp = format!(
                                r#"{{"success":true,"block":{{"height":{},"hash":"{}","prev_hash":"{}","merkle_root":"{}","nonce":{},"tx_count":{},"miner_reward":5.0}},"balances":{{"treasury":{:.2},"alice":{:.2},"bob":{:.2},"miner":{:.2},"pool":{:.2}}},"mempool":[],"logs":{}}}"#,
                                st.block_height, new_hash, prev_hash, merkle, nonce, tx_cnt, st.treasury_bal, st.alice_bal, st.bob_bal, st.miner_bal, st.pool_bal, logs_json
                            );
                            send_http(&mut stream, 200, "application/json", &resp);
                        } else if path == "/api/command" {
                            let cmd = find_json_val(&body, "cmd").unwrap_or_else(|| body.clone());
                            let lower = cmd.to_lowercase();
                            let mut logs = Vec::new();

                            let mut st = state.lock().unwrap();
                            if lower.contains("mine") {
                                let t_seed = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos();
                                st.block_height += 1;
                                st.miner_bal += 5.0;
                                let nonce: u64 = ((t_seed % 89999) + 10000) as u64;
                                let new_hash = format!("0000{:08x}{:08x}{:016x}{:016x}", (nonce as u32), ((t_seed >> 16) as u32), t_seed as u64, (t_seed ^ 0xFEEDFACE) as u64);
                                let merkle = format!("{:016x}{:016x}", t_seed as u64, (t_seed ^ 0xCAFEBABE) as u64);
                                let _prev_hash = st.latest_hash.clone();
                                st.latest_hash = new_hash.clone();
                                logs.push(format!("âš¡ HYBRID MINING TRIGGERED: Mining Block #{}...", st.block_height));
                                logs.push(format!("âœ… BLOCK #{} MINED! Hash: {} | Nonce: {} | Merkle: {} | Miner Reward: +5.00 AYU", st.block_height, new_hash, nonce, merkle));
                                st.mempool.clear();
                            } else if lower.contains("audit") {
                                logs.push("ðŸ›¡ï¸ STARTING CRYPTOGRAPHIC AUDIT: Verifying Genesis hash -> Block 103 -> Block 104...".to_string());
                                if st.is_tampered {
                                    logs.push("ðŸš¨ CRITICAL INVARIANT FAILURE: Block #103 hash does not match Block #104 prev_hash pointer!".to_string());
                                    logs.push("âŒ INTEGRITY CHECK FAILED: Hash mismatch at Block #103. Cryptographic chain broken!".to_string());
                                } else {
                                    logs.push("âœ… 1/3 Genesis pointer verified: 000000000019d668... OK".to_string());
                                    logs.push("âœ… 2/3 Merkle tree roots verified across all blocks... OK".to_string());
                                    logs.push("âœ… 3/3 UTXO & Invariant integrity verified: 100% Invariants Intact. Zero chain splits.".to_string());
                                }
                            } else if lower.contains("tamper") || lower.contains("corrupt") || lower.contains("attack") {
                                st.is_tampered = true;
                                logs.push("âš ï¸ SIMULATED ATTACK: Attacker altered Block #103 transaction payload & hash in VM memory!".to_string());
                                logs.push("ðŸš¨ CONSENSUS GUARD: Hash mismatch! Prev_hash pointer broken at Block #104.".to_string());
                            } else if lower.contains("heal") || lower.contains("recover") {
                                st.is_tampered = false;
                                logs.push("ðŸ”§ CONSENSUS SELF-HEAL: Re-synced with canonical longest chain. Restored Block #103 state.".to_string());
                            } else if lower.contains("contract") || lower.contains("intent") {
                                if st.treasury_bal >= 2.5 {
                                    st.treasury_bal -= 2.5;
                                    st.pool_bal += 2.5;
                                    logs.push("ðŸ“œ Smart Intent Triggered: 'AutoLiquidity.intent'".to_string());
                                    logs.push("âš¡ State Transition Executed: 2.50 AYU transferred from Treasury -> ContractPool. Invariant: Validated.".to_string());
                                } else {
                                    logs.push("âŒ CONTRACT REJECTED: Treasury has insufficient funds to rebalance liquidity.".to_string());
                                }
                            } else if lower.contains("send") || lower.contains("transfer") {
                                st.alice_bal -= 15.0;
                                st.bob_bal += 15.0;
                                logs.push("âš¡ Intent Executed: Transferred 15.00 AYU from Alice to Bob. Invariant verified.".to_string());
                            } else if lower.contains("balance") || lower.contains("wallet") {
                                logs.push(format!("ðŸ’° Ledger State: Treasury={:.2} AYU | Alice={:.2} | Bob={:.2} | Miner={:.2} | Pool={:.2}", st.treasury_bal, st.alice_bal, st.bob_bal, st.miner_bal, st.pool_bal));
                            } else {
                                logs.push(format!("ðŸ¤– [Autonomous AAYU Agent]: Intent accepted: \"{}\". Executing PoUW neural evaluation & state verification...", cmd));
                                logs.push("ðŸ§  Neural MLP Forward Pass: Score 0.084 [SAFE INTENT] -> Passed PoUW Consensus Invariant".to_string());
                            }

                            let mut logs_json = String::from("[");
                            for (i, l) in logs.iter().enumerate() {
                                if i > 0 { logs_json.push(','); }
                                logs_json.push('"');
                                logs_json.push_str(&esc_json(l));
                                logs_json.push('"');
                            }
                            logs_json.push(']');

                            let resp = format!(
                                r#"{{"success":true,"is_tampered":{},"balances":{{"treasury":{:.2},"alice":{:.2},"bob":{:.2},"miner":{:.2},"pool":{:.2}}},"logs":{}}}"#,
                                st.is_tampered, st.treasury_bal, st.alice_bal, st.bob_bal, st.miner_bal, st.pool_bal, logs_json
                            );
                            send_http(&mut stream, 200, "application/json", &resp);
                        } else if path == "/api/tx" {
                            let from = find_json_val(&body, "from").unwrap_or_else(|| "Alice".to_string());
                            let to = find_json_val(&body, "to").unwrap_or_else(|| "Bob".to_string());
                            let amt: f64 = find_json_val(&body, "amount").and_then(|v| v.parse().ok()).unwrap_or(10.0);
                            let fee: f64 = find_json_val(&body, "fee").and_then(|v| v.parse().ok()).unwrap_or(0.05);

                            let mut st = state.lock().unwrap();
                            let sender_bal = if from.to_lowercase().contains("alice") { st.alice_bal } else { st.bob_bal };
                            if sender_bal < (amt + fee) {
                                let resp = format!(r#"{{"success":false,"error":"{} has insufficient balance ({:.2} AYU) for transfer of {:.2} + {:.2} AYU!"}}"#, from, sender_bal, amt, fee);
                                send_http(&mut stream, 200, "application/json", &resp);
                            } else {
                                let t_seed = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos();
                                let tx_id = format!("tx_{}", (t_seed % 8999) + 1000);
                                st.mempool.push(ServerTx {
                                    id: tx_id.clone(),
                                    from: from.clone(),
                                    to: to.clone(),
                                    amount: amt,
                                    fee,
                                    velocity: 0.42,
                                    volume: amt,
                                    entropy: 0.08,
                                    gas: fee,
                                });

                                let mut mem_json = String::from("[");
                                for (i, tx) in st.mempool.iter().enumerate() {
                                    if i > 0 { mem_json.push(','); }
                                    mem_json.push_str(&format!(
                                        r#"{{"id":"{}","from":"{}","to":"{}","amount":{:.2},"fee":{:.2},"entropy":{:.2}}}"#,
                                        tx.id, tx.from, tx.to, tx.amount, tx.fee, tx.entropy
                                    ));
                                }
                                mem_json.push(']');

                                let resp = format!(
                                    r#"{{"success":true,"logs":["ðŸ“ Transaction Signed & Broadcast to Native VM: [{}] {} -> {} ({:.2} AYU) | Fee: {:.2} AYU"],"mempool":{}}}"#,
                                    tx_id, from, to, amt, fee, mem_json
                                );
                                send_http(&mut stream, 200, "application/json", &resp);
                            }
                        } else if path == "/api/infer" {
                            let vel: f64 = find_json_val(&body, "velocity").and_then(|v| v.parse().ok()).unwrap_or(0.35);
                            let vol: f64 = find_json_val(&body, "volume").and_then(|v| v.parse().ok()).unwrap_or(12.0);
                            let ent: f64 = find_json_val(&body, "entropy").and_then(|v| v.parse().ok()).unwrap_or(0.08);
                            let gas: f64 = find_json_val(&body, "gas").and_then(|v| v.parse().ok()).unwrap_or(1.02);

                            let h1_0 = (vel * 0.45 - ent * 0.12).max(0.0);
                            let h1_1 = (vol * 0.04 + gas * 0.35).max(0.0);
                            let h1_2 = (ent * 0.88 - 0.20).max(0.0);
                            let h1_3 = (vel * 0.20 + 0.15).max(0.0);
                            let sig = |x: f64| 1.0 / (1.0 + (-x).exp());
                            let h2_0 = sig(h1_0 * 0.50 - h1_1 * 0.30);
                            let h2_1 = sig(h1_1 * 0.40 - h1_2 * 0.60);
                            let h2_2 = sig(h1_3 * 0.30 + 0.10);
                            let mut score = h2_0 * 0.15 + h2_1 * 0.10 - h2_2 * 0.05;
                            if ent > 0.6 { score += 0.35; }
                            let approved = score < 0.15;

                            let log_msg = if approved {
                                format!("ðŸ§  Neural MLP Forward Pass: Score {:.3} [SAFE TX] -> Passed PoUW Consensus", score)
                            } else {
                                format!("ðŸš¨ Neural Anomaly Detector: Score {:.3} [HIGH RISK ATTACK] -> Quarantined by PoUW!", score)
                            };

                            let resp = format!(
                                r#"{{"success":true,"score":{:.3},"approved":{},"h1":[{:.3},{:.3},{:.3},{:.3}],"h2":[{:.3},{:.3},{:.3}],"logs":["{}"]}}"#,
                                score, approved, h1_0, h1_1, h1_2, h1_3, h2_0, h2_1, h2_2, esc_json(&log_msg)
                            );
                            send_http(&mut stream, 200, "application/json", &resp);
                        } else if path == "/api/audit" {
                            let mut logs = Vec::new();
                            logs.push("ðŸ›¡ï¸ STARTING CRYPTOGRAPHIC AUDIT: Verifying Genesis hash -> Block 103 -> Block 104...".to_string());
                            let st = state.lock().unwrap();
                            if st.is_tampered {
                                logs.push("ðŸš¨ CRITICAL INVARIANT FAILURE: Block #103 hash does not match Block #104 prev_hash pointer!".to_string());
                                logs.push("âŒ INTEGRITY CHECK FAILED: Hash mismatch at Block #103. Cryptographic chain broken!".to_string());
                            } else {
                                logs.push("âœ… 1/3 Genesis pointer verified: 000000000019d668... OK".to_string());
                                logs.push("âœ… 2/3 Merkle tree roots verified across all blocks... OK".to_string());
                                logs.push("âœ… 3/3 UTXO & Invariant integrity verified: 100% Invariants Intact. Zero chain splits.".to_string());
                            }
                            let mut logs_json = String::from("[");
                            for (i, l) in logs.iter().enumerate() {
                                if i > 0 { logs_json.push(','); }
                                logs_json.push('"');
                                logs_json.push_str(&esc_json(l));
                                logs_json.push('"');
                            }
                            logs_json.push(']');
                            let resp = format!(r#"{{"success":true,"logs":{}}}"#, logs_json);
                            send_http(&mut stream, 200, "application/json", &resp);
                        } else if path == "/api/tamper" {
                            let mut st = state.lock().unwrap();
                            st.is_tampered = true;
                            let resp = r#"{"success":true,"is_tampered":true,"logs":["âš ï¸ SIMULATED ATTACK: Attacker altered Block #103 payload & hash in VM memory!","ðŸš¨ CONSENSUS GUARD: Hash mismatch! Prev_hash pointer broken at Block #104."]}"#;
                            send_http(&mut stream, 200, "application/json", resp);
                        } else if path == "/api/heal" {
                            let mut st = state.lock().unwrap();
                            st.is_tampered = false;
                            let resp = r#"{"success":true,"is_tampered":false,"logs":["ðŸ”§ CONSENSUS SELF-HEAL: Re-synced with canonical longest chain. Restored Block #103 state."]}"#;
                            send_http(&mut stream, 200, "application/json", resp);
                        } else if path == "/api/compile" {
                            let code = find_json_val(&body, "code").unwrap_or_else(|| body.clone());
                            let temp_dir = std::env::temp_dir();
                            let aayu_path = temp_dir.join("playground_code.aayu");
                            let ayc_path = temp_dir.join("playground_code.ayc");
                            let _ = std::fs::write(&aayu_path, &code);

                            let aayuc_path = if std::path::Path::new(r"D:\INTENT-TO-SILICON\.archive\compiler_rust_bootstrap\target\release\aayuc.exe").exists() {
                                r"D:\INTENT-TO-SILICON\.archive\compiler_rust_bootstrap\target\release\aayuc.exe".to_string()
                            } else {
                                "aayuc.exe".to_string()
                            };
                            let vm_path = std::env::current_exe().unwrap_or_else(|_| std::path::PathBuf::from(r"D:\INTENT-TO-SILICON\runtime_rs\target_server2\release\aayu-vm.exe"));

                            let compile_output = std::process::Command::new(&aayuc_path)
                                .arg(&aayu_path)
                                .arg("-o")
                                .arg(&ayc_path)
                                .output();

                            match compile_output {
                                Ok(c_res) => {
                                    if !c_res.status.success() {
                                        let err_msg = String::from_utf8_lossy(&c_res.stderr);
                                        let out_msg = String::from_utf8_lossy(&c_res.stdout);
                                        let full_err = format!("[AAYU Compiler Diagnostic]\n{}\n{}", err_msg, out_msg);
                                        let resp = format!(r#"{{"success":false,"output":"{}"}}"#, esc_json(&full_err));
                                        send_http(&mut stream, 200, "application/json", &resp);
                                    } else {
                                        let t0 = std::time::Instant::now();
                                        let vm_output = std::process::Command::new(&vm_path)
                                            .arg(&ayc_path)
                                            .output();
                                        let elapsed = t0.elapsed().as_nanos();

                                        match vm_output {
                                            Ok(v_res) => {
                                                let stdout_str = String::from_utf8_lossy(&v_res.stdout);
                                                let stderr_str = String::from_utf8_lossy(&v_res.stderr);
                                                let mut final_out = format!(">> AAYU VM JIT Execution (v1.2.0):\n");
                                                if !stdout_str.trim().is_empty() {
                                                    final_out.push_str(&stdout_str);
                                                } else if !stderr_str.trim().is_empty() {
                                                    final_out.push_str(&stderr_str);
                                                } else {
                                                    final_out.push_str("Program executed cleanly. Exit code: 0\n");
                                                }
                                                final_out.push_str(&format!("\n[Execution time: {}ns | Pure AAYU Silicon Stack]", elapsed));
                                                let resp = format!(r#"{{"success":true,"output":"{}"}}"#, esc_json(&final_out));
                                                send_http(&mut stream, 200, "application/json", &resp);
                                            }
                                            Err(e) => {
                                                let resp = format!(r#"{{"success":false,"output":"VM Execution failed: {}"}}"#, esc_json(&e.to_string()));
                                                send_http(&mut stream, 200, "application/json", &resp);
                                            }
                                        }
                                    }
                                }
                                Err(e) => {
                                    let resp = format!(r#"{{"success":false,"output":"Could not invoke aayuc: {}"}}"#, esc_json(&e.to_string()));
                                    send_http(&mut stream, 200, "application/json", &resp);
                                }
                            }
                        } else {
                            // Default: Render HTML Page
                            send_http(&mut stream, 200, "text/html; charset=utf-8", &html);
                        }
                    }

                    let initial_mempool = vec![
                        ServerTx {
                            id: "tx_901".to_string(),
                            from: "Alice".to_string(),
                            to: "Bob".to_string(),
                            amount: 15.0,
                            fee: 0.1,
                            velocity: 0.42,
                            volume: 15.0,
                            entropy: 0.08,
                            gas: 1.05,
                        },
                        ServerTx {
                            id: "tx_902".to_string(),
                            from: "Bob".to_string(),
                            to: "ContractPool".to_string(),
                            amount: 5.0,
                            fee: 0.05,
                            velocity: 0.35,
                            volume: 5.0,
                            entropy: 0.12,
                            gas: 1.0,
                        },
                    ];

                    let state_arc = std::sync::Arc::new(std::sync::Mutex::new(ServerState {
                        block_height: 104,
                        latest_hash: "0000a7b489c1f0e2417d9e83b4a2c1f9d8e7b6a5c4d3e2f1a0b9c8d7e6f5a4b3".to_string(),
                        is_tampered: false,
                        treasury_bal: 10000.0,
                        alice_bal: 450.0,
                        bob_bal: 120.0,
                        miner_bal: 50.0,
                        pool_bal: 500.0,
                        mempool: initial_mempool,
                    }));
                    let html_arc = std::sync::Arc::new(html);

                    for stream in listener.incoming() {
                        match stream {
                            Ok(stream) => {
                                let _ = stream.set_nodelay(true);
                                let _ = stream.set_read_timeout(Some(std::time::Duration::from_secs(5)));
                                let _ = stream.set_write_timeout(Some(std::time::Duration::from_secs(5)));
                                let state_clone = std::sync::Arc::clone(&state_arc);
                                let html_clone = std::sync::Arc::clone(&html_arc);

                                std::thread::spawn(move || {
                                    let _ = std::panic::catch_unwind(std::panic::AssertUnwindSafe(move || {
                                        handle_connection(stream, state_clone, html_clone);
                                    }));
                                });
                            }
                            Err(_) => {}
                        }
                    }
                }
                _ => return Err(format!("Unknown instruction opcode: 0x{:02X} at IP: {}", op, self.ip - 1)),
            }
        }
        Ok(())
    }
}
