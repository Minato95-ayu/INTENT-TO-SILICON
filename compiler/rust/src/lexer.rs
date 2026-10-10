#[derive(Debug, PartialEq, Clone)]
pub enum Token {
    Let,
    Print,
    Identifier(String),
    Integer(i64),
    Plus,
    LeftParen,
    RightParen,
    Equal,
    Newline,
    Eof,
}

pub struct Lexer {
    chars: Vec<char>,
    pos: usize,
}

impl Lexer {
    pub fn new(source: &str) -> Self {
        Self {
            chars: source.chars().collect(),
            pos: 0,
        }
    }

    pub fn tokenize(&mut self) -> Vec<Token> {
        let mut tokens = Vec::new();
        while self.pos < self.chars.len() {
            let c = self.chars[self.pos];
            match c {
                ' ' | '\r' | '\t' => self.pos += 1,
                '\n' => {
                    tokens.push(Token::Newline);
                    self.pos += 1;
                }
                '+' => {
                    tokens.push(Token::Plus);
                    self.pos += 1;
                }
                '=' => {
                    tokens.push(Token::Equal);
                    self.pos += 1;
                }
                '(' => {
                    tokens.push(Token::LeftParen);
                    self.pos += 1;
                }
                ')' => {
                    tokens.push(Token::RightParen);
                    self.pos += 1;
                }
                _ if c.is_ascii_digit() => {
                    let mut num_str = String::new();
                    while self.pos < self.chars.len() && self.chars[self.pos].is_ascii_digit() {
                        num_str.push(self.chars[self.pos]);
                        self.pos += 1;
                    }
                    tokens.push(Token::Integer(num_str.parse().unwrap()));
                }
                _ if c.is_alphabetic() => {
                    let mut id_str = String::new();
                    while self.pos < self.chars.len() && (self.chars[self.pos].is_alphanumeric() || self.chars[self.pos] == '_') {
                        id_str.push(self.chars[self.pos]);
                        self.pos += 1;
                    }
                    match id_str.as_str() {
                        "let" => tokens.push(Token::Let),
                        "print" => tokens.push(Token::Print),
                        _ => tokens.push(Token::Identifier(id_str)),
                    }
                }
                _ => {
                    self.pos += 1; // Ignore unknown
                }
            }
        }
        tokens.push(Token::Eof);
        tokens
    }
}
