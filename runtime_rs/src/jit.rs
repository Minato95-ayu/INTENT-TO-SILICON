use std::fs::File;
use std::io::Write;
use std::process::Command;
use crate::vm::NanVal;

pub fn can_compile(bytecode: &[u8]) -> bool {
    let mut ip = 0;
    while ip < bytecode.len() {
        let op = bytecode[ip];
        ip += 1;
        match op {
            0x00 | 0xFF => {}
            0x01 => {
                if ip + 2 > bytecode.len() { return false; }
                ip += 2;
            }
            0x05 | 0x06 => {
                if ip + 1 > bytecode.len() { return false; }
                ip += 1;
            }
            16 | 17 | 18 | 19 | 20 => {}
            38 | 39 | 41 | 42 | 43 | 44 => {}
            32 | 33 => {
                if ip + 2 > bytecode.len() { return false; }
                ip += 2;
            }
            81 => {}
            _ => return false,
        }
    }
    true
}

pub fn compile_and_run(bytecode: &[u8], constants: &[NanVal]) -> bool {
    let c_code = generate_c(bytecode, constants);
    
    let source_path = "aayu_jit_temp.c";
    let exe_path = if cfg!(windows) { "aayu_jit_temp.exe" } else { "./aayu_jit_temp" };
    let run_path = if cfg!(windows) { ".\\aayu_jit_temp.exe" } else { "./aayu_jit_temp" };
    
    {
        let mut file = match File::create(source_path) {
            Ok(f) => f,
            Err(_) => return false,
        };
        if file.write_all(c_code.as_bytes()).is_err() || file.flush().is_err() {
            let _ = std::fs::remove_file(source_path);
            return false;
        }
    }
    
    // Try gcc, then clang
    let mut compiler = Command::new("gcc");
    compiler.args(["-O2", "-march=native", source_path, "-o", exe_path]);
    
    let mut compiled = false;
    if let Ok(s) = compiler.status() {
        if s.success() {
            compiled = true;
        }
    }

    if !compiled {
        let mut clang = Command::new("clang");
        clang.args(["-O2", "-march=native", source_path, "-o", exe_path]);
        if let Ok(s) = clang.status() {
            if s.success() {
                compiled = true;
            }
        }
    }

    if !compiled {
        let _ = std::fs::remove_file(source_path);
        return false;
    }
    
    let run_res = Command::new(run_path).status();
    let _ = std::fs::remove_file(source_path);
    let _ = std::fs::remove_file(exe_path);

    match run_res {
        Ok(s) => s.success(),
        Err(_) => false,
    }
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
            16 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = a + b; }\n");
            }
            17 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = a - b; }\n");
            }
            18 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = a * b; }\n");
            }
            19 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = (b != 0) ? (a / b) : 0; }\n");
            }
            20 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = (b != 0) ? (a % b) : 0; }\n");
            }
            38 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = (a == b) ? 1 : 0; }\n");
            }
            39 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = (a != b) ? 1 : 0; }\n");
            }
            41 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = (a < b) ? 1 : 0; }\n");
            }
            42 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = (a > b) ? 1 : 0; }\n");
            }
            43 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = (a <= b) ? 1 : 0; }\n");
            }
            44 => {
                c.push_str("    { int64_t b = stack[--sp]; int64_t a = stack[--sp]; stack[sp++] = (a >= b) ? 1 : 0; }\n");
            }
            32 => {
                let offset = ((bytecode[ip] as usize) << 8) | bytecode[ip + 1] as usize;
                ip += 2;
                c.push_str(&format!("    goto L_{};\n", offset));
            }
            33 => {
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
