import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.semantic.errors import SemanticError

class TestSemanticAnalyzer(unittest.TestCase):
    def test_duplicate_state_declaration(self):
        code = """
        state counter = 0
        state counter = 1
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            analyzer.analyze(ast)
            
        self.assertIn("Duplicate declaration", str(context.exception))

    def test_valid_state_declaration(self):
        code = "state counter = 0"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_ast = analyzer.analyze(ast)
        self.assertIsNotNone(semantic_ast)

    def test_undeclared_identifier_read(self):
        code = """
        action do_something()
            print(unknown)
        end
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            analyzer.analyze(ast)
        self.assertIn("Undeclared identifier 'unknown'", str(context.exception))

    def test_undeclared_identifier_assignment(self):
        code = """
        action do_something()
            unknown = 1
        end
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            analyzer.analyze(ast)
        self.assertIn("Undeclared identifier 'unknown'", str(context.exception))

    def test_let_declaration(self):
        code = """
        action do_something()
            let x = 1
            x = x + 5
        end
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_ast = analyzer.analyze(ast)
        self.assertIsNotNone(semantic_ast)

if __name__ == "__main__":
    unittest.main()
