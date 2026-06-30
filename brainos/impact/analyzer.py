from enum import Enum
from ..task.task import Task

class RegressionRisk(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class ImpactAnalyzer:
    def analyze(self, task: Task) -> RegressionRisk:
        """
        Outputs affected components and regression risk via heuristics.
        """
        # MVP: Stub heuristic
        desc = task.description.lower()
        if "compiler" in desc or "vm" in desc or "parser" in desc:
            return RegressionRisk.HIGH
        elif "runtime" in desc:
            return RegressionRisk.MEDIUM
        return RegressionRisk.LOW
