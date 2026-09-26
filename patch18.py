import sys

with open('runtime/renderers/web_renderer.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'oldEl.classList.remove' in line and 'iconMap[oldIcon]' in line:
        lines[i] = '            oldEl.classList.remove("fa-" + (iconMap[oldIcon] || "user"));\n'
    elif 'oldEl.classList.add' in line and 'iconMap[newIcon]' in line:
        lines[i] = '            oldEl.classList.add("fa-" + (iconMap[newIcon] || "user"));\n'

with open('runtime/renderers/web_renderer.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print("PATCHED js error line by line")