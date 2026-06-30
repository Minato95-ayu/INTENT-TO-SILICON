import os
import json
import hashlib
from typing import Dict, Any, List

class ModuleCache:
    def __init__(self, name: str, source_hash: str, dependencies: List[str], exports: List[str], bytecode_path: str = ""):
        self.name = name
        self.source_hash = source_hash
        self.dependencies = dependencies
        self.exports = exports
        self.bytecode_path = bytecode_path

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "source_hash": self.source_hash,
            "dependencies": self.dependencies,
            "exports": self.exports,
            "bytecode_path": self.bytecode_path
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ModuleCache':
        return cls(
            name=data.get("name", ""),
            source_hash=data.get("source_hash", ""),
            dependencies=data.get("dependencies", []),
            exports=data.get("exports", []),
            bytecode_path=data.get("bytecode_path", "")
        )

class IncrementalCache:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.cache_dir = os.path.join(workspace_root, ".aayu_cache")
        self.manifest_path = os.path.join(self.cache_dir, "manifest.json")
        self.modules: Dict[str, ModuleCache] = {}
        
        self._ensure_cache_dir()
        self.load()

    def _ensure_cache_dir(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            os.makedirs(os.path.join(self.cache_dir, "bytecode"))

    def load(self):
        if os.path.exists(self.manifest_path):
            try:
                with open(self.manifest_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for k, v in data.get("modules", {}).items():
                        self.modules[k] = ModuleCache.from_dict(v)
            except Exception:
                pass # If cache is corrupted, just start fresh

    def save(self):
        data = {
            "version": "1.0",
            "modules": {k: v.to_dict() for k, v in self.modules.items()}
        }
        with open(self.manifest_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def hash_file(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            return ""
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    def is_up_to_date(self, module_name: str, filepath: str) -> bool:
        if module_name not in self.modules:
            return False
            
        current_hash = self.hash_file(filepath)
        cached_module = self.modules[module_name]
        
        if current_hash != cached_module.source_hash:
            return False
            
        # Also need to check if dependencies changed, but the orchestrator handles cascading invalidation
        return True
        
    def update_module(self, module_name: str, filepath: str, dependencies: List[str], exports: List[str], bytecode_path: str = ""):
        self.modules[module_name] = ModuleCache(
            name=module_name,
            source_hash=self.hash_file(filepath),
            dependencies=dependencies,
            exports=exports,
            bytecode_path=bytecode_path
        )
