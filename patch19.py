import sys

with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'el.className = "widget-container";',
    'el.className = "widget-container";\n        if (["row", "center", "expanded", "padding", "card"].includes(t)) el.classList.add(t);'
)

with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("PATCHED row layout")