#[derive(Debug, PartialEq, Clone)]
pub enum Token {
    Let,
    Print,
    If,
    Else,
    While,
    End,
    Action,
    Return, App, State, Page, Column, Row, Heading, Text, Button, Container, Card, Icon, Grid, Run, StringLiteral(String),
    Identifier(String),
    Integer(i64),
    Plus,
    LessThan,
    GreaterThan,
    DoubleEqual,
    LeftParen,
    RightParen,
    Equal,
    Newline,
    Eof,
}

pub struct Lexer<'a> {
    input: &'a str,
    pos: usize,
}

impl<'a> Lexer<'a> {
    pub fn new(input: &'a str) -> Self {
        Self { input, pos: 0 }
    }

    pub fn tokenize(&mut self) -> Vec<Token> {
        let mut tokens = Vec::new();
        while self.pos < self.input.len() {
            let ch = self.current_char();
            if ch == '"' {
            self.pos += 1;
            let mut s = String::new();
            while self.pos < self.input.len() && self.input.as_bytes()[self.pos] as char != '"' {
                s.push(self.input.as_bytes()[self.pos] as char);
                self.pos += 1;
            }
            self.pos += 1; // skip closing quote
            tokens.push(Token::StringLiteral(s));
            continue;
        }
        if ch.is_whitespace() {
                if ch == '\n' {
                    tokens.push(Token::Newline);
                }
                self.pos += 1;
            } else if ch.is_ascii_alphabetic() {
                let start = self.pos;
                while self.pos < self.input.len() && (self.current_char().is_ascii_alphanumeric() || self.current_char() == '_') {
                    self.pos += 1;
                }
                let word = &self.input[start..self.pos];
                match word {
                    "let" => tokens.push(Token::Let),
                    "print" => tokens.push(Token::Print),
                    "if" => tokens.push(Token::If),
                    "else" => tokens.push(Token::Else),
                    "while" => tokens.push(Token::While),
                    "action" => tokens.push(Token::Action),
                    "return" => tokens.push(Token::Return),
                    "app" => tokens.push(Token::App),
                    "state" => tokens.push(Token::State),
                    "page" => tokens.push(Token::Page), "Page" => tokens.push(Token::Page),
                    "Column" => tokens.push(Token::Column),
                "Container" => tokens.push(Token::Container),
                "Card" => tokens.push(Token::Card),
                "Icon" => tokens.push(Token::Icon),
                "Grid" => tokens.push(Token::Grid),
                    "Row" => tokens.push(Token::Row),
                    "Heading" => tokens.push(Token::Heading),
                    "Text" => tokens.push(Token::Text),
                    "Button" => tokens.push(Token::Button),
                    "run" => tokens.push(Token::Run), "Run" => tokens.push(Token::Run),
                    "end" => tokens.push(Token::End),
                    _ => tokens.push(Token::Identifier(word.to_string())),
                }
            } else if ch.is_ascii_digit() {
                let start = self.pos;
                while self.pos < self.input.len() && self.current_char().is_ascii_digit() {
                    self.pos += 1;
                }
                let num_str = &self.input[start..self.pos];
                tokens.push(Token::Integer(num_str.parse().unwrap()));
            } else {
                match ch {
                    '+' => tokens.push(Token::Plus),
                    '(' => tokens.push(Token::LeftParen),
                    ')' => tokens.push(Token::RightParen),
                    '=' => {
                        if self.peek_char() == '=' {
                            self.pos += 1;
                            tokens.push(Token::DoubleEqual);
                        } else {
                            tokens.push(Token::Equal);
                        }
                    }
                    '<' => tokens.push(Token::LessThan),
                    '>' => tokens.push(Token::GreaterThan),
                    _ => {} // Ignore unknown for MVP
                }
                self.pos += 1;
            }
        }
        tokens.push(Token::Eof);
        tokens
    }

    fn current_char(&self) -> char {
        self.input[self.pos..].chars().next().unwrap_or('\0')
    }

    fn peek_char(&self) -> char {
        let mut it = self.input[self.pos..].chars();
        it.next();
        it.next().unwrap_or('\0')
    }
}






