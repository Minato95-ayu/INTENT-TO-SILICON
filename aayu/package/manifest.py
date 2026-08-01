import os
import sys
import json
try:
    import tomllib
except ModuleNotFoundError:
    print("Error: AAYU requires Python 3.11+ for tomllib support.")
    sys.exit(1)

class AayuManifest:
    def __init__(self, project_dir="."):
        self.project_dir = os.path.abspath(project_dir)
        self.toml_path = os.path.join(self.project_dir, "Aayu.toml")
        self.json_path = os.path.join(self.project_dir, "aayu.json")
        self.data = self._load()

    def _load(self):
        # 1. Prefer Aayu.toml
        if os.path.exists(self.toml_path):
            with open(self.toml_path, "rb") as f:
                try:
                    return tomllib.load(f)
                except tomllib.TOMLDecodeError as e:
                    print(f"Error parsing Aayu.toml: {e}")
                    sys.exit(1)
        
        # 2. Fallback to aayu.json
        if os.path.exists(self.json_path):
            print("\033[93mWarning:\naayu.json is deprecated.\n\nPlease migrate to Aayu.toml.\n\nRun:\n\n  aayu migrate\033[0m\n")
            with open(self.json_path, "r", encoding="utf-8") as f:
                try:
                    json_data = json.load(f)
                    # Convert json structure to match toml structure if needed
                    # aayu.json typically has: name, version, dependencies
                    data = {
                        "package": {
                            "name": json_data.get("name", "Unknown"),
                            "version": json_data.get("version", "0.1.0")
                        },
                        "dependencies": json_data.get("dependencies", {})
                    }
                    if "entry" in json_data:
                        data["app"] = {"entry": json_data["entry"]}
                    return data
                except json.JSONDecodeError as e:
                    print(f"Error parsing aayu.json: {e}")
                    sys.exit(1)
                    
        return None

    def exists(self):
        return self.data is not None

    def get_package_name(self):
        # Support both [package] and root name for flexibility
        if self.data and "package" in self.data:
            return self.data["package"].get("name", "Unknown")
        elif self.data and "name" in self.data:
            return self.data.get("name", "Unknown")
        return "Unknown"

    def get_entry(self):
        if self.data and "app" in self.data:
            return self.data["app"].get("entry", "src/main.aayu")
        return "src/main.aayu"

    def get_build_target(self):
        if self.data and "build" in self.data:
            return self.data["build"].get("target", "web")
        return "web"

    def get_dependencies(self):
        if self.data and "dependencies" in self.data:
            return self.data["dependencies"]
        return {}
        
    def add_dependency(self, name, version):
        if not os.path.exists(self.toml_path):
            print("Error: Aayu.toml not found. Run 'aayu init' first.")
            return False
            
        with open(self.toml_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        # Find [dependencies] section
        dep_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == "[dependencies]":
                dep_idx = i
                break
                
        if dep_idx == -1:
            lines.append("\n[dependencies]\n")
            dep_idx = len(lines) - 1
            
        # Check if exists
        updated = False
        for i in range(dep_idx + 1, len(lines)):
            line = lines[i].strip()
            if line.startswith("["): # Next section
                lines.insert(i, f'{name} = "{version}"\n')
                updated = True
                break
            if line.startswith(f"{name} =") or line.startswith(f'{name}='):
                lines[i] = f'{name} = "{version}"\n'
                updated = True
                break
                
        if not updated:
            lines.append(f'{name} = "{version}"\n')
            
        with open(self.toml_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
            
        return True

    def remove_dependency(self, name):
        if not os.path.exists(self.toml_path):
            print("Error: Aayu.toml not found. Run 'aayu init' first.")
            return False
            
        with open(self.toml_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        dep_idx = -1
        for i, line in enumerate(lines):
            if line.strip() == "[dependencies]":
                dep_idx = i
                break
                
        if dep_idx == -1:
            return False
            
        removed = False
        for i in range(dep_idx + 1, len(lines)):
            line = lines[i].strip()
            if line.startswith("["):
                break
            if line.startswith(f"{name} =") or line.startswith(f'{name}='):
                lines.pop(i)
                removed = True
                break
                
        if removed:
            with open(self.toml_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
                
        return removed

    @staticmethod
    def create_default(name, entry="src/main.aayu"):
        return f"""name = "{name}"
version = "0.1.0"
description = ""
license = ""
authors = []
homepage = ""
repository = ""
language = ">=0.1.0"

[app]
entry = "{entry}"

[dependencies]

[dev-dependencies]

[features]

[build]
target = "web"

[target]

[assets]

[env]

[scripts]
"""
