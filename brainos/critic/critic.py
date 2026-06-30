from ..task.task import Task

class Critic:
    def evaluate(self, task: Task, execution_result: str) -> str:
        """
        Evaluates execution results, tests, diagnostics, and architecture violations.
        Returns 'PASS', 'FAIL', or 'SKIP'.
        """
        if execution_result != "PASS":
            return execution_result
            
        print("\n" + "="*50)
        print(f"CRITIC VERIFICATION: {task.id}")
        print("Running tests... (mock: PASS)")
        print("Checking Architecture Freeze... (mock: PASS)")
        print("Checking Regression... (mock: PASS)")
        print("="*50)
        
        while True:
            doc_sync = input("Has documentation (Snapshot, Roadmap, Decision Log, Changelog) been synced? (PASS / FAIL): ").strip().upper()
            if doc_sync in ("PASS", "FAIL"):
                if doc_sync == "FAIL":
                    return "FAIL"
                break
            print("Invalid input. Please enter PASS or FAIL.")
            
        while True:
            type_cov = input("Is Type Coverage acceptable for this phase? (PASS / FAIL): ").strip().upper()
            if type_cov in ("PASS", "FAIL"):
                return type_cov
            print("Invalid input. Please enter PASS or FAIL.")
