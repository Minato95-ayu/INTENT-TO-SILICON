from typing import Dict, List
from .semver import SemVer
from .exceptions import CircularDependencyError, ResolutionError, PackageNotFoundError

class Resolver:
    """Resolves dependency graphs and detects circular dependencies."""
    
    def __init__(self, registry):
        self.registry = registry
        
    def resolve(self, root_dependencies: dict) -> dict:
        """
        Takes a dict of { "pkg_name": "version_req" }
        Returns a flat dict of { "pkg_name": {"version": "...", "checksum": "...", "deps": {...}} }
        """
        resolved = {}
        visiting = set()
        
        def _visit(name, req):
            if name in visiting:
                path = " -> ".join(list(visiting) + [name])
                raise CircularDependencyError(f"Circular Dependency Detected\n{path}")
                
            if name in resolved:
                # Basic conflict check
                existing_ver = resolved[name]["version"]
                if not SemVer(req).satisfies(existing_ver):
                    raise ResolutionError(f"Version conflict for {name}: {req} vs {existing_ver}")
                return
                
            visiting.add(name)
            
            meta = self.registry.fetch_manifest(name, req)
            if not meta or "versions" not in meta:
                raise PackageNotFoundError(f"Package {name} not found in registry")
                
            # Find highest compatible version
            best_ver = None
            req_semver = SemVer(req)
            for v in meta["versions"].keys():
                if req_semver.satisfies(v):
                    # We just take the first compatible for now (in real PM, sort descending)
                    best_ver = v
                    break
                    
            if not best_ver:
                raise ResolutionError(f"No compatible version found for {name} matching {req}")
                
            version_meta = meta["versions"][best_ver]
            
            # Store resolved info
            resolved[name] = {
                "version": best_ver,
                "checksum": version_meta.get("checksum", ""),
                "dependencies": version_meta.get("dependencies", {})
            }
            
            # Recurse
            for dep_name, dep_req in version_meta.get("dependencies", {}).items():
                _visit(dep_name, dep_req)
                
            visiting.remove(name)
            
        for pkg, req in root_dependencies.items():
            _visit(pkg, req)
            
        return resolved
