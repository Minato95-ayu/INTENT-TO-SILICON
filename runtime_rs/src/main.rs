use std::env;
use std::fs::File;
use std::io::Read;
use std::path::Path;

use aayu_vm::vm::{AayuVM, NanVal};
use aayu_vm::jit;
use aayu_vm::compiler;

fn print_banner() {
    println!("AAYU Intent-to-Silicon Engine v1.2.0");
    println!("Architecture: {} ({})", env::consts::ARCH, env::consts::OS);
    println!("Runtime: Native Rust Bytecode VM | Embedded Compiler & JIT");
}

fn print_help() {
    print_banner();
    println!("\nUsage: aayu [command] [options] <file>\n");
    println!("Commands:");
    println!("  run <file.aayu> [--jit]    Compile and execute AAYU source code");
    println!("  run <file.ayc> [--jit]     Execute precompiled bytecode directly");
    println!("  build <file.aayu> [-o out] Compile source to .ayc bytecode");
    println!("  check <file.aayu>          Validate syntax & structure without running");
    println!("  init <project_name>        Scaffold a brand new AAYU project");
    println!("  info, sysinfo              Display detailed environment & system info");
    println!("  version, -v, --version     Display engine version information");
    println!("  help, -h, --help           Display this help manual\n");
    println!("Examples:");
    println!("  aayu run hello.aayu");
    println!("  aayu run portfolio.ayc --jit");
    println!("  aayu build app.aayu -o app.ayc");
    println!("  aayu check app.aayu");
    println!("  aayu init my_app");
}

fn print_sysinfo() {
    println!("==================================================");
    println!("       AAYU INTENT-TO-SILICON ENGINE INFO         ");
    println!("==================================================");
    println!("Engine Version:   1.2.0 (Self-Hosted Intent-to-Silicon)");
    println!("Operating System: {}", env::consts::OS);
    println!("Architecture:     {}", env::consts::ARCH);
    let is_termux = env::var("TERMUX_VERSION").is_ok()
        || Path::new("/data/data/com.termux").exists()
        || env::var("PREFIX").map(|p| p.contains("com.termux")).unwrap_or(false);
    if is_termux {
        let ver = env::var("TERMUX_VERSION").unwrap_or_else(|_| "detected".into());
        println!("Environment:      Android Termux (v{})", ver);
    } else {
        println!("Environment:      Native Host ({})", env::consts::OS);
    }
    println!("VM Runtime:       AAYU High-Speed Silicon Stack VM");
    println!("JIT Acceleration: Dynamic C-Level JIT Engine");
    println!("Compiler Engine:  Pure Self-Hosted AAYU Lexer/Parser/Emitter");
    println!("Standard Library: std/ (math, collections, fs, os, ai, db, http, json, ledger, server, ui)");
    println!("Zero Dependencies: SQLite, HTTP, Math, UI, DB Built-In");
    println!("==================================================");
}

fn compile_aayu_file(input_path: &str, output_path: &str) -> bool {
    let path = Path::new(input_path);
    match compiler::compile_file(path) {
        Ok(bytecode) => {
            if let Err(e) = std::fs::write(output_path, bytecode) {
                eprintln!("[AAYU Error] Failed to write bytecode output '{}': {}", output_path, e);
                return false;
            }
            true
        }
        Err(e) => {
            eprintln!("[AAYU Compile Error in '{}']:\n{}", input_path, e);
            false
        }
    }
}

fn run_aayuc_cli(args: &[String]) {
    if args.len() < 2 {
        println!("AAYU Compiler (aayuc) v1.2.0");
        println!("Usage: aayuc <input.aayu> [-o <output.ayc>]");
        return;
    }
    let input_file = &args[1];
    let mut output_file = "output.ayc".to_string();
    if let Some(pos) = args.iter().position(|a| a == "-o") {
        if pos + 1 < args.len() {
            output_file = args[pos + 1].clone();
        }
    } else if args.len() >= 3 && !args[2].starts_with('-') {
        output_file = args[2].clone();
    } else {
        let stem = Path::new(input_file).file_stem().and_then(|s| s.to_str()).unwrap_or("app");
        output_file = format!("{}.ayc", stem);
    }
    if compile_aayu_file(input_file, &output_file) {
        println!("Compiled successfully to {}", output_file);
    } else {
        std::process::exit(1);
    }
}

