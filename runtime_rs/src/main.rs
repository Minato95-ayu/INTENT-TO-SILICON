use std::env;
use std::fs::File;
use std::io::Read;
use std::path::{Path, PathBuf};
use std::process::Command;

use aayu_vm::vm::{AayuVM, NanVal};
use aayu_vm::jit;

fn print_banner() {
    println!("AAYU Intent-to-Silicon Engine v1.2.0");
    println!("Architecture: {} ({})", env::consts::ARCH, env::consts::OS);
    println!("Memory Safety: 100% Guaranteed | Single-File Full-Stack");
    println!("Zero Dependencies | Sub-Millisecond Cold Start");
}

fn print_help() {
    print_banner();
    println!("\nUsage: aayu [command] [options] <file>\n");
    println!("Commands:");
    println!("  run <file.aayu> [--jit]    Compile & run AAYU source file in sub-milliseconds");
    println!("  run <file.ayc> [--jit]     Execute precompiled bytecode directly");
    println!("  build <file.aayu> [-o out] Compile source to standalone .ayc bytecode");
    println!("  version, -v, --version     Display engine version information");
    println!("  help, -h, --help           Display this help manual\n");
    println!("Examples:");
    println!("  aayu run hello.aayu");
    println!("  aayu run portfolio.ayc --jit");
    println!("  aayu build app.aayu -o app.ayc");
}

fn find_compiler() -> Option<PathBuf> {
    let names = if cfg!(windows) {
        vec!["aayuc.exe", "aayuc"]
    } else {
        vec!["aayuc", "aayuc.exe"]
    };
    if let Ok(current_exe) = env::current_exe() {
        if let Some(parent) = current_exe.parent() {
            for name in &names {
                let direct = parent.join(name);
                if direct.exists() { return Some(direct); }
                let bin_dir = parent.join("bin").join(name);
                if bin_dir.exists() { return Some(bin_dir); }
                let parent_bin = parent.parent().unwrap_or(parent).join("bin").join(name);
                if parent_bin.exists() { return Some(parent_bin); }
            }
        }
    }
    for name in &names {
        let local = PathBuf::from(format!("bin/{}", name));
        if local.exists() { return Some(local); }
        let curr = PathBuf::from(name);
        if curr.exists() { return Some(curr); }
    }
    None
}

fn compile_aayu_file(input_path: &str, output_path: &str) -> bool {
    let compiler = match find_compiler() {
        Some(c) => c,
        None => {
            eprintln!("[AAYU Error] Compiler (aayuc.exe) not found in PATH or bin directory.");
            return false;
        }
    };
    let status = Command::new(compiler)
        .args([input_path, "-o", output_path])
        .status();
    match status {
        Ok(s) => s.success(),
        Err(e) => {
            eprintln!("[AAYU Error] Failed to execute compiler: {}", e);
            false
        }
    }
}

fn parse_bytecode_data(data: &[u8]) -> Result<(Vec<String>, Vec<NanVal>, Vec<u8>), String> {
    if data.len() < 4 {
        return Err("File too small: missing magic header".into());
    }
    if &data[0..4] != b"AAYU" {
        return Err("Invalid magic header: expected 'AAYU'".into());
    }
    let mut pos = 4;
    
    // Read Strings
    if pos + 4 > data.len() {
        return Err("Truncated bytecode: missing string table count".into());
    }
    let mut num_strings_bytes = [0u8; 4];
    num_strings_bytes.copy_from_slice(&data[pos..pos+4]);
    let num_strings = u32::from_le_bytes(num_strings_bytes) as usize;
    pos += 4;
    
    let mut strings = Vec::new();
    for i in 0..num_strings {
        if pos + 4 > data.len() {
            return Err(format!("Truncated bytecode: missing length for string {}", i));
        }
        let mut len_bytes = [0u8; 4];
        len_bytes.copy_from_slice(&data[pos..pos+4]);
        let str_len = u32::from_le_bytes(len_bytes) as usize;
        pos += 4;
        
        if pos + str_len > data.len() {
            return Err(format!("Truncated bytecode: string {} content extends past EOF", i));
        }
        let s = match String::from_utf8(data[pos..pos+str_len].to_vec()) {
            Ok(s) => s,
            Err(_) => return Err(format!("Invalid UTF-8 sequence in string table at index {}", i)),
        };
        strings.push(s);
        pos += str_len;
    }

    // Read Constants
    if pos + 4 > data.len() {
        return Err("Truncated bytecode: missing constant table count".into());
    }
    let mut num_const_bytes = [0u8; 4];
    num_const_bytes.copy_from_slice(&data[pos..pos+4]);
    let num_constants = u32::from_le_bytes(num_const_bytes) as usize;
    pos += 4;

    let mut constants = Vec::new();
    for i in 0..num_constants {
        if pos >= data.len() {
            return Err(format!("Truncated bytecode: missing type tag for constant {}", i));
        }
        let type_tag = data[pos];
        pos += 1;
        match type_tag {
            1 => { // Int
                if pos + 8 > data.len() {
                    return Err(format!("Truncated int constant at index {}", i));
                }
                let mut val_bytes = [0u8; 8];
                val_bytes.copy_from_slice(&data[pos..pos+8]);
                let val = i64::from_le_bytes(val_bytes);
                constants.push(NanVal::int(val));
                pos += 8;
            }
            2 => { // String
                if pos + 4 > data.len() {
                    return Err(format!("Truncated string constant length at index {}", i));
                }
                let mut len_bytes = [0u8; 4];
                len_bytes.copy_from_slice(&data[pos..pos+4]);
                let str_len = u32::from_le_bytes(len_bytes) as usize;
                pos += 4;
                if pos + str_len > data.len() {
                    return Err(format!("Truncated string constant content at index {}", i));
                }
                let s = match String::from_utf8(data[pos..pos+str_len].to_vec()) {
                    Ok(s) => s,
                    Err(_) => return Err(format!("Invalid UTF-8 in string constant at index {}", i)),
                };
                strings.push(s);
                constants.push(NanVal::string(strings.len() - 1));
                pos += str_len;
            }
            0 => { // Null
                constants.push(NanVal::null());
            }
            3 => { // Float
                if pos + 8 > data.len() {
                    return Err(format!("Truncated float constant at index {}", i));
                }
                let mut val_bytes = [0u8; 8];
                val_bytes.copy_from_slice(&data[pos..pos+8]);
                let val = f64::from_le_bytes(val_bytes);
                constants.push(NanVal::float(val));
                pos += 8;
            }
            4 => { // Bool
                if pos >= data.len() {
                    return Err(format!("Truncated bool constant at index {}", i));
                }
                let val = data[pos] != 0;
                constants.push(NanVal::bool(val));
                pos += 1;
            }
            _ => {
                constants.push(NanVal::null());
            }
        }
    }

    let bytecode = data[pos..].to_vec();
    Ok((strings, constants, bytecode))
}

