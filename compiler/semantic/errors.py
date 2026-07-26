class SemanticError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Semantic Error at line {line}, col {column}: {message}")
        self.line = line
        self.column = column

class TypeError(Exception):
    def __init__(self, expected: str, received: str, line: int, column: int, hint: str = ""):
        message = f"\nType Error\n"
        message += f"Line {line}, Column {column}\n"
        message += f"Expected: {expected}\n"
        message += f"Received: {received}\n"
        if hint:
            message += f"Hint: {hint}\n"
            
        super().__init__(message)
        self.line = line
        self.column = column
        self.expected = expected
        self.received = received
        self.hint = hint
