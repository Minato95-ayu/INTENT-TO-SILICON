use crate::lexer::Token;

#[derive(Debug, Clone, PartialEq)]
pub enum BinaryOp {
    Add,
}

#[derive(Debug, Clone, PartialEq)]
pub enum Expr {
    Integer(i64),
    Variable(String),
    Binary {
        left: Box<Expr>,
        op: BinaryOp,
        right: Box<Expr>,
    },
}

#[derive(Debug, Clone, PartialEq)]
pub enum Statement {
    Let { name: String, value: Expr },
    Print(Expr),
}

pub struct Parser {
    tokens: Vec<Token>,
    pos: usize,
}

impl Parser {
    pub fn new(tokens: Vec<Token>) -> Self {
        Self { tokens, pos: 0 }
    }

    fn peek(&self) -> &Token {
        if self.pos < self.tokens.len() {
            &self.tokens[self.pos]
        } else {
            &Token::Eof
        }
    }

    fn consume(&mut self) -> Token {
        let t = self.peek().clone();
        self.pos += 1;
        t
    }

    pub fn parse(&mut self) -> Vec<Statement> {
        let mut stmts = Vec::new();
        while self.peek() != &Token::Eof {
            if self.peek() == &Token::Newline {
                self.consume();
                continue;
            }
            if let Some(stmt) = self.parse_statement() {
                stmts.push(stmt);
            } else {
                self.consume();
            }
        }
        stmts
    }

    fn parse_statement(&mut self) -> Option<Statement> {
        match self.peek() {
            Token::Let => {
                self.consume(); // eat let
                let Token::Identifier(name) = self.consume() else { return None; };
                if self.peek() != &Token::Equal { return None; }
                self.consume(); // eat =
                let value = self.parse_expr()?;
                Some(Statement::Let { name, value })
            }
            Token::Print => {
                self.consume(); // eat print
                if self.peek() != &Token::LeftParen { return None; }
                self.consume(); // eat (
                let expr = self.parse_expr()?;
                if self.peek() != &Token::RightParen { return None; }
                self.consume(); // eat )
                Some(Statement::Print(expr))
            }
            _ => None,
        }
    }

    fn parse_expr(&mut self) -> Option<Expr> {
        let left = self.parse_primary()?;
        
        if self.peek() == &Token::Plus {
            self.consume();
            let right = self.parse_primary()?;
            return Some(Expr::Binary {
                left: Box::new(left),
                op: BinaryOp::Add,
                right: Box::new(right),
            });
        }
        
        Some(left)
    }

    fn parse_primary(&mut self) -> Option<Expr> {
        match self.peek() {
            Token::Integer(n) => {
                let val = *n;
                self.consume();
                Some(Expr::Integer(val))
            }
            Token::Identifier(name) => {
                let name = name.clone();
                self.consume();
                Some(Expr::Variable(name))
            }
            _ => None,
        }
    }
}
