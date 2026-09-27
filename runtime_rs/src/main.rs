use std::env;
use std::fs::File;
use std::io::Read;

pub mod opcodes;
pub mod vm;

use vm::VM;

fn main() {
    println!("AAYU Native Rust Virtual Machine (v0.1.0) - Initializing");
    
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage: aayu-vm <file.aybc>");
        // Dummy test for now if no file is provided
        println!("Running test scaffold...");
        let sample_bytecode = vec![
            opcodes::OpCode::PushConst as u8, 0, 0, // Push constant index 0
            opcodes::OpCode::Halt as u8,
        ];
        let mut vm = VM::new(sample_bytecode);
        let start = std::time::Instant::now();
        vm.run();
        println!("Execution completed in {:?} (Target: <0.01s)", start.elapsed());
        return;
    }

    let filename = &args[1];
    println!("Loading bytecode from: {}", filename);
    
    let mut file = match File::open(filename) {
        Ok(f) => f,
        Err(e) => {
            println!("Error opening file: {}", e);
            return;
        }
    };

    let mut bytecode = Vec::new();
    if let Err(e) = file.read_to_end(&mut bytecode) {
        println!("Error reading bytecode: {}", e);
        return;
    }

    println!("Loaded {} bytes. Executing...", bytecode.len());
    
    let mut vm = VM::new(bytecode);
    
    let start = std::time::Instant::now();
    vm.run();
    let duration = start.elapsed();
    
    println!("Execution completed natively in {:?} (Target: <0.01s)", duration);
}
