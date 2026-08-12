import os
from typing import List, Set

class MiniLexer:
    """
    A lightweight, deterministic lexer designed exclusively to extract `import` statements.
    Safely ignores strings and comments without incurring the cost of full tokenization.
    """
    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.pos = 0

    def extract_imports(self) -> List[str]:
        imports = []
        
        while self.pos < self.length:
            c = self.source[self.pos]
            
            # String literals
            if c == '"' or c == "'":
                quote = c
                self.pos += 1
                while self.pos < self.length:
                    if self.source[self.pos] == '\\':
                        self.pos += 2
                        continue
                    if self.source[self.pos] == quote:
                        self.pos += 1
                        break
                    self.pos += 1
                continue
                
            # Comments
            if c == '/':
                if self.pos + 1 < self.length:
                    nc = self.source[self.pos + 1]
                    # Single-line comment
                    if nc == '/':
                        self.pos += 2
                        while self.pos < self.length and self.source[self.pos] != '\n':
                            self.pos += 1
                        continue
                    # Multi-line comment
                    elif nc == '*':
                        self.pos += 2
                        while self.pos + 1 < self.length:
                            if self.source[self.pos] == '*' and self.source[self.pos+1] == '/':
                                self.pos += 2
                                break
                            self.pos += 1
                        continue
            
            # Identifier scanning
            if c.isalpha() or c == '_':
                start = self.pos
                while self.pos < self.length and (self.source[self.pos].isalnum() or self.source[self.pos] == '_'):
                    self.pos += 1
                ident = self.source[start:self.pos]
                
                if ident == "import":
                    # skip whitespace
                    while self.pos < self.length and self.source[self.pos].isspace():
                        self.pos += 1
                        
                    # parse module name
                    mod_start = self.pos
                    while self.pos < self.length and (self.source[self.pos].isalnum() or self.source[self.pos] in '_.'):
                        self.pos += 1
                    mod_name = self.source[mod_start:self.pos]
                    
                    if mod_name:
                        imports.append(mod_name)
                continue
                
            self.pos += 1
            
        return imports


class DependencyResolver:
    """
    Resolves physical file dependencies by parsing their imports safely using MiniLexer.
    """
    def __init__(self):
        self.resolved_imports = {}

    def get_dependencies_for_file(self, filepath: str) -> List[str]:
        if not os.path.exists(filepath):
            return []
            
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
            
        lexer = MiniLexer(source)
        return lexer.extract_imports()
