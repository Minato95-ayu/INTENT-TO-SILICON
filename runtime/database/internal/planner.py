# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

class QueryPlanner:
    def build_logical_plan(self, ast):
        # Convert AST to relational algebra (Logical Plan)
        return {"type": "logical_plan", "ast": ast}
        
    def build_physical_plan(self, logical_plan):
        # Decide execution strategy (Table Scan vs Index Scan)
        return {"type": "physical_plan", "logical": logical_plan, "strategy": "table_scan"}
