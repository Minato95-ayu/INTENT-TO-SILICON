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
    println!("  repl                       Launch interactive microsecond REPL shell");
    println!("  run <file.aayu> [--jit]    Compile and execute AAYU source code");
    println!("  run <file.ayc> [--jit]     Execute precompiled bytecode directly");
    println!("  disasm <file>              Silicon bytecode disassembler (inspect opcodes)");
    println!("  build <file.aayu> [-o out] Compile source to .ayc bytecode");
    println!("  check <file.aayu>          Validate syntax & structure without running");
    println!("  init <name> [--template]   Scaffold project (templates: rest, ml, web, default)");
    println!("  info, sysinfo              Display detailed environment & system info");
    println!("  version, -v, --version     Display engine version information");
    println!("  help, -h, --help           Display this help manual\n");
    println!("Examples:");
    println!("  aayu repl");
    println!("  aayu run hello.aayu");
    println!("  aayu disasm mega_test.aayu");
    println!("  aayu init my_api --template rest");
    println!("  aayu init my_ai --template ml");
    println!("  aayu init my_ui --template web");
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

fn run_init(project_name: &str, template: Option<&str>) {
    let dir = Path::new(project_name);
    if let Err(e) = std::fs::create_dir_all(dir) {
        eprintln!("[AAYU Error] Failed to create directory '{}': {}", project_name, e);
        std::process::exit(1);
    }
    let tpl = template.unwrap_or("default");
    
    let (main_aayu, app_desc) = match tpl {
        "rest" | "api" => (
            format!(r#"# AAYU High-Speed REST API Service
import "std/server"
import "std/json"
import "std/db"

action main
    print("==================================================")
    print("Starting AAYU REST API Service...")
    print("Server initialized on port 8080")
    let r1 = db_create_record(1, "Silicon Chip A1", 199)
    let r2 = db_create_record(2, "Neural Core N1", 499)
    let items = [r1, r2]
    print("Database records loaded: " + len(items))
    let resp = json_response(200, "{{\"status\": \"online\", \"records\": 2}}")
    print("API Health Check: " + resp)
    print("==================================================")
end

main()
"#, ),
            "AAYU High-Speed REST API Service"
        ),
        "ml" | "ai" => (
            format!(r#"# AAYU Native AI / Neural Inference Project
import "std/math"
import "std/ai"

action main
    print("==================================================")
    print("AAYU Neural Inference & Machine Learning Pipeline")
    print("Zero External Dependencies | C-Speed Silicon Execution")
    print("==================================================")

    let v1 = [1.0, 2.0, 3.0]
    let v2 = [10.0, 20.0, 30.0]
    let v_sum = vec_add(v1, v2)
    print("Feature vector addition: [" + v_sum[0] + ", " + v_sum[1] + ", " + v_sum[2] + "]")
    print("Neural activation complete.")
    print("==================================================")
end

main()
"#, ),
            "AAYU Native AI/ML Inference Service"
        ),
        "web" | "ui" => (
            format!(r#"# AAYU Full-Stack Declarative UI Application
import "std/ui"

action main
    print("Compiling and rendering AAYU Declarative UI...")
    let heading = create_text("AAYU Reactive Dashboard")
    let btn = create_button("Trigger Analytics", "handleClick")
    let col = create_column([heading, btn])
    let html = render(col)
    print("Page Home rendered with full HTML & Reactive State:")
    print(html)
end

main()
"#, ),
            "AAYU Full-Stack Declarative UI Application"
        ),
        _ => (
            format!(r#"# AAYU Application: {}
app {}

action main
    print("==================================================")
    print("Welcome to {} written in pure AAYU!")
    print("Platform: " + platform() + " | Architecture: " + arch())
    print("==================================================")
end

main()
"#, project_name, project_name.replace('-', "_"), project_name),
            "AAYU Intent-to-Silicon Project"
        )
    };

    let config_json = format!(r#"{{
  "name": "{}",
  "version": "0.1.0",
  "template": "{}",
  "entry": "main.aayu",
  "description": "{}"
}}
"#, project_name, tpl, app_desc);

    let gitignore = "*.ayc\n*.tmp*\n";
    let readme = format!("# {}\n\n{}\n\n## Running the Project\n```bash\naayu run main.aayu\n```\n", project_name, app_desc);

    let _ = std::fs::write(dir.join("main.aayu"), main_aayu);
    let _ = std::fs::write(dir.join("aayu.json"), config_json);
    let _ = std::fs::write(dir.join(".gitignore"), gitignore);
    let _ = std::fs::write(dir.join("README.md"), readme);

    println!("Created new AAYU [{}] project '{}' successfully!", tpl, project_name);
    println!("  - {}/main.aayu", project_name);
    println!("  - {}/aayu.json", project_name);
    println!("  - {}/.gitignore", project_name);
    println!("  - {}/README.md", project_name);
    println!("\nTo run your project:");
    println!("  cd {}", project_name);
    println!("  aayu run main.aayu");
}

fn run_disasm(input_file: &str) {
    let data = if input_file.ends_with(".aayu") || input_file.ends_with(".ay") || input_file.ends_with(".aa") {
        let temp_ayc = format!("{}.tmp.ayc", input_file);
        if !compile_aayu_file(input_file, &temp_ayc) {
            std::process::exit(1);
        }
        let bytes = std::fs::read(&temp_ayc).unwrap_or_default();
        let _ = std::fs::remove_file(&temp_ayc);
        bytes
    } else {
        match std::fs::read(input_file) {
            Ok(b) => b,
            Err(e) => {
                eprintln!("[AAYU Error] Cannot read bytecode file '{}': {}", input_file, e);
                std::process::exit(1);
            }
        }
    };

    let (strings, constants, bytecode) = match parse_bytecode_data(&data) {
        Ok(parsed) => parsed,
        Err(e) => {
            eprintln!("[AAYU Error] Malformed Bytecode: {}", e);
            std::process::exit(1);
        }
    };

    println!("==================================================");
    println!("       AAYU SILICON BYTECODE DISASSEMBLER         ");
    println!("==================================================");
    println!("Target: {} (Bytecode: {} bytes, Constants: {})", input_file, bytecode.len(), constants.len());
    println!("\n[CONSTANT POOL ({} entries)]:", constants.len());
    for (i, c) in constants.iter().enumerate() {
        if c.is_int() {
            println!("  #{}: Int({})", i, c.as_int());
        } else if c.is_float() {
            println!("  #{}: Float({})", i, c.as_float());
        } else if c.is_string() {
            let s = strings.get(c.as_string_idx()).map(|s| s.as_str()).unwrap_or("<invalid string>");
            println!("  #{}: String(\"{}\")", i, s);
        } else if c.is_bool() {
            println!("  #{}: Bool({})", i, c.as_bool());
        } else if c.is_null() {
            println!("  #{}: Null", i);
        } else {
            println!("  #{}: NanVal", i);
        }
    }

    println!("\n[BYTECODE INSTRUCTION STREAM]:");
    let mut pc = 0;
    let len = bytecode.len();
    while pc < len {
        let op_pc = pc;
        let op = bytecode[pc];
        pc += 1;

        match op {
            0x00 | 0xFF => {
                println!("  {:04X}: HALT", op_pc);
            }
            0x01 => {
                if pc + 2 <= len {
                    let idx = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    pc += 2;
                    let val_str = if idx < constants.len() {
                        let c = constants[idx];
                        if c.is_int() { format!("{}", c.as_int()) }
                        else if c.is_float() { format!("{}", c.as_float()) }
                        else if c.is_string() { strings.get(c.as_string_idx()).map(|s| format!("\"{}\"", s)).unwrap_or_default() }
                        else if c.is_bool() { format!("{}", c.as_bool()) }
                        else { "null".into() }
                    } else { "?".into() };
                    println!("  {:04X}: PUSH_CONST     #{} ({})", op_pc, idx, val_str);
                } else {
                    println!("  {:04X}: PUSH_CONST     [truncated]", op_pc);
                    break;
                }
            }
            0x02 => { println!("  {:04X}: POP", op_pc); }
            0x05 => {
                if pc < len {
                    let slot = bytecode[pc]; pc += 1;
                    println!("  {:04X}: LOAD_VAR       slot:{}", op_pc, slot);
                }
            }
            0x06 => {
                if pc < len {
                    let slot = bytecode[pc]; pc += 1;
                    println!("  {:04X}: STORE_VAR      slot:{}", op_pc, slot);
                }
            }
            0x07 => {
                if pc < len {
                    let slot = bytecode[pc]; pc += 1;
                    println!("  {:04X}: LOAD_GLOBAL    slot:{}", op_pc, slot);
                }
            }
            0x08 => {
                if pc < len {
                    let slot = bytecode[pc]; pc += 1;
                    println!("  {:04X}: STORE_GLOBAL   slot:{}", op_pc, slot);
                }
            }
            0x10 => { println!("  {:04X}: ADD", op_pc); }
            0x11 => { println!("  {:04X}: SUB", op_pc); }
            0x12 => { println!("  {:04X}: MUL", op_pc); }
            0x13 => { println!("  {:04X}: DIV", op_pc); }
            0x14 => { println!("  {:04X}: MOD", op_pc); }
            0x15 => { println!("  {:04X}: NEG", op_pc); }
            0x20 => {
                if pc + 2 <= len {
                    let target = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    pc += 2;
                    println!("  {:04X}: JUMP           -> 0x{:04X}", op_pc, target);
                }
            }
            0x21 => {
                if pc + 2 <= len {
                    let target = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    pc += 2;
                    println!("  {:04X}: JUMP_IF_FALSE  -> 0x{:04X}", op_pc, target);
                }
            }
            34 => {
                if pc + 2 <= len {
                    let argc = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    pc += 2;
                    println!("  {:04X}: CALL           argc:{}", op_pc, argc);
                }
            }
            35 => { println!("  {:04X}: RET", op_pc); }
            36 => {
                if pc + 4 <= len {
                    let argc = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    let target = ((bytecode[pc + 2] as usize) << 8) | bytecode[pc + 3] as usize;
                    pc += 4;
                    println!("  {:04X}: CALL_LOCAL     argc:{} -> 0x{:04X}", op_pc, argc, target);
                }
            }
            38 => { println!("  {:04X}: EQ", op_pc); }
            39 => { println!("  {:04X}: NEQ", op_pc); }
            41 => { println!("  {:04X}: LT", op_pc); }
            42 => { println!("  {:04X}: GT", op_pc); }
            43 => { println!("  {:04X}: LTE", op_pc); }
            44 => { println!("  {:04X}: GTE", op_pc); }
            48 => {
                if pc + 2 <= len {
                    let slot = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    pc += 2;
                    let name = if slot < constants.len() && constants[slot].is_string() {
                        strings.get(constants[slot].as_string_idx()).cloned().unwrap_or_default()
                    } else { String::new() };
                    println!("  {:04X}: STORE_STATE    slot:{} ({})", op_pc, slot, name);
                }
            }
            49 => {
                if pc + 2 <= len {
                    let slot = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    pc += 2;
                    let name = if slot < constants.len() && constants[slot].is_string() {
                        strings.get(constants[slot].as_string_idx()).cloned().unwrap_or_default()
                    } else { String::new() };
                    println!("  {:04X}: LOAD_STATE     slot:{} ({})", op_pc, slot, name);
                }
            }
            50 => {
                if pc + 2 <= len {
                    let slot = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    pc += 2;
                    println!("  {:04X}: INIT_STATE     slot:{}", op_pc, slot);
                }
            }
            81 => { println!("  {:04X}: PRINT", op_pc); }
            98 => { println!("  {:04X}: RET_VAL", op_pc); }
            128 => {
                if pc + 2 <= len {
                    let count = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    pc += 2;
                    println!("  {:04X}: BUILD_DICT     count:{}", op_pc, count);
                }
            }
            134 => {
                if pc + 2 <= len {
                    let count = ((bytecode[pc] as usize) << 8) | bytecode[pc + 1] as usize;
                    pc += 2;
                    println!("  {:04X}: CREATE_ARRAY   count:{}", op_pc, count);
                }
            }
            136 => { println!("  {:04X}: ARRAY_GET", op_pc); }
            137 => { println!("  {:04X}: ARRAY_SET", op_pc); }
            140 => { println!("  {:04X}: DICT_GET", op_pc); }
            141 => { println!("  {:04X}: DICT_SET", op_pc); }
            142 => { println!("  {:04X}: LEN", op_pc); }
            other => {
                println!("  {:04X}: OP_0x{:02X}", op_pc, other);
            }
        }
    }
    println!("==================================================");
}

fn run_repl() {
    println!("==================================================");
    println!("     AAYU Silicon Interactive Shell (REPL) v1.2.0 ");
    println!("     Architecture: {} ({})", env::consts::ARCH, env::consts::OS);
    println!("     Type 'exit' to quit, 'help' for guidance.    ");
    println!("==================================================");

    let stdin = std::io::stdin();
    let mut history_lines: Vec<String> = Vec::new();

    loop {
        use std::io::Write;
        print!("aayu> ");
        let _ = std::io::stdout().flush();

        let mut line = String::new();
        if stdin.read_line(&mut line).is_err() {
            break;
        }
        let trimmed = line.trim();
        if trimmed.is_empty() {
            continue;
        }
        if trimmed == "exit" || trimmed == "quit" {
            println!("Exiting AAYU shell. Goodbye!");
            break;
        }
        if trimmed == "help" {
            println!("AAYU REPL Commands:");
            println!("  help                  Display this guidance manual");
            println!("  clear                 Reset REPL session variables");
            println!("  exit, quit            Exit the interactive shell");
            println!("  <expression>          Evaluate expressions instantly (e.g. 10 * 5, sum([1,2,3]))");
            println!("  <statement>           Declare variables and actions (e.g. let x = 42, print(x))");
            continue;
        }
        if trimmed == "clear" {
            history_lines.clear();
            println!("[AAYU REPL] Session variables reset.");
            continue;
        }

        let is_action = trimmed.starts_with("action ") || trimmed.starts_with("if ") || trimmed.starts_with("while ");
        let is_stmt = trimmed.starts_with("let ")
            || trimmed.starts_with("state ")
            || trimmed.starts_with("print")
            || trimmed.starts_with("import ")
            || is_action
            || (trimmed.contains('=') && !trimmed.contains("=="));

        let candidate_code = if is_stmt {
            trimmed.to_string()
        } else {
            format!("print({})", trimmed)
        };

        let mut full_code = String::new();
        for hist in &history_lines {
            full_code.push_str(hist);
            full_code.push('\n');
        }
        full_code.push_str(&candidate_code);
        full_code.push('\n');

        match compiler::compile(&full_code) {
            Ok(bytecode) => {
                if let Ok((strings, constants, bc)) = parse_bytecode_data(&bytecode) {
                    let mut vm = AayuVM::new(bc, constants, strings);
                    if let Err(e) = vm.run() {
                        eprintln!("[AAYU Runtime Error] {}", e);
                    } else {
                        if trimmed.starts_with("let ") || trimmed.starts_with("import ") || (trimmed.contains('=') && !trimmed.contains("==")) {
                            history_lines.push(trimmed.to_string());
                        }
                    }
                }
            }
            Err(e) => {
                eprintln!("[AAYU Syntax Error]:\n{}", e);
            }
        }
    }
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
    
    if args.len() == 1 || (args.len() >= 2 && (args[1] == "repl" || args[1] == "shell")) {
        run_repl();
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

    if cmd == "disasm" || cmd == "dump" {
        if args.len() < 3 {
            eprintln!("[AAYU Error] Usage: aayu disasm <file.aayu | file.ayc>");
            std::process::exit(2);
        }
        run_disasm(&args[2]);
        return;
    }

    if cmd == "init" {
        let name = if args.len() >= 3 && !args[2].starts_with('-') { &args[2] } else { "aayu_app" };
        let mut template: Option<&str> = None;
        if let Some(pos) = args.iter().position(|a| a == "--template" || a == "-t") {
            if pos + 1 < args.len() {
                template = Some(&args[pos + 1]);
            }
        }
        run_init(name, template);
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

    let is_web = args.contains(&"--web".to_string());
    let mut custom_port: Option<u16> = None;
    if let Some(pos) = args.iter().position(|a| a == "--port") {
        if pos + 1 < args.len() {
            if let Ok(p) = args[pos + 1].parse::<u16>() {
                custom_port = Some(p);
            }
        }
    }

    let target_file = if cmd == "run" {
        if args.len() < 3 {
            eprintln!("[AAYU Error] Usage: aayu run <file.aayu | file.ayc> [--web] [--port <PORT>] [--jit]");
            std::process::exit(2);
        }
        &args[2]
    } else {
        cmd
    };

    if is_web {
        // Strict CLI verification: ensure that file contains route definitions or server startup
        if target_file.ends_with(".aayu") || target_file.ends_with(".ay") || target_file.ends_with(".aa") {
            let content = match std::fs::read_to_string(target_file) {
                Ok(c) => c,
                Err(e) => {
                    eprintln!("[AAYU Error] Failed to read source file '{}': {}", target_file, e);
                    std::process::exit(1);
                }
            };
            let has_route = content.contains("route ") || content.contains("route\"") || content.contains("route '") || content.contains("Server.start");
            if !has_route {
                eprintln!("[AAYU CLI Error] --web flag provided, but no routes found in '{}'", target_file);
                eprintln!("Execution halted. Please define 'route' blocks or remove the --web flag.");
                std::process::exit(1);
            }
        }
        if let Some(p) = custom_port {
            std::env::set_var("PORT", p.to_string());
        }
    }

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
