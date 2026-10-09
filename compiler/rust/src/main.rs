use std::env;
use std::fs;

mod vm;
pub mod memory;
pub mod bytecode;
pub mod entity;
pub mod workflow;
pub mod http;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("AAYU Compiler/Runtime Pipeline v0.1");
        println!("Usage: aayu-rust <file.ayc>");
        
        // Pipeline sanity check instantiation (fixes unconstructed warnings)
        let _mem = memory::MemoryManager::new();
        let _bc = bytecode::Bytecode::new();
        let _ent = entity::EntityManager::new();
        let _wf = workflow::WorkflowEngine::new();
        let _http = http::HttpServer::new();
        
        return;
    }

    let filename = &args[1];
    let contents = fs::read_to_string(filename).expect("Failed to read .ayc file");
    
    // Constructing the full pipeline
    let _mem = memory::MemoryManager::new();
    let _bc = bytecode::Bytecode::new();
    let _ent = entity::EntityManager::new();
    let _wf = workflow::WorkflowEngine::new();
    let _http = http::HttpServer::new();

    let mut virtual_machine = vm::VM::new();
    virtual_machine.execute(&contents);
}
