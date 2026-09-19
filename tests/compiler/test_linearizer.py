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
from compiler.ir.optimizer import SSAOptimizer
from compiler.ir.linearizer import Linearizer

class TestLinearizer(unittest.TestCase):
    def get_linear_mir(self, code: str):
        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)
        pipeline = IRPipeline()
        cfg = pipeline.to_ssa_cfg(semantic_ast)
        SSAOptimizer(cfg).optimize()
        return Linearizer(cfg).lower()

    def test_phi_elimination_and_linearization(self):
        code = """
        let x = 10
        if true
            x = 20
        else
            x = 30
        end
        print(x)
        """
        mir = self.get_linear_mir(code)
        opcodes = [inst.opcode for inst in mir]
        
        # Phi should be gone!
        self.assertNotIn("PHI", opcodes)
        
        # JUMP_IF_FALSE must exist for Branch
        self.assertIn("JUMP_IF_FALSE", opcodes)
        
        # Ensure we have LABELS
        self.assertIn("LABEL", opcodes)
        
        # Test copy insertion mapped to LOAD_VAR / SET_STATE
        self.assertIn("LOAD_VAR", opcodes)
        self.assertIn("SET_STATE", opcodes)

    def test_end_to_end_optimized_math(self):
        code = """
        let x = 10 + 20
        print(x)
        """
        mir = self.get_linear_mir(code)
        opcodes = [inst.opcode for inst in mir]
        
        # The math is folded! We should NOT see BINARY_OP
        self.assertNotIn("BINARY_OP", opcodes)
        
        # We should see OP_ASYNC_CALL for print
        self.assertIn("OP_ASYNC_CALL", opcodes)
        
        # The print should have pushed 30
        push_insts = [i for i in mir if i.opcode == "PUSH_CONST"]
        self.assertEqual(len(push_insts), 1)
        self.assertEqual(push_insts[0].operands[0], 30)
        
    def test_block_serialization(self):
        code = """
        let x = 10
        print(x)
        """
        mir = self.get_linear_mir(code)
        labels = [i for i in mir if i.opcode == "LABEL"]
        # There's only one block, entry_main
        self.assertEqual(len(labels), 1)
        self.assertEqual(labels[0].operands[0], "entry_main")

if __name__ == '__main__':
    unittest.main()
