from aayu.runtime.database.schema import SchemaEngine
from aayu.runtime.database.migration import MigrationEngine
from aayu.runtime.database.internal.planner import QueryPlanner
from aayu.runtime.database.internal.optimizer import QueryOptimizer
from aayu.runtime.database.adapter.sqlite import SQLiteAdapter

class StorageEngine:
    """
    The orchestrator for the entire Database Subsystem.
    It replaces the concept of an ORM.
    """
    def __init__(self, data_ir):
        self.data_ir = data_ir
        self.schema_engine = SchemaEngine(data_ir.get("models", []))
        self.migration_engine = MigrationEngine()
        self.adapter = SQLiteAdapter("aayu_data/Main.db")
        self.planner = QueryPlanner()
        self.optimizer = QueryOptimizer()

    def initialize(self):
        schema_ir = self.schema_engine.build_schema_ir()
        self.migration_engine.apply(schema_ir, self.adapter)

    def start(self):
        pass

    def execute_query_ast(self, query_ast):
        logical_plan = self.planner.build_logical_plan(query_ast)
        physical_plan = self.planner.build_physical_plan(logical_plan)
        optimized_plan = self.optimizer.optimize(physical_plan)
        return self.adapter.execute_plan(optimized_plan)
