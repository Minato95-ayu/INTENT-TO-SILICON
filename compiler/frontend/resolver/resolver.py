"""
=============================================================================
FILE: resolver.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from pathlib import Path
from typing import Dict, List, Set, Any
from .module_graph import ModuleGraph
from .loader import Loader
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.ast_nodes import ImportNode, ModuleDeclarationNode

class Resolver:
    def __init__(self, workspace: Any):
        self.workspace = workspace
        self.loader = Loader(workspace.root_path)
        self.graph = ModuleGraph()
        self.parsed_asts = {} # module_name -> AST
        self.module_paths = {} # module_name -> Path
        
    def resolve(self, entry_file: str) -> List[Any]:
        """
        Takes the entry file path, resolves all dependencies, and returns
        a topologically sorted list of ASTs ready for compilation.
        """
        entry_path = Path(entry_file).resolve()
        # For the entry file, we might not have a formal module name yet,
        # but let's assume it's __main__
        self._resolve_file("__main__", entry_path)
        
        # Get sorted module names
        sorted_modules = self.graph.get_topological_order()
        
        # Return (module_name, AST) in order
        return [(mod, self.parsed_asts[mod]) for mod in sorted_modules]
        
    def _resolve_file(self, module_name: str, file_path: Path):
        if module_name in self.parsed_asts:
            return
            
        self.module_paths[module_name] = str(file_path)
        
        source = self.loader.load_source(file_path)
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Verify if module declares its name
        declared_module_name = None
        for stmt in ast.statements:
            if isinstance(stmt, ModuleDeclarationNode):
                declared_module_name = stmt.name
                break
                
        # If the file declares a module name, we might want to register it under that name.
        # But wait, we were resolving `module_name`. If it mismatch, raise error?
        if declared_module_name and module_name != "__main__":
            if declared_module_name != module_name:
                raise Exception(f"File {file_path} declares module '{declared_module_name}', but was imported as '{module_name}'")
                
        self.parsed_asts[module_name] = ast
        self.graph.add_module(module_name)
        
        # Extract imports
        for stmt in ast.statements:
            if isinstance(stmt, ImportNode):
                dep_name = stmt.module_name
                self.graph.add_dependency(module_name, dep_name)
                
                # Recursively resolve
                dep_path = self.loader.find_module(dep_name, file_path)
                if not dep_path:
                    raise Exception(f"Could not find module '{dep_name}' imported from {file_path}")
                self._resolve_file(dep_name, dep_path)
