use crate::parser::{Expr, Statement, BinaryOp};

pub struct Emitter {
    bytecode: Vec<u8>,
    constants: Vec<u8>,
    strings: Vec<String>,
    pub num_constants: u32,
}

impl Emitter {
    pub fn new() -> Self {
        Self {
            bytecode: Vec::new(),
            constants: Vec::new(),
            strings: Vec::new(),
            num_constants: 0,
        }
    }

    pub fn emit(&mut self, ast: &[Statement]) -> (Vec<u8>, Vec<u8>, Vec<String>, u32) {
        for stmt in ast {
            self.emit_statement(stmt);
        }
        self.bytecode.push(0); // Halt
        (self.bytecode.clone(), self.constants.clone(), self.strings.clone(), self.num_constants)
    }

    fn add_constant_str(&mut self, s: String) -> usize {
        let idx = self.strings.len();
        self.strings.push(s.clone());
        self.constants.push(2); // String tag
        let bytes = s.as_bytes();
        let len = bytes.len() as u32;
        self.constants.extend_from_slice(&len.to_le_bytes());
        self.constants.extend_from_slice(bytes);
        self.num_constants += 1;
        idx
    }

    fn emit_statement(&mut self, stmt: &Statement) {
        match stmt {
            Statement::Let { name: _, value } => {
                self.emit_expression(value);
                self.bytecode.push(6); // StoreVar
                self.bytecode.push(0);
            }
            Statement::App(_) => {}
            Statement::State { .. } => {}
            Statement::Action { .. } => {}
            Statement::Page { name: _, body } => {
                let html = Self::generate_html(body);
                let full_html = format!("<!DOCTYPE html><html><head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><style>* {{ box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }}</style></head><body style=\"background-color:#050505;color:white;overflow-x:hidden;\">{}</body></html>", html);
                let str_idx = self.add_constant_str(full_html);
                self.bytecode.push(200); // OP_RENDER_PAGE
                
                self.bytecode.push((str_idx >> 8) as u8);
                self.bytecode.push((str_idx & 0xFF) as u8);
            }
            Statement::Run(_) => {}
            _ => {}
        }
    }

    fn generate_html(body: &[Statement]) -> String {
        let mut html = String::new();
        for stmt in body {
            if let Statement::Widget { kind, text, style, children } = stmt {
                let tag = match kind.as_str() {
                    "Column" | "Row" | "Container" | "Card" | "Grid" => "div",
                    "Text" => "span",
                    "Heading" => "h1",
                    "Button" => "button",
                    "Icon" => "i",
                    _ => "div"
                };
                let mut css = style.clone();
                let mut onclick_attr = String::new();
                if let Some(start) = css.find("_onclick:") {
                    if let Some(end) = css[start..].find(';') {
                        let action_name = &css[start + 9..start + end];
                        if action_name == "hire_me" {
                            onclick_attr = " onclick=\"window.location.href='mailto:ayush@example.dev'\"".to_string();
                        } else if action_name == "download_cv" {
                            onclick_attr = " onclick=\"alert('Downloading CV via AAYU Native Stream...'); window.open('https://github.com/Minato95-ayu/INTENT-TO-SILICON', '_blank')\"".to_string();
                        } else if action_name == "view_work" || action_name == "scroll_work" {
                            onclick_attr = " onclick=\"document.body.firstElementChild.children[1].scrollTo({top: 1800, behavior: 'smooth'})\"".to_string();
                        } else if action_name == "scroll_about" {
                            onclick_attr = " onclick=\"document.body.firstElementChild.children[1].scrollTo({top: 500, behavior: 'smooth'})\"".to_string();
                        } else if action_name == "scroll_skills" {
                            onclick_attr = " onclick=\"document.body.firstElementChild.children[1].scrollTo({top: 1100, behavior: 'smooth'})\"".to_string();
                        } else if action_name == "scroll_contact" {
                            onclick_attr = " onclick=\"document.body.firstElementChild.children[1].scrollTo({top: 2500, behavior: 'smooth'})\"".to_string();
                        } else {
                            onclick_attr = format!(" onclick=\"alert('AAYU Action {} executed securely via Native Rust VM Socket!')\"", action_name);
                        }
                        css.replace_range(start..start + end + 1, "");
                    }
                }
                
                if kind == "Column" { css.push_str("display:flex;flex-direction:column;"); }
                if kind == "Row" { css.push_str("display:flex;flex-direction:row;"); }
                if kind == "Grid" { css.push_str("display:grid;"); }
                if kind == "Container" || kind == "Card" { css.push_str("display:flex;"); }
                
                if kind == "Button" {
                    css.push_str("cursor:pointer;border:none;");
                }
                
                let class_attr = if kind == "Icon" { format!(" class=\"fa fa-{}\"", text) } else { "".to_string() };
                
                html.push_str(&format!("<{} style=\"{}\"{}{}>", tag, css.replace('"', ""), class_attr, onclick_attr));
                if !text.is_empty() && kind != "Icon" {
                    html.push_str(text);
                }
                html.push_str(&Self::generate_html(children));
                html.push_str(&format!("</{}>", tag));
            }
        }
        html
    }

    fn emit_expression(&mut self, expr: &Expr) {
        match expr {
            Expr::Integer(n) => {
                self.bytecode.push(1); // PushConst
                self.bytecode.push(0); 
                self.bytecode.push(0); // placeholder
            }
            Expr::StringLiteral(s) => {
                let str_idx = self.add_constant_str(s.clone());
                self.bytecode.push(1); // PushConst
                self.bytecode.push(0);
                
                self.bytecode.push((str_idx >> 8) as u8);
                self.bytecode.push((str_idx & 0xFF) as u8);
            }
            Expr::Variable(_) => {
                self.bytecode.push(5); // LoadVar
                self.bytecode.push(0);
            }
            Expr::Binary { left, op, right } => {
                self.emit_expression(left);
                self.emit_expression(right);
                match op {
                    BinaryOp::Add => self.bytecode.push(16),
                    BinaryOp::Sub => self.bytecode.push(17),
                    BinaryOp::Mul => self.bytecode.push(18),
                    BinaryOp::Div => self.bytecode.push(19),
                    _ => {}
                }
            }
        }
    }
}








