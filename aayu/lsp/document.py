from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.errors import CompilerError
from .diagnostics import DiagnosticTranslator

class Document:
    def __init__(self, uri, text):
        self.uri = uri
        self.text = text
        self.tokens = []
        self.ast = None
        self.diagnostics = []
        self.parse()

    def update(self, text):
        self.text = text
        self.parse()

    def parse(self):
        self.diagnostics = []
        try:
            lexer = Lexer(self.text)
            self.tokens = lexer.tokenize()
            parser = Parser(self.tokens)
            self.ast = parser.parse()
        except CompilerError as e:
            self.diagnostics.append(DiagnosticTranslator.translate_error(e))
        except Exception as e:
            pass
            
    def get_diagnostics(self):
        return self.diagnostics
