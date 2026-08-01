class BreakpointManager:
    """Manages different types of breakpoints."""
    
    def __init__(self):
        # map line -> { condition, hit_count, current_hits }
        self.breakpoints = {}
        self.exception_filters = set() # "all", "uncaught"
        
    def set_breakpoint(self, line: int, condition: str = None, hit_count: int = 0):
        self.breakpoints[line] = {
            "condition": condition,
            "target_hits": hit_count,
            "current_hits": 0
        }
        
    def set_exception_breakpoints(self, filters: list):
        self.exception_filters = set(filters)
        
    def should_break(self, line: int, snapshot=None) -> bool:
        if line not in self.breakpoints:
            return False
            
        bp = self.breakpoints[line]
        
        # Hit count logic
        bp["current_hits"] += 1
        if bp["target_hits"] > 0 and bp["current_hits"] < bp["target_hits"]:
            return False
            
        # Conditional logic
        if bp["condition"] and snapshot:
            from .watch import WatchEvaluator
            evaluator = WatchEvaluator(snapshot)
            try:
                # Basic eval check
                res = evaluator.evaluate(bp["condition"])
                if res in ("False", "0", ""):
                    return False
            except:
                # If condition fails to evaluate, break anyway or ignore? Standard is ignore.
                return False
                
        return True
