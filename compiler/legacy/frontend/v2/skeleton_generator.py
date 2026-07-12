"""
=============================================================================
FILE: skeleton_generator.py
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
import json
import re

class SkeletonGenerator:
    def __init__(self):
        self.templates = {}
        
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        try:
            with open(os.path.join(base_dir, 'dictionary', 'skeleton_templates.json'), 'r') as f:
                self.templates = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load skeleton_templates.json: {e}")

    def _to_camel_case(self, snake_str):
        components = snake_str.split('_')
        return ''.join(x.title() for x in components)
        
    def _to_title(self, snake_str):
        return snake_str.replace('_', ' ').title()

    def generate(self, blueprint, output_dir):
        """
        Takes a generated blueprint and an output directory, and generates
        the actual source code skeleton files.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        generated_files = []
            
        # 1. Frontend Pages
        frontend_pages_dir = os.path.join(output_dir, 'frontend', 'pages')
        os.makedirs(frontend_pages_dir, exist_ok=True)
        
        for module in blueprint.get("frontend_modules", []):
            name_camel = self._to_camel_case(module)
            title = self._to_title(module)
            
            template = self.templates.get("frontend_page", "")
            content = template.replace("{{name}}", name_camel)\
                              .replace("{{name_lowercase}}", module)\
                              .replace("{{title}}", title)
                              
            filepath = os.path.join(frontend_pages_dir, f"{name_camel}.tsx")
            with open(filepath, 'w') as f:
                f.write(content)
            generated_files.append(filepath)

        # 2. Backend APIs
        backend_api_dir = os.path.join(output_dir, 'backend', 'api')
        os.makedirs(backend_api_dir, exist_ok=True)
        
        for module in blueprint.get("backend_modules", []):
            name_camel = self._to_camel_case(module)
            
            template = self.templates.get("backend_api", "")
            content = template.replace("{{name}}", name_camel)\
                              .replace("{{name_lowercase}}", module)
                              
            filepath = os.path.join(backend_api_dir, f"{module}.py")
            with open(filepath, 'w') as f:
                f.write(content)
            generated_files.append(filepath)

        # 3. Database Models (Placeholder for next sprint, but we can generate a consolidated schema.sql)
        db_dir = os.path.join(output_dir, 'database')
        os.makedirs(db_dir, exist_ok=True)
        
        schema_content = ""
        for entity in blueprint.get("data_entities", []):
            template = self.templates.get("database_model", "")
            schema_content += template.replace("{{name_lowercase}}", entity) + "\n"
            
        if schema_content:
            filepath = os.path.join(db_dir, "schema.sql")
            with open(filepath, 'w') as f:
                f.write(schema_content)
            generated_files.append(filepath)

        return generated_files

if __name__ == "__main__":
    generator = SkeletonGenerator()
    test_blueprint = {
        "frontend_modules": ["library_page", "hostel_page"],
        "backend_modules": ["booking_api"],
        "data_entities": ["student", "library"]
    }
    
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    output_dir = os.path.join(base_dir, 'generated_project')
    
    files = generator.generate(test_blueprint, output_dir)
    print("Generated Skeleton Files:")
    for f in files:
        print(f)
