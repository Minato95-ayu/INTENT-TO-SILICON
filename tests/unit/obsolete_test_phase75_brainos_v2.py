import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brainos.v2.pipeline import BrainOSPipeline
from brainos.v2.agents.planner import PlannerAgent
from brainos.v2.agents.architect import ArchitectAgent
from brainos.v2.agents.reviewer import ReviewerAgent
from brainos.v2.agents.optimizer import OptimizerAgent
from brainos.v2.agents.validator import ValidatorAgent
from brainos.v2.agents.executor import ExecutorAgent

class TestBrainOSv2(unittest.TestCase):
    def setUp(self):
        self.mock_intent = {
            "entities": ["database", "api", "frontend"],
            "actions": ["create", "deploy"],
            "non_functional": {
                "security": "high",
                "scalability": "high"
            }
        }
        self.planner = PlannerAgent()
        self.architect = ArchitectAgent()
        self.reviewer = ReviewerAgent()
        self.optimizer = OptimizerAgent()
        self.validator = ValidatorAgent()
        self.executor = ExecutorAgent()
        self.pipeline = BrainOSPipeline()

    def test_planner_agent(self):
        plan = self.planner.execute(self.mock_intent)
        self.assertIn("roadmap", plan)
        phases = [step["phase"] for step in plan["roadmap"]]
        self.assertEqual(phases, ["Data Layer", "API Layer", "Presentation Layer"])

    def test_architect_agent(self):
        plan = self.planner.execute(self.mock_intent)
        arch = self.architect.execute(plan)
        self.assertIn("modules", arch["architecture"])
        self.assertIn("database", arch["architecture"]["modules"])
        self.assertIn("api", arch["architecture"]["modules"])
        self.assertIn("ui", arch["architecture"]["modules"])

    def test_reviewer_agent(self):
        plan = self.planner.execute(self.mock_intent)
        arch = self.architect.execute(plan)
        review = self.reviewer.execute(arch)
        self.assertIn("reviews", review)
        self.assertTrue(any(r["type"] == "security" for r in review["reviews"]))
        self.assertTrue(any(r["type"] == "scalability" for r in review["reviews"]))

    def test_optimizer_agent(self):
        plan = self.planner.execute(self.mock_intent)
        arch = self.architect.execute(plan)
        review = self.reviewer.execute(arch)
        opt = self.optimizer.execute(review)
        self.assertIn("optimizations_applied", opt)
        self.assertTrue(len(opt["optimizations_applied"]) > 0)
        self.assertIn("strict_env_only", opt["architecture"].get("security_policy", ""))

    def test_validator_agent(self):
        plan = self.planner.execute(self.mock_intent)
        arch = self.architect.execute(plan)
        review = self.reviewer.execute(arch)
        opt = self.optimizer.execute(review)
        is_valid = self.validator.execute(opt)
        self.assertTrue(is_valid)

    def test_executor_agent(self):
        plan = self.planner.execute(self.mock_intent)
        arch = self.architect.execute(plan)
        review = self.reviewer.execute(arch)
        opt = self.optimizer.execute(review)
        self.assertTrue(self.validator.execute(opt))
        result = self.executor.execute(opt)
        self.assertEqual(result["status"], "success")
        self.assertIn("generated_files", result)

    def test_pipeline_integration(self):
        result = self.pipeline.process_intent(self.mock_intent)
        self.assertEqual(result["status"], "success")
        self.assertIn("src/db/schema.aayu", result["generated_files"])
        self.assertIn("src/main.aayu", result["generated_files"])

if __name__ == '__main__':
    unittest.main()
