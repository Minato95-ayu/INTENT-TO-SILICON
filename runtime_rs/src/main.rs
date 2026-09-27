pub mod opcodes;
pub mod vm;

use vm::VM;

fn main() {
    println!("AAYU Native Rust Virtual Machine (v0.1.0) - Initialization");
    
    // In the future, this will read a .aybc (AAYU ByteCode) file
    // For now, it's just the God-level 0.01s engine scaffold.
    let sample_bytecode = vec![
        opcodes::OpCode::PushConst as u8, 0, 0, // Push constant index 0
        opcodes::OpCode::Halt as u8,
    ];

    let mut vm = VM::new(sample_bytecode);
    
    let start = std::time::Instant::now();
    vm.run();
    let duration = start.elapsed();
    
    println!("Execution completed in {:?} (Target: <0.01s)", duration);
}
