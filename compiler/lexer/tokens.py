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
    "app", "run",
    "page", "layout", "text", "button", "input", "state", "model",
    "route", "server", "task", "event", "if", "else", "for", "while",
    "return", "fn", "end", "import", "action"
}

OPERATORS = {
    "=", "+", "-", "*", "/", "+=", "-=", "==", "!=", ">", "<", ">=", "<="
}

SYMBOLS = {
    "(", ")", "{", "}", "[", "]", ",", ".", ":"
}
