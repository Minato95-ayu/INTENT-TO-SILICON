use std::env;
use std::fs::File;
use std::io::Read;

use aayu_vm::vm::{AayuVM, NanVal};
use aayu_vm::jit;

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() >= 3 && args[1] == "--sum" {
        let n: i64 = args[2].parse().expect("N must be an integer");
        run_sum(n, args.contains(&"--jit".to_string()));
        return;
    }

    if args.len() == 1 {
        println!("AAYU Native REPL (v1.2.0) - Intent-to-Silicon Engine");
        return;
    }

    let filename = &args[1];
    let mut file = File::open(filename).expect("Cannot open file");
    let mut data = Vec::new();
    file.read_to_end(&mut data).expect("Cannot read file");

    if data.len() < 4 || &data[0..4] != b"AAYU" {
        println!("Invalid Bytecode File.");
        return;
    }
    
    let mut pos = 4;
    
    // Read Strings
    let mut num_strings_bytes = [0u8; 4];
    num_strings_bytes.copy_from_slice(&data[pos..pos+4]);
    let num_strings = u32::from_le_bytes(num_strings_bytes) as usize;
    pos += 4;
    
    let mut strings = Vec::new();
    for _ in 0..num_strings {
        let mut len_bytes = [0u8; 4];
        len_bytes.copy_from_slice(&data[pos..pos+4]);
        let str_len = u32::from_le_bytes(len_bytes) as usize;
        pos += 4;
        
        let s = String::from_utf8(data[pos..pos+str_len].to_vec()).unwrap();
        strings.push(s);
        pos += str_len;
    }

    // Read Constants (new)
    let mut num_const_bytes = [0u8; 4];
    num_const_bytes.copy_from_slice(&data[pos..pos+4]);
    let num_constants = u32::from_le_bytes(num_const_bytes) as usize;
    pos += 4;

    let mut constants = Vec::new();
    for _ in 0..num_constants {
        let type_tag = data[pos];
        pos += 1;
        match type_tag {
            1 => { // Int
                let mut val_bytes = [0u8; 8];
                val_bytes.copy_from_slice(&data[pos..pos+8]);
                let val = i64::from_le_bytes(val_bytes);
                constants.push(NanVal::int(val)); // NanVal int
                pos += 8;
            }
            // Add Float, Bool, etc. as needed
            _ => panic!("Unknown constant type tag"),
        }
    }

    let bytecode = data[pos..].to_vec();
    if args.contains(&"--jit".to_string()) {
        jit::compile_and_run(&bytecode, &constants);
    } else {
        let mut vm = AayuVM::new(bytecode, constants, strings);
        vm.run();
    }
}

fn run_sum(n: i64, use_jit: bool) {
    let constants = vec![NanVal::int(0), NanVal::int(n), NanVal::int(1)];
    let mut bc: Vec<u8> = vec![];
    bc.extend([0x01,0,0, 0x06,0]);           // sum = 0
    bc.extend([0x01,0,0, 0x06,1]);           // i = 0
    let loop_start = bc.len();
    bc.extend([0x05,1, 0x01,0,1, 41]);     // i < n (LT is 41)
    bc.extend([0x21,0,0]);
    let patch = bc.len() - 2;
    bc.extend([0x05,0, 0x05,1, 0x10, 0x06,0]); // sum += i
    bc.extend([0x05,1, 0x01,0,2, 0x10, 0x06,1]); // i += 1
    bc.extend([0x20,(loop_start>>8) as u8,(loop_start&0xFF) as u8]);
    let end = bc.len();
    bc[patch] = (end>>8) as u8; bc[patch+1] = (end&0xFF) as u8;
    bc.extend([0x05,0, 81, 0x00]);         // print(sum); halt -> Print opcode is 81
    
    if use_jit {
        jit::compile_and_run(&bc, &constants);
    } else {
        let mut vm = AayuVM::new(bc, constants, vec![]);
        let t = std::time::Instant::now();
        vm.run();
        println!("AAYU_VM_NS {}", t.elapsed().as_nanos());
    }
}

