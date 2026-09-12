import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.hir import HIRNode
from compiler.ir.mir import MIRNode
from compiler.ir.lir import LIRNode

class TestIRPipeline(unittest.TestCase):
    def test_ir_lowering_pipeline(self):
        code = "state counter = 0"
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        semantic_ast = SemanticAnalyzer().analyze(parser.parse())
        
        pipeline = IRPipeline()
        hir = pipeline.to_hir(semantic_ast)
        mir = pipeline.to_mir(hir)
        lir = pipeline.to_lir(mir)
        
        self.assertIsInstance(hir[0], HIRNode)
        self.assertIsInstance(mir[0], MIRNode)
        self.assertIsInstance(lir[0], LIRNode)
        
        # LIR generates PUSH_CONST and STORE_STATE in a stack machine
        opcodes = [n.opcode for n in lir]
        self.assertIn("PUSH_CONST", opcodes)
        self.assertIn("STATE_INIT", opcodes)

if __name__ == "__main__":
    unittest.main()

