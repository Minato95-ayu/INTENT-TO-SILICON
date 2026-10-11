use std::collections::HashMap;
use crate::parser::{Expr, Statement, BinaryOp};

pub struct Emitter {
    bytecode: Vec<u8>,
    constants: Vec<u8>,
    strings: Vec<String>,
    pub num_constants: u32,
    var_map: HashMap<String, usize>,
    next_slot: usize,
}

impl Emitter {
    pub fn new() -> Self {
        Self {
            bytecode: Vec::new(),
            constants: Vec::new(),
            strings: Vec::new(),
            num_constants: 0,
            var_map: HashMap::new(),
            next_slot: 0,
        }
    }

    pub fn emit(&mut self, ast: &[Statement]) -> (Vec<u8>, Vec<u8>, Vec<String>, u32) {
        for stmt in ast {
            self.emit_statement(stmt);
        }
        self.bytecode.push(0); // HALT opcode
        (self.bytecode.clone(), self.constants.clone(), self.strings.clone(), self.num_constants)
    }

    fn add_constant_int(&mut self, n: i64) -> usize {
        let const_idx = self.num_constants as usize;
        self.constants.push(1); // Int tag
        self.constants.extend_from_slice(&n.to_le_bytes());
        self.num_constants += 1;
        const_idx
    }

    fn add_constant_float(&mut self, f: f64) -> usize {
        let const_idx = self.num_constants as usize;
        self.constants.push(3); // Float tag
        self.constants.extend_from_slice(&f.to_le_bytes());
        self.num_constants += 1;
        const_idx
    }

    fn add_constant_str(&mut self, s: String) -> (usize, usize) {
        let str_idx = self.strings.len();
        self.strings.push(s.clone());
        let const_idx = self.num_constants as usize;
        self.constants.push(2); // String tag
        let bytes = s.as_bytes();
        let len = bytes.len() as u32;
        self.constants.extend_from_slice(&len.to_le_bytes());
        self.constants.extend_from_slice(bytes);
        self.num_constants += 1;
        (const_idx, str_idx)
    }

    fn add_constant_null(&mut self) -> usize {
        let const_idx = self.num_constants as usize;
        self.constants.push(0); // Null tag
        self.num_constants += 1;
        const_idx
    }

    fn get_var_slot(&mut self, name: &str) -> usize {
        if let Some(&slot) = self.var_map.get(name) {
            slot
        } else {
            let slot = self.next_slot;
            self.next_slot += 1;
            self.var_map.insert(name.to_string(), slot);
            slot
        }
    }

