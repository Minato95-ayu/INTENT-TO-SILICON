use crate::lexer::Token;

#[derive(Debug, Clone, PartialEq)]
pub enum BinaryOp { Add, Sub, Mul, Div, Lt, Gt, EqEq }

#[derive(Debug, Clone)]
pub enum Expr {
    Integer(i64),
    StringLiteral(String),
    Variable(String),
    Binary { left: Box<Expr>, op: BinaryOp, right: Box<Expr> },
}

#[derive(Debug, Clone)]
pub enum Statement {
    Let { name: String, value: Expr },
    App(String),
    State { name: String, value: Expr },
    Action { name: String, body: Vec<Statement> },
    Widget { kind: String, text: String, style: String, children: Vec<Statement> },
    Page { name: String, body: Vec<Statement> },
    Assignment { name: String, value: Expr },
    Run(String),
}

pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self { Self { tokens, pos: 0 } }

    pub fn parse(&mut self) -> Vec<Statement> {
        let mut stmts = Vec::new();
        while self.current() != &Token::Eof {
            if let Some(stmt) = self.parse_statement() { stmts.push(stmt); }
        }
        stmts
    }

    fn parse_block(&mut self) -> Vec<Statement> {
        let mut stmts = Vec::new();
        while self.current() != &Token::Eof && self.current() != &Token::End {
            if let Some(stmt) = self.parse_statement() { stmts.push(stmt); }
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
                    let state_name = name.clone();
                    self.pos += 1;
                    if self.current() == &Token::Equal {
                        self.pos += 1;
                        let expr = self.parse_expression();
                        return Some(Statement::State { name: state_name, value: expr });
                    }
                }
            }
            Token::Action => {
                self.pos += 1;
                if let Token::Identifier(name) = self.current() {
                    let act_name = name.clone();
                    self.pos += 1;
                    let body = self.parse_block();
                    if self.current() == &Token::End { self.pos += 1; }
                    return Some(Statement::Action { name: act_name, body });
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
            Token::Column | Token::Row | Token::Container | Token::Card | Token::Grid => {
                let kind = match self.current() {
                    Token::Column => "Column", Token::Row => "Row", Token::Container => "Container",
                    Token::Card => "Card", Token::Grid => "Grid", _ => unreachable!()
                }.to_string();
                self.pos += 1;
                let style = self.parse_attributes();
                let body = self.parse_block();
                if self.current() == &Token::End { self.pos += 1; }
                return Some(Statement::Widget { kind, text: String::new(), style, children: body });
            }
            Token::Text | Token::Heading | Token::Button => {
                let kind = match self.current() {
                    Token::Text => "Text", Token::Heading => "Heading", Token::Button => "Button", _ => unreachable!()
                }.to_string();
                self.pos += 1;
                let text = if let Token::StringLiteral(s) = self.current() {
                    let val = s.clone();
                    self.pos += 1;
                    val
                } else if let Token::Identifier(i) = self.current() {
                    let val = i.clone();
                    self.pos += 1;
                    val
                } else { String::new() };
                let style = self.parse_attributes();
                return Some(Statement::Widget { kind, text, style, children: vec![] });
            }
            Token::Icon => {
                self.pos += 1;
                let style = self.parse_attributes();
                return Some(Statement::Widget { kind: "Icon".to_string(), text: String::new(), style, children: vec![] });
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
            Token::Identifier(name) => {
                let var_name = name.clone();
                self.pos += 1;
                if self.current() == &Token::Equal {
                    self.pos += 1;
                    let expr = self.parse_expression();
                    return Some(Statement::Assignment { name: var_name, value: expr });
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
            Token::Newline => { self.pos += 1; return None; }
            _ => { self.pos += 1; return None; }
        }
        None
    }

    fn parse_expression(&mut self) -> Expr {
        let mut left = self.parse_primary();
        while matches!(self.current(), Token::Plus | Token::LessThan | Token::GreaterThan | Token::DoubleEqual) {
            let op = match self.current() {
                Token::Plus => BinaryOp::Add,
                Token::LessThan => BinaryOp::Lt,
                Token::GreaterThan => BinaryOp::Gt,
                Token::DoubleEqual => BinaryOp::EqEq,
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
            Token::StringLiteral(s) => { let val = s.clone(); self.pos += 1; Expr::StringLiteral(val) }
            Token::Identifier(name) => { let val = name.clone(); self.pos += 1; Expr::Variable(val) }
            _ => { self.pos += 1; Expr::Integer(0) }
        }
    }

    fn current(&self) -> &Token {
        if self.pos < self.tokens.len() { &self.tokens[self.pos] } else { &Token::Eof }
    }
}



