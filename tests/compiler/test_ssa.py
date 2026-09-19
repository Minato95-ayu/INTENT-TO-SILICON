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
from compiler.ir.mir import Value

class TestSSA(unittest.TestCase):
    def get_ssa(self, code: str):
        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)
        pipeline = IRPipeline()
        return pipeline.to_ssa_cfg(semantic_ast)

    def test_ssa_straight_line(self):
        code = """
        let x = 10
        let y = x
        """
        cfg = self.get_ssa(code)
        entry = cfg.entry_block
        
        # Should have CONST 10. LOAD_VAR and STORE_VAR should be GONE.
        opcodes = [i.opcode for i in entry.instructions]
        self.assertNotIn("LOAD_VAR", opcodes)
        self.assertNotIn("STORE_VAR", opcodes)

    def test_ssa_if_else(self):
        code = """
        let x = 10
        if true
            x = 20
        else
            x = 30
        end
        print(x)
        """
        cfg = self.get_ssa(code)
        
        # Verify no LOAD_VAR / STORE_VAR
        for b in cfg.blocks:
            opcodes = [i.opcode for i in b.instructions]
            self.assertNotIn("LOAD_VAR", opcodes)
            self.assertNotIn("STORE_VAR", opcodes)
            
        blocks = {b.id: b for b in cfg.blocks}
        entry = blocks["entry_main"]
        then_b = blocks["then_1"]
        else_b = blocks["else_2"]
        merge_b = blocks["endif_3"]
        
        # 1. PHI node correctly placed in merge block
        self.assertEqual(merge_b.instructions[0].opcode, "PHI")
        phi_inst = merge_b.instructions[0]
        phi_dict = phi_inst.operands[0]
        
        # 2. PHI has correct predecessors
        self.assertIn(then_b, phi_dict)
        self.assertIn(else_b, phi_dict)
        
        # 3. Print instruction consumes the exact PHI result
        print_inst = next(i for i in merge_b.instructions if i.opcode == "CALL" and i.operands[0] == "print")
        self.assertEqual(print_inst.operands[1], phi_inst.result)

    def test_ssa_for_loop(self):
        code = """
        let total = 0
        let arr = [1, 2]
        for i in arr
            total = total + i
        end
        print(total)
        """
        cfg = self.get_ssa(code)
        
        # Verify no LOAD_VAR / STORE_VAR
        for b in cfg.blocks:
            opcodes = [i.opcode for i in b.instructions]
            self.assertNotIn("LOAD_VAR", opcodes)
            self.assertNotIn("STORE_VAR", opcodes)
            
        blocks = {b.id: b for b in cfg.blocks}
        entry = blocks["entry_main"]
        header = blocks["loop_header_1"]
        body = blocks["loop_body_2"]
        exit_b = blocks["loop_exit_3"]
        
        # Header should have a PHI for total
        phi_inst = next(i for i in header.instructions if i.opcode == "PHI" and entry in i.operands[0])
        phi_dict = phi_inst.operands[0]
        self.assertIn(entry, phi_dict) # From before loop
        self.assertIn(body, phi_dict) # From backedge
if __name__ == '__main__':
    unittest.main()