fn run_init(project_name: &str) {
    let dir = Path::new(project_name);
    if let Err(e) = std::fs::create_dir_all(dir) {
        eprintln!("[AAYU Error] Failed to create directory '{}': {}", project_name, e);
        std::process::exit(1);
    }
    let main_aayu = format!(
r#"# AAYU Application: {}
app {}

action main
    print("==================================================")
    print("Welcome to {} written in pure AAYU!")
    print("Platform: " + platform() + " | Architecture: " + arch())
    print("==================================================")
end

run main
"#, project_name, project_name.replace('-', "_"), project_name);

    let config_json = format!(
r#"{{
  "name": "{}",
  "version": "0.1.0",
  "entry": "main.aayu",
  "description": "AAYU Intent-to-Silicon Project"
}}
"#, project_name);

    let gitignore = "*.ayc\n*.tmp*\n";

    let _ = std::fs::write(dir.join("main.aayu"), main_aayu);
    let _ = std::fs::write(dir.join("aayu.json"), config_json);
    let _ = std::fs::write(dir.join(".gitignore"), gitignore);

    println!("Created new AAYU project '{}' successfully!", project_name);
    println!("  - {}/main.aayu", project_name);
    println!("  - {}/aayu.json", project_name);
    println!("  - {}/.gitignore", project_name);
    println!("\nTo run your project:");
    println!("  cd {}", project_name);
    println!("  aayu run main.aayu");
}

fn run_check(input_file: &str) {
    let contents = match std::fs::read_to_string(input_file) {
        Ok(c) => c,
        Err(e) => {
            eprintln!("[AAYU Error] Failed to read file '{}': {}", input_file, e);
            std::process::exit(1);
        }
    };
    match compiler::compile(&contents) {
        Ok(bc) => {
            println!("[AAYU Check] Syntax OK: '{}' (Generated {} bytes bytecode)", input_file, bc.len());
        }
        Err(e) => {
            eprintln!("[AAYU Syntax Error in '{}']:\n{}", input_file, e);
            std::process::exit(1);
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
                return Err(format!("Unknown constant type tag 0x{:02X} at constant index {}", type_tag, i));
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
            std::process::exit(1);
        }
    };
    let mut data = Vec::new();
    if let Err(e) = file.read_to_end(&mut data) {
        eprintln!("[AAYU Error] Failed to read bytecode file: {}", e);
        std::process::exit(1);
    }

    let (strings, constants, bytecode) = match parse_bytecode_data(&data) {
        Ok(parsed) => parsed,
        Err(e) => {
            eprintln!("[AAYU Security Error] Malformed Bytecode Rejected: {}", e);
            std::process::exit(1);
        }
    };

    let mut vm = AayuVM::new(bytecode.clone(), constants.clone(), strings.clone());
    if let Err(e) = vm.validate() {
        eprintln!("[AAYU Security Error] Bytecode Verification Failed: {}", e);
        std::process::exit(1);
    }

    if use_jit {
        if jit::can_compile(&bytecode) {
            if !jit::compile_and_run(&bytecode, &constants) {
                eprintln!("[AAYU JIT] Native C compiler unavailable or build failed. Safely executing via Silicon VM...");
                if let Err(e) = vm.run() {
                    eprintln!("[AAYU Runtime Error] Execution halted: {}", e);
                    std::process::exit(1);
                }
            }
        } else {
            eprintln!("[AAYU JIT] This bytecode is not verified for native execution. Running it in the Rust VM...");
            if let Err(e) = vm.run() {
                eprintln!("[AAYU Runtime Error] Execution halted: {}", e);
                std::process::exit(1);
            }
        }
    } else {
        if let Err(e) = vm.run() {
            eprintln!("[AAYU Runtime Error] Execution halted: {}", e);
            std::process::exit(1);
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    
    if args.len() == 1 {
        print_help();
        return;
    }

    // Check if executed as aayuc or aayuc.exe
    let prog = &args[0];
    let is_aayuc = prog.ends_with("aayuc") || prog.ends_with("aayuc.exe");
    if is_aayuc {
        run_aayuc_cli(&args);
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

    if cmd == "info" || cmd == "sysinfo" {
        print_sysinfo();
        return;
    }

    if cmd == "check" {
        if args.len() < 3 {
            eprintln!("[AAYU Error] Usage: aayu check <file.aayu>");
            std::process::exit(2);
        }
        run_check(&args[2]);
        return;
    }

    if cmd == "init" {
        let name = if args.len() >= 3 { &args[2] } else { "aayu_app" };
        run_init(name);
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
            std::process::exit(2);
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
            println!("Built AAYU bytecode: {}", output_file);
        } else {
            std::process::exit(1);
        }
        return;
    }

    let target_file = if cmd == "run" {
        if args.len() < 3 {
            eprintln!("[AAYU Error] Usage: aayu run <file.aayu | file.ayc> [--jit]");
            std::process::exit(2);
        }
        &args[2]
    } else {
        cmd
    };

    if target_file.ends_with(".aayu") || target_file.ends_with(".ay") || target_file.ends_with(".aa") {
        let temp_ayc = format!("{}.tmp.ayc", target_file);
        if !compile_aayu_file(target_file, &temp_ayc) {
            std::process::exit(1);
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
