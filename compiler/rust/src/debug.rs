use crate::lexer::{Lexer, Token};
use crate::parser::Parser;
pub fn main() {
    let mut lexer = Lexer::new("heading "AAYU Studio"\ntext "A complete webpage"\n".to_string());
    let tokens = lexer.tokenize();
    println!("{:?}", tokens);
}
