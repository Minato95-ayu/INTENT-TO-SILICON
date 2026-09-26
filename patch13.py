import sys

with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('node_type = node.widget_type.lower()', 'node_type = node.type.lower()')

with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("PATCHED")