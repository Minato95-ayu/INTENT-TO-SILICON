from typing import Dict, Any, Optional

class ExecutionPlan:
    """
    Immutable representation of a database operation.
    Created by Planner, optionally rewritten by Optimizer, consumed by Adapter.
    """
    def __init__(self, operation: str, table: str, fields: Optional[Dict[str, Any]] = None, conditions: Optional[Dict[str, Any]] = None):
        self._operation = operation
        self._table = table
        self._fields = fields or {}
        self._conditions = conditions or {}
        
    @property
    def operation(self) -> str:
        return self._operation
        
    @property
    def table(self) -> str:
        return self._table
        
    @property
    def fields(self) -> Dict[str, Any]:
        # Return a copy to ensure immutability
        return dict(self._fields)
        
    @property
    def conditions(self) -> Dict[str, Any]:
        return dict(self._conditions)
        
    def with_optimization(self, new_fields=None, new_conditions=None) -> 'ExecutionPlan':
        """
        Returns a new ExecutionPlan if the Optimizer needs to rewrite it.
        """
        return ExecutionPlan(
            operation=self._operation,
            table=self._table,
            fields=new_fields if new_fields is not None else self._fields,
            conditions=new_conditions if new_conditions is not None else self._conditions
        )
