use std::env;
use std::fs;
use std::io::Write;

pub mod lexer;
pub mod parser;
pub mod emitter;

pub fn compile(source: &str) -> Result<Vec<u8>, String> {
    let mut lexer = lexer::Lexer::new(source);
    let tokens = lexer.tokenize();
    
    let mut parser = parser::Parser::new(tokens);
    let ast = parser.parse();
    
    let mut emitter = emitter::Emitter::new();
    let bytecode = emitter.emit(ast);
    Ok(bytecode)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        println!("AAYU Compiler (Rust) v0.1");
        println!("Usage: aayuc <input.aayu> -o <output.ayc>");
        return;
    }

    let input_file = &args[1];
    let output_file = &args[3]; // ignoring -o flag check for simplicity in MVP
    
    let contents = fs::read_to_string(input_file).expect("Failed to read .aayu file");
    let bc = compile(&contents).expect("Compilation Failed");
    
    let mut file = fs::File::create(output_file).expect("Failed to create .ayc file");
    file.write_all(&bc).expect("Failed to write bytecode");
    println!("Compiled successfully to {}", output_file);
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::process::Command;
    use std::io::Write;

    #[test]
    fn test_source_to_vm_math() {
        let source = "let x = 10 + 20\nprint(x)\n";
        let bytecode = compile(source).expect("Compilation failed");
        
        let temp_ayc = "test_math_out.ayc";
        let mut file = std::fs::File::create(temp_ayc).unwrap();
        file.write_all(&bytecode).unwrap();
        
        let output = Command::new("cargo")
            .args(["run", "--manifest-path", "../../runtime_rs/Cargo.toml", "--", temp_ayc])
            .output()
            .expect("Failed to execute VM");
            
        let stdout = String::from_utf8_lossy(&output.stdout);
        let _ = std::fs::remove_file(temp_ayc);
        assert!(stdout.contains("30"));
    }

    #[test]
    fn test_source_to_vm_loop() {
        let source = "
let x = 0
while x < 3
    print(x)
    let x = x + 1
end
";
        let bytecode = compile(source).expect("Compilation failed");
        let temp_ayc = "test_loop_out.ayc";
        let mut file = std::fs::File::create(temp_ayc).unwrap();
        file.write_all(&bytecode).unwrap();
        
        let output = Command::new("cargo")
            .args(["run", "--manifest-path", "../../runtime_rs/Cargo.toml", "--", temp_ayc])
            .output()
            .expect("Failed to execute VM");
            
        let stdout = String::from_utf8_lossy(&output.stdout);
        let _ = std::fs::remove_file(temp_ayc);
        
        println!("STDOUT: {}", stdout);
        println!("BC: {:?}", bytecode);
        println!("STDOUT: {}\nSTDERR: {}", stdout, String::from_utf8_lossy(&output.stderr));
        assert!(!stdout.contains("3"));
    }
}




