from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

@dataclass
class SourceSpan:
    start_line: int
    start_col: int
    end_line: int
    end_col: int
    byte_offset: int = 0
    length: int = 0
    file: str = ""

    def __str__(self):
        return f"{self.file}:{self.start_line}:{self.start_col}"

class DiagnosticSeverity(Enum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    FATAL = auto()

@dataclass
class DiagnosticMessage:
    severity: DiagnosticSeverity
    message: str
    span: Optional[SourceSpan] = None
    hint: str = ""

    def format(self) -> str:
        prefix = self.severity.name
        loc = f" at {self.span}" if self.span else ""
        out = f"[{prefix}]{loc}: {self.message}"
        if self.hint:
            out += f"\n  Hint: {self.hint}"
        return out

class CompilerError(Exception):
    """
    A fatal compiler error that abruptly halts compilation if not caught.
    This should generally only be raised by the DiagnosticEngine on FATAL severity.
    """
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

class InternalCompilerError(CompilerError):
    """
    A fatal compiler error triggered by an internal invariant violation.
    Indicates a bug in the compiler itself, not in the user's code.
    """
    def __init__(self, phase: str, invariant: str, node_id: Optional[int] = None, module: str = "<unknown>"):
        import platform
        self.phase = phase
        self.invariant = invariant
        self.node_id = node_id
        self.module = module
        self.compiler_version = f"prototype (python {platform.python_version()})"
        
        msg = (
            f"INTERNAL COMPILER ERROR (ICE)\n"
            f"Phase: {self.phase}\n"
            f"Module: {self.module}\n"
            f"Node ID: {self.node_id if self.node_id is not None else 'N/A'}\n"
            f"Invariant Failed: {self.invariant}\n"
            f"Compiler Version: {self.compiler_version}\n"
            f"This is a compiler bug. Please report it."
        )
        super().__init__(message=msg)
        
    def __str__(self):
        return self.message


class DiagnosticEngine:
    """
    Centralized diagnostic reporter for the AAYU compiler.
    Eliminates bare asserts and raw exceptions during compilation.
    """
    def __init__(self):
        self.diagnostics: List[DiagnosticMessage] = []
    
    def has_errors(self) -> bool:
        return any(d.severity in (DiagnosticSeverity.ERROR, DiagnosticSeverity.FATAL) for d in self.diagnostics)
    
    def report(self, severity: DiagnosticSeverity, message: str, span: Optional[SourceSpan] = None, hint: str = ""):
        diag = DiagnosticMessage(severity, message, span, hint)
        self.diagnostics.append(diag)
        if severity == DiagnosticSeverity.FATAL:
            # FATAL severity halts execution immediately with a graceful CompilerError
            line = span.start_line if span else 0
            col = span.start_col if span else 0
            raise CompilerError(message, line, col, hint=hint)

    def print_all(self):
        for d in self.diagnostics:
            print(d.format())

    def clear(self):
        self.diagnostics.clear()