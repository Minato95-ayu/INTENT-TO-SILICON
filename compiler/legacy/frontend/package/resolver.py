"""
=============================================================================
FILE: resolver.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import List, Dict, Optional
from manifest.model import PackageManifest, Dependency
from compiler.frontend.compiler_context import Diagnostics
from .graph import PackageGraph, PackageNode, PackageEdge
from .registry import RegistryClient

class DependencyResolver:
    def __init__(self, diagnostics: Diagnostics, registry: RegistryClient):
        self.diagnostics = diagnostics
        self.registry = registry
        
    def resolve(self, root_manifest: PackageManifest) -> PackageGraph:
        graph = PackageGraph()
        visited = set()
        
        # Add root node (the workspace itself)
        root_node = PackageNode(root_manifest.package.name, root_manifest.package.version)
        graph.add_node(root_node)
        
        self._resolve_dependencies(root_manifest.dependencies, root_node, graph, visited)
        
        # Verify cycles by trying topological sort
        try:
            graph.get_topological_order()
        except Exception as e:
            self.diagnostics.error(str(e), "Aayu.toml")
            
        return graph
        
    def _resolve_dependencies(self, dependencies: Dict[str, Dependency], parent_node: PackageNode, graph: PackageGraph, visited: set):
        for name, dep in dependencies.items():
            manifest = self.registry.resolve(name, dep.version)
            if not manifest:
                self.diagnostics.error(f"PackageNotFound: Could not resolve dependency '{name}' version '{dep.version}'", "Aayu.toml")
                continue
                
            dep_node = PackageNode(manifest.package.name, manifest.package.version)
            
            # Check duplicate/conflict
            if dep_node.name in graph.nodes:
                existing = graph.nodes[dep_node.name]
                if str(existing.version) != str(dep_node.version):
                    self.diagnostics.error(f"DependencyConflict: '{dep_node.name}' has conflicting versions ({existing.version} vs {dep_node.version})", "Aayu.toml")
            
            graph.add_edge(parent_node, dep_node)
            
            if dep_node.name not in visited:
                visited.add(dep_node.name)
                self._resolve_dependencies(manifest.dependencies, dep_node, graph, visited)
