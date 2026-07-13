import json
import os

class LockFile:
    """Manages the aayu.lock deterministic installation file."""
    
    def __init__(self, data: dict, path: str = None):
        self.data = data
        self.path = path
        
    @classmethod
    def load(cls, path: str):
        if not os.path.exists(path):
            return cls({"version": 1, "packages": {}}, path)
            
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return cls(data, path)
            except json.JSONDecodeError:
                return cls({"version": 1, "packages": {}}, path)
                
    def save(self):
        if not self.path:
            return
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
            
    def update_package(self, name: str, version: str, checksum: str, dependencies: dict):
        if "packages" not in self.data:
            self.data["packages"] = {}
            
        self.data["packages"][name] = {
            "version": version,
            "checksum": checksum,
            "dependencies": dependencies
        }