    fn emit_statement(&mut self, stmt: &Statement) {
        match stmt {
            Statement::Let { name, value } | Statement::Assignment { name, value } => {
                self.emit_expression(value);
                let slot = self.get_var_slot(name);
                self.bytecode.push(6); // STORE_VAR
                self.bytecode.push((slot % 256) as u8);
            }
            Statement::State { name, value } => {
                self.emit_expression(value);
                let (const_idx, _) = self.add_constant_str(name.clone());
                self.bytecode.push(48); // STORE_STATE
                self.bytecode.push((const_idx >> 8) as u8);
                self.bytecode.push((const_idx & 0xFF) as u8);
            }
            Statement::Print(expr) => {
                self.emit_expression(expr);
                self.bytecode.push(81); // PRINT
            }
            Statement::While { cond, body } => {
                let loop_start = self.bytecode.len();
                self.emit_expression(cond);
                self.bytecode.push(33); // OP_JMP_IF_FALSE (0x21)
                let jmp_false_idx = self.bytecode.len();
                self.bytecode.push(0);
                self.bytecode.push(0);

                for s in body {
                    self.emit_statement(s);
                }

                self.bytecode.push(32); // OP_JMP (0x20)
                self.bytecode.push((loop_start >> 8) as u8);
                self.bytecode.push((loop_start & 0xFF) as u8);

                let exit_target = self.bytecode.len();
                self.bytecode[jmp_false_idx] = (exit_target >> 8) as u8;
                self.bytecode[jmp_false_idx + 1] = (exit_target & 0xFF) as u8;
            }
            Statement::If { cond, then_branch, else_branch } => {
                self.emit_expression(cond);
                self.bytecode.push(33); // OP_JMP_IF_FALSE (0x21)
                let jmp_false_idx = self.bytecode.len();
                self.bytecode.push(0);
                self.bytecode.push(0);

                for s in then_branch {
                    self.emit_statement(s);
                }

                if !else_branch.is_empty() {
                    self.bytecode.push(32); // OP_JMP (0x20)
                    let jmp_end_idx = self.bytecode.len();
                    self.bytecode.push(0);
                    self.bytecode.push(0);

                    let else_start = self.bytecode.len();
                    self.bytecode[jmp_false_idx] = (else_start >> 8) as u8;
                    self.bytecode[jmp_false_idx + 1] = (else_start & 0xFF) as u8;

                    for s in else_branch {
                        self.emit_statement(s);
                    }

                    let end_target = self.bytecode.len();
                    self.bytecode[jmp_end_idx] = (end_target >> 8) as u8;
                    self.bytecode[jmp_end_idx + 1] = (end_target & 0xFF) as u8;
                } else {
                    let exit_target = self.bytecode.len();
                    self.bytecode[jmp_false_idx] = (exit_target >> 8) as u8;
                    self.bytecode[jmp_false_idx + 1] = (exit_target & 0xFF) as u8;
                }
            }
            Statement::Action { body, .. } => {
                for s in body {
                    self.emit_statement(s);
                }
            }
            Statement::Return(opt_expr) => {
                if let Some(expr) = opt_expr {
                    self.emit_expression(expr);
                } else {
                    let null_idx = self.add_constant_null();
                    self.bytecode.push(1); // PUSH_CONST
                    self.bytecode.push((null_idx >> 8) as u8);
                    self.bytecode.push((null_idx & 0xFF) as u8);
                }
                self.bytecode.push(35); // RET
            }
            Statement::Expr(expr) => {
                self.emit_expression(expr);
                self.bytecode.push(2); // POP
            }
            Statement::App(_) => {}
            Statement::Page { name, body } => {
                let html = Self::generate_html(body);
                let title = match name.as_str() {
                    "Dashboard" => "AAYU NeuroLedger | Autonomous AI-Verified Blockchain & Smart Contract Engine",
                    "Portfolio" => "Ayush Kaushik | Systems Builder & Creator of AAYU",
                    _ => "AAYU Native Application"
                };
                let full_html = format!("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><title>{}</title><link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css\"><style>* {{ box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }} html, body {{ width: 100%; height: 100%; }} a {{ text-decoration: none; color: inherit; }} div[onclick] {{ transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease; cursor: pointer; }} div[onclick]:hover {{ transform: translateY(-3px); border-color: #6366f1 !important; box-shadow: 0 10px 25px -5px rgba(99, 102, 241, 0.25); }}</style></head><body style=\"background-color:#0b0f19;color:white;overflow-x:hidden;\">{}{}</body></html>", title, html, MODAL_HTML_AND_SCRIPT);
                let (_, str_idx) = self.add_constant_str(full_html);
                self.bytecode.push(200); // OP_RENDER_PAGE
                self.bytecode.push((str_idx >> 8) as u8);
                self.bytecode.push((str_idx & 0xFF) as u8);
            }
            Statement::Widget { .. } => {}
            Statement::Run(_) => {}
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
                    "Input" => "input",
                    _ => "div"
                };
                let mut css = style.clone();
                let onclick_attr = String::new();
                let href_attr = String::new();
                let id_attr = String::new();
                let placeholder_attr = String::new();
                let mut value_attr = String::new();

                if kind == "Column" { css.push_str("display:flex;flex-direction:column;"); }
                if kind == "Row" { css.push_str("display:flex;flex-direction:row;"); }
                if kind == "Grid" { css.push_str("display:grid;"); }
                if kind == "Container" || kind == "Card" { css.push_str("display:flex;"); }
                if !onclick_attr.is_empty() { css.push_str("cursor:pointer;"); }
                if kind == "Button" && href_attr.is_empty() { css.push_str("cursor:pointer;border:none;"); }

                let class_attr = if kind == "Icon" { format!(" class=\"fa fa-{}\"", text) } else { "".to_string() };

                if tag == "textarea" || (kind == "Input" && id_attr.contains("playgroundCode")) {
                    let inner_val = if !value_attr.is_empty() {
                        let stripped = value_attr.trim_start_matches(" value=\"").trim_end_matches('"');
                        stripped.replace("\\n", "\n")
                    } else {
                        text.clone()
                    };
                    html.push_str(&format!("<textarea style=\"{}\"{}{}{}>{}</textarea>", css.replace('"', ""), id_attr, placeholder_attr, onclick_attr, inner_val));
                } else if kind == "Input" {
                    if value_attr.is_empty() && !text.is_empty() {
                        value_attr = format!(" value=\"{}\"", text);
                    }
                    html.push_str(&format!("<input style=\"{}\"{}{}{}{}{}>", css.replace('"', ""), id_attr, placeholder_attr, value_attr, class_attr, onclick_attr));
                } else {
                    html.push_str(&format!("<{} style=\"{}\"{}{}{}{}>", tag, css.replace('"', ""), id_attr, href_attr, class_attr, onclick_attr));
                    if !text.is_empty() && kind != "Icon" {
                        html.push_str(text);
                    }
                    html.push_str(&Self::generate_html(children));
                    html.push_str(&format!("</{}>", tag));
                }
            }
        }
        html
    }

    fn emit_expression(&mut self, expr: &Expr) {
        match expr {
            Expr::Integer(n) => {
                let const_idx = self.add_constant_int(*n);
                self.bytecode.push(1); // PUSH_CONST
                self.bytecode.push((const_idx >> 8) as u8);
                self.bytecode.push((const_idx & 0xFF) as u8);
            }
            Expr::Float(f) => {
                let const_idx = self.add_constant_float(*f);
                self.bytecode.push(1); // PUSH_CONST
                self.bytecode.push((const_idx >> 8) as u8);
                self.bytecode.push((const_idx & 0xFF) as u8);
            }
            Expr::StringLiteral(s) => {
                let (const_idx, _) = self.add_constant_str(s.clone());
                self.bytecode.push(1); // PUSH_CONST
                self.bytecode.push((const_idx >> 8) as u8);
                self.bytecode.push((const_idx & 0xFF) as u8);
            }
            Expr::Variable(name) => {
                let slot = self.get_var_slot(name);
                self.bytecode.push(5); // LOAD_VAR
                self.bytecode.push((slot % 256) as u8);
            }
            Expr::Binary { left, op, right } => {
                self.emit_expression(left);
                self.emit_expression(right);
                match op {
                    BinaryOp::Add => self.bytecode.push(16),
                    BinaryOp::Sub => self.bytecode.push(17),
                    BinaryOp::Mul => self.bytecode.push(18),
                    BinaryOp::Div => self.bytecode.push(19),
                    BinaryOp::EqEq => self.bytecode.push(38),
                    BinaryOp::NotEq => self.bytecode.push(39),
                    BinaryOp::Lt => self.bytecode.push(41),
                    BinaryOp::Gt => self.bytecode.push(42),
                    BinaryOp::Lte => self.bytecode.push(43),
                    BinaryOp::Gte => self.bytecode.push(44),
                }
            }
            Expr::Call { callee, args } => {
                if callee == "print" {
                    for arg in args {
                        self.emit_expression(arg);
                        self.bytecode.push(81); // PRINT
                    }
                    let null_idx = self.add_constant_null();
                    self.bytecode.push(1);
                    self.bytecode.push((null_idx >> 8) as u8);
                    self.bytecode.push((null_idx & 0xFF) as u8);
                } else {
                    let (name_idx, _) = self.add_constant_str(callee.clone());
                    self.bytecode.push(1); // PUSH_CONST (func name)
                    self.bytecode.push((name_idx >> 8) as u8);
                    self.bytecode.push((name_idx & 0xFF) as u8);
                    for arg in args {
                        self.emit_expression(arg);
                    }
                    self.bytecode.push(34); // OP_CALL
                    self.bytecode.push((args.len() >> 8) as u8);
                    self.bytecode.push((args.len() & 0xFF) as u8);
                }
            }
        }
    }
}

