import os
import json
import shutil
from .registry import Registry

class OfficialRegistry(Registry):
    """Mock implementation of the Official AAYU Registry using local filesystem."""
    
    def __init__(self, cache_dir: str):
        # We will mock the official registry as a folder inside the cache dir for now
        self.registry_dir = os.path.join(cache_dir, "registry_mock")
        os.makedirs(self.registry_dir, exist_ok=True)
        
    def _get_pkg_dir(self, name: str):
        return os.path.join(self.registry_dir, name)
        
    def search(self, query: str):
        results = []
        if not os.path.exists(self.registry_dir): return results
        
        for pkg_name in os.listdir(self.registry_dir):
            if query.lower() in pkg_name.lower():
                meta_path = os.path.join(self._get_pkg_dir(pkg_name), "meta.json")
                if os.path.exists(meta_path):
                    with open(meta_path, 'r') as f:
                        results.append(json.load(f))
        return results
        
    def fetch_manifest(self, package_name: str, version_req: str = None):
        meta_path = os.path.join(self._get_pkg_dir(package_name), "meta.json")
        if not os.path.exists(meta_path):
            return None
        with open(meta_path, 'r') as f:
            return json.load(f)
            
    def download(self, package_name: str, version: str, dest_path: str):
        pkg_file = os.path.join(self._get_pkg_dir(package_name), f"{version}.zip")
        if not os.path.exists(pkg_file):
            return False
        shutil.copy2(pkg_file, dest_path)
        return True
        
    def publish(self, manifest_data: dict, zip_path: str):
        name = manifest_data["name"]
        version = manifest_data["version"]
        
        pkg_dir = self._get_pkg_dir(name)
        os.makedirs(pkg_dir, exist_ok=True)
        
        # Save meta
        meta_path = os.path.join(pkg_dir, "meta.json")
        meta = {}
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                meta = json.load(f)
                
        meta["name"] = name
        meta["description"] = manifest_data.get("description", "")
        meta["owner"] = manifest_data["author"]
        if "versions" not in meta:
            meta["versions"] = {}
            
        meta["versions"][version] = {
            "checksum": manifest_data.get("checksum", ""),
            "dependencies": manifest_data.get("dependencies", {})
        }
        
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
            
        # Copy zip
        dest_zip = os.path.join(pkg_dir, f"{version}.zip")
        shutil.copy2(zip_path, dest_zip)
