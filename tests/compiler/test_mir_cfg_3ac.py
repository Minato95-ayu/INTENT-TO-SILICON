import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.mir import Value
from compiler.ir.mir_cfg import CFG, BasicBlock, Jump, Branch, Return

class TestMIRCFG3AC(unittest.TestCase):
    def get_cfg(self, code: str) -> CFG:
        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)
        pipeline = IRPipeline()
        return pipeline.to_cfg(semantic_ast)

    def test_3ac_value_invariants(self):
        code = """
        let a = 5
        let b = 10
        let x = a + b
        """
        cfg = self.get_cfg(code)
        entry = cfg.entry_block
        
        # entry should have 5 instructions: 
        # CONST 5, STORE a
        # CONST 10, STORE b
        # LOAD a, LOAD b, BINARY_+, STORE x
        # Wait, let's just find the BINARY_+ instruction.
        add_inst = next(i for i in entry.instructions if i.opcode == "BINARY_+")
        
        # Test 1: ADD instruction produces a result Value
        self.assertIsInstance(add_inst.result, Value)
        
        # Test 2: The result's defining instruction is the ADD instruction itself
        self.assertEqual(add_inst.result.defining_inst, add_inst)
        
        # Test 3: The subsequent STORE_VAR uses the exact same Value
        store_inst = next(i for i in entry.instructions if i.opcode == "STORE_VAR" and i.operands[0] == "x")
        self.assertEqual(store_inst.operands[1], add_inst.result)

    def test_branch_terminator_uses_value(self):
        code = """
        if true
            print("yes")
        end
        """
        cfg = self.get_cfg(code)
        entry = cfg.entry_block
        
        # Test: Branch terminator consumes a Value (not a string placeholder)
        term = entry.terminator
        self.assertIsInstance(term, Branch)
        self.assertIsInstance(term.condition, Value)
        
        # Test: The condition value is defined by an instruction in the entry block
        cond_inst = term.condition.defining_inst
        self.assertIn(cond_inst, entry.instructions)
        self.assertEqual(cond_inst.opcode, "CONST")

if __name__ == '__main__':
    unittest.main()