pub const MODAL_HTML_AND_SCRIPT: &str = r##"
<div id="projectModal" style="display:none;position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,0.85);backdrop-filter:blur(8px);z-index:9999;align-items:center;justify-content:center;padding:20px;" onclick="if(event.target===this)closeProjectModal()">
  <div style="background:#111827;border:1px solid #374151;border-radius:16px;max-width:860px;width:100%;max-height:88vh;overflow-y:auto;box-shadow:0 25px 50px -12px rgba(0,0,0,0.7);padding:32px;display:flex;flex-direction:column;gap:18px;position:relative;">
    <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:16px;">
      <div>
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;flex-wrap:wrap;">
          <span id="modalBadge" style="font-size:11px;font-weight:bold;padding:4px 10px;border-radius:6px;background:#064e3b;color:#10b981;">STATUS</span>
          <span id="modalStack" style="font-size:13px;color:#818cf8;font-weight:600;">Stack</span>
        </div>
        <h2 id="modalTitle" style="font-size:26px;font-weight:800;color:#ffffff;line-height:1.2;">Project Title</h2>
      </div>
      <button onclick="closeProjectModal()" style="background:#1f2937;border:1px solid #374151;color:#9ca3af;font-size:18px;width:38px;height:38px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;">✕</button>
    </div>
    
    <div style="display:flex;flex-direction:column;gap:6px;">
      <span style="font-size:12px;font-weight:bold;color:#9ca3af;letter-spacing:1px;text-transform:uppercase;">Overview</span>
      <p id="modalDesc" style="font-size:15px;color:#d1d5db;line-height:1.7;margin:0;"></p>
    </div>

    <div style="display:flex;flex-direction:column;gap:6px;">
      <span style="font-size:12px;font-weight:bold;color:#22d3ee;letter-spacing:1px;text-transform:uppercase;">Technical Architecture & Pipeline</span>
      <div id="modalArch" style="font-size:14px;color:#e5e7eb;line-height:1.7;background:#0d1220;border:1px solid #1f2937;padding:16px;border-radius:8px;white-space:pre-wrap;font-family:system-ui,sans-serif;"></div>
    </div>

    <div style="display:flex;flex-direction:column;gap:6px;">
      <span style="font-size:12px;font-weight:bold;color:#a855f7;letter-spacing:1px;text-transform:uppercase;">Verified Source Code (.aayu)</span>
    </div>
  </div>
</div>
"##;
