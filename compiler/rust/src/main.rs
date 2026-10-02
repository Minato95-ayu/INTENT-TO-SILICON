use std::env;
use std::fs;

mod vm;
mod memory;
mod bytecode;
mod entity;
mod workflow;
mod http;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("AAYU Runtime v0.1");
        println!("Usage: cargo run <file.ayc>");
        return;
    }

    let filename = &args[1];
    let contents = fs::read_to_string(filename).expect("Failed to read .ayc file");
    
    let mut virtual_machine = vm::VM::new();
    virtual_machine.execute(&contents);
}
