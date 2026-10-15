use std::fs;
use std::path::{Path, PathBuf};
use std::collections::{HashMap, HashSet};

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

pub fn compile_file(path: &Path) -> Result<Vec<u8>, String> {
    let ast = expand_file(path, &mut HashSet::new(), &mut HashSet::new())?;
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
    validate_supported(ast)?;
    let mut emitter = emitter::Emitter::new();
    let (bytecode, constants, strings, num_constants) = emitter.emit(ast);
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
            if resolved.extension().is_none() { resolved.set_extension("aayu"); }
            if !resolved.exists() {
                let mut curr = canonical.parent();
                let mut found = None;
                while let Some(parent) = curr {
                    let mut candidate = parent.join(requested);
                    if candidate.extension().is_none() { candidate.set_extension("aayu"); }
                    if candidate.exists() {
                        found = Some(candidate);
                        break;
                    }
                    let mut std_candidate = parent.join("std").join(requested);
                    if std_candidate.extension().is_none() { std_candidate.set_extension("aayu"); }
                    if std_candidate.exists() {
                        found = Some(std_candidate);
                        break;
                    }
                    curr = parent.parent();
                }
                if let Some(f) = found {
                    resolved = f;
                } else {
                    let mut global_dirs: Vec<PathBuf> = Vec::new();
                    if let Ok(home) = std::env::var("AAYU_HOME") {
                        global_dirs.push(PathBuf::from(home));
                    }
                    if let Ok(userprofile) = std::env::var("USERPROFILE") {
                        global_dirs.push(PathBuf::from(userprofile).join(".aayu"));
                    }
                    if let Ok(home) = std::env::var("HOME") {
                        global_dirs.push(PathBuf::from(home).join(".aayu"));
                    }
                    for gdir in &global_dirs {
                        let mut cand1 = gdir.join(requested);
                        if cand1.extension().is_none() { cand1.set_extension("aayu"); }
                        if cand1.exists() { resolved = cand1; break; }

                        let mut cand2 = gdir.join("std").join(requested);
                        if cand2.extension().is_none() { cand2.set_extension("aayu"); }
                        if cand2.exists() { resolved = cand2; break; }

                        if requested.starts_with("std") {
                            if let Ok(stripped) = requested.strip_prefix("std") {
                                let mut cand3 = gdir.join("std").join(stripped);
                                if cand3.extension().is_none() { cand3.set_extension("aayu"); }
                                if cand3.exists() { resolved = cand3; break; }
                            }
                        }
                    }
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

fn validate_supported(statements: &[parser::Statement]) -> Result<(), String> {
    fn check_expr(expr: &parser::Expr, functions: &HashMap<String, usize>) -> Result<(), String> {
        use parser::Expr;
        match expr {
            Expr::Integer(value) if !(-(1i64 << 47)..=(1i64 << 47) - 1).contains(value) => Err(
                format!("integer literal {} is outside the signed 48-bit VM range", value)
            ),
            Expr::Call { callee, args } => {
                if callee == "len" {
                    if args.len() != 1 { return Err("len() expects exactly one argument".into()); }
                } else if callee != "print" && callee != "respond" && callee != "hash_str" && callee != "type" && callee != "typeof" && callee != "platform" && callee != "arch" && callee != "env_get" && callee != "read_file" && callee != "write_file" && callee != "time_micros" && callee != "time_us" && callee != "time_ms" && callee != "file_mtime" && callee != "file_size" && callee != "sleep_ms" && callee != "append" && callee != "push" {
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
                Statement::SubscriptAssignment { object, key, value } => {
                    collect_expr_vars(object, vars);
                    collect_expr_vars(key, vars);
                    collect_expr_vars(value, vars);
                }
                Statement::Print(value) | Statement::State { value, .. } |
                Statement::Return(Some(value)) | Statement::Expr(value) |
                Statement::Respond(value) => collect_expr_vars(value, vars),
                Statement::While { cond, body } => { collect_expr_vars(cond, vars); collect_body_vars(body, vars); }
                Statement::If { cond, then_branch, else_branch } => {
                    collect_expr_vars(cond, vars); collect_body_vars(then_branch, vars); collect_body_vars(else_branch, vars);
                }
                Statement::Page { body, .. } | Statement::Widget { children: body, .. } => collect_body_vars(body, vars),
                Statement::Route { handlers, .. } => {
                    for (_, h_body) in handlers {
                        collect_body_vars(h_body, vars);
                    }
                }
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
                Statement::SubscriptAssignment { object, key, value } => {
                    check_expr(object, functions)?;
                    check_expr(key, functions)?;
                    check_expr(value, functions)?;
                }
                Statement::Respond(value) => check_expr(value, functions)?,
                Statement::Route { handlers, .. } => {
                    for (_, h_body) in handlers {
                        validate_body(h_body, functions, in_function)?;
                    }
                }
                Statement::Model { .. } => {}
                Statement::Page { body, .. } | Statement::Widget { children: body, .. } => validate_body(body, functions, in_function)?,
                _ => {}
            }
        }
        Ok(())
    }
    validate_body(statements, &functions, false)
}
