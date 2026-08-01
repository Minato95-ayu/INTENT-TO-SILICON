import unittest
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.ir.hir import HIRNode
from aayu.compiler.ir.mir import MIRNode
from aayu.compiler.ir.lir import LIRNode

class TestIRPipeline(unittest.TestCase):
    def test_ir_lowering_pipeline(self):
        code = "state counter = 0"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        semantic_ast = SemanticAnalyzer().analyze(parser.parse())
        
        pipeline = IRPipeline()
        
        # 1. Lower to HIR
        hir = pipeline.to_hir(semantic_ast)
        self.assertIsInstance(hir[0], HIRNode)
        
        # 2. Lower to MIR
        mir = pipeline.to_mir(hir)
        self.assertIsInstance(mir[0], MIRNode)
        
        # 3. Lower to LIR
        lir = pipeline.to_lir(mir)
        self.assertIsInstance(lir[0], LIRNode)
        
        # In LIR, it should look like an SSA assignment
        self.assertEqual(lir[0].opcode, "STATE_INIT")
        self.assertEqual(lir[0].operands[0], "counter")
        self.assertEqual(lir[0].operands[1], "0")

if __name__ == '__main__':
    unittest.main()
