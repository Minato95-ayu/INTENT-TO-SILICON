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
from compiler.ir.dominators import DominatorTree

class TestDominatorAnalysis(unittest.TestCase):
    def get_dom_tree(self, code: str) -> DominatorTree:
        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)
        cfg = IRPipeline().to_cfg(semantic_ast)
        return DominatorTree(cfg)

    def test_if_else_dominance(self):
        code = """
        let x = 10
        if x > 5
            x = 20
        else
            x = 30
        end
        """
        dt = self.get_dom_tree(code)
        blocks = {b.id: b for b in dt.cfg.blocks}
        entry = blocks["entry_main"]
        then_b = blocks["then_1"]
        else_b = blocks["else_2"]
        merge_b = blocks["endif_3"]
        
        # Test DOM sets
        self.assertIn(entry, dt.doms[then_b])
        self.assertIn(entry, dt.doms[else_b])
        self.assertIn(entry, dt.doms[merge_b])
        self.assertNotIn(then_b, dt.doms[merge_b]) # Then does not dominate Merge
        self.assertNotIn(else_b, dt.doms[merge_b]) # Else does not dominate Merge
        
        # Test idom (Immediate Dominator)
        self.assertEqual(dt.idom[then_b], entry)
        self.assertEqual(dt.idom[else_b], entry)
        self.assertEqual(dt.idom[merge_b], entry)
        
        # Test Dominance Frontier (DF)
        self.assertIn(merge_b, dt.df[then_b])
        self.assertIn(merge_b, dt.df[else_b])
        self.assertNotIn(merge_b, dt.df[entry])

    def test_for_loop_dominance(self):
        code = """
        let arr = [1, 2]
        for i in arr
            print(i)
        end
        """
        dt = self.get_dom_tree(code)
        blocks = {b.id: b for b in dt.cfg.blocks}
        entry = blocks["entry_main"]
        header = blocks["loop_header_1"]
        body = blocks["loop_body_2"]
        exit_b = blocks["loop_exit_3"]
        
        # Test idom
        self.assertEqual(dt.idom[header], entry)
        self.assertEqual(dt.idom[body], header)
        self.assertEqual(dt.idom[exit_b], header)
        
        # Test Dominance Frontier
        # The backedge body -> header makes header part of body's DF
        # And header is part of its own DF because entry -> header and body -> header
        self.assertIn(header, dt.df[body])
        self.assertIn(header, dt.df[header])
        self.assertNotIn(exit_b, dt.df[body])

if __name__ == '__main__':
    unittest.main()
