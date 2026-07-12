import os

test_path = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests\test_v1_1_sprint.py'
with open(test_path, 'w', encoding='utf-8') as f:
    f.write('''\
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intent_engine.intent_ir import IntentIR
from intent_engine.knowledge_graph import KnowledgeGraph
from brainos.validator import Validator

class TestV11Sprint(unittest.TestCase):
    def test_intent_ir_schema(self):
        ir = IntentIR()
        data = ir.to_dict()
        self.assertIn("goal", data)
        self.assertIn("non_functional", data)
        self.assertIn("workflows", data)
        self.assertEqual(data["confidence"], 0.0)

    def test_knowledge_graph_resolution(self):
        kg = KnowledgeGraph()
        # Mocking a semantic graph node
        class MockNode:
            def __init__(self, t, p):
                self.token = t
                self.pos = p
        
        class MockSGraph:
            def __init__(self):
                self.nodes = [MockNode("database", "NOUN"), MockNode("fast", "ADJ")]
                
        sgraph = MockSGraph()
        resolved = kg.resolve(sgraph)
        
        self.assertTrue(any(n.entity == "database" for n in resolved))
        db_node = next(n for n in resolved if n.entity == "database")
        self.assertIn("host", db_node.fields)

    def test_validator(self):
        v = Validator()
        res = v.validate({"modules": [], "security_level": "standard"})
        self.assertTrue(res["is_valid"])
        
        res_fail = v.validate({"security_level": "low"})
        self.assertFalse(res_fail["is_valid"])
        self.assertIn("Missing modules", res_fail["issues"][0])

if __name__ == "__main__":
    unittest.main()
'''
)
print("Created v1.1 tests")
