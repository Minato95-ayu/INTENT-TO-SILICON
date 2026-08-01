import unittest
from aayu.compiler.ir.lir import LIRNode
from aayu.compiler.optimizer.optimizer import Optimizer
from aayu.compiler.optimizer.passes import DeadCodeElimination

class TestOptimizer(unittest.TestCase):
    def test_dead_code_elimination(self):
        lir = [
            LIRNode("STATE_INIT", ["a", "1"]),
            LIRNode("STATE_INIT", ["b", "2"]), # 'b' is never used
            LIRNode("STATE_GET", ["a"]),
            LIRNode("CALL", ["print"])
        ]
        
        optimizer = Optimizer()
        optimizer.register_pass(DeadCodeElimination())
        
        optimized_lir = optimizer.optimize(lir)
        
        # 'b' should be removed
        opcodes = [n.opcode for n in optimized_lir]
        self.assertEqual(len(optimized_lir), 3)
        self.assertNotIn("b", [n.operands[0] for n in optimized_lir if n.opcode == "STATE_INIT"])

if __name__ == '__main__':
    unittest.main()
