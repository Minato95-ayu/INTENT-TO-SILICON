import json
from typing import Any, Dict

from compiler.ast.nodes import (
    ASTNode,
    AppDeclarationNode,
    ArrayNode,
    BinaryOpNode,
    ExternLibraryNode,
    IdentifierNode,
    LiteralNode,
    ModelDeclNode,
    ProgramNode,
    RouteNode,
    StateDeclarationNode,
    ThemeNode,
    WidgetNode,
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
            if isinstance(stmt, AppDeclarationNode):
                self.ir["project"] = stmt.name

            elif isinstance(stmt, ThemeNode):
                self.ir["ui_ir"]["themes"].append({
                    "name": stmt.name,
                    "properties": {name: self._serialize_val(value) for name, value in stmt.properties.items()}
                })

            elif isinstance(stmt, StateDeclarationNode):
                self.ir["ui_ir"]["state"].append({
                    "name": stmt.name,
                    "initial_value": self._serialize_val(stmt.value)
                })

            elif isinstance(stmt, RouteNode):
                self.ir["ui_ir"]["routes"].append({
                    "path": stmt.path,
                    "methods": [
                        {"method": method.method, "body": [type(node).__name__ for node in method.body]}
                        for method in stmt.methods
                    ]
                })

            elif isinstance(stmt, WidgetNode) and stmt.widget_type.lower() == "page":
                page_ir = {
                    "type": "page",
                    "name": stmt.props.get("name", "Home"),
                    "children": []
                }
                page_ir["children"] = [self._build_component_node(child) for child in stmt.children]
                self.ir["ui_ir"]["pages"].append(page_ir)

            elif isinstance(stmt, ModelDeclNode):
                self.ir["data_ir"]["models"].append({
                    "name": stmt.name,
                    "fields": [{"name": field.name, "type": field.field_type} for field in stmt.fields],
                    "decorators": stmt.decorators,
                })

            elif isinstance(stmt, ExternLibraryNode):
                self.ir.setdefault("interop_ir", {"libraries": []})["libraries"].append({
                    "name": stmt.name,
                    "provider": stmt.provider,
                })

        self._add_generator_compatibility_views()

        return self.ir

    def _build_component_node(self, node: ASTNode) -> Dict[str, Any]:
        if isinstance(node, StateDeclarationNode):
            # If state is defined inside a page, bubble it up to the global/page state
            self.ir["ui_ir"]["state"].append({
                "name": node.name,
                "initial_value": self._serialize_val(node.value)
            })
            return {"type": "state_binding", "name": node.name}

        if not isinstance(node, WidgetNode):
            return {"type": type(node).__name__, "properties": {}, "children": []}

        properties = {key: self._serialize_val(value) for key, value in node.props.items()}
        if "value_node" in node.props:
            properties["text"] = self._serialize_val(node.props["value_node"])

        return {
            "type": node.widget_type.lower(),
            "category": "component",
            "properties": properties,
            "children": [self._build_component_node(child) for child in node.children],
        }

    def _serialize_val(self, val_node: Any) -> Any:
        if isinstance(val_node, LiteralNode):
            return val_node.value
        if isinstance(val_node, IdentifierNode):
            return {"__bind__": val_node.name}
        if isinstance(val_node, ArrayNode):
            return [self._serialize_val(value) for value in val_node.elements]
        if isinstance(val_node, BinaryOpNode):
            return {
                "left": self._serialize_val(val_node.left),
                "operator": val_node.operator,
                "right": self._serialize_val(val_node.right),
            }
        if isinstance(val_node, ASTNode):
            return {"__node__": type(val_node).__name__}
        return val_node

    def _add_generator_compatibility_views(self) -> None:
        """Expose legacy generator keys while adapters migrate to the canonical IR."""
        ui_ir = self.ir["ui_ir"]
        self.ir["theme_tree"] = ui_ir["themes"][0] if ui_ir["themes"] else None
        self.ir["state_tree"] = ui_ir["state"]
        self.ir["route_tree"] = ui_ir["routes"]
        self.ir["ui_tree"] = ui_ir["pages"]
        self.ir["serve"] = ui_ir["serve"]

    def dump_json(self) -> str:
        return json.dumps(self.build(), indent=2)
