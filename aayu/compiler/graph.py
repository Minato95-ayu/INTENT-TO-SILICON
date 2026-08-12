from typing import List, Dict, Set
from dataclasses import dataclass, field
import hashlib
import os

from aayu.compiler.workspace import WorkspaceLoader, PackageResolver
from aayu.compiler.resolver import DependencyResolver

@dataclass
class Diagnostic:
    severity: str
    message: str

@dataclass
class ModuleNode:
    name: str
    id: str
    path: str
    version: str
    imports: List[str] = field(default_factory=list)
    exports: List[str] = field(default_factory=list)
    
    # Hashes
    source_hash: str = ""
    ast_hash: str = ""
    hir_hash: str = ""
    mir_hash: str = ""
    dep_hash: str = ""
    
    # Graph edges
    dependencies: List['ModuleNode'] = field(default_factory=list)
    dependents: List['ModuleNode'] = field(default_factory=list)
    
    compile_state: str = "NotParsed"
    diagnostics: List[Diagnostic] = field(default_factory=list)
    
    def compute_source_hash(self):
        if not os.path.exists(self.path):
            self.source_hash = ""
            return
        with open(self.path, "rb") as f:
            data = f.read()
            self.source_hash = hashlib.sha256(data).hexdigest()
            
    def compute_dep_hash(self):
        # The dep_hash is the combined hash of all dependencies' source_hashes (or mir_hashes later)
        # We sort them to ensure deterministic hashing
        dep_hashes = sorted([d.source_hash for d in self.dependencies])
        combined = "".join(dep_hashes).encode("utf-8")
        self.dep_hash = hashlib.sha256(combined).hexdigest()

class ModuleGraph:
    """
    Constructs a Directed Acyclic Graph (DAG) of the workspace.
    Employs Kahn's Algorithm for Topological Sort and deterministic Cycle Detection.
    """
    def __init__(self, workspace: WorkspaceLoader):
        self.workspace = workspace
        self.package_resolver = PackageResolver(workspace)
        self.dependency_resolver = DependencyResolver()
        self.nodes: Dict[str, ModuleNode] = {}
        
    def build_graph(self):
        # We start by registering all packages in the workspace
        # In a real compiler, we might only traverse starting from 'main', 
        # but indexing the whole workspace guarantees all nodes exist.
        for pkg_name, config in self.workspace.members.items():
            entry_path = self.package_resolver.resolve(pkg_name)
            if not entry_path:
                continue
                
            node = ModuleNode(
                name=pkg_name,
                id=pkg_name,
                path=entry_path,
                version=config.package.version
            )
            node.compute_source_hash()
            self.nodes[pkg_name] = node
            
        # Extract imports and build edges
        for node in self.nodes.values():
            imports = self.dependency_resolver.get_dependencies_for_file(node.path)
            # Dedup
            seen = set()
            for imp in imports:
                if imp not in seen:
                    seen.add(imp)
                    node.imports.append(imp)
                    
            for imp in node.imports:
                if imp in self.nodes:
                    dep_node = self.nodes[imp]
                    node.dependencies.append(dep_node)
                    dep_node.dependents.append(node)
                    
        # Compute dep hashes bottom-up roughly, but Kahn's sort will allow strict bottom up.
        # We'll defer dep_hash calculation to the topological sort sequence if needed.

    def kahn_topological_sort(self) -> List[ModuleNode]:
        """
        Returns a bottom-up compilation order using Kahn's Algorithm.
        Raises an exception if a cycle is detected, tracing the exact cyclic path.
        """
        in_degree = {node_id: len(node.dependencies) for node_id, node in self.nodes.items()}
        queue = [self.nodes[node_id] for node_id, degree in in_degree.items() if degree == 0]
        
        # We sort queue alphabetically for determinism
        queue.sort(key=lambda n: n.id)
        
        sorted_nodes = []
        
        while queue:
            node = queue.pop(0)
            sorted_nodes.append(node)
            
            # Since we are compiling bottom-up, node is a leaf or its dependencies are met.
            # dependents are the parents who depend on `node`.
            dependents_to_process = sorted(node.dependents, key=lambda n: n.id)
            for dependent in dependents_to_process:
                in_degree[dependent.id] -= 1
                if in_degree[dependent.id] == 0:
                    queue.append(dependent)
                    
        if len(sorted_nodes) != len(self.nodes):
            self._report_cycle(in_degree)
            
        return sorted_nodes
        
    def _report_cycle(self, in_degree: Dict[str, int]):
        # Nodes with in_degree > 0 are part of the cycle
        cycle_nodes = {node_id for node_id, degree in in_degree.items() if degree > 0}
        
        # Find one path using DFS within the cycle_nodes
        path = []
        visited = set()
        
        def dfs(curr: str):
            if curr in visited:
                path.append(curr)
                return True
            visited.add(curr)
            path.append(curr)
            
            node = self.nodes[curr]
            # explore dependencies that are also in the cycle
            for dep in node.dependencies:
                if dep.id in cycle_nodes:
                    if dfs(dep.id):
                        return True
            path.pop()
            return False

        # Start from any cycle node
        start_node = next(iter(cycle_nodes))
        dfs(start_node)
        
        # Extract the exact cycle
        if len(path) > 1:
            cycle_start_index = path.index(path[-1])
            actual_cycle = path[cycle_start_index:]
            
            trace_str = " -> ".join(actual_cycle)
            
            # Generate professional diagnostic
            msg = f"Circular Dependency Detected!\n\n"
            for p in actual_cycle:
                msg += f" {p}\n ↓\n"
            msg = msg.rstrip(" ↓\n")
            
            prob_lines = []
            for i in range(len(actual_cycle)-1):
                prob_lines.append(f"{actual_cycle[i]} imports {actual_cycle[i+1]}")
                
            msg += f"\n\nProblem:\n" + "\n".join(prob_lines)
            msg += f"\n\nSuggestion:\nExtract shared state/structs into a common base module."
            
            raise ValueError(msg)
        
        raise ValueError("Circular dependency detected, but could not trace the exact path.")
