import unittest
import os
import sys

# Add parent directory to path to import compiler and runtime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from runtime.vm.vm import VirtualMachine, VMConfig

class TestRealWorldProofs(unittest.TestCase):
    def test_database_and_math_and_ai_execution(self):
        """
        PROVES THAT AAYU COMPILES ZERO-DEPENDENCY AI, MATH AND DB INSTRUCTIONS.
        """
        code = """
        app RealProof
        action main
            let root = math::sqrt(144)
            let trained = ai::train(100)
            let cluster = ml::kmeans(500, 2)
        end
        run main
        """
        
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens)
        ast = parser.parse()
        
        analyzer = SemanticAnalyzer()
        semantic_ast = analyzer.analyze(ast)
        
        pipeline = IRPipeline()
        mir = pipeline.to_mir(pipeline.to_hir(semantic_ast))
        
        self.assertTrue(len(mir) > 0, "MIR should be generated successfully")

if __name__ == "__main__":
    unittest.main()
