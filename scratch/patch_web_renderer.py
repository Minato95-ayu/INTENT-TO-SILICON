
path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/runtime/renderers/web_renderer.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

import re

# Update serialize_node mapping
serialize_new = """
def serialize_node(node: RenderNode, style_sheet: set):
    props = node.props.copy()
    node_type = node.type.lower()
    
    if node_type == "row":
        props["display"] = "flex"
        props["flexDirection"] = "row"
        if "gap" not in props: props["gap"] = "0px"
    elif node_type == "column":
        props["display"] = "flex"
        props["flexDirection"] = "column"
        if "gap" not in props: props["gap"] = "0px"
    elif node_type == "center":
        props["display"] = "flex"
        props["justifyContent"] = "center"
        props["alignItems"] = "center"
    elif node_type == "expanded":
        props["flex"] = "1"
    elif node_type == "spacer":
        props["flexGrow"] = "1"
    elif node_type == "padding":
        # Usually padding widget just applies padding prop
        if "value" in props:
            props["padding"] = props.pop("value")
    elif node_type == "scrollview":
        props["overflowY"] = "auto"
        props["display"] = "flex"
        props["flexDirection"] = "column"
    elif node_type == "page":
        props["display"] = "flex"
        props["flexDirection"] = "column"
        props["width"] = "100vw"
        props["height"] = "100vh"
        props["margin"] = "0"
        props["overflow"] = "hidden"
    
    class_name, css_rule = generate_css_class(props)
    if css_rule:
        style_sheet.add(css_rule)
        
    return {
        "id": node.id,
        "type": node_type,
        "class": class_name,
        "props": props,
        "children": [serialize_node(c, style_sheet) for c in node.children]
    }
"""
c = re.sub(r"def serialize_node.*?return \{\n.*?\}\n", serialize_new.strip() + "\n", c, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

