from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class ProjectSnapshot:
    project_name: str = "AAYU Language"
    version: str = "1.0"
    milestone: str = "5A"
    phase: str = "BrainOS Foundation (Non-AI Orchestrator)"
    completed: List[str] = field(default_factory=list)
    frozen: List[str] = field(default_factory=list)
    matrix: Dict[str, str] = field(default_factory=dict)
    debt: List[str] = field(default_factory=list)
    branch: str = "feature/milestone-5"
    next_target: str = ""
    regression_risk: str = ""
