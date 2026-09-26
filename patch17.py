import sys
import re

with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'const iconName =' in line:
        # replace the next line completely
        lines[i+1] = '        el.className = "fas fa-" + (iconMap[iconName] || "user");\n'

with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("PATCHED js error line by line")