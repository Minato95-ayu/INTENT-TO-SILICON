import hashlib
import os
import json
from pathlib import Path
from typing import Optional, Dict

class IncrementalManager:
    """
    Manages file-level dirty tracking and artifact caching.
    Ensures we skip compilation for files that haven't changed.
    """
    def __init__(self, cache_dir: str = ".aayu_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.manifest_file = self.cache_dir / "incremental_manifest.json"
        
        self.manifest: Dict[str, str] = {}
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file, "r") as f:
                    self.manifest = json.load(f)
            except json.JSONDecodeError:
                pass

    def _hash_file(self, filepath: str) -> str:
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            hasher.update(f.read())
        return hasher.hexdigest()

    def is_dirty(self, filepath: str) -> bool:
        """Returns True if the file has changed since the last compile."""
        if not os.path.exists(filepath):
            return True
            
        current_hash = self._hash_file(filepath)
        cached_hash = self.manifest.get(filepath)
        
        return current_hash != cached_hash

    def mark_clean(self, filepath: str):
        """Marks a file as clean by saving its hash to the manifest."""
        self.manifest[filepath] = self._hash_file(filepath)
        self._save_manifest()
        
    def _save_manifest(self):
        with open(self.manifest_file, "w") as f:
            json.dump(self.manifest, f, indent=2)

    def get_cached_artifact(self, filepath: str) -> Optional[bytes]:
        """Returns the cached bytecode artifact if the source file is clean."""
        if self.is_dirty(filepath):
            return None
            
        # The bytecode is typically cached in `.aayu_cache/<hash>.aybc`
        file_hash = self.manifest.get(filepath)
        artifact_path = self.cache_dir / f"{file_hash}.aybc"
        
        if artifact_path.exists():
            with open(artifact_path, "rb") as f:
                return f.read()
        return None
        
    def save_artifact(self, filepath: str, bytecode: bytes):
        """Saves the compiled bytecode to the cache."""
        self.mark_clean(filepath)
        file_hash = self.manifest.get(filepath)
        artifact_path = self.cache_dir / f"{file_hash}.aybc"
        
        with open(artifact_path, "wb") as f:
            f.write(bytecode)
