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
    let (bytecode, constants, strings, num_constants) = emitter.emit(&ast);

    
    let mut out = Vec::new();
    out.extend_from_slice(b"AAYU"); // 4 bytes header
    
    let num_strings = strings.len() as u32;
    out.extend_from_slice(&num_strings.to_le_bytes());
    for s in strings {
        let bytes = s.as_bytes();
        let len = bytes.len() as u32;
        out.extend_from_slice(&len.to_le_bytes());
        out.extend_from_slice(bytes);
    }
    
    out.extend_from_slice(&num_constants.to_le_bytes());
    out.extend_from_slice(&constants);
    
    out.extend_from_slice(&bytecode);
    Ok(out)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        println!("AAYU Compiler (Rust) v0.1");
        println!("Usage: aayuc <input.aayu> -o <output.ayc>");
        return;
    }

    let input_file = &args[1];
    let output_file = if args.len() >= 4 && args[2] == "-o" {
        &args[3]
    } else if args.len() >= 3 {
        &args[2]
    } else {
        "output.ayc"
    };
    
    let contents = fs::read_to_string(input_file).expect("Failed to read .aayu file");
    let bc = compile(&contents).expect("Compilation Failed");
    
    let mut file = fs::File::create(output_file).expect("Failed to create .ayc file");
    file.write_all(&bc).expect("Failed to write bytecode");
    println!("Compiled successfully to {}", output_file);
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn dummy() {}
}



