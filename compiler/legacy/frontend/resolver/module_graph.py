"""
=============================================================================
FILE: module_graph.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import Dict, List, Set

class ModuleGraph:
    def __init__(self):
        # module_name -> list of dependencies (module_names)
        self.dependencies: Dict[str, List[str]] = {}
        
    def add_module(self, module_name: str):
        if module_name not in self.dependencies:
            self.dependencies[module_name] = []
            
    def add_dependency(self, from_module: str, to_module: str):
        self.add_module(from_module)
        self.add_module(to_module)
        if to_module not in self.dependencies[from_module]:
            self.dependencies[from_module].append(to_module)
            
    def get_topological_order(self) -> List[str]:
        """
        Returns a topologically sorted list of modules using Kahn's algorithm or DFS.
        Raises an Exception if a cycle is detected.
        """
        visited = set()
        temp_mark = set()
        order = []
        
        def visit(node: str):
            if node in temp_mark:
                raise Exception(f"Circular dependency detected involving module '{node}'")
            if node not in visited:
                temp_mark.add(node)
                for dep in self.dependencies.get(node, []):
                    visit(dep)
                temp_mark.remove(node)
                visited.add(node)
                order.append(node)
                
        for module in self.dependencies:
            if module not in visited:
                visit(module)
                
        return order
