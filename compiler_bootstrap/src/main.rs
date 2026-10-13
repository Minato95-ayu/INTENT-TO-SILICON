use std::env;
use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::collections::HashSet;

pub mod lexer;
pub mod parser;
pub mod emitter;

pub fn compile(source: &str) -> Result<Vec<u8>, String> {
    let ast = parse_source(source)?;
    if ast.iter().any(|s| matches!(s, parser::Statement::Import(_))) {
        return Err("imports require compiling a file so relative paths can be resolved".into());
    }
    compile_ast(&ast)
}

fn parse_source(source: &str) -> Result<Vec<parser::Statement>, String> {
    let mut lexer = lexer::Lexer::new(source);
    let tokens = lexer.tokenize();
    
    let mut parser = parser::Parser::new(tokens);
    let ast = parser.parse();
    if !parser.errors().is_empty() {
        return Err(parser.errors().join("\n"));
    }
    Ok(ast)
}

fn compile_ast(ast: &[parser::Statement]) -> Result<Vec<u8>, String> {
    validate_supported(&ast)?;
    let mut emitter = emitter::Emitter::new();
    let (bytecode, constants, strings, num_constants) = emitter.emit(&ast);
    if bytecode.len() > u16::MAX as usize {
        return Err("compiled code exceeds the current 65535-byte address limit".into());
    }
    if num_constants > u16::MAX as u32 + 1 {
        return Err("compiled program exceeds the 65536-entry constant limit".into());
    }

    
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

fn expand_file(path: &Path, visiting: &mut HashSet<PathBuf>, loaded: &mut HashSet<PathBuf>) -> Result<Vec<parser::Statement>, String> {
    let canonical = fs::canonicalize(path).map_err(|e| format!("cannot resolve module '{}': {}", path.display(), e))?;
    if visiting.contains(&canonical) {
        return Err(format!("cyclic import detected at '{}'", canonical.display()));
    }
    if !loaded.insert(canonical.clone()) { return Ok(Vec::new()); }
    visiting.insert(canonical.clone());
    let source = fs::read_to_string(&canonical).map_err(|e| format!("cannot read module '{}': {}", canonical.display(), e))?;
    let statements = parse_source(&source).map_err(|e| format!("{}: {}", canonical.display(), e))?;
    let mut expanded = Vec::new();
    for statement in statements {
        if let parser::Statement::Import(import_path) = statement {
            let requested = Path::new(&import_path);
            if requested.is_absolute() {
                return Err(format!("{}: imports must use relative paths", canonical.display()));
            }
            let mut resolved = canonical.parent().unwrap_or(Path::new(".")).join(requested);
            if resolved.extension().is_none() {
                if let Some(c) = ["aayu", "ay", "aa"].iter().map(|ext| resolved.with_extension(ext)).find(|p| p.exists()) {
                    resolved = c;
                } else {
                    resolved.set_extension("aayu");
                }
            }
            if !resolved.exists() {
                let mut curr = canonical.parent();
                let mut found = None;
                while let Some(parent) = curr {
                    for ext in &["aayu", "ay", "aa"] {
                        let candidate = parent.join(requested).with_extension(ext);
                        if candidate.exists() {
                            found = Some(candidate);
                            break;
                        }
                        let std_candidate = parent.join("std").join(requested).with_extension(ext);
                        if std_candidate.exists() {
                            found = Some(std_candidate);
                            break;
                        }
                    }
                    if found.is_some() { break; }
                    curr = parent.parent();
                }
                if found.is_none() {
                    let home = std::env::var("USERPROFILE").or_else(|_| std::env::var("HOME")).map(PathBuf::from);
                    if let Ok(home_path) = home {
                        let aayu_home = home_path.join(".aayu");
                        for ext in &["aayu", "ay", "aa"] {
                            let cand1 = aayu_home.join("std").join(requested).with_extension(ext);
                            if cand1.exists() {
                                found = Some(cand1);
                                break;
                            }
                            let cand2 = aayu_home.join(requested).with_extension(ext);
                            if cand2.exists() {
                                found = Some(cand2);
                                break;
                            }
                            if let Ok(rel) = requested.strip_prefix("std") {
                                let cand3 = aayu_home.join("std").join(rel).with_extension(ext);
                                if cand3.exists() {
                                    found = Some(cand3);
                                    break;
                                }
                            }
                        }
                    }
                }
                if let Some(f) = found {
                    resolved = f;
                }
            }
            expanded.extend(expand_file(&resolved, visiting, loaded)?);
        } else {
            expanded.push(statement);
        }
    }
    visiting.remove(&canonical);
    Ok(expanded)
}

pub fn compile_file(path: &Path) -> Result<Vec<u8>, String> {
    let ast = expand_file(path, &mut HashSet::new(), &mut HashSet::new())?;
    compile_ast(&ast)
}

fn validate_supported(statements: &[parser::Statement]) -> Result<(), String> {
    use std::collections::{HashMap, HashSet};
    fn check_expr(expr: &parser::Expr, functions: &HashMap<String, usize>) -> Result<(), String> {
        use parser::Expr;
        match expr {
            Expr::Integer(value) if !(-(1i64 << 47)..=(1i64 << 47) - 1).contains(value) => Err(
                format!("integer literal {} is outside the signed 48-bit VM range", value)
            ),
            Expr::Call { callee, args } => {
                if callee == "len" {
                    if args.len() != 1 { return Err("len() expects exactly one argument".into()); }
                } else if callee != "print" {
                    let expected = functions.get(callee).ok_or_else(|| format!("unknown function '{}'", callee))?;
                    if args.len() != *expected {
                        return Err(format!("function '{}' expects {} arguments, got {}", callee, expected, args.len()));
                    }
                }
                for arg in args { check_expr(arg, functions)?; }
                Ok(())
            }
            Expr::Unary { expr, .. } => check_expr(expr, functions),
            Expr::Array(items) => { for item in items { check_expr(item, functions)?; } Ok(()) },
            Expr::Dict(entries) => { for (key, value) in entries { check_expr(key, functions)?; check_expr(value, functions)?; } Ok(()) },
            Expr::Index { object, key } => { check_expr(object, functions)?; check_expr(key, functions) },
            Expr::Binary { left, right, .. } => { check_expr(left, functions)?; check_expr(right, functions) },
            _ => Ok(()),
        }
    }

    fn collect_expr_vars(expr: &parser::Expr, vars: &mut HashSet<String>) {
        match expr {
            parser::Expr::Variable(name) => { vars.insert(name.clone()); }
            parser::Expr::Unary { expr, .. } => collect_expr_vars(expr, vars),
            parser::Expr::Array(items) => for item in items { collect_expr_vars(item, vars); },
            parser::Expr::Dict(entries) => for (key, value) in entries { collect_expr_vars(key, vars); collect_expr_vars(value, vars); },
            parser::Expr::Index { object, key } => { collect_expr_vars(object, vars); collect_expr_vars(key, vars); }
            parser::Expr::Binary { left, right, .. } => { collect_expr_vars(left, vars); collect_expr_vars(right, vars); }
            parser::Expr::Call { args, .. } => for arg in args { collect_expr_vars(arg, vars); },
            _ => {}
        }
    }
    fn collect_body_vars(body: &[parser::Statement], vars: &mut HashSet<String>) {
        use parser::Statement;
        for statement in body {
            match statement {
                Statement::Let { name, value } | Statement::Assignment { name, value } => {
                    vars.insert(name.clone()); collect_expr_vars(value, vars);
                }
                Statement::Print(value) | Statement::State { value, .. } |
                Statement::Return(Some(value)) | Statement::Expr(value) => collect_expr_vars(value, vars),
                Statement::While { cond, body } => { collect_expr_vars(cond, vars); collect_body_vars(body, vars); }
                Statement::If { cond, then_branch, else_branch } => {
                    collect_expr_vars(cond, vars); collect_body_vars(then_branch, vars); collect_body_vars(else_branch, vars);
                }
                Statement::Page { body, .. } | Statement::Widget { children: body, .. } => collect_body_vars(body, vars),
                _ => {}
            }
        }
    }

    let mut functions = HashMap::new();
    for statement in statements {
        if let parser::Statement::Action { name, args, .. } = statement {
            if functions.insert(name.clone(), args.len()).is_some() {
                return Err(format!("duplicate function declaration '{}'", name));
            }
            let mut seen = HashSet::new();
            if args.iter().any(|arg| !seen.insert(arg)) {
                return Err(format!("function '{}' has duplicate parameter names", name));
            }
            if args.len() > 256 { return Err(format!("function '{}' exceeds the 256-parameter limit", name)); }
        }
    }

    let mut global_vars = HashSet::new();
    for statement in statements {
        if let parser::Statement::Action { name, args, body } = statement {
            let mut vars: HashSet<String> = args.iter().cloned().collect();
            collect_body_vars(body, &mut vars);
            if vars.len() > 256 { return Err(format!("function '{}' requires {} local slots; maximum is 256", name, vars.len())); }
        } else {
            collect_body_vars(std::slice::from_ref(statement), &mut global_vars);
        }
    }
    if global_vars.len() > 256 { return Err(format!("program requires {} local slots; maximum is 256", global_vars.len())); }

    fn validate_body(statements: &[parser::Statement], functions: &HashMap<String, usize>, in_function: bool) -> Result<(), String> {
    for statement in statements {
        use parser::Statement;
        match statement {
            Statement::Action { body, .. } => {
                if in_function { return Err("nested action declarations are not supported".into()); }
                validate_body(body, functions, true)?;
            }
            Statement::Let { value, .. } | Statement::Assignment { value, .. } |
            Statement::Print(value) | Statement::State { value, .. } => check_expr(value, functions)?,
            Statement::While { cond, body } => { check_expr(cond, functions)?; validate_body(body, functions, in_function)?; },
            Statement::If { cond, then_branch, else_branch } => {
                check_expr(cond, functions)?; validate_body(then_branch, functions, in_function)?; validate_body(else_branch, functions, in_function)?;
            }
            Statement::Return(Some(value)) => {
                if !in_function { return Err("return is only valid inside an action".into()); }
                check_expr(value, functions)?;
            }
            Statement::Return(None) if !in_function => return Err("return is only valid inside an action".into()),
            Statement::Expr(value) => check_expr(value, functions)?,
            Statement::Page { body, .. } | Statement::Widget { children: body, .. } => validate_body(body, functions, in_function)?,
            _ => {}
        }
    }
    Ok(())
    }
    validate_body(statements, &functions, false)
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
    
    let bc = match compile_file(Path::new(input_file)) {
        Ok(bytecode) => bytecode,
        Err(error) => { eprintln!("[AAYU Compile Error] {}", error); std::process::exit(1); }
    };
    
    let mut file = fs::File::create(output_file).expect("Failed to create .ayc file");
    file.write_all(&bc).expect("Failed to write bytecode");
    let is_verbose = args.contains(&"--verbose".to_string()) || args.contains(&"-v".to_string());
    if is_verbose {
        println!("Compiled successfully to {}", output_file);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn compiles_variable_print_program_to_aayu_bytecode() {
        let bytecode = compile("let value = 7\nprint(value)\n").expect("valid core program should compile");
        assert!(bytecode.starts_with(b"AAYU"));
        assert!(bytecode.len() > 8);
    }

    #[test]
    fn rejects_invalid_source_instead_of_emitting_placeholder_values() {
        for source in ["print(@)", "print(\"unfinished)", "let value = \nprint(value)"] {
            assert!(compile(source).is_err(), "source should be rejected: {source:?}");
        }
    }

    #[test]
    fn compiles_user_functions_and_rejects_wrong_arity() {
        let source = "action add(a, b)\n return a + b\nend\nprint(add(2, 3))\n";
        assert!(compile(source).is_ok());
        let error = compile("action add(a, b)\n return a + b\nend\nprint(add(2))\n").unwrap_err();
        assert!(error.contains("expects 2 arguments"));
        assert!(compile("print(missing(1))\n").unwrap_err().contains("unknown function"));
        assert!(compile("action bad(a b)\n return a\nend\n").is_err());
        assert!(compile("return 1\n").unwrap_err().contains("only valid inside an action"));
    }

    #[test]
    fn rejects_integer_literals_outside_the_vm_range() {
        assert!(compile("let too_large = 140737488355328\n").is_err());
        assert!(compile("let minimum = -140737488355328\n").is_ok());
        assert!(compile("let too_large_for_parser = 999999999999999999999999999999\n").is_err());
        let too_large_float = format!("let too_large_float = {}.0\n", "9".repeat(400));
        assert!(compile(&too_large_float).is_err());
    }

    #[test]
    fn lexer_handles_multibyte_utf8_in_string_literals() {
        assert!(compile("print(\"नमस्ते AAYU\")\n").is_ok());
    }

    #[test]
    fn reports_import_cycles_with_the_module_path() {
        let root = env::temp_dir().join(format!("aayu_import_cycle_{}", std::process::id()));
        fs::create_dir_all(&root).unwrap();
        fs::write(root.join("main.aayu"), "import \"child\"\n").unwrap();
        fs::write(root.join("child.aayu"), "import \"main.aayu\"\n").unwrap();
        let error = compile_file(&root.join("main.aayu")).unwrap_err();
        assert!(error.contains("cyclic import detected"), "unexpected error: {error}");
        fs::remove_dir_all(root).unwrap();
    }

    #[test]
    fn reports_missing_imports_and_rejects_absolute_imports() {
        let root = env::temp_dir().join(format!("aayu_import_errors_{}", std::process::id()));
        fs::create_dir_all(&root).unwrap();
        let main = root.join("main.aayu");
        fs::write(&main, "import \"missing\"\n").unwrap();
        assert!(compile_file(&main).unwrap_err().contains("cannot resolve module"));
        fs::write(&main, "import \"C:/private.aayu\"\n").unwrap();
        assert!(compile_file(&main).unwrap_err().contains("imports must use relative paths"));
        fs::remove_dir_all(root).unwrap();
    }
}



