from typing import List, Dict, Set
from .models import InstalledPackage
from manifest.model import Version

class PackageNode:
    def __init__(self, name: str, version: Version):
        self.name = name
        self.version = version
        
    def __eq__(self, other):
        if not isinstance(other, PackageNode):
            return False
        return self.name == other.name and str(self.version) == str(other.version)
        
    def __hash__(self):
        return hash((self.name, str(self.version)))

class PackageEdge:
    def __init__(self, from_node: PackageNode, to_node: PackageNode):
        self.from_node = from_node
        self.to_node = to_node

class PackageGraph:
    def __init__(self):
        self.nodes: Dict[str, PackageNode] = {}
        self.edges: List[PackageEdge] = []
        self.dependencies: Dict[str, List[str]] = {}
        
    def add_node(self, node: PackageNode):
        if node.name not in self.nodes:
            self.nodes[node.name] = node
            self.dependencies[node.name] = []
            
    def add_edge(self, from_node: PackageNode, to_node: PackageNode):
        self.add_node(from_node)
        self.add_node(to_node)
        
        edge = PackageEdge(from_node, to_node)
        self.edges.append(edge)
        
        if to_node.name not in self.dependencies[from_node.name]:
            self.dependencies[from_node.name].append(to_node.name)
            
    def get_topological_order(self) -> List[str]:
        visited = set()
        temp_mark = set()
        order = []
        
        def visit(node: str):
            if node in temp_mark:
                raise Exception(f"Circular package dependency detected involving '{node}'")
            if node not in visited:
                temp_mark.add(node)
                for dep in self.dependencies.get(node, []):
                    visit(dep)
                temp_mark.remove(node)
                visited.add(node)
                order.append(node)
                
        for node in self.nodes:
            if node not in visited:
                visit(node)
                
        return order
