import os
import shutil
from .exceptions import PackageNotFoundError

class CacheManager:
    """Manages the ~/.aayu/ local cache."""
    
    def __init__(self, home_dir: str = None):
        self.home_dir = home_dir or os.path.expanduser("~")
        self.aayu_dir = os.path.join(self.home_dir, ".aayu")
        self.cache_dir = os.path.join(self.aayu_dir, "cache")
        self.packages_dir = os.path.join(self.aayu_dir, "packages")
        
        self._init_dirs()
        
    def _init_dirs(self):
        os.makedirs(self.cache_dir, exist_ok=True)
        os.makedirs(self.packages_dir, exist_ok=True)
        
    def is_cached(self, name: str, version: str) -> bool:
        return os.path.exists(self._get_pkg_path(name, version))
        
    def _get_pkg_path(self, name: str, version: str):
        return os.path.join(self.packages_dir, f"{name}@{version}.zip")
        
    def store(self, name: str, version: str, zip_path: str):
        dest = self._get_pkg_path(name, version)
        shutil.copy2(zip_path, dest)
        return dest
        
    def get(self, name: str, version: str):
        path = self._get_pkg_path(name, version)
        if not os.path.exists(path):
            raise PackageNotFoundError(f"Package {name}@{version} not found in cache")
        return path
