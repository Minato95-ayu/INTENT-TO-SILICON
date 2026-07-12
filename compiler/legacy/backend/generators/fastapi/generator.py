"""
=============================================================================
FILE: generator.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import string
from generators.base import BaseGenerator

class FastAPIGenerator(BaseGenerator):
    def __init__(self, ir_data: dict, output_dir: str):
        super().__init__(ir_data, output_dir)
        self.tpl_dir = os.path.join(os.path.dirname(__file__), "templates")
        
        # Mapping AAYU types to Python/Pydantic types
        self.type_map = {
            "text": "str",
            "number": "float", # Or int, but float is safer generic
            "boolean": "bool",
            "date": "str"
        }

    def _read_tpl(self, name: str) -> str:
        with open(os.path.join(self.tpl_dir, name), "r", encoding="utf-8") as f:
            return f.read()

    def generate(self):
        print(f"Generating FastAPI Backend in {self.output_dir}...")
        
        app_name = self.ir.get("system", {}).get("name", "AAYU_App")
        entities = self.ir.get("entities", [])
        
        # 1. Root Files
        self.write_file("requirements.txt", self._read_tpl("requirements.txt.tpl"))
        
        main_tpl = string.Template(self._read_tpl("main.py.tpl"))
        self.write_file("main.py", main_tpl.substitute(app_name=app_name))

        # 2. App Directory
        self.ensure_dir("app")
        self.write_file("app/__init__.py", "")
        self.write_file("app/database.py", self._read_tpl("database.py.tpl"))
        
        # 3. Models Generation
        models_content = ""
        for entity in entities:
            name = entity.get("name")
            fields = entity.get("fields", [])
            models_content += f"class {name}(BaseModel):\n"
            if not fields:
                models_content += "    pass\n"
            else:
                for field in fields:
                    fname = field.get("name")
                    ftype = self.type_map.get(field.get("type", "text"), "str")
                    models_content += f"    {fname}: Optional[{ftype}] = None\n"
            models_content += "\n"
            
        models_tpl = string.Template(self._read_tpl("models.py.tpl"))
        self.write_file("app/models.py", models_tpl.substitute(models_content=models_content))
        
        # 4. Routers Generation
        routers_content = ""
        model_names = [e["name"] for e in entities]
        for name in model_names:
            route_path = f"/{name.lower()}s"
            routers_content += f"@router.get('{route_path}', response_model=List[{name}])\n"
            routers_content += f"def get_{name.lower()}s():\n"
            routers_content += f"    return []\n\n"
            
        router_tpl = string.Template(self._read_tpl("routers.py.tpl"))
        self.write_file("app/routers.py", router_tpl.substitute(
            model_imports=", ".join(model_names) if model_names else "BaseModel",
            routers_content=routers_content
        ))

        print("FastAPI generation complete.")
