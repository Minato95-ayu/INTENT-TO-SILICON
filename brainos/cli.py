import argparse
import os
import json
from brainos.storage import SQLiteDriver
from brainos.core import GraphEngine, ContextEngine, DecisionEngine, TaskScheduler

def init_brain(args):
    os.makedirs(".brain", exist_ok=True)
    db_path = os.path.join(".brain", "brain.db")
    storage = SQLiteDriver(db_path)
    storage.setup()
    print("Initialized BrainOS in .brain/")

def get_engine():
    db_path = os.path.join(".brain", "brain.db")
    if not os.path.exists(db_path):
        print("Error: BrainOS not initialized. Run 'brain init' first.")
        exit(1)
    storage = SQLiteDriver(db_path)
    return GraphEngine(storage)

def add_node(args):
    engine = get_engine()
    data = json.loads(args.data) if args.data else {}
    node_id = engine.create_node(args.type, args.name, data)
    print(f"Added node '{args.name}' (type: {args.type}) with ID: {node_id}")

def add_edge(args):
    engine = get_engine()
    from_node = engine.get_node_by_name(args.from_name)
    to_node = engine.get_node_by_name(args.to_name)
    
    if not from_node:
        print(f"Error: Source node '{args.from_name}' not found.")
        return
    if not to_node:
        print(f"Error: Target node '{args.to_name}' not found.")
        return
        
    edge_id = engine.create_edge(from_node["id"], to_node["id"], args.relation)
    print(f"Added edge ({args.from_name} -[{args.relation}]-> {args.to_name}) with ID: {edge_id}")

def impact(args):
    engine = get_engine()
    result = engine.impact_analysis(args.node_name)
    
    if "error" in result:
        print(result["error"])
        return
        
    target = result["target"]
    affected = result["affected"]
    
    print(f"Target: {target['name']} ({target['type']})\n")
    print("Affected nodes:")
    if not affected:
        print("  None")
    for node in affected:
        print(f"  - {node['name']} ({node['type']})")

def context(args):
    engine = get_engine()
    context_engine = ContextEngine(engine)
    
    os.makedirs(os.path.join(".brain", "exports"), exist_ok=True)
    out_path = os.path.join(".brain", "exports", "bundle.json")
    
    bundle = context_engine.export_bundle(args.node_name, out_path)
    if "error" in bundle:
        print(bundle["error"])
    else:
        print(f"Generated Context Bundle for '{args.node_name}' at {out_path}")

def freeze(args):
    engine = get_engine()
    decision_engine = DecisionEngine(engine)
    node_id = decision_engine.freeze(args.decision_name)
    
    # Check if there are things to freeze implicitly or just log it
    print(f"Decision '{args.decision_name}' has been FROZEN. (Node ID: {node_id})")

def modify(args):
    engine = get_engine()
    decision_engine = DecisionEngine(engine)
    
    result = decision_engine.check_conflict(args.node_name)
    if result["conflict"]:
        print(f"[BLOCKED] Operation Blocked\n")
        print("Reason:")
        for d in result["decisions"]:
            print(f" - Violates frozen decision: '{d['name']}'")
        
        print("\nAffected Components:")
        for a in result["impact"]:
            print(f" - {a['name']} ({a['type']})")
    else:
        print(f"[ALLOWED] Modification allowed on '{args.node_name}'. No frozen decisions violated.")

def status(args):
    engine = get_engine()
    scheduler = TaskScheduler(engine)
    stat = scheduler.get_status()
    
    print("Project: AAYU")
    print(f"Progress: {stat['progress_percent']}%")
    print(f"Open Tasks: {stat['open_tasks']}")
    print(f"Blocked Tasks: {stat['blocked_tasks']}")
    print(f"Frozen Decisions: {stat['frozen_decisions']}")

def main():
    parser = argparse.ArgumentParser(description="BrainOS CLI")
    subparsers = parser.add_subparsers(dest="command")

    # init
    init_parser = subparsers.add_parser("init", help="Initialize BrainOS in the current directory")
    init_parser.set_defaults(func=init_brain)

    # add-node
    add_node_parser = subparsers.add_parser("add-node", help="Add a node to the graph")
    add_node_parser.add_argument("type", help="Node type (e.g., Component, Decision)")
    add_node_parser.add_argument("name", help="Node name")
    add_node_parser.add_argument("--data", help="JSON string of additional data", default="")
    add_node_parser.set_defaults(func=add_node)

    # add-edge
    add_edge_parser = subparsers.add_parser("add-edge", help="Add an edge to the graph")
    add_edge_parser.add_argument("from_name", help="Source node name")
    add_edge_parser.add_argument("relation", help="Relation (e.g., depends_on)")
    add_edge_parser.add_argument("to_name", help="Target node name")
    add_edge_parser.set_defaults(func=add_edge)

    # impact
    impact_parser = subparsers.add_parser("impact", help="Run impact analysis")
    impact_parser.add_argument("node_name", help="Node to analyze")
    impact_parser.set_defaults(func=impact)
    
    # context
    context_parser = subparsers.add_parser("context", help="Generate a context bundle")
    context_parser.add_argument("node_name", help="Target node name")
    context_parser.set_defaults(func=context)

    # freeze
    freeze_parser = subparsers.add_parser("freeze", help="Freeze a decision")
    freeze_parser.add_argument("decision_name", help="Name of the decision to freeze")
    freeze_parser.set_defaults(func=freeze)

    # modify
    modify_parser = subparsers.add_parser("modify", help="Check if a component can be modified safely")
    modify_parser.add_argument("node_name", help="Name of the component to modify")
    modify_parser.set_defaults(func=modify)

    # status
    status_parser = subparsers.add_parser("status", help="Show project status")
    status_parser.set_defaults(func=status)

    args = parser.parse_args()
    if args.command:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
