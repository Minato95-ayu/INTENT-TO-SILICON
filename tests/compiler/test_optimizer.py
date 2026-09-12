import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.optimizer import SSAOptimizer

class TestOptimizer(unittest.TestCase):
    def get_optimized_ssa(self, code: str):
        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)
        pipeline = IRPipeline()
        cfg = pipeline.to_ssa_cfg(semantic_ast)
        optimizer = SSAOptimizer(cfg)
        optimizer.optimize()
        return cfg

    def test_pure_unused_calculation_removed(self):
        code = """
        let x = 10 + 20
        """
        cfg = self.get_optimized_ssa(code)
        entry = cfg.entry_block
        # Everything should be eliminated because x is unused!
        self.assertEqual(len(entry.instructions), 0)

    def test_print_preserved(self):
        code = """
        let x = 10
        print(x)
        """
        cfg = self.get_optimized_ssa(code)
        entry = cfg.entry_block
        # We expect CONST 10 to be fully propagated into PRINT.
        # Thus, CONST 10 is eliminated because 0 uses, but PRINT(10) stays!
        self.assertEqual(len(entry.instructions), 1)
        self.assertEqual(entry.instructions[0].opcode, "CALL")
        self.assertEqual(entry.instructions[0].operands, ["print", 10])

    def test_call_preserved(self):
        """CALL instructions must survive DCE even if their result is unused,
        because they may have side effects.
        """
        code = """
        print(42)
        """
        cfg = self.get_optimized_ssa(code)
        # The CALL to print must be preserved — it has side effects.
        all_opcodes = [inst.opcode
                       for b in cfg.blocks
                       for inst in b.instructions]
        self.assertIn("CALL", all_opcodes)

    def test_constant_folding_and_propagation(self):
        code = """
        let x = 10
        let y = 20
        let z = x + y
        print(z)
        """
        cfg = self.get_optimized_ssa(code)
        entry = cfg.entry_block
        # Expected: CONST 10, CONST 20 disappear. ADD folds to CONST 30.
        # But wait, CONST 30 is propagated into PRINT, so CONST 30 is also eliminated!
        # Result: PRINT 30
        self.assertEqual(len(entry.instructions), 1)
        self.assertEqual(entry.instructions[0].opcode, "CALL")
        self.assertEqual(entry.instructions[0].operands, ["print", 30])

if __name__ == '__main__':
    unittest.main()