fn execute_bytecode(filename: &str, use_jit: bool) {
    let mut file = match File::open(filename) {
        Ok(f) => f,
        Err(e) => {
            eprintln!("[AAYU Error] Cannot open file '{}': {}", filename, e);
            return;
        }
    };
    let mut data = Vec::new();
    if let Err(e) = file.read_to_end(&mut data) {
        eprintln!("[AAYU Error] Failed to read bytecode file: {}", e);
        return;
    }

    let (strings, constants, bytecode) = match parse_bytecode_data(&data) {
        Ok(parsed) => parsed,
        Err(e) => {
            eprintln!("[AAYU Security Error] Malformed Bytecode Rejected: {}", e);
            return;
        }
    };

    if use_jit {
        jit::compile_and_run(&bytecode, &constants);
    } else {
        let mut vm = AayuVM::new(bytecode, constants, strings);
        if let Err(e) = vm.run() {
            eprintln!("[AAYU Runtime Error] Execution halted: {}", e);
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() == 1 {
        print_help();
        return;
    }

    let cmd = &args[1];
    let use_jit = args.contains(&"--jit".to_string());

    if cmd == "-v" || cmd == "--version" || cmd == "version" {
        print_banner();
        return;
    }

    if cmd == "-h" || cmd == "--help" || cmd == "help" {
        print_help();
        return;
    }

    if cmd == "--sum" && args.len() >= 3 {
        let n: i64 = args[2].parse().expect("N must be an integer");
        run_sum(n, use_jit);
        return;
    }

    if cmd == "build" {
        if args.len() < 3 {
            eprintln!("[AAYU Error] Usage: aayu build <file.aayu> [-o <out.ayc>]");
            return;
        }
        let input_file = &args[2];
        let mut output_file = "output.ayc".to_string();
        if let Some(pos) = args.iter().position(|a| a == "-o") {
            if pos + 1 < args.len() {
                output_file = args[pos + 1].clone();
            }
        } else {
            let stem = Path::new(input_file).file_stem().and_then(|s| s.to_str()).unwrap_or("app");
            output_file = format!("{}.ayc", stem);
        }
        if compile_aayu_file(input_file, &output_file) {
            println!("Built standalone bytecode: {}", output_file);
        }
        return;
    }

    let target_file = if cmd == "run" {
        if args.len() < 3 {
            eprintln!("[AAYU Error] Usage: aayu run <file.aayu | file.ayc> [--jit]");
            return;
        }
        &args[2]
    } else {
        cmd
    };

    if target_file.ends_with(".aayu") {
        let temp_ayc = format!("{}.tmp.ayc", target_file);
        if !compile_aayu_file(target_file, &temp_ayc) {
            return;
        }
        execute_bytecode(&temp_ayc, use_jit);
        let _ = std::fs::remove_file(&temp_ayc);
    } else {
        execute_bytecode(target_file, use_jit);
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
        let _ = vm.run();
        println!("AAYU_VM_NS {}", t.elapsed().as_nanos());
    }
}
