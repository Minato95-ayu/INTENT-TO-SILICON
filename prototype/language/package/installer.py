import os
from .graph import PackageGraph
from .registry import RegistryClient
from compiler_context import Diagnostics

class PackageInstaller:
    def __init__(self, diagnostics: Diagnostics, registry: RegistryClient, packages_dir: str):
        self.diagnostics = diagnostics
        self.registry = registry
        self.packages_dir = packages_dir
        
    def install(self, graph: PackageGraph, root_name: str) -> bool:
        if not os.path.exists(self.packages_dir):
            os.makedirs(self.packages_dir)
            
        try:
            order = graph.get_topological_order()
        except Exception:
            return False
            
        success = True
        for pkg_name in order:
            if pkg_name == root_name:
                continue
                
            node = graph.nodes[pkg_name]
            target_dir = os.path.join(self.packages_dir, pkg_name)
            
            if not self.registry.download(node.name, node.version, target_dir):
                self.diagnostics.error(f"Failed to install package '{node.name}'", "PackageManager")
                success = False
                
        return success
