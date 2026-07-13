import json
import os
from .exceptions import ManifestError

class Manifest:
    """Manages aayu.json parsing and validation."""
    
    REQUIRED_KEYS = ["name", "version", "author", "license", "entry"]
    
    def __init__(self, data: dict, path: str = None):
        self.data = data
        self.path = path
        self._validate()
        
    def _validate(self):
        for key in self.REQUIRED_KEYS:
            if key not in self.data:
                raise ManifestError(f"Manifest missing required key: '{key}'")
                
        # Dependencies are optional but default to empty dict
        if "dependencies" not in self.data:
            self.data["dependencies"] = {}
            
    @property
    def name(self): return self.data["name"]
    @property
    def version(self): return self.data["version"]
    @property
    def checksum(self): return self.data.get("checksum")
    @property
    def dependencies(self): return self.data["dependencies"]
    
    @classmethod
    def load(cls, path: str):
        if not os.path.exists(path):
            raise ManifestError(f"Manifest not found at {path}")
        with open(path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                return cls(data, path)
            except json.JSONDecodeError:
                raise ManifestError(f"Invalid JSON in {path}")
                
    def save(self):
        if not self.path:
            raise ManifestError("No path associated with manifest.")
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)
            
    @classmethod
    def create_default(cls, path: str, name: str = "app"):
        data = {
            "name": name,
            "version": "1.0.0",
            "description": "An AAYU project",
            "author": "Unknown",
            "license": "MIT",
            "entry": "main.aayu",
            "dependencies": {}
        }
        manifest = cls(data, path)
        manifest.save()
        return manifest
