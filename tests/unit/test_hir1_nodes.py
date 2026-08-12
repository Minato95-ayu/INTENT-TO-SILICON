import unittest
from aayu.compiler.hir.nodes import (
    HIRLiteral, HIRVariable, HIRAssignment, HIRBinary, HIRUnary, 
    HIRReturn, HIRCall, HIRStructInit, HIRStructFieldAccess, 
    HIREnumValue, HIRBlock, HIRAction, HIRModule
)

class TestHIR1Nodes(unittest.TestCase):
    def test_literal_node(self):
        node = HIRLiteral(origin_node_id=1, type_id="Int", value=42)
        self.assertEqual(node.value, 42)
        self.assertEqual(node.type_id, "Int")
        self.assertEqual(node.origin_node_id, 1)
        self.assertTrue(hasattr(node, "hir_node_id"))

    def test_variable_node(self):
        node = HIRVariable(origin_node_id=2, type_id="String", name="user", is_global=False)
        self.assertEqual(node.name, "user")
        self.assertFalse(node.is_global)

    def test_assignment_node(self):
        target = HIRVariable(origin_node_id=3, type_id="Int", name="x", is_global=False)
        val = HIRLiteral(origin_node_id=4, type_id="Int", value=100)
        assign = HIRAssignment(origin_node_id=5, target=target, value=val)
        self.assertEqual(assign.target.name, "x")
        self.assertEqual(assign.value.value, 100)

    def test_binary_node(self):
        left = HIRLiteral(origin_node_id=6, type_id="Int", value=5)
        right = HIRLiteral(origin_node_id=7, type_id="Int", value=10)
        bin_op = HIRBinary(origin_node_id=8, type_id="Int", operator="+", left=left, right=right)
        self.assertEqual(bin_op.operator, "+")

    def test_block_and_action(self):
        stmt = HIRReturn(origin_node_id=9, value=HIRLiteral(origin_node_id=10, type_id="Int", value=0))
        block = HIRBlock(origin_node_id=11, statements=[stmt])
        action = HIRAction(origin_node_id=12, name="main", body=block)
        self.assertEqual(action.name, "main")
        self.assertEqual(len(action.body.statements), 1)

if __name__ == '__main__':
    unittest.main()
