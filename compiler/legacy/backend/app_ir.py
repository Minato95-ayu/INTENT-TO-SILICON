import json
from typing import Dict, Any, List
from compiler.frontend.ast_nodes import (
    Node, ProgramNode, ProjectDefNode, PageDefNode, TitleDefNode, ButtonDefNode, UIServeNode,
    ThemeNode, StateDefNode, RouteDefNode, EventNode, LayoutNode, ComponentNode, TextNode, VariableNode,
    StorageNode, ModelNode, ServiceNode, SecurityNode
)

class AppIRBuilder:
    """
    Transforms AAYU AST into a generalized JSON-like Application Intermediate Representation (App IR).
    This acts as the single source of truth for all downstream platform adapters (React, Express, Prisma, etc.).
    """
    def __init__(self, ast: ProgramNode):
        self.ast = ast
        self.ir = {
            "project": "App",
            "ui_ir": {
                "pages": [],
                "themes": [],
                "state": [],
                "routes": [],
                "serve": False
            },
            "data_ir": {
                "storages": [],
                "models": []
            },
            "api_ir": {
                "services": []
            },
            "security_ir": {
                "features": []
            },
            "config_ir": {},
            "deployment_ir": {},
            "package_ir": {}
        }

    def build(self) -> Dict[str, Any]:
        for stmt in self.ast.statements:
            if isinstance(stmt, ProjectDefNode):
                self.ir["project"] = stmt.name
            
            elif isinstance(stmt, ThemeNode):
                self.ir["ui_ir"]["themes"].append({
                    "name": stmt.name,
                    "properties": {prop["name"]: self._serialize_val(prop["value"]) for prop in stmt.properties}
                })
                
            elif isinstance(stmt, StateDefNode):
                self.ir["ui_ir"]["state"].append({
                    "name": stmt.name,
                    "initial_value": self._serialize_val(stmt.initial_value)
                })
                
            elif isinstance(stmt, RouteDefNode):
                self.ir["ui_ir"]["routes"].append({
                    "path": stmt.path,
                    "target_page": stmt.target_page
                })
                
            elif isinstance(stmt, PageDefNode):
                page_ir = {
                    "type": "page",
                    "name": stmt.name,
                    "children": []
                }
                if stmt.children:
                    for child in stmt.children:
                        page_ir["children"].append(self._build_component_node(child))
                self.ir["ui_ir"]["pages"].append(page_ir)
                
            elif isinstance(stmt, UIServeNode):
                self.ir["ui_ir"]["serve"] = True

            # Phase 2 Nodes
            elif isinstance(stmt, StorageNode):
                self.ir["data_ir"]["storages"].append({
                    "name": stmt.name
                })
                
            elif isinstance(stmt, ModelNode):
                self.ir["data_ir"]["models"].append({
                    "name": stmt.name,
                    "fields": [{"name": f.name, "type": f.field_type} for f in stmt.fields]
                })
                
            elif isinstance(stmt, ServiceNode):
                self.ir["api_ir"]["services"].append({
                    "name": stmt.name,
                    "endpoints": [{"method": e.method, "path": e.path, "returns": e.returns, "action": self._serialize_action_block(e.action_block) if e.action_block else None} for e in stmt.endpoints]
                })
                
            elif isinstance(stmt, SecurityNode):
                self.ir["security_ir"]["features"].extend(stmt.features)

        return self.ir

    def _build_component_node(self, node: Node) -> Dict[str, Any]:
        if isinstance(node, StateDefNode):
            # If state is defined inside a page, bubble it up to the global/page state
            self.ir["state_tree"].append({
                "name": node.name,
                "initial_value": self._serialize_val(node.initial_value)
            })
            return {"type": "state_binding", "name": node.name}

        comp_ir = {}
        if isinstance(node, LayoutNode):
            comp_ir["type"] = node.layout_type
            comp_ir["category"] = "layout"
            comp_ir["properties"] = self._build_properties(node.properties)
            comp_ir["children"] = [self._build_component_node(c) for c in node.children]
        elif isinstance(node, ComponentNode):
            comp_ir["type"] = node.component_type
            comp_ir["category"] = "component"
            comp_ir["properties"] = self._build_properties(node.properties)
            comp_ir["children"] = [self._build_component_node(c) for c in node.children] if node.children else []
        elif isinstance(node, TitleDefNode):
             comp_ir = {"type": "heading", "category": "component", "properties": {"text": node.text}, "children": []}
        elif isinstance(node, ButtonDefNode):
             comp_ir = {"type": "button", "category": "component", "properties": {"text": node.text}, "children": []}
        return comp_ir

    def _build_properties(self, properties: list) -> Dict[str, Any]:
        props = {}
        for prop in properties:
            name = prop["name"]
            val = prop["value"]
            if name == "event" and isinstance(val, EventNode):
                # We could register it in event_tree or embed it. Embedding is easier for now.
                props["on_" + val.event_type] = self._serialize_action_block(val.action_block)
            else:
                props[name] = self._serialize_val(val)
        return props

    def _serialize_val(self, val_node: Node) -> Any:
        if isinstance(val_node, TextNode):
            return val_node.value
        elif type(val_node).__name__ == 'NumberNode':
            return val_node.value
        elif isinstance(val_node, VariableNode):
            return {"__bind__": val_node.name}
        return str(val_node)

    def _serialize_action_block(self, block_node: Node) -> str:
        # Simplistic AST serialization to JS code for React generator
        # Normally, we'd use a full backend compiler to transpile AAYU AST to JS.
        # For now, we'll extract binary expressions for state updates.
        code = []
        for stmt in block_node.statements:
            if type(stmt).__name__ == "BinaryExpressionNode" and stmt.operator == "+=":
                code.append(f"set{stmt.left.name.capitalize()}((prev: any) => prev + {self._serialize_val(stmt.right)});")
        return " ".join(code)

    def dump_json(self) -> str:
        return json.dumps(self.build(), indent=2)
