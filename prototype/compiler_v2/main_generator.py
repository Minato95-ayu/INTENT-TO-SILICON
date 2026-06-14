"""
Aayu Main Application Generator

Generates the main.py entrypoint file.
"""
from .schema_nodes import SchemaModel

class MainGenerator:
    def generate(self, schema: SchemaModel) -> str:
        lines = [
            "from fastapi import FastAPI",
            "from .database import engine",
            "from . import models",
            ""
        ]
        
        # Import routers
        for table in schema.tables:
            lines.append(f"from .routers import {table.name}")
            
        lines.append("")
        lines.append("# Create database tables")
        lines.append("models.Base.metadata.create_all(bind=engine)")
        lines.append("")
        lines.append("app = FastAPI(title='Aayu Generated Application')")
        lines.append("")
        
        # Health check
        lines.append("@app.get('/')")
        lines.append("def health_check():")
        lines.append("    return {'status': 'ok'}")
        lines.append("")
        
        # Include routers
        for table in schema.tables:
            lines.append(f"app.include_router({table.name}.router)")
            
        return "\n".join(lines)
