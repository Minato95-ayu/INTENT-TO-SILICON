class SemanticError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Semantic Error at line {line}, col {column}: {message}")
        self.line = line
        self.column = column
