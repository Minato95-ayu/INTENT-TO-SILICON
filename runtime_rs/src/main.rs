use std::env;
use std::fs::File;
use std::io::Read;

pub mod opcodes;
pub mod math;
pub mod db;
pub mod net;
pub mod ui;
pub mod vm;

use vm::{AayuVM, NanVal};

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() >= 3 && args[1] == "--sum" {
        let n: i64 = args[2].parse().expect("N must be an integer");
        run_sum(n);
        return;
    }

    if args.len() == 1 {
        println!("AAYU Native REPL (v1.1.0) - Fast Silicon Engine");
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

    let bytecode = data[pos..].to_vec();
    let mut vm = AayuVM::new(bytecode, vec![], strings);
    vm.run();
}

fn run_sum(n: i64) {
    let constants = vec![NanVal::int(0), NanVal::int(n), NanVal::int(1)];
    let mut bc: Vec<u8> = vec![];
    bc.extend([0x01,0,0, 0x06,0]);           // sum = 0
    bc.extend([0x01,0,0, 0x06,1]);           // i = 0
    let loop_start = bc.len();
    bc.extend([0x05,1, 0x01,0,1, 0x14]);     // i < n
    bc.extend([0x21,0,0]);
    let patch = bc.len() - 2;
    bc.extend([0x05,0, 0x05,1, 0x10, 0x06,0]); // sum += i
    bc.extend([0x05,1, 0x01,0,2, 0x10, 0x06,1]); // i += 1
    bc.extend([0x20,(loop_start>>8) as u8,(loop_start&0xFF) as u8]);
    let end = bc.len();
    bc[patch] = (end>>8) as u8; bc[patch+1] = (end&0xFF) as u8;
    bc.extend([0x05,0, 81, 0x00]);         // print(sum); halt -> Print opcode is 81
    let mut vm = AayuVM::new(bc, constants, vec![]);
    let t = std::time::Instant::now();
    vm.run();
    println!("AAYU_VM_NS {}", t.elapsed().as_nanos());
}
