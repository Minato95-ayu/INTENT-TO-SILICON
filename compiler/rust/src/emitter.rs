use crate::parser::{Expr, Statement, BinaryOp};
use aayu_vm::opcodes::OpCode;

pub struct Emitter {
    bytecode: Vec<u8>,
    constants: Vec<i64>, 
    strings: Vec<String>,
    vars: Vec<String>,
}

impl Default for Emitter {
    fn default() -> Self {
        Self::new()
    }
}

impl Emitter {
    pub fn new() -> Self {
        Self {
            bytecode: Vec::new(),
            constants: Vec::new(),
            strings: Vec::new(),
            vars: Vec::new(),
        }
    }

    fn add_constant(&mut self, val: i64) -> u16 {
        self.constants.push(val);
        (self.constants.len() - 1) as u16
    }

    fn get_or_add_var(&mut self, name: &str) -> u16 {
        if let Some(pos) = self.vars.iter().position(|v| v == name) {
            return pos as u16;
        }
        self.vars.push(name.to_string());
        (self.vars.len() - 1) as u16
    }

    pub fn emit(&mut self, stmts: Vec<Statement>) -> Vec<u8> {
        for stmt in stmts {
            self.emit_stmt(&stmt);
        }
        self.bytecode.push(OpCode::Halt as u8);

        let mut output = Vec::new();
        output.extend_from_slice(b"AAYU");
        
        // Strings
        output.extend_from_slice(&(self.strings.len() as u32).to_le_bytes());
        for s in &self.strings {
            output.extend_from_slice(&(s.len() as u32).to_le_bytes());
            output.extend_from_slice(s.as_bytes());
        }

        // Constants
        output.extend_from_slice(&(self.constants.len() as u32).to_le_bytes());
        for c in &self.constants {
            output.push(1); // 1 = Int
            output.extend_from_slice(&c.to_le_bytes());
        }

        // Bytecode
        output.extend_from_slice(&self.bytecode);

        output
    }

    fn emit_stmt(&mut self, stmt: &Statement) {
        match stmt {
            Statement::Let { name, value } => {
                self.emit_expr(value);
                let var_idx = self.get_or_add_var(name);
                self.bytecode.push(OpCode::StoreVar as u8);
                self.bytecode.push((var_idx & 0xFF) as u8);
            }
            Statement::Print(expr) => {
                self.emit_expr(expr);
                self.bytecode.push(OpCode::Print as u8);
                self.bytecode.push(0); // number of args (0 args means newline)
            }
        }
    }

    fn emit_expr(&mut self, expr: &Expr) {
        match expr {
            Expr::Integer(n) => {
                let idx = self.add_constant(*n);
                self.bytecode.push(OpCode::PushConst as u8);
                self.bytecode.push((idx >> 8) as u8);
                self.bytecode.push((idx & 0xFF) as u8);
            }
            Expr::Variable(name) => {
                let var_idx = self.get_or_add_var(name);
                self.bytecode.push(OpCode::LoadVar as u8);
                self.bytecode.push((var_idx & 0xFF) as u8);
            }
            Expr::Binary { left, op, right } => {
                self.emit_expr(left);
                self.emit_expr(right);
                match op {
                    BinaryOp::Add => self.bytecode.push(OpCode::Add as u8),
                }
            }
        }
    }
}

