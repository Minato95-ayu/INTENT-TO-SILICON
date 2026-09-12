import json
from typing import Any, Dict

from compiler.ast.nodes import AppDeclarationNode, ProgramNode, WidgetNode

class UIIRBuilder:
    """
    Transforms AAYU AST into a generalized JSON-like Intermediate Representation (UI IR).
    This acts as the single source of truth for all downstream UI generators (React, HTML, Flutter, etc.).
    """
    def __init__(self, ast: ProgramNode):
        self.ast = ast
        self.ir = {
            "project": "App",
            "pages": [],
            "serve": False
        }

    def build(self) -> Dict[str, Any]:
        current_page = None

        for stmt in self.ast.statements:
            if isinstance(stmt, AppDeclarationNode):
                self.ir["project"] = stmt.name

            elif isinstance(stmt, WidgetNode) and stmt.widget_type.lower() == "page":
                current_page = {
                    "name": stmt.props.get("name", "Home"),
                    "components": []
                }
                self.ir["pages"].append(current_page)

                current_page["components"].extend(
                    self._serialize_widget(child) for child in stmt.children
                )

            elif isinstance(stmt, WidgetNode):
                if current_page is None:
                    current_page = {"name": "Home", "components": []}
                    self.ir["pages"].append(current_page)
                current_page["components"].append(self._serialize_widget(stmt))

            elif type(stmt).__name__ == "RunNode":
                self.ir["serve"] = True

        return self.ir

    def _serialize_widget(self, widget: WidgetNode) -> Dict[str, Any]:
        properties = {key: self._serialize_value(value) for key, value in widget.props.items()}
        if "value_node" in widget.props:
            properties["text"] = self._serialize_value(widget.props["value_node"])
        return {
            "type": widget.widget_type.lower(),
            "properties": properties,
            "children": [self._serialize_widget(child) for child in widget.children],
        }

    def _serialize_value(self, value: Any) -> Any:
        if hasattr(value, "value"):
            return value.value
        if hasattr(value, "name"):
            return {"__bind__": value.name}
        return value

    def dump_json(self) -> str:
        return json.dumps(self.build(), indent=2)
