class QueryPlanner:
    def build_logical_plan(self, ast):
        # Convert AST to relational algebra (Logical Plan)
        return {"type": "logical_plan", "ast": ast}
        
    def build_physical_plan(self, logical_plan):
        # Decide execution strategy (Table Scan vs Index Scan)
        return {"type": "physical_plan", "logical": logical_plan, "strategy": "table_scan"}
