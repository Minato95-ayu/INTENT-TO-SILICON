use std::env;
use std::fs::File;
use std::io::Read;

pub mod opcodes;
pub mod vm;

use vm::{AayuVM, NanVal};

fn main() {
    println!("AAYU Native Rust VM (v0.3.2) - Native Web API");
    
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage: aayu-vm <file.aybc>");
        println!();
        run_full_benchmark();
        return;
    }

    let filename = &args[1];
    println!("Loading: {}", filename);
    let mut file = File::open(filename).expect("Cannot open file");
    let mut bytecode = Vec::new();
    file.read_to_end(&mut bytecode).expect("Cannot read file");
    println!("Loaded {} bytes", bytecode.len());

    let mut vm = AayuVM::new(bytecode, vec![], vec![]);
    let start = std::time::Instant::now();
    vm.run();
    println!("Done in {:?}", start.elapsed());
}

fn run_full_benchmark() {
    println!("=== AAYU VM BENCHMARK SUITE (v0.3.2 Native HTTP) ===");
    println!();

    // --- Correctness Tests ---
    println!("[ CORRECTNESS TESTS ]");

    // Test 6: Strings & File Write/Read
    {
        let strings = vec![
            "test_output_aayu.txt".to_string(),
            "AAYU Native Rust Engine File I/O works perfectly!".to_string()
        ];
        let constants = vec![NanVal::string(0), NanVal::string(1)];
        let bc = vec![
            0x01,0,0, // PUSH const 0 (filename)
            0x01,0,1, // PUSH const 1 (content)
            0x61,     // FILE_WRITE
            0x02,     // POP (bool result)
            0x01,0,0, // PUSH const 0 (filename)
            0x60,     // FILE_READ
            0x51,     // PRINT
            0x00      // HALT
        ];
        let mut vm = AayuVM::new(bc, constants, strings);
        println!("  - Test 6 (File I/O): Writing and Reading 'test_output_aayu.txt'");
        vm.run();
    }

    // Test 7: HTTP GET (Native Web API)
    {
        println!("  - Test 7 (Web API): Fetching JSON from public API (jsonplaceholder.typicode.com)...");
        // 0x70 = HTTP_GET
        let strings = vec!["https://jsonplaceholder.typicode.com/todos/1".to_string()];
        let constants = vec![NanVal::string(0)];
        let bc = vec![
            0x01,0,0, // PUSH const 0 (url)
            0x70,     // HTTP_GET (pops url, pushes response string)
            0x51,     // PRINT response
            0x00      // HALT
        ];
        let mut vm = AayuVM::new(bc, constants, strings);
        vm.run();
    }

    println!();
    println!("[ SPEED BENCHMARKS ]");

    let turbo_time;
    {
        let c = vec![NanVal::int(1)];
        let mut bc: Vec<u8> = Vec::with_capacity(4_000_005);
        bc.extend_from_slice(&[0x01, 0, 0]);
        for _ in 0..999_999 {
            bc.extend_from_slice(&[0x01, 0, 0]);
            bc.push(0x10);
        }
        bc.push(0x51);
        bc.push(0x00);
        let mut vm = AayuVM::new(bc, c, vec![]);
        let start = std::time::Instant::now();
        vm.run();
        turbo_time = start.elapsed();
        println!("  * AayuVM (NaN-boxed) 1M adds: {:?}", turbo_time);
    }
}
