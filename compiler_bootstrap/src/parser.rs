use crate::lexer::Token;

#[derive(Debug, Clone, PartialEq)]
pub enum BinaryOp {
    Add,
    Sub,
    Mul,
    Div,
    Lt,
    Gt,
    EqEq,
    NotEq,
    Lte,
    Gte,
}

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
    Call {
        callee: String,
        args: Vec<Expr>,
    },
}

#[derive(Debug, Clone)]
pub enum Statement {
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
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self { tokens, pos: 0 }
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

    fn parse_block(&mut self) -> Vec<Statement> {
        let mut stmts = Vec::new();
        while self.current() != &Token::Eof && self.current() != &Token::End && self.current() != &Token::Else {
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
                }
                return Some(Statement::While { cond, body });
            }
            Token::If => {
                self.pos += 1;
                let cond = self.parse_expression();
                let mut then_branch = Vec::new();
                let mut else_branch = Vec::new();
                while self.current() != &Token::Eof && self.current() != &Token::End && self.current() != &Token::Else {
                    if let Some(stmt) = self.parse_statement() {
                        then_branch.push(stmt);
                    }
                }
                if self.current() == &Token::Else {
                    self.pos += 1;
                    while self.current() != &Token::Eof && self.current() != &Token::End {
                        if let Some(stmt) = self.parse_statement() {
                            else_branch.push(stmt);
                        }
                    }
                }
                if self.current() == &Token::End {
                    self.pos += 1;
                }
                return Some(Statement::If { cond, then_branch, else_branch });
            }
            Token::Print => {
                self.pos += 1;
                let has_paren = self.current() == &Token::LeftParen;
                if has_paren { self.pos += 1; }
                let expr = self.parse_expression();
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
                            if let Token::Identifier(arg) = self.current() {
                                args.push(arg.clone());
                                self.pos += 1;
                                if self.current() == &Token::Comma {
                                    self.pos += 1;
                                }
                            } else {
                                self.pos += 1;
                            }
                        }
                        if self.current() == &Token::RightParen {
                            self.pos += 1;
                        }
                    }
                    let body = self.parse_block();
                    if self.current() == &Token::End {
                        self.pos += 1;
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
                return Some(Statement::Widget { kind, text, style, children });
            }
            Token::Newline => { self.pos += 1; return None; }
            _ => { self.pos += 1; return None; }
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
        let mut left = self.parse_primary();
        while matches!(self.current(), Token::Star | Token::Slash) {
            let op = match self.current() {
                Token::Star => BinaryOp::Mul,
                Token::Slash => BinaryOp::Div,
                _ => unreachable!(),
            };
            self.pos += 1;
            let right = self.parse_primary();
            left = Expr::Binary { left: Box::new(left), op, right: Box::new(right) };
        }
        left
    }

    fn parse_primary(&mut self) -> Expr {
        match self.current() {
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
                        args.push(self.parse_expression());
                        if self.current() == &Token::Comma {
                            self.pos += 1;
                        }
                    }
                    if self.current() == &Token::RightParen {
                        self.pos += 1;
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
            _ => { self.pos += 1; Expr::Integer(0) }
        }
    }

    fn current(&self) -> &Token {
        if self.pos < self.tokens.len() { &self.tokens[self.pos] } else { &Token::Eof }
    }

    #[allow(dead_code)]
    fn peek(&self) -> &Token {
        if self.pos + 1 < self.tokens.len() { &self.tokens[self.pos + 1] } else { &Token::Eof }
    }
}
