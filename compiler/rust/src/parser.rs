use crate::lexer::Token;

#[derive(Debug)]
pub enum BinaryOp {
    Add,
    Lt,
    Gt,
    EqEq,
}

#[derive(Debug)]
pub enum Expr {
    Integer(i64),
    Variable(String),
    Binary {
        left: Box<Expr>,
        op: BinaryOp,
        right: Box<Expr>,
    },
}

#[derive(Debug)]
pub enum Statement {
    Let { name: String, value: Expr },
    Print(Expr),
    If { condition: Expr, then_branch: Vec<Statement>, else_branch: Option<Vec<Statement>> },
    While { condition: Expr, body: Vec<Statement> },
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
        while self.pos < self.tokens.len() && self.current() != &Token::Eof {
            if self.current() == &Token::Newline {
                self.pos += 1;
                continue;
            }
            if let Some(stmt) = self.parse_statement() {
                stmts.push(stmt);
            }
        }
        stmts
    }

    fn parse_statement(&mut self) -> Option<Statement> {
        match self.current() {
            Token::Let => {
                self.pos += 1; // consume Let
                if let Token::Identifier(name) = self.current() {
                    let var_name = name.clone();
                    self.pos += 1; // consume Ident
                    if self.current() == &Token::Equal {
                        self.pos += 1; // consume Equal
                        let expr = self.parse_expression();
                        return Some(Statement::Let { name: var_name, value: expr });
                    }
                }
            }
            Token::Print => {
                self.pos += 1; // consume Print
                if self.current() == &Token::LeftParen {
                    self.pos += 1; // consume (
                    let expr = self.parse_expression();
                    if self.current() == &Token::RightParen {
                        self.pos += 1; // consume )
                        return Some(Statement::Print(expr));
                    }
                }
            }
            Token::If => {
                self.pos += 1; // consume If
                let condition = self.parse_expression();
                let then_branch = self.parse_block();
                
                let mut else_branch = None;
                if self.current() == &Token::Else {
                    self.pos += 1; // consume Else
                    else_branch = Some(self.parse_block());
                }
                
                if self.current() == &Token::End {
                    self.pos += 1; // consume End
                }
                return Some(Statement::If { condition, then_branch, else_branch });
            }
            Token::While => {
                self.pos += 1; // consume While
                let condition = self.parse_expression();
                let body = self.parse_block();
                if self.current() == &Token::End {
                    self.pos += 1; // consume End
                }
                return Some(Statement::While { condition, body });
            }
            _ => {
                self.pos += 1;
            }
        }
        None
    }

    fn parse_block(&mut self) -> Vec<Statement> {
        let mut stmts = Vec::new();
        while self.pos < self.tokens.len() {
            if self.current() == &Token::Newline {
                self.pos += 1;
                continue;
            }
            if matches!(self.current(), Token::End | Token::Else | Token::Eof) {
                break;
            }
            if let Some(stmt) = self.parse_statement() {
                stmts.push(stmt);
            }
        }
        stmts
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
            self.pos += 1; // consume op
            let right = self.parse_primary();
            left = Expr::Binary {
                left: Box::new(left),
                op,
                right: Box::new(right),
            };
        }
        left
    }

    fn parse_primary(&mut self) -> Expr {
        match self.current() {
            Token::Integer(n) => {
                let val = *n;
                self.pos += 1;
                Expr::Integer(val)
            }
            Token::Identifier(name) => {
                let val = name.clone();
                self.pos += 1;
                Expr::Variable(val)
            }
            _ => {
                self.pos += 1;
                Expr::Integer(0) // Dummy
            }
        }
    }

    fn current(&self) -> &Token {
        if self.pos < self.tokens.len() {
            &self.tokens[self.pos]
        } else {
            &Token::Eof
        }
    }
}
