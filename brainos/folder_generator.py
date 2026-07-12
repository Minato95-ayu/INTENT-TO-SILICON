import os
import json

class FolderGenerator:
    def generate(self, base_path: str, structure: dict):
        for item in structure.get('folders', []):
            os.makedirs(os.path.join(base_path, item), exist_ok=True)
        return {"status": "success", "base_path": base_path}
