import os
import json
from compiler.ast.nodes import ProgramNode, WidgetNode, StateDeclarationNode, LiteralNode

class WebTarget:
    """Transpiles AAYU AST directly to standard HTML/CSS/JS via Intermediate DOM."""
    
    def __init__(self):
        self.state_vars = {}
        
    def build(self, ast, assets):
        print("[Builder] Transpiling AST to Web components...")
        
        # 1. Walk AST to build Intermediate DOM
        idom, state, actions = self._generate_idom(ast)
        
        # 2. Render IDOM to HTML and JS
        html_body = self._render_html(idom)
        js_logic = self._render_js(state, actions)
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>AAYU Web App</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="style.css">
    <script src="app.js" defer></script>
</head>
<body>
    <div id="app">
        {html_body}
    </div>
</body>
</html>"""

        out_dir = os.path.join("build", "web")
        os.makedirs(out_dir, exist_ok=True)
        
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(html_content)
            
        with open(os.path.join(out_dir, "style.css"), "w", encoding="utf-8") as f:
            f.write("body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f9; padding: 20px; }\n")
            f.write(".card { background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); padding: 20px; margin: 10px 0; }\n")
            f.write("button { background: #4F46E5; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }\n")
            f.write("input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; margin-right: 10px; }\n")
            
        with open(os.path.join(out_dir, "app.js"), "w", encoding="utf-8") as f:
            f.write(js_logic)
            
        print(f"[Builder] Web bundle generated at: {out_dir}")
        print("[Builder] Successfully generated web package.")

    def _generate_idom(self, ast):
        if not ast:
            # Fallback for mock builds where ast might be None
            return [{"type": "Text", "content": "Welcome to AAYU Web App!"}], {"greeting": "Hello World"}, []
            
        idom = []
        state = {}
        actions = []
        if isinstance(ast, ProgramNode):
            for stmt in ast.statements:
                if isinstance(stmt, StateDeclarationNode):
                    val = stmt.value.value if isinstance(stmt.value, LiteralNode) else ""
                    state[stmt.name] = val
                elif isinstance(stmt, WidgetNode):
                    idom.append(self._widget_to_idom(stmt))
                elif type(stmt).__name__ == "ActionDeclarationNode":
                    # Extract logic
                    actions.append(stmt)
        return idom, state, actions

    def _widget_to_idom(self, node):
        return {
            "type": node.widget_type,
            "props": node.props,
            "children": [self._widget_to_idom(c) for c in node.children]
        }

    def _render_html(self, idom_nodes):
        out = ""
        for node in idom_nodes:
            t = node.get("type", "").lower()
            props = node.get("props", {})
            children_html = self._render_html(node.get("children", []))
            
            # Simple component mapping
            if t == "container" or t == "page":
                out += f"<div>{children_html}</div>"
            elif t == "card":
                out += f"<div class='card'>{children_html}</div>"
            elif t == "text":
                text = props.get("text", "")
                if "bind" in props:
                    out += f"<span id='bind_{props['bind']}'>{text}</span>"
                else:
                    out += f"<span>{text}</span>"
            elif t == "heading":
                level = props.get("level", 1)
                out += f"<h{level}>{props.get('text', '')}{children_html}</h{level}>"
            elif t == "button":
                click = props.get("onClick", "")
                out += f"<button onclick='{click}()'>{props.get('text', 'Button')}</button>"
            elif t == "input":
                bind = props.get("bind", "")
                placeholder = props.get("placeholder", "")
                out += f"<input type='text' placeholder='{placeholder}' oninput='updateState(\"{bind}\", this.value)' id='input_{bind}'>"
            elif t == "image":
                src = props.get("src", "")
                out += f"<img src='{src}' />"
            else:
                out += f"<div>{children_html}</div>"
        return out
        
    def _render_js(self, state, actions):
        js = "const state = " + json.dumps(state) + ";\n\n"
        js += """
function updateState(key, value) {
    state[key] = value;
    let bindEl = document.getElementById('bind_' + key);
    if (bindEl) {
        bindEl.innerText = value;
    }
}
"""
        # Generate dynamic functions from AST Actions
        for action in actions:
            js += f"\nfunction {action.name}() {{\n"
            for stmt in action.statements:
                stmt_type = type(stmt).__name__
                if stmt_type == "AssignmentNode":
                    # state assignment
                    val = f'"{stmt.value.value}"' if isinstance(stmt.value, LiteralNode) and isinstance(stmt.value.value, str) else stmt.value.value if isinstance(stmt.value, LiteralNode) else stmt.value.name if type(stmt.value).__name__ == "IdentifierNode" else "null"
                    js += f"    updateState('{stmt.target}', {val});\n"
                elif stmt_type == "ActionCallNode":
                    args = ", ".join([f'"{a.value}"' if isinstance(a, LiteralNode) and isinstance(a.value, str) else str(a.value) if isinstance(a, LiteralNode) else f"state['{a.name}']" for a in stmt.args])
                    if stmt.name == "alert":
                        js += f"    alert({args});\n"
                    else:
                        js += f"    {stmt.name}({args});\n"
            js += "}\n"
            
        return js
