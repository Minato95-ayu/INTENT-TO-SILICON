#[derive(Debug, PartialEq, Clone)]
pub enum Token {
    Let,
    Print,
    If,
    Else,
    While,
    End,
    Action,
    Return,
    App,
    State,
    Page,
    Column,
    Row,
    Heading,
    Text,
    Button,
    Input,
    Container,
    Card,
    Icon,
    Grid,
    Run,
    StringLiteral(String),
    Identifier(String),
    Integer(i64),
    Float(f64),
    Plus,
    Minus,
    Star,
    Slash,
    LessThan,
    GreaterThan,
    DoubleEqual,
    NotEqual,
    LessEqual,
    GreaterEqual,
    LeftParen,
    RightParen,
    LeftBracket,
    RightBracket,
    LeftBrace,
    RightBrace,
    Equal,
    Comma,
    Colon,
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

            // 1. Skip comments: # or //
            if ch == '#' || (ch == '/' && self.peek_char() == '/') {
                while self.pos < self.input.len() && self.current_char() != '\n' {
                    self.pos += 1;
                }
                continue;
            }

            // 2. Strings
            if ch == '"' {
                self.pos += 1;
                let mut s = String::new();
                while self.pos < self.input.len() {
                    let c = self.current_char();
                    if c == '\\' && self.pos + 1 < self.input.len() {
                        let next = self.peek_char();
                        if next == '"' {
                            s.push('"');
                            self.pos += 2;
                            continue;
                        } else if next == 'n' {
                            s.push('\n');
                            self.pos += 2;
                            continue;
                        } else if next == 'r' {
                            s.push('\r');
                            self.pos += 2;
                            continue;
                        } else if next == 't' {
                            s.push('\t');
                            self.pos += 2;
                            continue;
                        } else if next == '\\' {
                            s.push('\\');
                            self.pos += 2;
                            continue;
                        }
                    }
                    if c == '"' {
                        break;
                    }
                    s.push(c);
                    self.pos += 1;
                }
                if self.pos < self.input.len() {
                    self.pos += 1; // skip closing quote
                }
                tokens.push(Token::StringLiteral(s));
                continue;
            }

            // 3. Whitespace
            if ch.is_whitespace() {
                if ch == '\n' {
                    tokens.push(Token::Newline);
                }
                self.pos += 1;
            } else if ch.is_ascii_alphabetic() || ch == '_' {
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
                    "page" | "Page" => tokens.push(Token::Page),
                    "Column" => tokens.push(Token::Column),
                    "Container" => tokens.push(Token::Container),
                    "Card" => tokens.push(Token::Card),
                    "Icon" => tokens.push(Token::Icon),
                    "Grid" => tokens.push(Token::Grid),
                    "Row" => tokens.push(Token::Row),
                    "Heading" => tokens.push(Token::Heading),
                    "Text" => tokens.push(Token::Text),
                    "Button" => tokens.push(Token::Button),
                    "Input" => tokens.push(Token::Input),
                    "run" | "Run" => tokens.push(Token::Run),
                    "end" => tokens.push(Token::End),
                    _ => tokens.push(Token::Identifier(word.to_string())),
                }
            } else if ch.is_ascii_digit() {
                let start = self.pos;
                let mut is_float = false;
                while self.pos < self.input.len() {
                    let c = self.current_char();
                    if c.is_ascii_digit() {
                        self.pos += 1;
                    } else if c == '.' && !is_float && self.peek_char().is_ascii_digit() {
                        is_float = true;
                        self.pos += 1;
                    } else {
                        break;
                    }
                }
                let num_str = &self.input[start..self.pos];
                if is_float {
                    tokens.push(Token::Float(num_str.parse().unwrap_or(0.0)));
                } else {
                    tokens.push(Token::Integer(num_str.parse().unwrap_or(0)));
                }
            } else {
                match ch {
                    '+' => tokens.push(Token::Plus),
                    '-' => tokens.push(Token::Minus),
                    '*' => tokens.push(Token::Star),
                    '/' => tokens.push(Token::Slash),
                    '(' => tokens.push(Token::LeftParen),
                    ')' => tokens.push(Token::RightParen),
                    '[' => tokens.push(Token::LeftBracket),
                    ']' => tokens.push(Token::RightBracket),
                    '{' => tokens.push(Token::LeftBrace),
                    '}' => tokens.push(Token::RightBrace),
                    ',' => tokens.push(Token::Comma),
                    ':' => tokens.push(Token::Colon),
                    '=' => {
                        if self.peek_char() == '=' {
                            self.pos += 1;
                            tokens.push(Token::DoubleEqual);
                        } else {
                            tokens.push(Token::Equal);
                        }
                    }
                    '!' => {
                        if self.peek_char() == '=' {
                            self.pos += 1;
                            tokens.push(Token::NotEqual);
                        }
                    }
                    '<' => {
                        if self.peek_char() == '=' {
                            self.pos += 1;
                            tokens.push(Token::LessEqual);
                        } else {
                            tokens.push(Token::LessThan);
                        }
                    }
                    '>' => {
                        if self.peek_char() == '=' {
                            self.pos += 1;
                            tokens.push(Token::GreaterEqual);
                        } else {
                            tokens.push(Token::GreaterThan);
                        }
                    }
                    _ => {} // Ignore unknown
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
