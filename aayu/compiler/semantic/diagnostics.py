import sys
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Any

class DiagnosticSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    NOTE = "note"
    SUGGESTION = "suggestion"

@dataclass
class Diagnostic:
    severity: DiagnosticSeverity
    message: str
    code: str = "E000"
    line: int = 0
    column: int = 0
    file_name: str = "<unknown>"
    notes: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    span: Optional[Any] = None
    hint: Optional[str] = None
    
    def __post_init__(self):
        if self.hint:
            self.notes.append(self.hint)

    def add_note(self, note: str):
        self.notes.append(note)

    def add_suggestion(self, suggestion: str):
        self.suggestions.append(suggestion)

    def __str__(self):
        # ANSI escape codes for coloring (if supported, otherwise fallback to plain text)
        RED = "\033[91m"
        YELLOW = "\033[93m"
        BLUE = "\033[94m"
        GREEN = "\033[92m"
        RESET = "\033[0m"
        BOLD = "\033[1m"
        
        color = RED if self.severity == DiagnosticSeverity.ERROR else YELLOW
        
        out = f"{BOLD}{self.file_name}:{self.line}:{self.column}: {color}{self.severity.value}[{self.code}]: {self.message}{RESET}\n"
        
        for note in self.notes:
            out += f"  {BLUE}note:{RESET} {note}\n"
            
        for sugg in self.suggestions:
            out += f"  {GREEN}suggestion:{RESET} {sugg}\n"
            
        return out

class DiagnosticEngine:
    def __init__(self):
        self.diagnostics: List[Diagnostic] = []
        
    def report(self, diagnostic: Diagnostic):
        self.diagnostics.append(diagnostic)
        
    def has_errors(self) -> bool:
        return any(d.severity == DiagnosticSeverity.ERROR for d in self.diagnostics)
        
    def print_all(self):
        for d in self.diagnostics:
            print(str(d), file=sys.stderr)
            
    def clear(self):
        self.diagnostics.clear()

# Global instance for the compiler pipeline
engine = DiagnosticEngine()
