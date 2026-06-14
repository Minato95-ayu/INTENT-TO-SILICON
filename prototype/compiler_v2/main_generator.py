"""
Aayu Main Application Generator

Generates the main.py entrypoint file.
"""
from .schema_nodes import SchemaModel

class MainGenerator:
    def __init__(self):
        pass
        
    def generate(self, schema: SchemaModel) -> str:
        lines = [
            "from fastapi import FastAPI",
            "from fastapi.middleware.cors import CORSMiddleware",
            "from database import engine",
            "import models",
            ""
        ]
        
        if getattr(schema, 'has_auth', False):
            lines.append("from routers import auth")
            
        for table in schema.tables:
            lines.append(f"from routers import {table.name}")
            
        lines.append("")
        lines.append("# Create database tables")
        lines.append("models.Base.metadata.create_all(bind=engine)")
        lines.append("")
        lines.append("app = FastAPI(title='Aayu Generated Application')")
        lines.append("")
        lines.append("app.add_middleware(")
        lines.append("    CORSMiddleware,")
        lines.append("    allow_origins=['*'],")
        lines.append("    allow_credentials=True,")
        lines.append("    allow_methods=['*'],")
        lines.append("    allow_headers=['*'],")
        lines.append(")")
        lines.append("")
        
        # Health check
        lines.append("@app.get('/')")
        lines.append("def health_check():")
        lines.append("    return {'status': 'ok'}")
        lines.append("")
        
        # Include routers
        if getattr(schema, 'has_auth', False):
            lines.append("app.include_router(auth.router)")
            
        for table in schema.tables:
            lines.append(f"app.include_router({table.name}.router)")
            
        return "\n".join(lines)
