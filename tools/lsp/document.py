from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.errors import CompilerError

class Document:
    """Represents a single file, caching its Tokens, AST, and Semantic Result."""
    
    def __init__(self, uri: str, text: str):
        self.uri = uri
        self.text = text
        self.version = 0
        
        # Cached representations
        self.tokens = None
        self.ast = None
        self.semantic_result = None
        self.diagnostics = []
        
        self.parse()
        
    def update(self, text: str, version: int = None):
        self.text = text
        if version is not None:
            self.version = version
        else:
            self.version += 1
            
        self.parse()
        
    def parse(self):
        """Runs the compiler pipeline to generate cached state and diagnostics."""
        self.diagnostics = []
        self.tokens = None
        self.ast = None
        self.semantic_result = None
        
        try:
            lexer = Lexer(self.text)
            self.tokens = lexer.tokenize()
            
            parser = Parser(self.tokens)
            self.ast = parser.parse()
            
            analyzer = SemanticAnalyzer()
            analyzer.analyze(self.ast)
            
            # Semantic analyzer might store scope info here for completion/hover
            self.semantic_result = analyzer
            
        except CompilerError as e:
            # Catch strict compiler errors and format them as Diagnostics
            self.diagnostics.append({
                "range": {
                    "start": {"line": e.line - 1, "character": e.column - 1},
                    # Best effort length, defaults to 1 if we don't have exact token length
                    "end": {"line": e.line - 1, "character": e.column}
                },
                "severity": 1, # Error
                "message": e.message,
                "source": "aayu"
            })
        except Exception as e:
            # Fallback for unexpected crashes
            self.diagnostics.append({
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 0, "character": 1}
                },
                "severity": 1,
                "message": f"Internal Compiler Error: {str(e)}",
                "source": "aayu"
            })
