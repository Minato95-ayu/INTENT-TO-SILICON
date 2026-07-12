"""
=============================================================================
FILE: ir_generator.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
from typing import Dict, Any, List
import compiler.frontend.ast_nodes as ast

class IRGenerator:
    """
    Translates an AAYU AST (ProgramNode) into the AAYU Intermediate Representation (IR).
    The IR stores architecture, not behavior. Behavior remains inside the AST.
    """
    def __init__(self):
        self.ir: Dict[str, Any] = {
            "ir_version": "1.0",
            "system": {"name": "AAYU_App"},
            "entities": [],
            "relations": [],
            "roles": [],
            "permissions": [],
            "pages": [],
            "workflows": [],
            "routes": [],
            "modules": [],
            "features": []
        }
        self.detected_features = set()

    def generate(self, program: ast.ProgramNode) -> str:
        self._traverse(program.statements)
        self.ir["features"] = list(self.detected_features)
        return json.dumps(self.ir, indent=2)

    def _traverse(self, nodes: List[ast.Node]):
        for node in nodes:
            if isinstance(node, ast.EntityDeclarationNode):
                self.ir["entities"].append({
                    "name": node.name,
                    "fields": node.fields
                })
                self.detected_features.add("database")
            elif isinstance(node, ast.RelationDefNode):
                self.ir["relations"].append({
                    "source": node.entity1,
                    "type": node.rel_type,
                    "target": node.entity2
                })
                self.detected_features.add("database")
            elif isinstance(node, ast.RoleDefNode):
                self.ir["roles"].append({
                    "name": node.name
                })
                self.detected_features.add("rbac")
            elif isinstance(node, ast.AllowDefNode):
                self.ir["permissions"].append({
                    "role": node.role,
                    "action": node.action,
                    "target": node.target_entity
                })
                self.detected_features.add("rbac")
            elif isinstance(node, ast.UIPageNode):
                self.ir["pages"].append({
                    "name": node.name
                })
                self.detected_features.add("ui")
            elif isinstance(node, ast.WorkflowDefNode):
                steps = []
                for step in node.steps:
                    steps.append(step.name)
                self.ir["workflows"].append({
                    "name": node.name,
                    "entity": node.entity_name,
                    "steps": steps
                })
                self.detected_features.add("workflow")
            elif isinstance(node, ast.RouteNode):
                self.ir["routes"].append({
                    "path": node.path.value if isinstance(node.path, ast.TextNode) else str(node.path),
                    "method": node.method.upper(),
                    "handler": node.handler_name
                })
                self.detected_features.add("api")
            elif isinstance(node, ast.UseNode):
                self.ir["modules"].append({
                    "name": node.module
                })
                if node.module == "http":
                    self.detected_features.add("api")
                elif node.module == "db":
                    self.detected_features.add("database")
                elif node.module == "auth" or node.module == "rbac":
                    self.detected_features.add("rbac")
            # For blocks that might contain declarative sub-nodes (like tests, tasks), 
            # we generally ignore behavior for IR v1, but we can recursively search 
            # if we wanted to find nested declarations. For now, declarative nodes 
            # are top level in AAYU.

def generate_ir(ast_tree: ast.ProgramNode) -> str:
    generator = IRGenerator()
    return generator.generate(ast_tree)
