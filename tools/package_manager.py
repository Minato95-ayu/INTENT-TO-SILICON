"""
=============================================================================
FILE: package_manager.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import sys
import json
import hashlib
import shutil
import zipfile
import tempfile
from typing import Dict, List, Optional, Tuple, Any

try:
    import tomllib
except ImportError:
    print("Error: AAYU Package Manager requires Python 3.11+ (tomllib not found).")
    sys.exit(1)

def get_global_aayu_dir() -> str:
    home = os.path.expanduser("~")
    path = os.path.join(home, ".aayu")
    os.makedirs(os.path.join(path, "registry", "index"), exist_ok=True)
    os.makedirs(os.path.join(path, "cache"), exist_ok=True)
    return path

def get_local_project_dir() -> str:
    path = os.getcwd()
    os.makedirs(os.path.join(path, ".aayu", "packages"), exist_ok=True)
    return path

class AAYUPackageManager:
    def __init__(self):
        self.global_dir = get_global_aayu_dir()
        self.registry_dir = os.path.join(self.global_dir, "registry")
        self.cache_dir = os.path.join(self.global_dir, "cache")
        
        self.local_dir = get_local_project_dir()
        self.packages_dir = os.path.join(self.local_dir, ".aayu", "packages")
        
        self.aayu_toml_path = os.path.join(self.local_dir, "aayu.toml")
        self.aayu_lock_path = os.path.join(self.local_dir, "aayu.lock")

    def _read_toml(self, path: str) -> Dict:
        if not os.path.exists(path):
            return {}
        with open(path, "rb") as f:
            return tomllib.load(f)


    def _write_toml(self, path: str, data: Dict):
        # A simple recursive TOML writer for MVP
        def format_value(v):
            if isinstance(v, dict):
                items = []
                for kk, vv in v.items():
                    items.append(f"{kk} = {format_value(vv)}")
                return "{ " + ", ".join(items) + " }"
            elif isinstance(v, str):
                return f'"{v}"'
            elif isinstance(v, bool):
                return "true" if v else "false"
            elif v is None:
                return '""'
            else:
                return str(v)

        with open(path, "w", encoding="utf-8") as f:
            for key, value in data.items():
                if isinstance(value, dict) and key in ["dependencies", "packages", "versions"]:
                    if key == "versions":
                        for v_key, v_val in value.items():
                            f.write(f'\n[versions."{v_key}"]\n'.replace('\n', '\n'))
                            for meta_k, meta_v in v_val.items():
                                f.write(f'{meta_k} = {format_value(meta_v)}\n'.replace('\n', '\n'))
                    else:
                        f.write(f"\n[{key}]\n".replace('\n', '\n'))
                        for k, v in value.items():
                            f.write(f'{k} = {format_value(v)}\n'.replace('\n', '\n'))
                else:
                    f.write(f'{key} = {format_value(value)}\n'.replace('\n', '\n'))
    def _write_lock(self, resolved: Dict[str, str]):
        lock_data = {}
        for pkg, ver in resolved.items():
            lock_data[pkg] = ver
        self._write_toml(self.aayu_lock_path, {"packages": lock_data})

    def init_project(self, name: str):
        if os.path.exists(self.aayu_toml_path):
            print("Error: aayu.toml already exists.")
            return False
            
        data = {
            "name": name,
            "version": "0.1.0",
            "dependencies": {}
        }
        self._write_toml(self.aayu_toml_path, data)
        print(f"Initialized new AAYU project: {name}")
        return True

    def _get_registry_index(self, package_name: str) -> Optional[Dict]:
        index_path = os.path.join(self.registry_dir, "index", package_name, "index.toml")
        if not os.path.exists(index_path):
            return None
        return self._read_toml(index_path)

    def _resolve_graph(self, root_deps: Dict[str, str]) -> Dict[str, str]:
        resolved = {}
        visited = set()
        queue = list(root_deps.items())
        
        while queue:
            pkg_name, req_ver = queue.pop(0)
            if pkg_name in visited:
                continue
                
            idx = self._get_registry_index(pkg_name)
            if not idx or "versions" not in idx:
                print(f"Error: Package '{pkg_name}' not found in registry.")
                sys.exit(1)
                
            versions = idx["versions"]
            
            # Simple resolution: pick required version or latest if '*'
            target_ver = req_ver
            if target_ver == "*":
                target_ver = list(versions.keys())[-1] # Simplistic sort
            
            if target_ver not in versions:
                print(f"Error: Version '{target_ver}' for '{pkg_name}' not found.")
                sys.exit(1)
                
            resolved[pkg_name] = target_ver
            visited.add(pkg_name)
            
            # Queue nested dependencies
            pkg_meta = versions[target_ver]
            if "dependencies" in pkg_meta:
                for nested_pkg, nested_ver in pkg_meta["dependencies"].items():
                    if nested_pkg not in resolved:
                        queue.append((nested_pkg, nested_ver))
                    elif resolved[nested_pkg] != nested_ver and nested_ver != "*":
                        print(f"Conflict: {pkg_name} requires {nested_pkg}@{nested_ver} but {resolved[nested_pkg]} is selected.")
                        
        return resolved

    def _verify_hash(self, filepath: str, expected_hash: str) -> bool:
        sha256 = hashlib.sha256()
        with open(filepath, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        return sha256.hexdigest() == expected_hash

    def _install_from_cache(self, package_name: str, version: str, expected_hash: str):
        tarball = os.path.join(self.cache_dir, f"{package_name}-{version}.zip")
        if not os.path.exists(tarball):
            print(f"Error: {tarball} not found in cache. Ensure offline registry is populated.")
            sys.exit(1)
            
        if not self._verify_hash(tarball, expected_hash):
            print(f"Error: Hash mismatch for {package_name}@{version}. Rejecting.")
            sys.exit(1)
            
        # Extract to local .aayu/packages/
        dest = os.path.join(self.packages_dir, package_name)
        if os.path.exists(dest):
            shutil.rmtree(dest)
            
        with zipfile.ZipFile(tarball, 'r') as zip_ref:
            zip_ref.extractall(dest)
        print(f"Installed {package_name} v{version}")

    def install(self, package_name: Optional[str] = None, version: str = "*"):
        # Run pre-install hook
        print("Running pre-install hooks...")
        
        project = self._read_toml(self.aayu_toml_path)
        if "dependencies" not in project:
            project["dependencies"] = {}
            
        if package_name:
            project["dependencies"][package_name] = version
            self._write_toml(self.aayu_toml_path, project)
            
        deps = project.get("dependencies", {})
        if not deps:
            print("No dependencies to install.")
            return

        print("Resolving dependencies...")
        resolved = self._resolve_graph(deps)
        
        for pkg, ver in resolved.items():
            idx = self._get_registry_index(pkg)
            if not idx: continue
            expected_hash = idx["versions"][ver].get("hash", "")
            self._install_from_cache(pkg, ver, expected_hash)
            
        self._write_lock(resolved)
        print("Installation complete. Lockfile generated.")
        
        # Run post-install hook
        print("Running post-install hooks...")

    def remove(self, package_name: str):
        project = self._read_toml(self.aayu_toml_path)
        if "dependencies" in project and package_name in project["dependencies"]:
            del project["dependencies"][package_name]
            self._write_toml(self.aayu_toml_path, project)
            
        dest = os.path.join(self.packages_dir, package_name)
        if os.path.exists(dest):
            shutil.rmtree(dest)
            
        # Re-resolve graph
        self.install()
        print(f"Removed {package_name}")
        
    def update(self, package_name: Optional[str] = None):
        print("Updating packages (Mocked)...")
        self.install()
        
    def search(self, query: str):
        index_dir = os.path.join(self.registry_dir, "index")
        if not os.path.exists(index_dir):
            print("Registry empty.")
            return
            
        print(f"Search results for '{query}':")
        found = False
        for pkg in os.listdir(index_dir):
            if query.lower() in pkg.lower():
                idx = self._read_toml(os.path.join(index_dir, pkg, "index.toml"))
                latest = list(idx.get("versions", {}).keys())[-1] if "versions" in idx else "unknown"
                print(f"  {pkg} - v{latest}")
                found = True
        if not found:
            print("  No packages found.")
            
    def publish(self):
        project = self._read_toml(self.aayu_toml_path)
        if not project:
            print("Error: No aayu.toml found.")
            return
            
        name = project.get("name")
        version = project.get("version", "0.1.0")
        
        if not name:
            print("Error: Package name missing in aayu.toml")
            return
            
        # 1. Zip project directory (excluding .aayu)
        archive_name = f"{name}-{version}.zip"
        archive_path = os.path.join(tempfile.gettempdir(), archive_name)
        
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.local_dir):
                if ".aayu" in root or "__pycache__" in root:
                    continue
                for file in files:
                    if file.endswith(".zip"): continue
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.local_dir)
                    zipf.write(full_path, rel_path)
                    
        # 2. Compute hash
        sha256 = hashlib.sha256()
        with open(archive_path, "rb") as f:
            for block in iter(lambda: f.read(4096), b""):
                sha256.update(block)
        pkg_hash = sha256.hexdigest()
        
        # 3. Copy to global cache
        shutil.copy2(archive_path, os.path.join(self.cache_dir, archive_name))
        
        # 4. Update global registry index
        idx_dir = os.path.join(self.registry_dir, "index", name)
        os.makedirs(idx_dir, exist_ok=True)
        idx_file = os.path.join(idx_dir, "index.toml")
        
        idx_data = self._read_toml(idx_file) if os.path.exists(idx_file) else {"versions": {}}
        if "versions" not in idx_data: idx_data["versions"] = {}
        
        idx_data["versions"][version] = {
            "hash": pkg_hash,
            "dependencies": project.get("dependencies", {})
        }
        self._write_toml(idx_file, idx_data)
        
        print(f"Successfully published {name} v{version} to local registry.")
        print(f"SHA256: {pkg_hash}")
