"""
Aayu App Packager (Sprint 31)

Orchestrates all generators to write a runnable Full Stack project directory.
Contains `backend/` and `frontend/`.
"""
import os
import sys
import importlib.util
from .schema_nodes import SchemaModel
from .database_generator import DatabaseGenerator
from .sqlalchemy_generator import SQLAlchemyGenerator
from .pydantic_generator import PydanticGenerator
from .router_generator import RouterGenerator
from .main_generator import MainGenerator
from .frontend_generator import FrontendGenerator
from .deployment_generator import DeploymentGenerator

class AppPackager:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir

    def package(self, schema: SchemaModel):
        # 1. Setup directories
        backend_dir = os.path.join(self.output_dir, "backend")
        frontend_dir = os.path.join(self.output_dir, "frontend")
        os.makedirs(backend_dir, exist_ok=True)
        os.makedirs(frontend_dir, exist_ok=True)
        
        # 2. Generate Backend
        self._package_backend(schema, backend_dir)
        
        # 3. Extract OpenAPI Spec
        openapi_spec = self._extract_openapi_spec(backend_dir)
        
        # 4. Generate Frontend
        self._package_frontend(openapi_spec, frontend_dir)
        
        # 5. Generate Deployment Files
        self._package_deployment()
        
    def _package_deployment(self):
        generator = DeploymentGenerator()
        files = generator.generate()
        
        for file_path, content in files.items():
            full_path = os.path.join(self.output_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
        
    def _package_backend(self, schema: SchemaModel, backend_dir: str):
        # Write root module init
        with open(os.path.join(backend_dir, "__init__.py"), "w") as f: f.write("")
            
        with open(os.path.join(backend_dir, "database.py"), "w") as f:
            f.write(DatabaseGenerator().generate())
            
        with open(os.path.join(backend_dir, "models.py"), "w") as f:
            f.write(SQLAlchemyGenerator().generate(schema))
            
        with open(os.path.join(backend_dir, "schemas.py"), "w") as f:
            f.write(PydanticGenerator().generate(schema))
            
        routers_dir = os.path.join(backend_dir, "routers")
        os.makedirs(routers_dir, exist_ok=True)
        with open(os.path.join(routers_dir, "__init__.py"), "w") as f: f.write("")
            
        for filename, router_code in RouterGenerator().generate(schema).items():
            with open(os.path.join(routers_dir, filename), "w") as f:
                f.write(router_code)
                
        with open(os.path.join(backend_dir, "main.py"), "w") as f:
            f.write(MainGenerator().generate(schema))
            
        with open(os.path.join(backend_dir, "requirements.txt"), "w") as f:
            f.write("fastapi\nhttpx\npydantic\nsqlalchemy\nuvicorn\n")
            
        readme = [
            "# Aayu Generated Backend\n",
            "```bash\npip install -r requirements.txt\nuvicorn main:app --reload\n```\n"
        ]
        with open(os.path.join(backend_dir, "README.md"), "w") as f:
            f.write("\n".join(readme))
            
    def _extract_openapi_spec(self, backend_dir: str) -> dict:
        # Dynamically import the generated backend app to extract OpenAPI
        import sys
        parent_dir = os.path.dirname(backend_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
            
        backend_name = os.path.basename(backend_dir)
        app_name = os.path.basename(parent_dir)
        module_path = f"{app_name}.{backend_name}.main"
        
        main_module = importlib.import_module(module_path)
        return main_module.app.openapi()
        
    def _package_frontend(self, openapi_spec: dict, frontend_dir: str):
        generator = FrontendGenerator()
        files = generator.generate(openapi_spec)
        
        for file_path, content in files.items():
            full_path = os.path.join(frontend_dir, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
