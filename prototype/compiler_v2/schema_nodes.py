"""
Aayu Schema IR Nodes (Sprint 26)

Defines the Database Schema Intermediate Representation.
Provides a database-agnostic relational model (Tables, Columns, PKs, FKs).
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Column:
    name: str
    type: str  # e.g., 'UUID', 'INTEGER', 'VARCHAR'
    is_primary_key: bool = False
    is_foreign_key: bool = False
    references_table: Optional[str] = None
    is_unique: bool = False

@dataclass
class Table:
    name: str
    columns: List[Column] = field(default_factory=list)
    is_system: bool = False

    @property
    def searchable_columns(self) -> List[Column]:
        search_heuristics = {"name", "email", "title", "description", "username", "phone", "code"}
        return [c for c in self.columns if c.name in search_heuristics and c.type.upper() in ["VARCHAR", "STRING", "TEXT"]]

@dataclass
class SchemaModel:
    tables: List[Table] = field(default_factory=list)
    has_auth: bool = False

    def get_table(self, name: str) -> Optional[Table]:
        for t in self.tables:
            if t.name == name:
                return t
        return None
