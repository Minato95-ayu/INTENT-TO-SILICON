import os
import sys
from aayu.package.manifest import AayuManifest

def handle(args):
    project_dir = os.getcwd()
    json_path = os.path.join(project_dir, "aayu.json")
    toml_path = os.path.join(project_dir, "Aayu.toml")
    
    if not os.path.exists(json_path):
        print("No aayu.json found in current directory.")
        sys.exit(1)
        
    if os.path.exists(toml_path):
        print("Aayu.toml already exists. Migration aborted to prevent overwriting.")
        sys.exit(1)
        
    import json
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        name = data.get("name", os.path.basename(project_dir))
        version = data.get("version", "0.1.0")
        dependencies = data.get("dependencies", {})
        
        # Build TOML manually
        lines = []
        lines.append(f'name = "{name}"')
        lines.append(f'version = "{version}"')
        lines.append('description = ""')
        lines.append('license = ""')
        lines.append('authors = []')
        lines.append('homepage = ""')
        lines.append('repository = ""')
        lines.append('language = ">=0.1.0"')
        lines.append('')
        lines.append('[app]')
        entry = data.get("entry", "src/main.aayu")
        lines.append(f'entry = "{entry}"')
        lines.append('')
        lines.append('[dependencies]')
        for dep, ver in dependencies.items():
            lines.append(f'{dep} = "{ver}"')
        
        lines.append('')
        lines.append('[dev-dependencies]')
        lines.append('')
        lines.append('[features]')
        lines.append('')
        lines.append('[build]')
        lines.append('target = "web"')
        lines.append('')
        lines.append('[target]')
        lines.append('')
        lines.append('[assets]')
        lines.append('')
        lines.append('[env]')
        lines.append('')
        lines.append('[scripts]')
        lines.append('')
        
        with open(toml_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
            
        os.remove(json_path)
        print("Successfully migrated aayu.json to Aayu.toml")
    except Exception as e:
        print(f"Error during migration: {e}")
        sys.exit(1)
