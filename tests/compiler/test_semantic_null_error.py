import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.semantic.type_inference import TypeInference
from compiler.semantic.type_checker import TypeChecker
from compiler.semantic.errors import TypeError

class TestSemanticNullError(unittest.TestCase):
    def test_assign_null_to_strict_primitive(self):
        code = """
        action test()
            let x = 10
            x = null
        end
        """
        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        
        analyzer = SemanticAnalyzer()
        semantic_ast = analyzer.analyze(ast)
        
        TypeInference().infer(semantic_ast)
        
        with self.assertRaises(TypeError) as ctx:
            TypeChecker().check(semantic_ast)
            
        self.assertIn("Cannot assign Null to Integer", str(ctx.exception))

    def test_assign_null_to_untyped(self):
        code = """
        action test()
            let x = null
            x = 10
        end
        """
        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        
        analyzer = SemanticAnalyzer()
        semantic_ast = analyzer.analyze(ast)
        
        TypeInference().infer(semantic_ast)
        
        # Should not raise
        TypeChecker().check(semantic_ast)

if __name__ == "__main__":
    unittest.main()
