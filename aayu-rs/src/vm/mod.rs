use std::collections::HashMap;
use serde_json::Value;

#[derive(Clone, Debug, PartialEq)]
pub enum RuntimeValue {
    String(String),
    Number(f64),
    Bool(bool),
    Null,
}

impl RuntimeValue {
    fn from_json(v: &Value) -> Self {
        match v {
            Value::String(s) => RuntimeValue::String(s.clone()),
            Value::Number(n) => RuntimeValue::Number(n.as_f64().unwrap_or(0.0)),
            Value::Bool(b) => RuntimeValue::Bool(*b),
            _ => RuntimeValue::Null,
        }
    }
}

pub struct VM {
    stack: Vec<RuntimeValue>,
    vars: HashMap<String, RuntimeValue>,
    ip: usize,
}

impl VM {
    pub fn new() -> Self {
        Self {
            stack: Vec::new(),
            vars: HashMap::new(),
            ip: 0,
        }
    }

    pub fn execute(&mut self, json_bytecode: &str) {
        let bytecode: Value = serde_json::from_str(json_bytecode).expect("Failed to parse .ayc JSON");
        
        let instructions = bytecode["instructions"].as_array().expect("Instructions must be array");
        let constants = bytecode["constants"].as_array().expect("Constants must be array");
        let names = bytecode["names"].as_array().expect("Names must be array");

        self.ip = 0;
        
        while self.ip < instructions.len() {
            let inst = instructions[self.ip].as_array().unwrap();
            let op = inst[0].as_str().unwrap();
            let operand = if inst[1].is_number() {
                Some(inst[1].as_u64().unwrap() as usize)
            } else {
                None
            };

            match op {
                "LOAD_CONST" => {
                    let val = RuntimeValue::from_json(&constants[operand.unwrap()]);
                    self.stack.push(val);
                }
                "STORE_VAR" => {
                    let var_name = names[operand.unwrap()].as_str().unwrap().to_string();
                    if let Some(val) = self.stack.pop() {
                        self.vars.insert(var_name, val);
                    }
                }
                "LOAD_VAR" => {
                    let var_name = names[operand.unwrap()].as_str().unwrap();
                    if let Some(val) = self.vars.get(var_name) {
                        self.stack.push(val.clone());
                    } else {
                        self.stack.push(RuntimeValue::Null);
                    }
                }
                "COMPARE_EQ" => {
                    if let (Some(right), Some(left)) = (self.stack.pop(), self.stack.pop()) {
                        self.stack.push(RuntimeValue::Bool(left == right));
                    }
                }
                "JUMP_IF_FALSE" => {
                    if let Some(condition) = self.stack.pop() {
                        if let RuntimeValue::Bool(false) = condition {
                            self.ip += operand.unwrap();
                            continue;
                        }
                    }
                }
                "JUMP_FORWARD" => {
                    self.ip += operand.unwrap();
                    continue;
                }
                "CALL" => {
                    let argc = operand.unwrap();
                    let mut args = Vec::new();
                    for _ in 0..argc {
                        args.push(self.stack.pop().unwrap());
                    }
                    args.reverse();
                    
                    if let Some(RuntimeValue::String(fn_name)) = self.stack.pop() {
                        if fn_name == "print" {
                            if let Some(RuntimeValue::String(val)) = args.first() {
                                println!("{}", val);
                            }
                            self.stack.push(RuntimeValue::Null);
                        }
                    }
                }
                "RETURN" => {
                    break;
                }
                _ => {
                    println!("Unknown opcode: {}", op);
                }
            }
            self.ip += 1;
        }
    }
}
