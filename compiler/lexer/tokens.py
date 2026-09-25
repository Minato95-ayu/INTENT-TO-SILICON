# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

from enum import Enum, auto

class TokenType(Enum):
    KEYWORD = auto()
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    OPERATOR = auto()
    SYMBOL = auto()
    EOF = auto()
    UNKNOWN = auto()

class Token:
    def __init__(self, token_type: TokenType, value: str, line: int, column: int, source_line: str = ""):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
        self.source_line = source_line

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}', Line: {self.line})"

KEYWORDS = {
    "app", "run", "state", "let", "model", "page", "component",
    "route", "server", "task", "event", "if", "elif", "else", "for", "while",
    "return", "fn", "end", "import", "action", "in", "get", "post",
    "theme", "useTheme", "widget", "navigate", "validate",
    "await", "bind", "animate",
    "try", "catch", "finally", "throw", "rethrow", "extern", "as", "print",
    "insert", "find", "respond", "struct"
}

OPERATORS = {
    "=", "+", "-", "*", "/", "%", "+=", "-=", "==", "!=", ">", "<", ">=", "<=", "&&", "||", "::"
}

SYMBOLS = {
    "(", ")", "{", "}", "[", "]", ",", ".", ":", "@"
}

