import os

test_ie = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests\test_intent_engine.py'
with open(test_ie, 'w', encoding='utf-8') as f:
    f.write('''\
import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intent_engine.offline_nlp import OfflineNLPEngine
from intent_engine.intent_ir import IntentIR
from intent_engine.knowledge_graph import KnowledgeGraph

class TestIntentEngine(unittest.TestCase):
    def test_offline_nlp_tokenization(self):
        nlp = OfflineNLPEngine()
        tokens = nlp.tokenizer.tokenize("Build a global CRM system")
        self.assertIn("Build", tokens)
        self.assertIn("CRM", tokens)

    def test_knowledge_graph_domain_resolution(self):
        kg = KnowledgeGraph()
        # Mocking semantic node resolution for the new API
        class MockNode:
            def __init__(self, t, p):
                self.token = t
                self.pos = p
                self.dependencies = []
        
        class MockSGraph:
            def __init__(self):
                self.nodes = [MockNode("database", "NOUN")]
                
        sgraph = MockSGraph()
        resolved = kg.resolve(sgraph)
        self.assertTrue(any(r.entity == "database" for r in resolved))

    def test_intent_ir_integration(self):
        ir = IntentIR()
        ir.goal = "Create an API"
        self.assertEqual(ir.to_dict()["goal"], "Create an API")

if __name__ == "__main__":
    unittest.main()
''')
print("Updated test_intent_engine.py")
