import sys

with open('compiler/semantic/analyzer.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'analyzed_c.widget_type not in ["center", "expanded", "padding"]:',
    'analyzed_c.widget_type not in ["center", "expanded", "padding", "text", "heading", "button", "input", "passwordinput", "icon", "image", "chatbubble"]:'
)

with open('compiler/semantic/analyzer.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("PATCHED analyzer.py")