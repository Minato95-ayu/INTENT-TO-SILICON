import sys

with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the corrupted string
code = code.replace('el.className = \x0cas ;', 'el.className = as fa- + (iconMap[iconName] || \"user\");')

with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("PATCHED js error")