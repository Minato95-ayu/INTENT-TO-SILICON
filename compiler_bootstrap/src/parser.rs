use crate::lexer::Token;

#[derive(Debug, Clone, PartialEq)]
pub enum BinaryOp {
    Add,
    Sub,
    Mul,
    Div,
    Mod,
    Lt,
    Gt,
    EqEq,
    NotEq,
    Lte,
    Gte,
}

#[derive(Debug, Clone, Copy)]
pub enum UnaryOp { Negate }

#[derive(Debug, Clone)]
pub enum Expr {
    Integer(i64),
    Float(f64),
    StringLiteral(String),
    Variable(String),
    Binary {
        left: Box<Expr>,
        op: BinaryOp,
        right: Box<Expr>,
    },
    Unary { op: UnaryOp, expr: Box<Expr> },
    Call {
        callee: String,
        args: Vec<Expr>,
    },
    Array(Vec<Expr>),
    Dict(Vec<(Expr, Expr)>),
    Index { object: Box<Expr>, key: Box<Expr> },
}

#[derive(Debug, Clone)]
pub enum Statement {
    Import(String),
    Let { name: String, value: Expr },
    Assignment { name: String, value: Expr },
    While { cond: Expr, body: Vec<Statement> },
    If { cond: Expr, then_branch: Vec<Statement>, else_branch: Vec<Statement> },
    Print(Expr),
    App(String),
    State { name: String, value: Expr },
    Action { name: String, args: Vec<String>, body: Vec<Statement> },
    Widget { kind: String, text: String, style: String, children: Vec<Statement> },
    Page { name: String, body: Vec<Statement> },
    Return(Option<Expr>),
    Run(String),
    Expr(Expr),
}

pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
    errors: Vec<String>,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self { tokens, pos: 0, errors: Vec::new() }
    }

    pub fn parse(&mut self) -> Vec<Statement> {
        let mut stmts = Vec::new();
        while self.current() != &Token::Eof {
            if let Some(stmt) = self.parse_statement() {
                stmts.push(stmt);
            }
        }
        stmts
    }

    pub fn errors(&self) -> &[String] { &self.errors }

    fn parse_block(&mut self) -> Vec<Statement> {
        let mut stmts = Vec::new();
        while self.current() != &Token::Eof && self.current() != &Token::End && self.current() != &Token::Else && self.current() != &Token::Elif {
            if let Some(stmt) = self.parse_statement() {
                stmts.push(stmt);
            }
        }
        stmts
    }

    fn parse_attributes(&mut self) -> String {
        let mut style = String::new();
        while let Token::Identifier(k) = self.current() {
            let key = k.clone();
            self.pos += 1;
            if self.current() == &Token::Equal {
                self.pos += 1;
                let val = if let Token::StringLiteral(v) = self.current() {
                    let s = v.clone(); self.pos += 1; Some(s)
                } else if let Token::Identifier(v) = self.current() {
                    let s = v.clone(); self.pos += 1; Some(s)
                } else { None };

                if let Some(val) = val {
                    if key == "onClick" {
                        style.push_str(&format!("_onclick:{};", val));
                    } else {
                        let mut kebab = String::new();
                        for c in key.chars() {
                            if c.is_uppercase() {
                                kebab.push('-');
                                kebab.push(c.to_ascii_lowercase());
                            } else {
                                kebab.push(c);
                            }
                        }
                        style.push_str(&format!("{}:{};", kebab, val));
                    }
                } else { break; }
            } else {
                self.pos -= 1;
                break;
            }
        }
        style
    }

    fn parse_statement(&mut self) -> Option<Statement> {
        match self.current() {
            Token::Import => {
                self.pos += 1;
                if let Token::StringLiteral(path) = self.current() {
                    let path = path.clone();
                    self.pos += 1;
                    return Some(Statement::Import(path));
                }
                self.errors.push("import expects a quoted relative file path".into());
            }
            Token::App => {
                self.pos += 1;
                if let Token::Identifier(name) = self.current() {
                    let app_name = name.clone();
                    self.pos += 1;
                    return Some(Statement::App(app_name));
                }
            }
            Token::State => {
                self.pos += 1;
                if let Token::Identifier(name) = self.current() {
                    let var_name = name.clone();
                    self.pos += 1;
                    if self.current() == &Token::Equal {
                        self.pos += 1;
                        let expr = self.parse_expression();
                        return Some(Statement::State { name: var_name, value: expr });
                    }
                }
            }
            Token::Let => {
                self.pos += 1;
                if let Token::Identifier(name) = self.current() {
                    let var_name = name.clone();
                    self.pos += 1;
                    if self.current() == &Token::Equal {
                        self.pos += 1;
                        let expr = self.parse_expression();
                        return Some(Statement::Let { name: var_name, value: expr });
                    }
                }
            }
            Token::While => {
                self.pos += 1;
                let cond = self.parse_expression();
                let body = self.parse_block();
                if self.current() == &Token::End {
                    self.pos += 1;
                } else {
                    self.errors.push("unterminated while block: expected 'end'".to_string());
                }
                return Some(Statement::While { cond, body });
            }
            Token::If | Token::Elif => {
                self.pos += 1;
                let cond = self.parse_expression();
                let mut then_branch = Vec::new();
                let mut else_branch = Vec::new();
                while self.current() != &Token::Eof && self.current() != &Token::End && self.current() != &Token::Else && self.current() != &Token::Elif {
                    if let Some(stmt) = self.parse_statement() {
                        then_branch.push(stmt);
                    }
                }
                if self.current() == &Token::Elif {
                    if let Some(stmt) = self.parse_statement() {
                        else_branch.push(stmt);
                    }
                } else if self.current() == &Token::Else {
                    self.pos += 1;
                    while self.current() != &Token::Eof && self.current() != &Token::End {
                        if let Some(stmt) = self.parse_statement() {
                            else_branch.push(stmt);
                        }
                    }
                    if self.current() == &Token::End {
                        self.pos += 1;
                    } else {
                        self.errors.push("unterminated if block: expected 'end'".to_string());
                    }
                } else if self.current() == &Token::End {
                    self.pos += 1;
                } else {
                    self.errors.push("unterminated if block: expected 'end'".to_string());
                }
                return Some(Statement::If { cond, then_branch, else_branch });
            }
            Token::Global => {
                self.pos += 1;
                if let Token::Identifier(name) = self.current() {
                    let var_name = name.clone();
                    self.pos += 1;
                    if self.current() == &Token::Equal {
                        self.pos += 1;
                        let value = self.parse_expression();
                        return Some(Statement::Let { name: var_name, value });
                    }
                }
                self.errors.push("expected 'name = value' after global".to_string());
                return None;
            }
            Token::Print => {
                self.pos += 1;
                let has_paren = self.current() == &Token::LeftParen;
                if has_paren { self.pos += 1; }
                let mut expr = if has_paren && self.current() == &Token::RightParen {
                    Expr::StringLiteral("".to_string())
                } else {
                    self.parse_expression()
                };
                while self.current() == &Token::Comma {
                    self.pos += 1;
                    let next_expr = self.parse_expression();
                    let space = Expr::StringLiteral(" ".to_string());
                    let with_space = Expr::Binary {
                        left: Box::new(expr),
                        op: BinaryOp::Add,
                        right: Box::new(space),
                    };
                    expr = Expr::Binary {
                        left: Box::new(with_space),
                        op: BinaryOp::Add,
                        right: Box::new(next_expr),
                    };
                }
                if has_paren && self.current() == &Token::RightParen { self.pos += 1; }
                return Some(Statement::Print(expr));
            }
            Token::Action => {
                self.pos += 1;
                if let Token::Identifier(name) = self.current() {
                    let act_name = name.clone();
                    self.pos += 1;
                    let mut args = Vec::new();
                    if self.current() == &Token::LeftParen {
                        self.pos += 1;
                        while self.current() != &Token::RightParen && self.current() != &Token::Eof {
                            match self.current() {
                                Token::Identifier(arg) => { args.push(arg.clone()); self.pos += 1; }
                                token => {
                                    self.errors.push(format!("expected parameter name, found {:?}", token));
                                    let before = self.pos;
                                    self.synchronize_delimited();
                                    if self.current() == &Token::Comma { self.pos += 1; }
                                    else if self.current() == &Token::Newline { self.pos += 1; }
                                    else if self.pos == before && !matches!(self.current(), Token::RightParen | Token::Eof) { self.pos += 1; }
                                    continue;
                                }
                            }
                            if self.current() == &Token::Comma { self.pos += 1; }
                            else if self.current() != &Token::RightParen {
                                self.errors.push("expected ',' or ')' after action parameter".into());
                                self.synchronize_delimited();
                                if self.current() == &Token::Comma { self.pos += 1; }
                            }
                        }
                        if self.current() == &Token::RightParen {
                            self.pos += 1;
                        } else {
                            self.errors.push(format!("unterminated parameter list for action '{}'", act_name));
                        }
                    }
                    let body = self.parse_block();
                    if self.current() == &Token::End {
                        self.pos += 1;
                    } else {
                        self.errors.push(format!("unterminated action '{}': expected 'end'", act_name));
                    }
                    return Some(Statement::Action { name: act_name, args, body });
                }
            }
            Token::Return => {
                self.pos += 1;
                if self.current() != &Token::Newline && self.current() != &Token::End && self.current() != &Token::Eof {
                    let expr = self.parse_expression();
                    return Some(Statement::Return(Some(expr)));
                } else {
                    return Some(Statement::Return(None));
                }
            }
            Token::Identifier(name) => {
                let var_name = name.clone();
                self.pos += 1;
                if self.current() == &Token::Equal {
                    self.pos += 1;
                    let expr = self.parse_expression();
                    return Some(Statement::Assignment { name: var_name, value: expr });
                } else if self.current() == &Token::LeftParen {
                    self.pos += 1;
                    let mut args = Vec::new();
                    while self.current() != &Token::RightParen && self.current() != &Token::Eof {
                        args.push(self.parse_expression());
                        if self.current() == &Token::Comma {
                            self.pos += 1;
                        }
                    }
                    if self.current() == &Token::RightParen {
                        self.pos += 1;
                    }
                    if var_name == "print" {
                        if !args.is_empty() {
                            return Some(Statement::Print(args.remove(0)));
                        } else {
                            return Some(Statement::Print(Expr::StringLiteral(String::new())));
                        }
                    }
                    return Some(Statement::Expr(Expr::Call { callee: var_name, args }));
                } else {
                    self.errors.push(format!("unexpected identifier '{}' at statement position", var_name));
                }
            }
            Token::Run => {
                self.pos += 1;
                if let Token::Identifier(name) = self.current() {
                    let run_name = name.clone();
                    self.pos += 1;
                    return Some(Statement::Run(run_name));
                }
            }
            Token::Page => {
                self.pos += 1;
                if let Token::Identifier(name) = self.current() {
                    let page_name = name.clone();
                    self.pos += 1;
                    let body = self.parse_block();
                    if self.current() == &Token::End { self.pos += 1; }
                    else { self.errors.push(format!("unterminated page '{}': expected 'end'", page_name)); }
                    return Some(Statement::Page { name: page_name, body });
                }
            }
            Token::Column | Token::Row | Token::Grid | Token::Container | Token::Card |
            Token::Heading | Token::Text | Token::Button | Token::Input => {
                let kind = format!("{:?}", self.current());
                self.pos += 1;
                let text = if self.current() == &Token::LeftParen {
                    self.pos += 1;
                    let s = if let Token::StringLiteral(ref t) = self.current() {
                        t.clone()
                    } else { String::new() };
                    while self.current() != &Token::RightParen && self.current() != &Token::Eof { self.pos += 1; }
                    if self.current() == &Token::RightParen { self.pos += 1; }
                    s
                } else { String::new() };
                let style = self.parse_attributes();
                let children = self.parse_block();
                if self.current() == &Token::End { self.pos += 1; }
                else { self.errors.push(format!("unterminated {} widget: expected 'end'", kind)); }
                return Some(Statement::Widget { kind, text, style, children });
            }
            Token::Newline => { self.pos += 1; return None; }
            token => {
                self.errors.push(format!("unexpected token {:?}", token));
                self.pos += 1;
                return None;
            }
        }
        None
    }

    pub fn parse_expression(&mut self) -> Expr {
        self.parse_comparison()
    }

    fn parse_comparison(&mut self) -> Expr {
        let mut left = self.parse_additive();
        while matches!(self.current(), Token::DoubleEqual | Token::NotEqual | Token::LessThan | Token::GreaterThan | Token::LessEqual | Token::GreaterEqual) {
            let op = match self.current() {
                Token::DoubleEqual => BinaryOp::EqEq,
                Token::NotEqual => BinaryOp::NotEq,
                Token::LessThan => BinaryOp::Lt,
                Token::GreaterThan => BinaryOp::Gt,
                Token::LessEqual => BinaryOp::Lte,
                Token::GreaterEqual => BinaryOp::Gte,
                _ => unreachable!(),
            };
            self.pos += 1;
            let right = self.parse_additive();
            left = Expr::Binary { left: Box::new(left), op, right: Box::new(right) };
        }
        left
    }

    fn parse_additive(&mut self) -> Expr {
        let mut left = self.parse_multiplicative();
        while matches!(self.current(), Token::Plus | Token::Minus) {
            let op = match self.current() {
                Token::Plus => BinaryOp::Add,
                Token::Minus => BinaryOp::Sub,
                _ => unreachable!(),
            };
            self.pos += 1;
            let right = self.parse_multiplicative();
            left = Expr::Binary { left: Box::new(left), op, right: Box::new(right) };
        }
        left
    }

    fn parse_multiplicative(&mut self) -> Expr {
        let mut left = self.parse_unary();
        while matches!(self.current(), Token::Star | Token::Slash | Token::Percent) {
            let op = match self.current() {
                Token::Star => BinaryOp::Mul,
                Token::Slash => BinaryOp::Div,
                Token::Percent => BinaryOp::Mod,
                _ => unreachable!(),
            };
            self.pos += 1;
            let right = self.parse_unary();
            left = Expr::Binary { left: Box::new(left), op, right: Box::new(right) };
        }
        left
    }

    fn parse_unary(&mut self) -> Expr {
        if self.current() == &Token::Minus {
            self.pos += 1;
            return match self.current() {
                Token::Integer(n) => { let value = -*n; self.pos += 1; Expr::Integer(value) }
                Token::Float(n) => { let value = -*n; self.pos += 1; Expr::Float(value) }
                _ => Expr::Unary { op: UnaryOp::Negate, expr: Box::new(self.parse_unary()) },
            };
        }
        self.parse_primary()
    }

    fn parse_primary(&mut self) -> Expr {
        let mut expr = match self.current() {
            Token::Integer(n) => { let val = *n; self.pos += 1; Expr::Integer(val) }
            Token::Float(f) => { let val = *f; self.pos += 1; Expr::Float(val) }
            Token::StringLiteral(s) => { let val = s.clone(); self.pos += 1; Expr::StringLiteral(val) }
            Token::Identifier(name) => {
                let id = name.clone();
                self.pos += 1;
                if self.current() == &Token::LeftParen {
                    self.pos += 1;
                    let mut args = Vec::new();
                    while self.current() != &Token::RightParen && self.current() != &Token::Eof {
                        let before = self.pos;
                        args.push(self.parse_expression());
                        if self.current() == &Token::Comma {
                            self.pos += 1;
                        } else if self.current() != &Token::RightParen {
                            self.errors.push("expected ',' or ')' after call argument".into());
                            self.synchronize_delimited();
                            if self.current() == &Token::Comma { self.pos += 1; }
                        }
                        if self.pos == before && self.current() != &Token::Eof { self.pos += 1; }
                    }
                    if self.current() == &Token::RightParen {
                        self.pos += 1;
                    } else {
                        self.errors.push(format!("unterminated call to '{}'", id));
                    }
                    Expr::Call { callee: id, args }
                } else {
                    Expr::Variable(id)
                }
            }
            Token::LeftParen => {
                self.pos += 1;
                let expr = self.parse_expression();
                if self.current() == &Token::RightParen {
                    self.pos += 1;
                }
                expr
            }
            Token::LeftBracket => {
                self.pos += 1;
                let mut values = Vec::new();
                while self.current() == &Token::Newline { self.pos += 1; }
                while self.current() != &Token::RightBracket && self.current() != &Token::Eof {
                    let before = self.pos;
                    values.push(self.parse_expression());
                    while self.current() == &Token::Newline { self.pos += 1; }
                    if self.current() == &Token::Comma { self.pos += 1; }
                    else if self.current() != &Token::RightBracket {
                        self.errors.push("expected ',' or ']' after array item".into());
                        while !matches!(self.current(), Token::Comma | Token::RightBracket | Token::Eof | Token::Newline) { self.pos += 1; }
                        if self.current() == &Token::Comma { self.pos += 1; }
                    }
                    while self.current() == &Token::Newline { self.pos += 1; }
                    if before == self.pos && self.current() != &Token::Eof { self.pos += 1; }
                }
                if self.current() == &Token::RightBracket { self.pos += 1; }
                else { self.errors.push("unterminated array literal".into()); }
                Expr::Array(values)
            }
            Token::LeftBrace => {
                self.pos += 1;
                let mut entries = Vec::new();
                while self.current() == &Token::Newline { self.pos += 1; }
                while self.current() != &Token::RightBrace && self.current() != &Token::Eof {
                    let before = self.pos;
                    let key = self.parse_expression();
                    while self.current() == &Token::Newline { self.pos += 1; }
                    if self.current() == &Token::Colon { self.pos += 1; }
                    else { self.errors.push("expected ':' between dictionary key and value".into()); }
                    while self.current() == &Token::Newline { self.pos += 1; }
                    let value = self.parse_expression();
                    entries.push((key, value));
                    while self.current() == &Token::Newline { self.pos += 1; }
                    if self.current() == &Token::Comma { self.pos += 1; }
                    else if self.current() != &Token::RightBrace {
                        self.errors.push("expected ',' or '}' after dictionary entry".into());
                        while !matches!(self.current(), Token::Comma | Token::RightBrace | Token::Eof | Token::Newline) { self.pos += 1; }
                        if self.current() == &Token::Comma { self.pos += 1; }
                    }
                    while self.current() == &Token::Newline { self.pos += 1; }
                    if before == self.pos && self.current() != &Token::Eof { self.pos += 1; }
                }
                if self.current() == &Token::RightBrace { self.pos += 1; }
                else { self.errors.push("unterminated dictionary literal".into()); }
                Expr::Dict(entries)
            }
            token => {
                self.errors.push(format!("expected an expression, found {:?}", token));
                if self.current() != &Token::Eof { self.pos += 1; }
                Expr::Integer(0)
            }
        };
        while self.current() == &Token::LeftBracket {
            self.pos += 1;
            let key = self.parse_expression();
            if self.current() == &Token::RightBracket { self.pos += 1; }
            else { self.errors.push("expected ']' after index expression".into()); }
            expr = Expr::Index { object: Box::new(expr), key: Box::new(key) };
        }
        expr
    }

    fn current(&self) -> &Token {
        if self.pos < self.tokens.len() { &self.tokens[self.pos] } else { &Token::Eof }
    }

    fn synchronize_delimited(&mut self) {
        while !matches!(self.current(), Token::Comma | Token::RightParen | Token::Eof | Token::Newline) {
            self.pos += 1;
        }
    }

    #[allow(dead_code)]
    fn peek(&self) -> &Token {
        if self.pos + 1 < self.tokens.len() { &self.tokens[self.pos + 1] } else { &Token::Eof }
    }
}
