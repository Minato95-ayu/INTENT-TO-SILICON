import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from intent_engine.v2.engine import IntentEngine
from intent_engine.v2.tokenizer.tokenizer import Tokenizer
from intent_engine.v2.semantic.semantic import SemanticAnalyzer
from intent_engine.v2.graph.knowledge_graph import KnowledgeGraph
from intent_engine.v2.resolver.constraint_resolver import ConstraintResolver

class TestIntentEnginev2(unittest.TestCase):
    def setUp(self):
        self.engine = IntentEngine()

    def test_tokenizer_multi_intent(self):
        tokenizer = Tokenizer()
        tokens = tokenizer.tokenize("Build a CRM and deploy it")
        self.assertEqual(len(tokens), 2)
        self.assertIn("build", tokens[0])
        self.assertIn("deploy", tokens[1])

    def test_semantic_analyzer(self):
        analyzer = SemanticAnalyzer()
        tokens = [["build", "a", "crm"], ["deploy", "on", "kubernetes"]]
        entities, actions, requirements = analyzer.analyze(tokens)
        self.assertIn("crm", entities)
        self.assertIn("build", actions)
        self.assertIn("deploy", actions)
        self.assertEqual(requirements.get("deployment"), "kubernetes")

    def test_knowledge_graph_enrichment(self):
        kg = KnowledgeGraph()
        base_graph = {"entities": ["crm"], "actions": ["build"]}
        enriched = kg.enrich(base_graph)
        self.assertIn("database", enriched["entities"])
        self.assertIn("api", enriched["entities"])
        self.assertIn("ui", enriched["entities"])

    def test_constraint_resolver(self):
        cr = ConstraintResolver()
        graph = {"entities": ["crm"], "actions": ["deploy"]}
        resolved = cr.resolve(graph)
        self.assertIn("api", resolved["entities"])

    def test_intent_engine_end_to_end(self):
        prompt = "Build a CRM with authentication and deploy on Kubernetes"
        ir = self.engine.process_prompt(prompt)
        
        self.assertIn("crm", ir["entities"])
        self.assertIn("api", ir["entities"])
        self.assertIn("database", ir["entities"])
        
        self.assertIn("build", ir["actions"])
        self.assertIn("deploy", ir["actions"])
        
        self.assertEqual(ir["non_functional"].get("security"), "high")
        self.assertEqual(ir["non_functional"].get("deployment"), "kubernetes")

if __name__ == '__main__':
    unittest.main()
