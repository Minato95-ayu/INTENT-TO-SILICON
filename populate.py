import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from brainos.storage import SQLiteDriver
from brainos.core import GraphEngine, TaskScheduler

def populate():
    storage = SQLiteDriver(".brain/brain.db")
    engine = GraphEngine(storage)
    
    engine.create_node("Task", "Compiler Loops", {"status": "Done"})
    engine.create_node("Task", "Compiler Variables", {"status": "Open"})
    engine.create_node("Task", "Compiler Arrays", {"status": "Blocked"})
    
    t_loops = engine.get_node_by_name("Compiler Loops")
    t_vars = engine.get_node_by_name("Compiler Variables")
    t_arrays = engine.get_node_by_name("Compiler Arrays")
    
    engine.create_edge(t_arrays["id"], t_vars["id"], "depends_on")
    engine.create_edge(t_vars["id"], t_loops["id"], "depends_on")

    scheduler = TaskScheduler(engine)
    stat = scheduler.get_status()
    print("Project: AAYU")
    print(f"Progress: {stat['progress_percent']}%")
    print(f"Open Tasks: {stat['open_tasks']}")
    print(f"Blocked Tasks: {stat['blocked_tasks']}")
    print(f"Frozen Decisions: {stat['frozen_decisions']}")

if __name__ == "__main__":
    populate()
