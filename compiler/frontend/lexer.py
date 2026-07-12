"""
===============================================================================
AAYU Compiler - Lexer

Purpose:
    Ye file raw source code (text) ko Tokens (words) me convert karti hai.

Input:
    Raw AAYU Source Code (string)

Output:
    List of Tokens

Pipeline:
    Source Code
        ↓
    Lexer    ← (Current File)
        ↓
    Parser
        ↓
    AST
        ↓
    Semantic Analysis

Ye file kyun important hai?
    Compiler seedhe text nahi padh sakta. Lexer pehla step hai jo text ko words (Keywords, Strings, Symbols) me classify karta hai taaki aage ka process aasan ho.

Difficulty:
    ⭐ (Easy)

Recommended Reading Order:
    1. lexer.py (You are here)
    2. parser.py
    3. ast_nodes.py
===============================================================================
"""
import re
from dataclasses import dataclass
from typing import List
from compiler.frontend.errors import AAYUSyntaxError

@dataclass
class Token:
    type: str
    value: str
    line: int = 1
    column: int = 1

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.tokens: List[Token] = []
        self.current_pos = 0
        self.line = 1
        self.column = 1
        
        # Token specification
        self.token_specs = [
            ("COMMENT", r'#.*'),
            ("NUMBER", r'\d+(\.\d+)?'),
            ("STRING", r'"[^"]*"'),
            ("KEYWORD", r'\b(public|private|as|function|module|import|number|text|is|show|if|else|while|end|greater|less|equal|not|than|to|repeat|times|task|run|with|and|or|list|for|each|in|return|use|record|of|read|write|try|catch|finally|throw|panic|assert|add|map|set|get|post|put|from|export|serve|on|route|render|form|json|entity|create|insert|find|where|order|limit|offset|update|delete|login|logout|guard|session|account|test|expect|equals|project|page|title|component|heading|button|card|row|column|input|navbar|image|table|modal|sidebar|dashboard|chart|tabs|badge|alert|crud|relation|one_to_one|one_to_many|many_to_one|many_to_many|role|allow|workflow|step|let|print|interface|implements|extend|theme|state|click|password|textarea|checkbox|radio|switch|slider|progress|avatar|footer|hero|dialog|accordion|video|audio|canvas|icon|stack|container|grid|flex|wrap|scroll|spacer|divider|padding|margin|width|height|radius|background|color|font|shadow|center|alignStart|alignEnd|spaceBetween|spaceAround|spaceEvenly|storage|service|security|model|authentication|authorization|permissions|roles|Int|String|Boolean)\b'),
            ("IDENTIFIER", r'[A-Za-z_][A-Za-z0-9_]*'),
            ("DOUBLE_COLON", r'::'),
            ("PLUS_EQ", r'\+='),
            ("MINUS_EQ", r'-='),
            ("PLUS", r'\+'),
            ("MINUS", r'-'),
            ("STAR", r'\*'),
            ("SLASH", r'/'),
            ("PERCENT", r'%'),
            ("EQ_EQ", r'=='),
            ("NOT_EQ", r'!='),
            ("GTE", r'>='),
            ("LTE", r'<='),
            ("EQ", r'='),
            ("GREATER", r'>'),
            ("LESS", r'<'),
            ("LPAREN", r'\('),
            ("RPAREN", r'\)'),
            ("COMMA", r','),
            ("LBRACKET", r'\['),
            ("RBRACKET", r'\]'),
            ("LBRACE", r'\{'),
            ("RBRACE", r'\}'),
            ("COLON", r':'),
            ("DOT_DOT", r'\.\.'),
            ("DOT", r'\.'),
            ("WHITESPACE", r'[ \t]+'),
            ("NEWLINE", r'\n'),
            ("MISMATCH", r'.')
        ]
        
        self.regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specs))

    def tokenize(self) -> List[Token]:
        """
        Purpose:
            Regex patterns use karke source string ko tokens ki list me convert karta hai.

        Example Input:
            let a = 10.

        Output:
            [Token(KEYWORD, 'let'), Token(IDENTIFIER, 'a'), Token(EQ, '='), Token(NUMBER, '10'), Token(DOT, '.')]

        Steps:
            1. Har character pattern match karo.
            2. Whitespace aur Comments ignore karo.
            3. Matches ko Token list me save karo.
        """
        for match in self.regex.finditer(self.source_code):
            kind = match.lastgroup
            value = match.group()
            
            # Comments aur spaces compiler ke kaam ke nahi hote, isliye skip karte hain.
            if kind in ("WHITESPACE", "COMMENT"):
                self.column += len(value)
                continue
            elif kind == "NEWLINE":
                self.line += 1
                self.column = 1
                continue
            # Agar koi ajeeb character mile jo regex me na ho, to yahan syntax error aayega.
            elif kind == "MISMATCH":
                raise AAYUSyntaxError(f"Unexpected character '{value}'", self.line, column=self.column)

            
            self.tokens.append(Token(kind, value, self.line, self.column))
            self.column += len(value)
            
        self.tokens.append(Token("EOF", "", self.line, self.column))
        return self.tokens

if __name__ == "__main__":
    code = '''
    number a is 10.
    number b is 20.
    show a + b.
    '''
    lexer = Lexer(code)
    for token in lexer.tokenize():
        print(token)
