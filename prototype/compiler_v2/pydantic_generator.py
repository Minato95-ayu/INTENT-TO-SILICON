"""
Aayu Pydantic Generator

Generates the schemas.py file.
"""
from .schema_nodes import SchemaModel

class PydanticGenerator:
    def _to_pascal_case(self, snake_str: str) -> str:
        components = snake_str.split('_')
        return "".join(x.title() for x in components)
        
    def _map_pydantic_type(self, generic_type: str) -> str:
        if generic_type.upper() == "UUID":
            return "str"
        elif generic_type.upper() == "INTEGER":
            return "int"
        return "str"

    def generate(self, schema: SchemaModel) -> str:
        lines = [
            "from typing import List, Optional",
            "from pydantic import BaseModel, ConfigDict",
            ""
        ]
        
        for table in schema.tables:
            pascal_name = self._to_pascal_case(table.name)
            
            # Create Schema
            lines.append(f"class {pascal_name}Create(BaseModel):")
            has_create_fields = False
            for col in table.columns:
                if col.name != "id":
                    ptype = self._map_pydantic_type(col.type)
                    lines.append(f"    {col.name}: {ptype}")
                    has_create_fields = True
            if not has_create_fields:
                lines.append("    pass")
            lines.append("")
                
            # Update Schema
            lines.append(f"class {pascal_name}Update(BaseModel):")
            has_update_fields = False
            for col in table.columns:
                if col.name != "id":
                    ptype = self._map_pydantic_type(col.type)
                    lines.append(f"    {col.name}: Optional[{ptype}] = None")
                    has_update_fields = True
            if not has_update_fields:
                lines.append("    pass")
            lines.append("")
                
            # Response Schema
            lines.append(f"class {pascal_name}Response({pascal_name}Create):")
            id_col_type = next((self._map_pydantic_type(c.type) for c in table.columns if c.name == "id"), "str")
            lines.append(f"    id: {id_col_type}")
            lines.append("    model_config = ConfigDict(from_attributes=True)\n")
            
        return "\n".join(lines)
