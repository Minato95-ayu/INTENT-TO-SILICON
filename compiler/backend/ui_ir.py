import json
from typing import Dict, Any, List
from compiler.frontend.ast_nodes import (
    ProgramNode, ProjectDefNode, PageDefNode, TitleDefNode, ButtonDefNode, UIServeNode
)

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
            if isinstance(stmt, ProjectDefNode):
                self.ir["project"] = stmt.name
            
            elif isinstance(stmt, PageDefNode):
                current_page = {
                    "name": stmt.name,
                    "components": []
                }
                self.ir["pages"].append(current_page)
                
            elif isinstance(stmt, TitleDefNode):
                if current_page is None:
                    # Default page if none specified
                    current_page = {"name": "Home", "components": []}
                    self.ir["pages"].append(current_page)
                current_page["components"].append({
                    "type": "title",
                    "text": stmt.text
                })
                
            elif isinstance(stmt, ButtonDefNode):
                if current_page is None:
                    current_page = {"name": "Home", "components": []}
                    self.ir["pages"].append(current_page)
                current_page["components"].append({
                    "type": "button",
                    "text": stmt.text
                })
                
            elif isinstance(stmt, UIServeNode):
                self.ir["serve"] = True

        return self.ir

    def dump_json(self) -> str:
        return json.dumps(self.build(), indent=2)
