use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: aayu_cli <bytecode_file.ayc>");
        process::exit(1);
    }

    let filepath = &args[1];
    let json_str = match fs::read_to_string(filepath) {
        Ok(s) => s,
        Err(e) => {
            eprintln!("Failed to read file '{}': {}", filepath, e);
            process::exit(1);
        }
    };

    let bytecode = match aayu_core::serializer::deserialize_from_str(&json_str) {
        Ok(bc) => bc,
        Err(e) => {
            eprintln!("Failed to deserialize bytecode: {}", e);
            process::exit(1);
        }
    };

    let mut vm = aayu_vm::vm::VirtualMachine::new();
    match vm.run(bytecode) {
        Ok(_) => {}
        Err(e) => {
            eprintln!("VM Execution Error: {}", e);
            process::exit(1);
        }
    }
}
