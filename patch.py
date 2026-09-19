# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import re

with open('compiler/ir/pipeline.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('"drawer", "snackbar", "tabbar", "scaffold", "page", "component"', '"drawer", "snackbar", "tabbar", "scaffold", "page", "component", "input", "passwordinput", "fileinput"')
with open('compiler/ir/pipeline.py', 'w', encoding='utf-8') as f:
    f.write(content)

with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("'drawer', 'snackbar', 'tabbar', 'scaffold', 'page', 'component'", "'drawer', 'snackbar', 'tabbar', 'scaffold', 'page', 'component', 'input', 'passwordinput', 'fileinput'")

old_logic = """        node = RenderNode(widget_name, props=props)
        node.children = children
        if widget_name == 'PAGE':"""

new_logic = """        node_props = props.copy() if props else {}
        final_children = []
        for child in children:
            if isinstance(child, RenderNode) and child.type == 'BINDING':
                node_props['bind'] = child.props.get('target')
            elif isinstance(child, RenderNode) and child.type == 'VALIDATION':
                node_props['validate'] = child.props.get('fields')
            else:
                final_children.append(child)
                
        node = RenderNode(widget_name, props=node_props)
        node.children = final_children
        if widget_name == 'PAGE':"""

content = content.replace(old_logic, new_logic)
with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patch done!')
