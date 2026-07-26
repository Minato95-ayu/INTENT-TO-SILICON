import os
import shutil
import hashlib

class AssetManager:
    """
    Scans the project's 'assets' folder and copies files to '.aayu/build/assets/'
    with content-hashed filenames.
    """
    def __init__(self, project_dir: str):
        self.project_dir = project_dir
        self.assets_dir = os.path.join(project_dir, "assets")
        self.build_assets_dir = os.path.join(project_dir, ".aayu", "build", "assets")
        self.registry = {} # Mapping of original relative path to hashed path

    def _hash_file(self, filepath: str) -> str:
        hasher = hashlib.md5()
        with open(filepath, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()[:6]

    def build(self) -> dict:
        """
        Processes all assets and returns the registry mapping.
        """
        if not os.path.exists(self.assets_dir):
            return self.registry

        os.makedirs(self.build_assets_dir, exist_ok=True)

        for root, _, files in os.walk(self.assets_dir):
            for file in files:
                original_path = os.path.join(root, file)
                rel_path = os.path.relpath(original_path, self.project_dir)
                
                # Forward slashes for internal registry paths
                rel_path_key = rel_path.replace("\\", "/")
                
                file_hash = self._hash_file(original_path)
                
                filename, ext = os.path.splitext(file)
                hashed_filename = f"{filename}.{file_hash}{ext}"
                
                # Preserve directory structure inside assets
                rel_dir = os.path.relpath(root, self.assets_dir)
                if rel_dir == ".":
                    target_dir = self.build_assets_dir
                else:
                    target_dir = os.path.join(self.build_assets_dir, rel_dir)
                    os.makedirs(target_dir, exist_ok=True)
                    
                target_path = os.path.join(target_dir, hashed_filename)
                
                # Only copy if the hashed file doesn't already exist
                if not os.path.exists(target_path):
                    shutil.copy2(original_path, target_path)
                    
                # Create the hashed route (e.g. assets/logo.a81f29.png)
                rel_target_path = os.path.relpath(target_path, os.path.join(self.project_dir, ".aayu", "build"))
                rel_target_path = rel_target_path.replace("\\", "/")
                
                self.registry[rel_path_key] = rel_target_path
                
        return self.registry
