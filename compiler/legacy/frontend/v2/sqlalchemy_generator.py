"""
Aayu SQLAlchemy ORM Generator (Sprint 28)

Converts the generic database-agnostic SchemaModel into valid SQLAlchemy Python ORM classes.
Strictly maps tables to classes and columns to Column objects, omitting complex relationship() properties for v1.
"""

from .schema_nodes import SchemaModel, Table, Column

class SQLAlchemyGenerator:
    def __init__(self):
        pass

    def _to_pascal_case(self, snake_str: str) -> str:
        """Converts snake_case table name to PascalCase class name."""
        components = snake_str.split('_')
        return "".join(x.title() for x in components)

    def _map_type(self, generic_type: str) -> str:
        """Maps generic schema types to SQLAlchemy types."""
        if generic_type.upper() == "UUID":
            return "String" # SQLAlchemy String type
        elif generic_type.upper() == "INTEGER":
            return "Integer"
        return "String"

    def generate(self, schema: SchemaModel) -> str:
        """
        Generates a valid Python script containing SQLAlchemy models.
        """
        lines = [
            "from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table",
            "from sqlalchemy.orm import relationship",
            "from database import Base",
            ""
        ]

        # 2. Model Classes
        for table in schema.tables:
            class_name = self._to_pascal_case(table.name)
            lines.append(f"class {class_name}(Base):")
            lines.append(f'    __tablename__ = "{table.name}"\n')
            
            for col in table.columns:
                col_type = self._map_type(col.type)
                
                args = [col_type]
                
                if col.is_foreign_key and col.references_table:
                    # In SQLAlchemy, the ForeignKey must include the target column name (e.g. table.id)
                    args.append(f'ForeignKey("{col.references_table}.id")')
                    
                if col.is_primary_key:
                    args.append("primary_key=True")
                if col.is_unique:
                    args.append("unique=True")
                    
                args_str = ", ".join(args)
                lines.append(f"    {col.name} = Column({args_str})")
                
            lines.append("\n")

        return "\n".join(lines)
