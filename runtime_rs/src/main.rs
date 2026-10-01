use std::env;
use std::fs::File;
use std::io::{self, Read, Write};

pub mod opcodes;
pub mod vm;

use vm::{AayuVM, NanVal};

fn main() {
    let args: Vec<String> = env::args().collect();
    
    // REPL MODE
    if args.len() == 1 {
        println!("AAYU Native REPL (v0.3.3) - Cross-Platform Static Binary");
        println!("Running on OS: {}", env::consts::OS);
        println!("Type '.exit' to quit.");
        loop {
            print!("aayu> ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            io::stdin().read_line(&mut input).unwrap();
            
            let cmd = input.trim();
            if cmd == ".exit" { break; }
            if cmd.is_empty() { continue; }
            
            // In a real REPL, we'd compile the string to bytecode here.
            // For now, we simulate executing it.
            println!("(AAYU Engine executed: {})", cmd);
        }
        return;
    }

    let filename = &args[1];
    println!("Loading: {}", filename);
    let mut file = File::open(filename).expect("Cannot open file");
    let mut bytecode = Vec::new();
    file.read_to_end(&mut bytecode).expect("Cannot read file");

    let mut vm = AayuVM::new(bytecode, vec![], vec![]);
    vm.run();
}
