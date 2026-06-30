from ..task.task import Task
from ..task.graph import TaskGraph

class Planner:
    def __init__(self):
        pass
        
    def plan(self, goal: str) -> TaskGraph:
        """
        In MVP, this just returns a hardcoded task graph based on the goal.
        Future: Will call LLM to generate the graph.
        """
        graph = TaskGraph()
        
        if "Phase 5.1" in goal or "Type AST" in goal:
            t1 = Task(id="T1", description="Implement TypeNode hierarchy in type_nodes.py")
            t2 = Task(id="T2", description="Update ast_nodes.py to support type_annotation and return_type", dependencies=["T1"])
            t3 = Task(id="T3", description="Update parser.py to parse type annotations", dependencies=["T2"])
            graph.add_task(t1)
            graph.add_task(t2)
            graph.add_task(t3)
        elif "Phase 5.2" in goal or "Symbol Types" in goal:
            t1 = Task(id="T1", description="Update symbols.py with declared_type and resolved_type")
            t2 = Task(id="T2", description="Update scope_builder.py to bind AST types to Symbols", dependencies=["T1"])
            t3 = Task(id="T3", description="Upgrade BrainOS Critic to enforce Documentation Sync", dependencies=["T2"])
            graph.add_task(t1)
            graph.add_task(t2)
            graph.add_task(t3)
        else:
            task = Task(
                id="T1",
                description=f"Implement goal: {goal}"
            )
            graph.add_task(task)
            
        graph._update_ready_tasks()
        return graph
