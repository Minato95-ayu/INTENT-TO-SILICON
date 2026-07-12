import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.semantic.errors import SemanticError

class TestSemanticAnalyzer(unittest.TestCase):
    def test_valid_state_declaration(self):
        code = "state counter = 0"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_ast = analyzer.analyze(ast)
        
        # Should have one symbol in global scope
        self.assertIn("counter", analyzer.global_scope.symbols)
        
    def test_duplicate_state_declaration(self):
        code = '''
        state counter = 0
        state counter = 1
        '''
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            analyzer.analyze(ast)
            
        self.assertIn("Duplicate declaration of 'counter'", str(context.exception))

    def test_undefined_variable_assignment(self):
        code = "unknown = 1"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            analyzer.analyze(ast)
            
        self.assertIn("Undefined variable 'unknown'", str(context.exception))

if __name__ == '__main__':
    unittest.main()
