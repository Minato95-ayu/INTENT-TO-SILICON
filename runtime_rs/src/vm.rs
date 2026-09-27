use crate::opcodes::OpCode;

// Core Stack-based VM designed for absolute maximum execution speed
pub struct VM {
    stack: Vec<f64>, // Native fast array for numbers (will be enum RuntimeValue later)
    ip: usize,
    bytecode: Vec<u8>,
}

impl VM {
    pub fn new(bytecode: Vec<u8>) -> Self {
        Self {
            stack: Vec::with_capacity(1024), // Pre-allocated to avoid resizing delays
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

    pub fn run(&mut self) {
        loop {
            if self.ip >= self.bytecode.len() {
                break;
            }

            let instruction = self.fetch();

            // High speed match dispatch
            match instruction {
                0x00 => { // OpCode::Halt
                    break;
                }
                0x01 => { // OpCode::PushConst
                    // For now skip the 2 byte constant index
                    self.ip += 2;
                    self.stack.push(0.0);
                }
                _ => {
                    panic!("Unknown Opcode: 0x{:X}", instruction);
                }
            }
        }
    }
}
