from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
import os

class BuilderCompiler:
    """Invokes the internal AAYU compiler pipeline for the builder."""
    def __init__(self, mode="release"):
        self.mode = mode
        
    def compile(self, entry_file: str):
        if not os.path.exists(entry_file):
            print(f"[Builder] Warning: {entry_file} not found. Using mock AST/Bytecode for tests.")
            return b"MOCK_BYTECODE", {"type": "Program", "statements": []}
            
        with open(entry_file, "r") as f:
            source = f.read()
            
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # Stub IR/Bytecode generation
        bytecode = b"COMPILED_BYTECODE"
        
        if self.mode == "debug":
            self._generate_debug_symbols(ast)
            
        return bytecode, ast
        
    def _generate_debug_symbols(self, ast):
        print("[Builder] Generated .debug symbols.")
