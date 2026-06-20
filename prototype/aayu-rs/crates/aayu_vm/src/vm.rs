use crate::frame::RuntimeFrame;
use crate::value::RuntimeValue;
use aayu_core::bytecode::Bytecode;
use aayu_core::opcode::Opcode;
use aayu_diagnostics::VMError;
use std::collections::HashMap;
use std::rc::Rc;
use std::cell::RefCell;

pub trait NativeFunction {
    fn call(&self, args: Vec<RuntimeValue>) -> Result<RuntimeValue, VMError>;
}

pub struct CollectionLen;

impl NativeFunction for CollectionLen {
    fn call(&self, args: Vec<RuntimeValue>) -> Result<RuntimeValue, VMError> {
        if args.len() != 1 {
            return Err(VMError::TypeMismatch("collection_len expects exactly 1 argument".into()));
        }
        match &args[0] {
            RuntimeValue::List(list) => {
                let len = list.borrow().len();
                Ok(RuntimeValue::Number(len as f64))
            }
            RuntimeValue::Map(map) => {
                let len = map.borrow().len();
                Ok(RuntimeValue::Number(len as f64))
            }
            RuntimeValue::String(s) => {
                Ok(RuntimeValue::Number(s.len() as f64))
            }
            _ => Err(VMError::InvalidCollectionAccess("collection_len requires a list, map, or string".into())),
        }
    }
}

pub struct VirtualMachine {
    pub globals: HashMap<String, RuntimeValue>,
    pub frames: Vec<RuntimeFrame>,
    pub output: Vec<RuntimeValue>,
    pub stdlib: HashMap<String, Box<dyn NativeFunction>>,
}

impl VirtualMachine {
    pub fn new() -> Self {
        let mut stdlib: HashMap<String, Box<dyn NativeFunction>> = HashMap::new();
        stdlib.insert("collection_len".to_string(), Box::new(CollectionLen));

        let mut globals = HashMap::new();
        globals.insert("collection_len".to_string(), RuntimeValue::Native("collection_len".to_string()));

        Self {
            globals,
            frames: Vec::new(),
            output: Vec::new(),
            stdlib,
        }
    }

    fn pop_args(&self, stack: &mut crate::stack::RuntimeStack, n: usize) -> Result<Vec<RuntimeValue>, VMError> {
        let mut args = Vec::new();
        for _ in 0..n {
            args.push(stack.pop()?);
        }
        args.reverse();
        Ok(args)
    }

