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
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.optimizer.optimizer import Optimizer

from compiler.bytecode.encoder import BytecodeEncoder
from runtime.vm.vm import VirtualMachine
from runtime.vm.config import VMConfig

class TestCompilerPipeline(unittest.TestCase):
    def test_end_to_end(self):
        code = "state user_count = 42"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        semantic = SemanticAnalyzer()
        semantic_ast = semantic.analyze(ast)
        ir_pipeline = IRPipeline()
        hir = ir_pipeline.to_hir(semantic_ast)
        mir = ir_pipeline.to_mir(hir)
        lir = ir_pipeline.to_lir(mir)
        
        encoder = BytecodeEncoder()
        program = encoder.encode(lir)
        
        vm = VirtualMachine(VMConfig.development())
        # VM loading and basic init test
        self.assertIsNotNone(vm)
        self.assertEqual(len(program.bytecode) > 0, True)

if __name__ == "__main__":
    unittest.main()

