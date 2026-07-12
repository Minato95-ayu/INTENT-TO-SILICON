import os

brainos_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\brainos'

# validator.py
with open(os.path.join(brainos_dir, 'validator.py'), 'w', encoding='utf-8') as f:
    f.write('''\
class Validator:
    def validate(self, architecture_spec):
        """
        Validates the architecture spec before execution.
        Must check: Architecture, Dependencies, Security, Performance, Scalability, Compilation.
        """
        issues = []
        
        # Check architecture validity
        if "modules" not in architecture_spec:
            issues.append("Missing modules configuration.")
            
        # Check circular dependencies (mock logic for demo)
        deps = architecture_spec.get("dependencies", {})
        if "circular" in deps:
            issues.append("Circular dependency detected.")
            
        # Check security
        if architecture_spec.get("security_level") == "low":
            issues.append("Security level too low for production.")
            
        return {
            "is_valid": len(issues) == 0,
            "issues": issues
        }
''')

# orchestrator.py
with open(os.path.join(brainos_dir, 'orchestrator.py'), 'w', encoding='utf-8') as f:
    f.write('''\
from .production_review import ProductionReview
from .scaling_advisor import ScalingAdvisor
from .validator import Validator

class BrainOSOrchestrator:
    def __init__(self):
        self.reviewer = ProductionReview()
        self.optimizer = ScalingAdvisor()
        self.validator = Validator()
        # Planner and Architect logic can be represented as static methods for now
        
    def plan(self, intent_ir):
        return {"roadmap": ["Design DB", "Design API"]}
        
    def architect(self, plan, intent_ir):
        return {
            "modules": intent_ir.entities,
            "security_level": intent_ir.non_functional.get("security", "standard"),
            "technologies": ["fastapi"] if "api" in intent_ir.entities else []
        }
        
    def run_pipeline(self, intent_ir):
        # 1. Planner
        plan = self.plan(intent_ir)
        # 2. Architect
        arch = self.architect(plan, intent_ir)
        # 3. Reviewer
        review = self.reviewer.evaluate(arch)
        # 4. Optimizer
        opt = self.optimizer.advise({"requests_per_second": 5000}) # arbitrary
        arch["scaling"] = opt
        arch["review"] = review
        # 5. Validator
        val = self.validator.validate(arch)
        
        return {
            "architecture": arch,
            "is_valid": val["is_valid"],
            "validation_issues": val["issues"]
        }
''')

print("Created Phase 2 BrainOS Files")
