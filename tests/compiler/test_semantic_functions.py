import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.semantic.errors import SemanticError

class TestSemanticAnalyzer(unittest.TestCase):
    def test_action_argument_scope(self):
        code = """
        action do_something(val)
            print(val)
        end
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_ast = analyzer.analyze(ast)
        self.assertIsNotNone(semantic_ast)
        
    def test_action_argument_leak(self):
        code = """
        action do_something(val)
            print(val)
        end
        action another()
            print(val)
        end
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            analyzer.analyze(ast)
        self.assertIn("Undeclared identifier 'val'", str(context.exception))

    def test_undeclared_function_call(self):
        code = """
        action test()
            magic_function()
        end
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            analyzer.analyze(ast)
        self.assertIn("Undeclared function 'magic_function'", str(context.exception))

    def test_call_non_function(self):
        code = """
        action test()
            let x = 1
            x()
        end
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            analyzer.analyze(ast)
        self.assertIn("Identifier 'x' is not a function", str(context.exception))

    def test_incorrect_argument_count(self):
        code = """
        action test(a, b)
            print(a)
        end
        action trigger()
            test(1)
        end
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        with self.assertRaises(SemanticError) as context:
            analyzer.analyze(ast)
        self.assertIn("Function 'test' expects 2 arguments, but got 1", str(context.exception))

if __name__ == "__main__":
    unittest.main()
