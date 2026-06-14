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
            "import uuid",
            "from fastapi import FastAPI, Request",
            "from fastapi.responses import JSONResponse",
            "from fastapi.middleware.cors import CORSMiddleware",
            "from starlette.middleware.base import BaseHTTPMiddleware",
            "from database import engine",
            "from logger import get_logger",
            "import models",
            ""
        ]
        
        if getattr(schema, 'has_auth', False):
            lines.append("from routers import auth")
            
        for table in schema.tables:
            if getattr(table, 'is_system', False):
                continue
            lines.append(f"from routers import {table.name}")
            
        lines.append("")
        lines.append("logger = get_logger('main')")
        lines.append("")
        lines.append("# Create database tables")
        lines.append("models.Base.metadata.create_all(bind=engine)")
        lines.append("")
        lines.append("app = FastAPI(title='Aayu Generated Application')")
        lines.append("")
        lines.append("class RequestIdMiddleware(BaseHTTPMiddleware):")
        lines.append("    async def dispatch(self, request: Request, call_next):")
        lines.append("        request_id = str(uuid.uuid4())")
        lines.append("        request.state.request_id = request_id")
        lines.append("        response = await call_next(request)")
        lines.append("        response.headers['X-Request-ID'] = request_id")
        lines.append("        return response")
        lines.append("")
        lines.append("app.add_middleware(RequestIdMiddleware)")
        lines.append("")
        lines.append("app.add_middleware(")
        lines.append("    CORSMiddleware,")
        lines.append("    allow_origins=['*'],")
        lines.append("    allow_credentials=True,")
        lines.append("    allow_methods=['*'],")
        lines.append("    allow_headers=['*'],")
        lines.append(")")
        lines.append("")
        lines.append("@app.exception_handler(Exception)")
        lines.append("async def global_exception_handler(request: Request, exc: Exception):")
        lines.append("    request_id = getattr(request.state, 'request_id', 'unknown')")
        lines.append("    logger.error(f'Unhandled exception: {str(exc)}', exc_info=True, extra={'request_id': request_id})")
        lines.append("    return JSONResponse(")
        lines.append("        status_code=500,")
        lines.append("        content={'error': 'Internal Server Error', 'request_id': request_id}")
        lines.append("    )")
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
            if getattr(table, 'is_system', False):
                continue
            lines.append(f"app.include_router({table.name}.router)")
            
        return "\n".join(lines)
