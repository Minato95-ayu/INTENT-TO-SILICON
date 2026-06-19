import json

class AAYUError(Exception):
    def __init__(self, type_name, message, line, hint=""):
        self.type_name = type_name
        self.message = message
        self.line = line
        self.hint = hint
        super().__init__(self.message)

    def to_dict(self):
        return {
            "type": self.type_name,
            "line": self.line,
            "message": self.message,
            "hint": self.hint
        }

    def format(self, use_color=True):
        if use_color:
            RED = '\033[91m'
            YELLOW = '\033[93m'
            BLUE = '\033[94m'
            RESET = '\033[0m'
        else:
            RED = YELLOW = BLUE = RESET = ''

        err_type = f"{RED}🔴 [AAYU {self.type_name}]{RESET}"
        line_info = f"{BLUE}Line {self.line}{RESET}"
        hint_info = f"\n{YELLOW}🟡 Hint:\n{self.hint}{RESET}" if self.hint else ""

        return f"\n{err_type}\n\n{line_info}\n{self.message}\n{hint_info}\n"

class AAYUSyntaxError(AAYUError):
    def __init__(self, message, line, hint=""):
        super().__init__("Syntax Error", message, line, hint)

class AAYURuntimeError(AAYUError):
    def __init__(self, message, line, hint=""):
        super().__init__("Runtime Error", message, line, hint)

class AAYUDatabaseError(AAYUError):
    def __init__(self, message, line, hint=""):
        super().__init__("Database Error", message, line, hint)

class AAYUImportError(AAYUError):
    def __init__(self, message: str, line: int = 1, hint: str = ""):
        super().__init__("Import Error", message, line, hint)

class AAYUTestFailure(AAYUError):
    def __init__(self, message: str, line: int = 1, hint: str = ""):
        super().__init__("Test Failure", message, line, hint)
