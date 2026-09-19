# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

from typing import Dict, List, Optional
import sys

class PubGrubResolver:
    """
    Stub for a full PubGrub dependency resolver.
    Currently falls back to the simple BFS resolver.
    """
    def __init__(self, registry_fetcher):
        self.fetcher = registry_fetcher

    def resolve(self, root_dependencies: Dict[str, str]) -> Dict[str, str]:
        print("[PubGrub] Initializing dependency resolution...")
        # TODO: Implement full PubGrub algorithm with Incompatibilities and Derivation Trees.
        # Fallback to simple BFS resolution for now.
        return self._simple_resolve(root_dependencies)
        
    def _simple_resolve(self, root_deps: Dict[str, str]) -> Dict[str, str]:
        resolved = {}
        visited = set()
        queue = list(root_deps.items())
        
        while queue:
            pkg_name, req_ver = queue.pop(0)
            if pkg_name in visited:
                continue
                
            idx = self.fetcher(pkg_name)
            if not idx or "versions" not in idx:
                print(f"Error: Package '{pkg_name}' not found in registry.")
                sys.exit(1)
                
            versions = idx["versions"]
            
            target_ver = req_ver
            if target_ver == "*":
                target_ver = list(versions.keys())[-1]
            
            if target_ver not in versions:
                print(f"Error: Version '{target_ver}' for '{pkg_name}' not found.")
                sys.exit(1)
                
            resolved[pkg_name] = target_ver
            visited.add(pkg_name)
            
            pkg_meta = versions[target_ver]
            if "dependencies" in pkg_meta:
                for nested_pkg, nested_ver in pkg_meta["dependencies"].items():
                    if nested_pkg not in resolved:
                        queue.append((nested_pkg, nested_ver))
                    elif resolved[nested_pkg] != nested_ver and nested_ver != "*":
                        print(f"Conflict: {pkg_name} requires {nested_pkg}@{nested_ver} but {resolved[nested_pkg]} is selected.")
                        
        return resolved
