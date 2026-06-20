use crate::frame::RuntimeFrame;
use crate::value::RuntimeValue;
use aayu_core::bytecode::Bytecode;
use aayu_core::opcode::Opcode;
use aayu_diagnostics::VMError;
use std::collections::HashMap;

pub struct VirtualMachine {
    pub globals: HashMap<String, RuntimeValue>,
}

impl VirtualMachine {
    pub fn new() -> Self {
        Self {
            globals: HashMap::new(),
        }
    }

    pub fn run(&mut self, bytecode: Bytecode) -> Result<RuntimeValue, VMError> {
        let mut frame = RuntimeFrame::new(bytecode);
        
        while frame.ip < frame.bytecode.instructions.len() {
            let inst = &frame.bytecode.instructions[frame.ip];
            
            match inst.opcode {
                Opcode::LoadConst => {
                    let idx = inst.operand.ok_or(VMError::StackUnderflow)?;
                    let const_val = frame.bytecode.constants.get(idx)
                        .ok_or(VMError::StackUnderflow)?;
                    frame.stack.push(RuntimeValue::from(const_val));
                }
                Opcode::StoreName => {
                    let val = frame.stack.pop()?;
                    let idx = inst.operand.ok_or(VMError::StackUnderflow)?;
                    let name = frame.bytecode.names.get(idx)
                        .ok_or(VMError::StackUnderflow)?;
                    frame.locals.insert(name.clone(), val);
                }
                Opcode::LoadName => {
                    let idx = inst.operand.ok_or(VMError::StackUnderflow)?;
                    let name = frame.bytecode.names.get(idx)
                        .ok_or(VMError::StackUnderflow)?;
                    if let Some(val) = frame.locals.get(name) {
                        frame.stack.push(val.clone());
                    } else if let Some(val) = self.globals.get(name) {
                        frame.stack.push(val.clone());
                    } else {
                        return Err(VMError::UnknownVariable(name.clone()));
                    }
                }
                Opcode::Pop => {
                    let _ = frame.stack.pop()?;
                }
                Opcode::Add => {
                    let right = frame.stack.pop()?;
                    let left = frame.stack.pop()?;
                    match (left, right) {
                        (RuntimeValue::Number(l), RuntimeValue::Number(r)) => {
                            frame.stack.push(RuntimeValue::Number(l + r));
                        }
                        (RuntimeValue::String(l), RuntimeValue::String(r)) => {
                            frame.stack.push(RuntimeValue::String(format!("{}{}", l, r)));
                        }
                        _ => return Err(VMError::TypeMismatch("Addition operand types mismatch".into())),
                    }
                }
                Opcode::Sub => {
                    let right = frame.stack.pop()?;
                    let left = frame.stack.pop()?;
                    match (left, right) {
                        (RuntimeValue::Number(l), RuntimeValue::Number(r)) => {
                            frame.stack.push(RuntimeValue::Number(l - r));
                        }
                        _ => return Err(VMError::TypeMismatch("Subtraction requires numbers".into())),
                    }
                }
                Opcode::Mul => {
                    let right = frame.stack.pop()?;
                    let left = frame.stack.pop()?;
                    match (left, right) {
                        (RuntimeValue::Number(l), RuntimeValue::Number(r)) => {
                            frame.stack.push(RuntimeValue::Number(l * r));
                        }
                        _ => return Err(VMError::TypeMismatch("Multiplication requires numbers".into())),
                    }
                }
                Opcode::Div => {
                    let right = frame.stack.pop()?;
                    let left = frame.stack.pop()?;
                    match (left, right) {
                        (RuntimeValue::Number(l), RuntimeValue::Number(r)) => {
                            if r == 0.0 {
                                return Err(VMError::DivisionByZero);
                            }
                            frame.stack.push(RuntimeValue::Number(l / r));
                        }
                        _ => return Err(VMError::TypeMismatch("Division requires numbers".into())),
                    }
                }
                Opcode::Return => {
                    if !frame.stack.is_empty() {
                        return Ok(frame.stack.pop()?);
                    } else {
                        return Ok(RuntimeValue::Null);
                    }
                }
                _ => return Err(VMError::UnknownOpcode(inst.opcode as u8)),
            }
            
            frame.ip += 1;
        }
        
        Ok(RuntimeValue::Null)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use aayu_core::bytecode::{Bytecode, Constant};
    use aayu_core::instruction::Instruction;
    use aayu_core::opcode::Opcode;

    fn build_test_bytecode(instructions: Vec<Instruction>, constants: Vec<Constant>, names: Vec<String>) -> Bytecode {
        Bytecode {
            name: "test".into(),
            file: "test.aayu".into(),
            constants,
            names,
            parameters: vec![],
            instructions,
            tasks: HashMap::new(),
        }
    }

    #[test]
    fn test_addition() {
        // 10 + 20 = 30
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Add, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(10.0),
            Constant::Number(20.0),
        ];
        let bc = build_test_bytecode(instructions, constants, vec![]);
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Number(30.0));
    }

    #[test]
    fn test_subtraction() {
        // 50 - 20 = 30
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Sub, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(50.0),
            Constant::Number(20.0),
        ];
        let bc = build_test_bytecode(instructions, constants, vec![]);
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Number(30.0));
    }

    #[test]
    fn test_multiplication() {
        // 5 * 6 = 30
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Mul, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(5.0),
            Constant::Number(6.0),
        ];
        let bc = build_test_bytecode(instructions, constants, vec![]);
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Number(30.0));
    }

    #[test]
    fn test_division() {
        // 90 / 3 = 30
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Div, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(90.0),
            Constant::Number(3.0),
        ];
        let bc = build_test_bytecode(instructions, constants, vec![]);
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Number(30.0));
    }

    #[test]
    fn test_store_and_load_name() {
        // x = 30; return x
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::StoreName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(30.0),
        ];
        let names = vec![
            "x".to_string(),
        ];
        let bc = build_test_bytecode(instructions, constants, names);
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Number(30.0));
    }

    #[test]
    fn test_division_by_zero_error() {
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Div, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(10.0),
            Constant::Number(0.0),
        ];
        let bc = build_test_bytecode(instructions, constants, vec![]);
        let mut vm = VirtualMachine::new();
        let err = vm.run(bc).unwrap_err();
        assert_eq!(err, VMError::DivisionByZero);
    }
}
