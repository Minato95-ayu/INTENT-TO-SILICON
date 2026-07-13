class CompilerError(Exception):
    def __init__(self, message: str, line: int = 0, column: int = 0, source_line: str = "", hint: str = ""):
        self.message = message
        self.line = line
        self.column = column
        self.source_line = source_line
        self.hint = hint
        super().__init__(self.__str__())

    def __str__(self):
        if self.line == 0:
            msg = f"CompilerError: {self.message}"
            if self.hint:
                msg += f"\nHint: {self.hint}"
            return msg
            
        header = f"Error: {self.message}"
        if not self.source_line:
            if self.hint:
                header += f"\nHint: {self.hint}"
            return header
            
        # Format the error with a pointer caret
        pointer = " " * (max(0, self.column - 1)) + "^"
        output = f"\n{header}\n\n{self.line} | {self.source_line.rstrip()}\n  | {pointer}\n"
        if self.hint:
            output += f"\nHint:\n{self.hint}\n"
        return output