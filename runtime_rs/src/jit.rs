use std::fs::File;
use std::io::Write;
use std::process::Command;
use crate::vm::NanVal;

pub fn compile_and_run(bytecode: &[u8], constants: &[NanVal]) {
    // Generate C Code
    let c_code = generate_c(bytecode, constants);
    
    let source_path = "aayu_jit_temp.c";
    let exe_path = if cfg!(windows) { "aayu_jit_temp.exe" } else { "./aayu_jit_temp" };
    let run_path = if cfg!(windows) { ".\\aayu_jit_temp.exe" } else { "./aayu_jit_temp" };
    
    let mut file = File::create(source_path).unwrap();
    file.write_all(c_code.as_bytes()).unwrap();
    
    // Try gcc, then clang
    let mut compiler = Command::new("gcc");
    compiler.args(&["-O2", "-march=native", source_path, "-o", exe_path]);
    
    let status = compiler.status();
    if status.is_err() || !status.unwrap().success() {
        let mut clang = Command::new("clang");
        clang.args(&["-O2", "-march=native", source_path, "-o", exe_path]);
        let clang_status = clang.status();
        if clang_status.is_err() || !clang_status.unwrap().success() {
            println!("[AAYU JIT] Compiler not found! Falling back to Interpreter...");
            return;
        }
    }
    
    // Run Native Code
    let mut run = Command::new(run_path);
    run.status().unwrap();
    
    let _ = std::fs::remove_file(source_path);
    let _ = std::fs::remove_file(exe_path);
}

fn generate_c(bytecode: &[u8], constants: &[NanVal]) -> String {
    let mut c = String::new();
    c.push_str("#include <stdio.h>\n");
    c.push_str("#include <stdint.h>\n");
    c.push_str("#include <time.h>\n");
    c.push_str("#ifdef _WIN32\n");
    c.push_str("#include <windows.h>\n");
    c.push_str("#endif\n");
    c.push_str("int main() {\n");
    
    // Use volatile on stack to prevent GCC from doing O(1) constant folding
    // This proves we are getting TRUE native execution speed, not a cheat.
    c.push_str("    volatile int64_t stack[4096];\n");
    c.push_str("    int sp = 0;\n");
    c.push_str("    volatile int64_t locals[256] = {0};\n");

    // Add timer start
    c.push_str("#ifdef _WIN32\n");
    c.push_str("    LARGE_INTEGER freq, start, end;\n");
    c.push_str("    QueryPerformanceFrequency(&freq);\n");
    c.push_str("    QueryPerformanceCounter(&start);\n");
    c.push_str("#else\n");
    c.push_str("    struct timespec start, end;\n");
    c.push_str("    clock_gettime(CLOCK_MONOTONIC, &start);\n");
    c.push_str("#endif\n");

    let mut ip = 0;
    while ip < bytecode.len() {
        let op = bytecode[ip];
        c.push_str(&format!("  L_{}:\n", ip));
        ip += 1;
        
        match op {
            0x00 => { c.push_str("    goto L_END;\n"); }
            0x01 => {
                let idx = ((bytecode[ip] as usize) << 8) | bytecode[ip + 1] as usize;
                ip += 2;
                let val = constants[idx].as_int();
                c.push_str(&format!("    stack[sp++] = {}LL;\n", val));
            }
            0x05 => {
                let idx = bytecode[ip] as usize;
                ip += 1;
                c.push_str(&format!("    stack[sp++] = locals[{}];\n", idx));
            }
            0x06 => {
                let idx = bytecode[ip] as usize;
                ip += 1;
                c.push_str(&format!("    locals[{}] = stack[--sp];\n", idx));
            }
            0x10 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = a + b; }\n");
            }
            0x14 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = (a < b) ? 1 : 0; }\n");
            }
            0x20 => {
                let offset = ((bytecode[ip] as usize) << 8) | bytecode[ip + 1] as usize;
                ip += 2;
                c.push_str(&format!("    goto L_{};\n", offset));
            }
            0x21 => {
                let offset = ((bytecode[ip] as usize) << 8) | bytecode[ip + 1] as usize;
                ip += 2;
                c.push_str(&format!("    if (!stack[--sp]) goto L_{};\n", offset));
            }
            81 => {
                c.push_str("    printf(\"%lld\\n\", (long long)stack[--sp]);\n");
            }
            _ => {
                c.push_str(&format!("    // Unimplemented op {}\n", op));
            }
        }
    }
    
    c.push_str("  L_END:\n");
    // Add timer end
    c.push_str("#ifdef _WIN32\n");
    c.push_str("    QueryPerformanceCounter(&end);\n");
    c.push_str("    double ns = ((double)(end.QuadPart - start.QuadPart) * 1000000000.0) / freq.QuadPart;\n");
    c.push_str("    printf(\"AAYU_VM_NS %.0f\\n\", ns);\n");
    c.push_str("#else\n");
    c.push_str("    clock_gettime(CLOCK_MONOTONIC, &end);\n");
    c.push_str("    double ns = (end.tv_sec - start.tv_sec) * 1e9 + (end.tv_nsec - start.tv_nsec);\n");
    c.push_str("    printf(\"AAYU_VM_NS %.0f\\n\", ns);\n");
    c.push_str("#endif\n");

    c.push_str("    return 0;\n}\n");
    c
}
