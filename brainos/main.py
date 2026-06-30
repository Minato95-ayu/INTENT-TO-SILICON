import sys
import os
import argparse

# Add repository root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brainos.workflow.engine import WorkflowEngine

def main():
    parser = argparse.ArgumentParser(description="BrainOS Autonomous Pipeline MVP")
    parser.add_argument("--goal", type=str, required=True, help="The high-level goal to execute.")
    args = parser.parse_args()
    
    engine = WorkflowEngine(state_dir=os.path.join(os.path.dirname(__file__), "state"))
    engine.run(args.goal)

if __name__ == "__main__":
    main()
