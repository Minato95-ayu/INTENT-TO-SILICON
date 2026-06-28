from typing import Dict, Any, List, Optional
from .graph import GraphEngine

class TaskScheduler:
    def __init__(self, graph: GraphEngine):
        self.graph = graph

    def create_task(self, name: str, status: str = "Open") -> str:
        """Create a new Task node."""
        return self.graph.create_node("Task", name, {"status": status})

    def get_status(self) -> Dict[str, Any]:
        """Aggregate Project Status."""
        tasks = self.graph.storage.get_nodes_by_type("Task")
        decisions = self.graph.storage.get_nodes_by_type("Decision")
        
        open_tasks = sum(1 for t in tasks if t.get("data", {}).get("status") == "Open")
        blocked_tasks = sum(1 for t in tasks if t.get("data", {}).get("status") == "Blocked")
        done_tasks = sum(1 for t in tasks if t.get("data", {}).get("status") == "Done")
        
        frozen_decisions = sum(1 for d in decisions if d.get("data", {}).get("status") == "Frozen")
        
        total_tasks = len(tasks)
        progress = (done_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return {
            "progress_percent": round(progress, 2),
            "open_tasks": open_tasks,
            "blocked_tasks": blocked_tasks,
            "done_tasks": done_tasks,
            "frozen_decisions": frozen_decisions
        }
