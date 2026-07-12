"""
=============================================================================
FILE: analyzer.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

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
