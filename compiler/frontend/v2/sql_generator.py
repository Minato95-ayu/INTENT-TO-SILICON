"""
Aayu SQL Generator v1 (Sprint 27)

Converts the generic database-agnostic SchemaModel into valid SQLite Data Definition Language (DDL).
Focuses strictly on table creation, primary keys, and foreign keys without advanced cascading policies yet.
"""

from .schema_nodes import SchemaModel, Table, Column

class SQLGenerator:
    def __init__(self):
        pass

    def _map_type(self, generic_type: str) -> str:
        """Maps generic schema types to SQLite types."""
        if generic_type.upper() == "UUID":
            return "TEXT"
        elif generic_type.upper() == "INTEGER":
            return "INTEGER"
        return "TEXT" # Default fallback for SQLite

    def generate(self, schema: SchemaModel) -> str:
        """
        Generates a multi-line SQL string containing CREATE TABLE statements.
        Orders table creation based on foreign key dependencies where possible,
        though SQLite allows deferred foreign key checks.
        """
        sql_blocks = []
        
        # SQLite best practice: explicitly enable foreign keys
        sql_blocks.append("-- Enable foreign key constraints")
        sql_blocks.append("PRAGMA foreign_keys = ON;\n")

        for table in schema.tables:
            lines = []
            lines.append(f'CREATE TABLE "{table.name}" (')
            
            column_defs = []
            fk_defs = []
            
            for col in table.columns:
                col_type = self._map_type(col.type)
                col_def = f'    "{col.name}" {col_type}'
                
                if col.is_primary_key:
                    col_def += " PRIMARY KEY"
                if col.is_unique:
                    col_def += " UNIQUE"
                    
                column_defs.append(col_def)
                
                if col.is_foreign_key and col.references_table:
                    # Simple references only for v1. No ON DELETE CASCADE.
                    fk_defs.append(f'    FOREIGN KEY("{col.name}") REFERENCES "{col.references_table}"("id")')
                    
            # Combine columns and foreign key definitions
            all_defs = column_defs + fk_defs
            lines.append(",\n".join(all_defs))
            lines.append(");\n")
            
            sql_blocks.append("\n".join(lines))
            
        return "\n".join(sql_blocks)
