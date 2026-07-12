import os

test_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests'
os.makedirs(test_dir, exist_ok=True)

test_content = '''
import unittest
import sys
import os

# Add intent_engine to path for testing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../intent_engine')))

from offline_nlp import OfflineNLP
from knowledge_graph import KnowledgeGraph
from clarification_engine import ClarificationEngine
from intent_ir import IntentIR

class TestIntentEngine(unittest.TestCase):
    
    # 1. Unit Tests
    def test_offline_nlp_tokenization(self):
        nlp = OfflineNLP()
        tokens = nlp.tokenize("Build a global CRM system")
        self.assertIn("build", tokens)
        self.assertIn("global", tokens)
        self.assertIn("crm", tokens)
        self.assertIn("system", tokens)
        self.assertNotIn("a", tokens) # Stop word removed
        
    def test_knowledge_graph_domain_resolution(self):
        kg = KnowledgeGraph()
        self.assertEqual(kg.resolve_domain("I need a hospital app"), "hospital")
        self.assertEqual(kg.resolve_domain("Build an ecommerce platform"), "ecommerce")
        self.assertEqual(kg.resolve_domain("Something unknown"), "generic")
        
    def test_clarification_engine(self):
        ce = ClarificationEngine()
        # Ecommerce missing required properties
        missing = ce.check_missing_requirements("ecommerce", "Build an ecommerce app")
        self.assertIn("Payment Gateway", missing)
        self.assertIn("Inventory System", missing)
        
        # Ecommerce with properties fulfilled
        missing_none = ce.check_missing_requirements("ecommerce", "Build an ecommerce app with a payment gateway and inventory system")
        self.assertEqual(len(missing_none), 0)

    # 2. Integration Tests
    def test_intent_ir_integration(self):
        ir = IntentIR()
        intent = "Build a global CRM system with high read throughput"
        result = ir.parse(intent)
        
        self.assertEqual(result["domain"], "crm")
        self.assertIn("Build", result["actions"])
        self.assertIn("HighReadThroughput", result["constraints"])
        self.assertIn("Customer", result["entities"])
        self.assertIn("Cache", result["architecture"])
        self.assertIn("Email Integration", result["clarifications_needed"])

if __name__ == '__main__':
    unittest.main()
'''

with open(os.path.join(test_dir, "test_intent_engine.py"), "w", encoding="utf-8") as f:
    f.write(test_content.strip() + "\\n")

print("Automated tests created for Intent Engine.")