    pub fn run(&mut self, bytecode: Bytecode) -> Result<RuntimeValue, VMError> {
        self.frames.clear();
        self.output.clear();
        let main_frame = RuntimeFrame::new(bytecode);
        self.frames.push(main_frame);

        let mut final_return = RuntimeValue::Null;

        while let Some(mut frame) = self.frames.pop() {
            while frame.ip < frame.bytecode.instructions.len() {
                let inst = &frame.bytecode.instructions[frame.ip];
                let mut jumped = false;

                match inst.opcode {
                    Opcode::LoadConst => {
                        let idx = inst.operand.ok_or(VMError::InvalidConstantIndex)?;
                        let const_val = frame.bytecode.constants.get(idx)
                            .ok_or(VMError::InvalidConstantIndex)?;
                        frame.stack.push(RuntimeValue::from(const_val));
                    }
                    Opcode::StoreName => {
                        let val = frame.stack.pop()?;
                        let idx = inst.operand.ok_or(VMError::InvalidNameIndex)?;
                        let name = frame.bytecode.names.get(idx)
                            .ok_or(VMError::InvalidNameIndex)?;
                        if self.frames.is_empty() {
                            self.globals.insert(name.clone(), val);
                        } else {
                            frame.locals.insert(name.clone(), val);
                        }
                    }
                    Opcode::LoadName => {
                        let idx = inst.operand.ok_or(VMError::InvalidNameIndex)?;
                        let name = frame.bytecode.names.get(idx)
                            .ok_or(VMError::InvalidNameIndex)?;
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
                    Opcode::Equal => {
                        let right = frame.stack.pop()?;
                        let left = frame.stack.pop()?;
                        frame.stack.push(RuntimeValue::Boolean(left == right));
                    }
                    Opcode::Greater => {
                        let right = frame.stack.pop()?;
                        let left = frame.stack.pop()?;
                        match (left, right) {
                            (RuntimeValue::Number(l), RuntimeValue::Number(r)) => {
                                frame.stack.push(RuntimeValue::Boolean(l > r));
                            }
                            _ => return Err(VMError::TypeMismatch("Comparison requires numbers".into())),
                        }
                    }
                    Opcode::Less => {
                        let right = frame.stack.pop()?;
                        let left = frame.stack.pop()?;
                        match (left, right) {
                            (RuntimeValue::Number(l), RuntimeValue::Number(r)) => {
                                frame.stack.push(RuntimeValue::Boolean(l < r));
                            }
                            _ => return Err(VMError::TypeMismatch("Comparison requires numbers".into())),
                        }
                    }
                    Opcode::Not => {
                        let val = frame.stack.pop()?;
                        match val {
                            RuntimeValue::Boolean(b) => {
                                frame.stack.push(RuntimeValue::Boolean(!b));
                            }
                            _ => return Err(VMError::TypeMismatch("Not requires boolean".into())),
                        }
                    }
                    Opcode::JumpForward => {
                        let offset = inst.operand.ok_or(VMError::InvalidJump { current_ip: frame.ip, target_ip: frame.ip })?;
                        let target_ip = frame.ip + offset;
                        if target_ip > frame.bytecode.instructions.len() {
                            return Err(VMError::InvalidJump { current_ip: frame.ip, target_ip });
                        }
                        frame.ip = target_ip;
                        jumped = true;
                    }
                    Opcode::JumpIfFalse => {
                        let offset = inst.operand.ok_or(VMError::InvalidJump { current_ip: frame.ip, target_ip: frame.ip })?;
                        let condition = frame.stack.pop()?;
                        match condition {
                            RuntimeValue::Boolean(b) => {
                                if !b {
                                    let target_ip = frame.ip + offset;
                                    if target_ip > frame.bytecode.instructions.len() {
                                        return Err(VMError::InvalidJump { current_ip: frame.ip, target_ip });
                                    }
                                    frame.ip = target_ip;
                                    jumped = true;
                                }
                            }
                            _ => return Err(VMError::TypeMismatch("JumpIfFalse requires a boolean".into())),
                        }
                    }
                    Opcode::JumpBackward => {
                        let offset = inst.operand.ok_or(VMError::InvalidJump { current_ip: frame.ip, target_ip: frame.ip })?;
                        if offset > frame.ip {
                            let target_ip = frame.ip.saturating_sub(offset);
                            return Err(VMError::InvalidJump { current_ip: frame.ip, target_ip });
                        }
                        frame.ip -= offset;
                        jumped = true;
                    }
                    Opcode::CallTask => {
                        let n_args = inst.operand.ok_or(VMError::TypeMismatch("CallTask missing operand".into()))?;
                        let task_obj = frame.stack.pop()?;
                        let args = self.pop_args(&mut frame.stack, n_args)?;

                        match task_obj {
                            RuntimeValue::Task(callee_bc) => {
                                let mut locals = HashMap::new();
                                for (param, arg) in callee_bc.parameters.iter().zip(args.into_iter()) {
                                    locals.insert(param.clone(), arg);
                                }
                                let mut new_frame = RuntimeFrame::new(*callee_bc);
                                new_frame.locals = locals;

                                // Save caller frame's advanced IP (IP is advanced past CALL_TASK)
                                frame.ip += 1;
                                
                                // Push caller frame back, then push callee frame
                                self.frames.push(frame);
                                self.frames.push(new_frame);
                                
                                break; // Break loop to execute new frame
                            }
                            RuntimeValue::Native(name) => {
                                if let Some(func) = self.stdlib.get(&name) {
                                    let ret_val = func.call(args)?;
                                    frame.stack.push(ret_val);
                                } else {
                                    return Err(VMError::UnknownVariable(format!("Native function '{}' not registered", name)));
                                }
                            }
                            _ => return Err(VMError::InvalidCollectionAccess("Object is not callable".into())),
                        }
                    }
                    Opcode::Return => {
                        let ret_val = if !frame.stack.is_empty() {
                            frame.stack.pop()?
                        } else {
                            RuntimeValue::Null
                        };

                        // Pop current frame (already popped from self.frames)
                        if let Some(mut caller_frame) = self.frames.pop() {
                            caller_frame.stack.push(ret_val);
                            self.frames.push(caller_frame);
                        } else {
                            final_return = ret_val;
                        }

                        break; // Break loop to proceed with caller frame (or exit)
                    }
                    Opcode::BuildList => {
                        frame.stack.push(RuntimeValue::List(Rc::new(RefCell::new(Vec::new()))));
                    }
                    Opcode::BuildMap => {
                        frame.stack.push(RuntimeValue::Map(Rc::new(RefCell::new(HashMap::new()))));
                    }
                    Opcode::AddToList => {
                        let list_val = frame.stack.pop()?;
                        let item = frame.stack.pop()?;

                        match list_val {
                            RuntimeValue::List(list) => {
                                list.borrow_mut().push(item);
                                frame.stack.push(RuntimeValue::List(list));
                            }
                            _ => return Err(VMError::InvalidCollectionAccess("Target of add must be a list".into())),
                        }
                    }
                    Opcode::MapSet => {
                        let map_val = frame.stack.pop()?;
                        let key_val = frame.stack.pop()?;
                        let value = frame.stack.pop()?;

                        match map_val {
                            RuntimeValue::Map(map) => {
                                let key = match key_val {
                                    RuntimeValue::String(s) => crate::value::RuntimeKey::String(s),
                                    RuntimeValue::Number(n) => crate::value::RuntimeKey::Number(n),
                                    RuntimeValue::Boolean(b) => crate::value::RuntimeKey::Boolean(b),
                                    _ => return Err(VMError::InvalidIndexType("Unsupported key type".into())),
                                };
                                map.borrow_mut().insert(key, value);
                            }
                            _ => return Err(VMError::InvalidCollectionAccess("Target of set must be a map".into())),
                        }
                    }
                    Opcode::GetItem => {
                        let coll = frame.stack.pop()?;
                        let key_idx = frame.stack.pop()?;

                        match coll {
                            RuntimeValue::List(list) => {
                                match key_idx {
                                    RuntimeValue::Number(n) => {
                                        let idx = n as usize;
                                        let borrowed = list.borrow();
                                        if idx < borrowed.len() {
                                            frame.stack.push(borrowed[idx].clone());
                                        } else {
                                            return Err(VMError::IndexOutOfBounds(format!("List index {} out of range (length {})", idx, borrowed.len())));
                                        }
                                    }
                                    _ => return Err(VMError::InvalidIndexType("List index must be a number".into())),
                                }
                            }
                            RuntimeValue::Map(map) => {
                                let key = match key_idx {
                                    RuntimeValue::String(s) => crate::value::RuntimeKey::String(s),
                                    RuntimeValue::Number(n) => crate::value::RuntimeKey::Number(n),
                                    RuntimeValue::Boolean(b) => crate::value::RuntimeKey::Boolean(b),
                                    _ => return Err(VMError::InvalidIndexType("Unsupported key type".into())),
                                };
                                let borrowed = map.borrow();
                                if let Some(val) = borrowed.get(&key) {
                                    frame.stack.push(val.clone());
                                } else {
                                    return Err(VMError::KeyNotFound(format!("Key '{}' not found in map", key)));
                                }
                            }
                            _ => return Err(VMError::InvalidCollectionAccess("Cannot get item from a non-collection object".into())),
                        }
                    }
                    Opcode::Print => {
                        let val = frame.stack.pop()?;
                        println!("{}", val);
                        self.output.push(val.clone());
                    }
                }

                if !jumped {
                    frame.ip += 1;
                }
            }
        }

        Ok(final_return)
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

    #[test]
    fn test_if_condition_true() {
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None }, 
            Instruction { opcode: Opcode::StoreName, operand: Some(0), line: None, file: None }, 
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },  
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None }, 
            Instruction { opcode: Opcode::Greater, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::JumpIfFalse, operand: Some(3), line: None, file: None }, 
            Instruction { opcode: Opcode::LoadConst, operand: Some(2), line: None, file: None }, 
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(3), line: None, file: None }, 
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(5.0),
            Constant::Number(3.0),
            Constant::String("yes".into()),
            Constant::String("no".into()),
        ];
        let names = vec!["x".to_string()];
        let bc = build_test_bytecode(instructions, constants, names);
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::String("yes".into()));
    }

    #[test]
    fn test_if_condition_false() {
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None }, 
            Instruction { opcode: Opcode::StoreName, operand: Some(0), line: None, file: None }, 
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },  
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None }, 
            Instruction { opcode: Opcode::Greater, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::JumpIfFalse, operand: Some(3), line: None, file: None }, 
            Instruction { opcode: Opcode::LoadConst, operand: Some(2), line: None, file: None }, 
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(3), line: None, file: None }, 
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(2.0),
            Constant::Number(3.0),
            Constant::String("yes".into()),
            Constant::String("no".into()),
        ];
        let names = vec!["x".to_string()];
        let bc = build_test_bytecode(instructions, constants, names);
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::String("no".into()));
    }

    #[test]
    fn test_while_loop() {
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None }, 
            Instruction { opcode: Opcode::StoreName, operand: Some(0), line: None, file: None }, 
            
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },  
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None }, 
            Instruction { opcode: Opcode::Less, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::JumpIfFalse, operand: Some(6), line: None, file: None }, 
            
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },  
            Instruction { opcode: Opcode::LoadConst, operand: Some(2), line: None, file: None }, 
            Instruction { opcode: Opcode::Add, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::StoreName, operand: Some(0), line: None, file: None }, 
            Instruction { opcode: Opcode::JumpBackward, operand: Some(8), line: None, file: None }, 
            
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },  
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(0.0),
            Constant::Number(5.0),
            Constant::Number(1.0),
        ];
        let names = vec!["i".to_string()];
        let bc = build_test_bytecode(instructions, constants, names);
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Number(5.0));
    }

    #[test]
    fn test_simple_call() {
        let add_instructions = vec![
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Add, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let add_bytecode = Bytecode {
            name: "add".into(),
            file: "test.aayu".into(),
            constants: vec![],
            names: vec!["a".into(), "b".into()],
            parameters: vec!["a".into(), "b".into()],
            instructions: add_instructions,
            tasks: HashMap::new(),
        };

        let main_instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::StoreName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(2), line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::CallTask, operand: Some(2), line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let main_bytecode = Bytecode {
            name: "main".into(),
            file: "test.aayu".into(),
            constants: vec![
                Constant::Bytecode(aayu_core::bytecode::BytecodeWrapper::Bytecode(add_bytecode)),
                Constant::Number(10.0),
                Constant::Number(20.0),
            ],
            names: vec!["add".into()],
            parameters: vec![],
            instructions: main_instructions,
            tasks: HashMap::new(),
        };

        let mut vm = VirtualMachine::new();
        let result = vm.run(main_bytecode).unwrap();
        assert_eq!(result, RuntimeValue::Number(30.0));
    }

    #[test]
    fn test_nested_call() {
        let b_instructions = vec![
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::Mul, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let b_bytecode = Bytecode {
            name: "b".into(),
            file: "test.aayu".into(),
            constants: vec![Constant::Number(2.0)],
            names: vec!["y".into()],
            parameters: vec!["y".into()],
            instructions: b_instructions,
            tasks: HashMap::new(),
        };

        let a_instructions = vec![
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::CallTask, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let a_bytecode = Bytecode {
            name: "a".into(),
            file: "test.aayu".into(),
            constants: vec![],
            names: vec!["x".into(), "b".into()],
            parameters: vec!["x".into()],
            instructions: a_instructions,
            tasks: HashMap::new(),
        };

        let main_instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::StoreName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::StoreName, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(2), line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::CallTask, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];

        let main_bytecode = Bytecode {
            name: "main".into(),
            file: "test.aayu".into(),
            constants: vec![
                Constant::Bytecode(aayu_core::bytecode::BytecodeWrapper::Bytecode(a_bytecode)),
                Constant::Bytecode(aayu_core::bytecode::BytecodeWrapper::Bytecode(b_bytecode)),
                Constant::Number(5.0),
            ],
            names: vec!["a".into(), "b".into()],
            parameters: vec![],
            instructions: main_instructions,
            tasks: HashMap::new(),
        };

        let mut vm = VirtualMachine::new();
        let result = vm.run(main_bytecode).unwrap();
        assert_eq!(result, RuntimeValue::Number(10.0));
    }

    #[test]
    fn test_recursion_fib() {
        let fib_instructions = vec![
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::Equal, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::JumpIfFalse, operand: Some(3), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },

            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Equal, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::JumpIfFalse, operand: Some(3), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },

            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Sub, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::CallTask, operand: Some(1), line: None, file: None },
            
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(2), line: None, file: None },
            Instruction { opcode: Opcode::Sub, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::CallTask, operand: Some(1), line: None, file: None },
            
            Instruction { opcode: Opcode::Add, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];

        let fib_bytecode = Bytecode {
            name: "fib".into(),
            file: "test.aayu".into(),
            constants: vec![
                Constant::Number(0.0),
                Constant::Number(1.0),
                Constant::Number(2.0),
            ],
            names: vec!["n".into(), "fib".into()],
            parameters: vec!["n".into()],
            instructions: fib_instructions,
            tasks: HashMap::new(),
        };

        let main_instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::StoreName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::CallTask, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];

        let main_bytecode = Bytecode {
            name: "main".into(),
            file: "test.aayu".into(),
            constants: vec![
                Constant::Bytecode(aayu_core::bytecode::BytecodeWrapper::Bytecode(fib_bytecode)),
                Constant::Number(10.0),
            ],
            names: vec!["fib".into()],
            parameters: vec![],
            instructions: main_instructions,
            tasks: HashMap::new(),
        };

        let mut vm = VirtualMachine::new();
        let result = vm.run(main_bytecode).unwrap();
        assert_eq!(result, RuntimeValue::Number(55.0));
    }

    #[test]
    fn test_compiled_vm_if() {
        let manifest_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
        let path = std::path::Path::new(&manifest_dir)
            .join("../../../tests/vm_if.ayc");
        let json_str = std::fs::read_to_string(path).unwrap();
        
        let bc = aayu_core::serializer::deserialize_from_str(&json_str).unwrap();
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Null);
    }

    #[test]
    fn test_compiled_vm_while() {
        let manifest_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
        let path = std::path::Path::new(&manifest_dir)
            .join("../../../tests/vm_while.ayc");
        let json_str = std::fs::read_to_string(path).unwrap();
        
        let bc = aayu_core::serializer::deserialize_from_str(&json_str).unwrap();
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Null);
    }

    #[test]
    fn test_compiled_vm_nested_function() {
        let manifest_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
        let path = std::path::Path::new(&manifest_dir)
            .join("../../../tests/vm_nested_function.ayc");
        let json_str = std::fs::read_to_string(path).unwrap();
        
        let bc = aayu_core::serializer::deserialize_from_str(&json_str).unwrap();
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Null);
        assert_eq!(vm.output, vec![RuntimeValue::Number(25.0)]);
    }

    #[test]
    fn test_compiled_vm_fib() {
        let manifest_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
        let path = std::path::Path::new(&manifest_dir)
            .join("../../../tests/vm_fib.ayc");
        let json_str = std::fs::read_to_string(path).unwrap();
        
        let bc = aayu_core::serializer::deserialize_from_str(&json_str).unwrap();
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Null);
        assert_eq!(vm.output, vec![RuntimeValue::Number(55.0)]);
    }

    #[test]
    fn test_compiled_vm_collections() {
        let manifest_dir = std::env::var("CARGO_MANIFEST_DIR").unwrap();
        let path = std::path::Path::new(&manifest_dir)
            .join("../../../tests/vm_collections.ayc");
        let json_str = std::fs::read_to_string(path).unwrap();
        
        let bc = aayu_core::serializer::deserialize_from_str(&json_str).unwrap();
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Null);

        assert_eq!(vm.output.len(), 6);
        assert_eq!(vm.output[0], RuntimeValue::List(Rc::new(RefCell::new(vec![
            RuntimeValue::String("Learn VM".into()),
            RuntimeValue::String("Build Runtime".into()),
        ]))));
        assert_eq!(vm.output[1], RuntimeValue::String("Learn VM".into()));
        assert_eq!(vm.output[2], RuntimeValue::String("Build Runtime".into()));

        if let RuntimeValue::Map(ref map) = vm.output[3] {
            let borrowed = map.borrow();
            assert_eq!(borrowed.get(&crate::value::RuntimeKey::String("name".into())), Some(&RuntimeValue::String("Ayush".into())));
            assert_eq!(borrowed.get(&crate::value::RuntimeKey::String("age".into())), Some(&RuntimeValue::Number(20.0)));
        } else {
            panic!("Expected output[3] to be a Map");
        }
        
        assert_eq!(vm.output[4], RuntimeValue::String("Ayush".into()));
        assert_eq!(vm.output[5], RuntimeValue::Number(20.0));
    }

    #[test]
    fn test_invalid_jump_forward() {
        let instructions = vec![
            Instruction { opcode: Opcode::JumpForward, operand: Some(10), line: None, file: None },
        ];
        let bc = build_test_bytecode(instructions, vec![], vec![]);
        let mut vm = VirtualMachine::new();
        let err = vm.run(bc).unwrap_err();
        assert_eq!(err, VMError::InvalidJump { current_ip: 0, target_ip: 10 });
    }

    #[test]
    fn test_invalid_jump_backward() {
        let instructions = vec![
            Instruction { opcode: Opcode::JumpBackward, operand: Some(10), line: None, file: None },
        ];
        let bc = build_test_bytecode(instructions, vec![], vec![]);
        let mut vm = VirtualMachine::new();
        let err = vm.run(bc).unwrap_err();
        assert_eq!(err, VMError::InvalidJump { current_ip: 0, target_ip: 0 });
    }

    #[test]
    fn test_comparison_type_mismatch() {
        let instructions = vec![
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Less, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(10.0),
            Constant::String("not a number".into()),
        ];
        let bc = build_test_bytecode(instructions, constants, vec![]);
        let mut vm = VirtualMachine::new();
        let err = vm.run(bc).unwrap_err();
        assert_eq!(err, VMError::TypeMismatch("Comparison requires numbers".into()));
    }

    #[test]
    fn test_stdlib_bridge_collection_len() {
        let instructions = vec![
            Instruction { opcode: Opcode::BuildList, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::StoreName, operand: Some(0), line: None, file: None },
            
            Instruction { opcode: Opcode::LoadConst, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::AddToList, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Pop, operand: None, line: None, file: None },

            Instruction { opcode: Opcode::LoadConst, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::AddToList, operand: None, line: None, file: None },
            Instruction { opcode: Opcode::Pop, operand: None, line: None, file: None },

            Instruction { opcode: Opcode::LoadName, operand: Some(0), line: None, file: None },
            Instruction { opcode: Opcode::LoadName, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::CallTask, operand: Some(1), line: None, file: None },
            Instruction { opcode: Opcode::Return, operand: None, line: None, file: None },
        ];
        let constants = vec![
            Constant::Number(10.0),
            Constant::Number(20.0),
        ];
        let names = vec![
            "todos".to_string(),
            "collection_len".to_string(),
        ];
        let bc = build_test_bytecode(instructions, constants, names);
        let mut vm = VirtualMachine::new();
        let result = vm.run(bc).unwrap();
        assert_eq!(result, RuntimeValue::Number(2.0));
    }
}
