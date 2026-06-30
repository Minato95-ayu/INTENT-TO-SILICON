from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from ast_nodes import Node

@dataclass
class Diagnostic:
    level: str  # "error", "warning", "note"
    message: str
    file: str
    line: Optional[int] = None
    node: Optional[Node] = None

class Diagnostics:
    def __init__(self):
        self.diagnostics: List[Diagnostic] = []
        
    def error(self, message: str, file: str, line: Optional[int] = None, node: Optional[Node] = None):
        self.diagnostics.append(Diagnostic("error", message, file, line, node))
        
    def warning(self, message: str, file: str, line: Optional[int] = None, node: Optional[Node] = None):
        self.diagnostics.append(Diagnostic("warning", message, file, line, node))
        
    def note(self, message: str, file: str, line: Optional[int] = None, node: Optional[Node] = None):
        self.diagnostics.append(Diagnostic("note", message, file, line, node))
        
    def has_errors(self) -> bool:
        return any(d.level == "error" for d in self.diagnostics)
        
    def print_all(self):
        for d in self.diagnostics:
            loc = f"{d.file}"
            if d.line: loc += f":{d.line}"
            print(f"[{d.level.upper()}] {loc} - {d.message}")

class CompilerContext:
    def __init__(self, workspace=None, module_graph=None, cache=None, manifest=None):
        self.workspace = workspace
        self.module_graph = module_graph
        self.cache = cache
        self.manifest = manifest
        self.diagnostics = Diagnostics()
        self.symbol_tables: Dict[str, Any] = {} # Dict[module_name, SymbolTable]
        self.current_module: str = ""
        self.build_mode: str = "debug"
        self.configuration: Dict[str, Any] = {}
        
        # AST storage
        self.asts: Dict[str, Node] = {} # Dict[module_name, ProgramNode]
