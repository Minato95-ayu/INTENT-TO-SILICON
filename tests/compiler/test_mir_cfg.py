import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.mir_cfg import CFG, BasicBlock, Jump, Branch, Return

class TestMIRCFG(unittest.TestCase):
    def get_cfg(self, code: str) -> CFG:
        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)
        pipeline = IRPipeline()
        return pipeline.to_cfg(semantic_ast)

    def test_straight_line(self):
        code = """
        let x = 10
        let y = 20
        """
        cfg = self.get_cfg(code)
        self.assertEqual(len(cfg.blocks), 1)
        self.assertIsInstance(cfg.entry_block.terminator, Return)
        
    def test_if_else(self):
        code = """
        let x = 10
        if x > 5
            x = 20
        else
            x = 30
        end
        """
        cfg = self.get_cfg(code)
        # Entry, Then, Else, Merge
        self.assertEqual(len(cfg.blocks), 4)
        self.assertIsInstance(cfg.entry_block.terminator, Branch)
        self.assertIsInstance(cfg.blocks[1].terminator, Jump) # Then jumps to Merge
        self.assertIsInstance(cfg.blocks[2].terminator, Jump) # Else jumps to Merge
        self.assertIsInstance(cfg.blocks[3].terminator, Return) # Merge returns

    def test_for_loop(self):
        code = """
        let arr = [1, 2]
        for i in arr
            print(i)
        end
        """
        cfg = self.get_cfg(code)
        # Entry, Header, Body, Exit
        self.assertEqual(len(cfg.blocks), 4)
        self.assertIsInstance(cfg.entry_block.terminator, Jump)
        header = cfg.blocks[1]
        self.assertIsInstance(header.terminator, Branch)
        body = cfg.blocks[2]
        self.assertIsInstance(body.terminator, Jump)
        self.assertEqual(body.terminator.target, header) # Backedge
        exit_block = cfg.blocks[3]
        self.assertIsInstance(exit_block.terminator, Return)

    def test_early_return(self):
        code = """
        if true
            return 1
        end
        let unreachable = 2
        """
        cfg = self.get_cfg(code)
        # Check that after early return, we have proper dead blocks or early termination
        # Entry branches to Then and Merge
        then_block = cfg.blocks[1]
        self.assertIsInstance(then_block.terminator, Return)
        
if __name__ == '__main__':
    unittest.main()
