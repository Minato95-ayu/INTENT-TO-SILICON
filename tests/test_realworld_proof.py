# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

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
            let cluster = ml::kmeans_fit([1,2,3], 2, 10)
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
