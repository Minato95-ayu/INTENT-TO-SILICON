"""
=============================================================================
FILE: project_generator.py
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

class ProjectGenerator:
    def __init__(self):
        self.templates = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        try:
            with open(os.path.join(base_dir, 'dictionary', 'project_templates.json'), 'r') as f:
                self.templates = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load project_templates.json: {e}")

    def generate_project(self, blueprint, output_dir="generated_project"):
        """
        Takes a System Blueprint and generates the physical folder structure,
        architecture docs, and configuration files. Does NOT generate business logic.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Create standard top-level directories
        top_levels = ["frontend", "backend", "database", "docs"]
        for layer in top_levels:
            layer_dir = os.path.join(output_dir, layer)
            if not os.path.exists(layer_dir):
                os.makedirs(layer_dir)
                
            # Create subdirectories based on templates
            subdirs = self.templates.get(layer, {}).get("directories", [])
            for subdir in subdirs:
                os.makedirs(os.path.join(layer_dir, subdir), exist_ok=True)
                
        # Generate blueprint.json
        with open(os.path.join(output_dir, "blueprint.json"), 'w') as f:
            json.dump(blueprint, f, indent=2)
            
        # Generate architecture.md
        arch_md = self._generate_architecture_doc(blueprint)
        with open(os.path.join(output_dir, "docs", "architecture.md"), 'w') as f:
            f.write(arch_md)
            
        # Touch basic files (schema.sql placeholder)
        with open(os.path.join(output_dir, "database", "schema.sql"), 'w') as f:
            f.write("-- Auto-generated database schema placeholder\n")
            
        return output_dir

    def _generate_architecture_doc(self, blueprint):
        md = "# System Architecture Blueprint\n\n"
        
        md += "## Frontend Modules\n"
        for m in blueprint.get("frontend_modules", []):
            md += f"- {m}\n"
            
        md += "\n## Backend Modules\n"
        for m in blueprint.get("backend_modules", []):
            md += f"- {m}\n"
            
        md += "\n## Data Entities\n"
        for e in blueprint.get("data_entities", []):
            md += f"- {e}\n"
            
        md += "\n## External Integrations\n"
        for ext in blueprint.get("external_integrations", []):
            md += f"- {ext}\n"
            
        return md
